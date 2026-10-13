#!/usr/bin/env python3
"""GEO source audit: which sources do AI search engines cite for your buyers' questions?

Asks real buyer questions to AI search (OpenAI web search, Gemini with Google Search grounding),
collects the cited sources and checks whether your brand is mentioned or cited.
Output: geo-audit/<date>_geo-audit.md (visibility, delta vs. last run, outreach targets) + history.jsonl

The outreach targets (most-cited third-party domains) are your to-do list: get listed there,
contribute content, or ask for inclusion. Do not buy links.

Usage:  OPENAI_API_KEY=... GEMINI_API_KEY=... python3 geo_source_audit.py --config projects.json [--project all]
Made by KI-Agenten.shop (Culturetek Pte. Ltd., Singapore): https://ki-agenten.shop/
"""
import argparse, datetime as dt, json, os, re, sys, time, urllib.request, urllib.error
from collections import Counter
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("GEO_AUDIT_OUT", os.path.join(os.getcwd(), "geo-audit"))
HIST = os.path.join(OUT, "history.jsonl")


class creds:
    """API keys come from the environment only."""

    @staticmethod
    def openai_key():
        return os.environ.get("OPENAI_API_KEY", "")

    @staticmethod
    def gemini_key():
        return os.environ.get("GEMINI_API_KEY", "")


OPENAI_MODEL = os.environ.get("GEO_OPENAI_MODEL", "gpt-5.5")
GEMINI_MODEL = os.environ.get("GEO_GEMINI_MODEL", "gemini-2.5-flash")


def _post(url, body, headers, timeout=180):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def ask_openai(q):
    d = _post("https://api.openai.com/v1/responses",
              {"model": OPENAI_MODEL, "tools": [{"type": "web_search"}], "input": q},
              {"Authorization": f"Bearer {creds.openai_key()}"})
    text, urls = [], []
    for item in d.get("output", []):
        for c in item.get("content", []) or []:
            if c.get("type") == "output_text":
                text.append(c.get("text", ""))
                for a in c.get("annotations", []) or []:
                    if a.get("type") == "url_citation" and a.get("url"):
                        urls.append(a["url"])
        if item.get("type") == "web_search_call":
            for s in (item.get("action") or {}).get("sources", []) or []:
                if s.get("url"):
                    urls.append(s["url"])
    return "\n".join(text), urls


def ask_gemini(q):
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
           f"?key={creds.gemini_key()}")
    d = _post(url, {"contents": [{"parts": [{"text": q}]}], "tools": [{"google_search": {}}]}, {})
    text, urls = [], []
    for cand in d.get("candidates", []):
        for p in (cand.get("content") or {}).get("parts", []) or []:
            text.append(p.get("text", ""))
        for ch in (cand.get("groundingMetadata") or {}).get("groundingChunks", []) or []:
            w = ch.get("web") or {}
            # Gemini liefert Weiterleitungs-URLs; der Titel traegt die Domain.
            title = (w.get("title") or "").strip()
            urls.append("https://" + title if title and "." in title and " " not in title else w.get("uri", ""))
    return "\n".join(text), [u for u in urls if u]


ENGINES = {"openai": ask_openai, "gemini": ask_gemini}


def domain(u):
    try:
        parsed = urlparse(u if "://" in u else "https://" + u)
        if parsed.scheme.lower() not in ("http", "https") or parsed.username or parsed.password:
            return ""
        h = (parsed.hostname or "").lower().rstrip(".").encode("idna").decode("ascii")
    except (ValueError, UnicodeError, AttributeError, TypeError):
        return ""
    return h[4:] if h.startswith("www.") else h


def is_own(u, proj):
    host = domain(u)
    return bool(host) and any(host == own or host.endswith("." + own)
                              for own in (domain(od) for od in proj["own_domains"]) if own)


def named(text, proj):
    low = text.lower()
    return any(n.lower() in low for n in proj["own_names"])


def last_run(project):
    if not os.path.exists(HIST):
        return {}
    rows = [json.loads(l) for l in open(HIST, encoding="utf-8") if l.strip()]
    rows = [r for r in rows if r["project"] == project]
    if not rows:
        return {}
    runs = sorted({r["run"] for r in rows})
    prev = [r for r in rows if r["run"] == runs[-1]]
    return {"run": runs[-1], "named": sum(r["named"] for r in prev), "cited": sum(r["cited"] for r in prev),
            "n": len(prev)}


