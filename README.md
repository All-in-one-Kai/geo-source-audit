# geo-source-audit

**Find out which sources ChatGPT and Gemini cite when your buyers ask for a recommendation, and whether your brand shows up.**

Use repeated buyer questions to observe which sources appear in the collected answers. A citation or brand mention is evidence from that answer, not proof of a sale or guaranteed future visibility. This tool separates:

1. You write the questions your buyers really ask (no brand names).
2. The tool asks them to **OpenAI web search** and **Gemini with Google Search grounding**.
3. You get a report: is your brand **mentioned**? Is your domain **cited as a source**? And the list of **most-cited third-party domains**, which is your outreach list.

Run it weekly and you see whether your GEO (generative engine optimization) work moves the numbers.

## Free offline quick start

```bash
git clone https://github.com/All-in-one-Kai/geo-source-audit.git
cd geo-source-audit
python3 -m unittest discover -s tests -v
```

Python 3.10+; standard library only. No account, API key, dependency installation or network call is needed for the offline tests. View a reproducible **synthetic** report with `python3 tests/offline_demo.py`:

```text
## SYNTHETIC OFFLINE EXAMPLE — not a market measurement
Answers: 1 · mentioned: 1/1 · cited as source: 1/1
Outreach target: other.test
```

This deliberately small fixture explains the output contract. These numbers are not measured market results.

## Optional live audit — your provider account and charges

Live questions go to OpenAI and/or Google Gemini; provider usage can cost money. Use only public or approved non-sensitive questions, your own credentials, a selected model and a bounded question set. Model availability is account-specific. No key is supplied by this repository.

```bash
cp projects.example.json projects.json   # edit: your domains, brand names, buyer questions
# Set OPENAI_API_KEY and/or GEMINI_API_KEY privately in your environment.
python3 geo_source_audit.py --config projects.json
```

No dependencies beyond Python 3.10+. Results go to `./geo-audit/` (or `GEO_AUDIT_OUT`):

- `<date>_geo-audit.md`: mentioned / cited per engine and question, delta vs. the previous run, top outreach targets
- `history.jsonl`: one line per question, engine and run
- `latest.json`: machine-readable summary

Models can be changed with `GEO_OPENAI_MODEL` and `GEO_GEMINI_MODEL`.

## Limitations and contribution

Own-source matching uses the parsed host: exact domain or its subdomain, not a mention in a foreign URL/query. Gemini's source-title fallback is an approximation; it is not a verified final destination. Mentions are simple case-insensitive brand matching, not sentiment, buyer residence or purchase attribution. Engine failures are reported separately, not counted as negative answers. Unknown/partial coverage must remain explicit.

Do not publish real audit histories or secrets. See [CONTRIBUTING](CONTRIBUTING.md), [SECURITY](SECURITY.md) and [community conduct](CODE_OF_CONDUCT.md). This is an early tool, not a production SLA or guaranteed SEO/AI result.

## What to do with the outreach list

- **Neutral third parties** (comparison articles, directories, review portals, communities): get listed, contribute a useful article, or politely ask for inclusion.
- **Competitors** in the list show you which content format gets cited, typically honest buyer guides and FAQ pages. Build that format on your own site.
- **Do not buy links.** Paid do-follow links violate Google's spam policies and can cost you the rankings you are trying to build.

## Use as a Claude Code skill

Copy `skill/SKILL.md` into `~/.claude/skills/geo-source-audit/` and keep `geo_source_audit.py` next to it. Then ask Claude Code to "run a GEO source audit".

## Auf Deutsch, kurz

Das Werkzeug trennt Markennennung, eigene Quellenzitate und fremde Quellen in abgefragten KI-Antworten. Der kostenlose Offline-Einstieg benötigt keine Schlüssel; Liveabfragen kosten gegebenenfalls bei Ihrem Anbieter. Erst die Daten prüfen, dann eine passende Maßnahme wählen — keine Kauf- oder Rankinggarantie. Für die Auswahl einer konkreten Lösung: [KI-Agent kaufen: worauf achten](https://ki-agenten.shop/wissen/ki-agent-kaufen-worauf-achten/). Die Anleitung erklärt Auswahlkriterien; dieses Repo verkauft keinen automatisch eingerichteten Kundenanschluss.

## About

Maintained by [KI-Agenten.shop](https://ki-agenten.shop/) (Culturetek Pte. Ltd., Singapore). MIT licensed. Issues and pull requests welcome; provider setup and actual business impact remain separate from the offline tests.