def audit(key, proj, engines, run_id):
    rows, errors = [], []
    for q in proj["questions"]:
        for e in engines:
            text = None
            for attempt in range(3):
                try:
                    text, urls = ENGINES[e](q)
                    break
                except Exception as ex:  # Netz/API-Fehler duerfen den Lauf nicht abbrechen
                    # URLs/exception messages can contain provider keys or private input.
                    err = f"{e}: {type(ex).__name__} (request failed; details withheld)"
                    time.sleep(5 * (attempt + 1))
            if text is None:
                errors.append(err)
                continue
            doms = sorted({domain(u) for u in urls if domain(u)})
            rows.append({"run": run_id, "project": key, "engine": e, "question": q,
                         "named": named(text, proj), "cited": any(is_own(u, proj) for u in urls),
                         "domains": doms, "answer_chars": len(text)})
    return rows, errors


def report(key, proj, rows, errors, prev):
    n = len(rows)
    nm = sum(r["named"] for r in rows)
    ct = sum(r["cited"] for r in rows)
    third = Counter(d for r in rows for d in r["domains"] if not is_own(d, proj))
    out = [f"## {proj['label']}", "",
           f"Answers: {n} · mentioned: **{nm}/{n}** · cited as source: **{ct}/{n}**"]
    if prev:
        out.append(f"Previous run {prev['run']}: genannt {prev['named']}/{prev['n']} · cited {prev['cited']}/{prev['n']}")
    if errors:
        out.append(f"⚠️ Engine errors ({len(errors)}): " + "; ".join(sorted(set(errors))[:3]))
    out += ["", "| Frage | Engine | genannt | cited |", "|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['question'][:90]} | {r['engine']} | {'✅' if r['named'] else '—'} | {'✅' if r['cited'] else '—'} |")
    out += ["", "**Outreach-Ziele** (meistcitede Fremdquellen → eintragen / Beitrag / Listung anfragen):", ""]
    for d, c in third.most_common(15):
        out.append(f"- `{d}` — {c}× cited")
    out.append("")
    return "\n".join(out), {"named": nm, "cited": ct, "n": n, "targets": [d for d, _ in third.most_common(15)]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default="all")
    ap.add_argument("--engines", default="openai,gemini")
    ap.add_argument("--config", default=os.path.join(HERE, "projects.example.json"))
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    keys = [k for k in cfg if not k.startswith("_")] if a.project == "all" else [a.project]
    engines = [e.strip() for e in a.engines.split(",") if e.strip() in ENGINES]
    engines = [e for e in engines if (e == "openai" and creds.openai_key()) or (e == "gemini" and creds.gemini_key())]
    if not engines:
        print("Set OPENAI_API_KEY and/or GEMINI_API_KEY.")
        return 1
    os.makedirs(OUT, exist_ok=True)
    run_id = dt.datetime.now().strftime("%Y-%m-%dT%H:%M")
    parts, summary, any_data = [], {}, False
    for k in keys:
        prev = last_run(k)
        rows, errors = audit(k, cfg[k], engines, run_id)
        any_data |= bool(rows)
        with open(HIST, "a", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        md, s = report(k, cfg[k], rows, errors, prev)
        parts.append(md)
        summary[k] = s
    path = os.path.join(OUT, f"{run_id[:10]}_geo-audit.md")
    head = [f"# GEO source audit {run_id}", "",
            "Tool: [geo-source-audit](https://github.com/All-in-one-Kai/geo-source-audit) by [KI-Agenten.shop](https://ki-agenten.shop/)",
            f"Engines: {', '.join(engines)} · Modelle: {OPENAI_MODEL} / {GEMINI_MODEL}", ""]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(head + parts))
    with open(os.path.join(OUT, "latest.json"), "w", encoding="utf-8") as f:
        json.dump({"run": run_id, "report": path, "summary": summary}, f, ensure_ascii=False, indent=2)
    print(json.dumps({"report": path, "summary": {k: {x: v[x] for x in ("named", "cited", "n")} for k, v in summary.items()}},
                     ensure_ascii=False))
    return 0 if any_data else 1


if __name__ == "__main__":
    sys.exit(main())
