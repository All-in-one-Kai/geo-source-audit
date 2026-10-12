# geo-source-audit

**Find out which sources ChatGPT and Gemini cite when your buyers ask for a recommendation, and whether your brand shows up.**

AI search engines rarely recommend companies because of their own website. They repeat what comparison portals, directories, trade articles, forums and Reddit say. This tool makes that visible:

1. You write the questions your buyers really ask (no brand names).
2. The tool asks them to **OpenAI web search** and **Gemini with Google Search grounding**.
3. You get a report: is your brand **mentioned**? Is your domain **cited as a source**? And the list of **most-cited third-party domains**, which is your outreach list.

Run it weekly and you see whether your GEO (generative engine optimization) work moves the numbers.

## Quick start

```bash
git clone https://github.com/All-in-one-Kai/geo-source-audit.git
cd geo-source-audit
cp projects.example.json projects.json   # edit: your domains, brand names, buyer questions
export OPENAI_API_KEY=...                # and/or
export GEMINI_API_KEY=...
python3 geo_source_audit.py --config projects.json
```

No dependencies beyond Python 3.10+. Results go to `./geo-audit/` (or `GEO_AUDIT_OUT`):

- `<date>_geo-audit.md`: mentioned / cited per engine and question, delta vs. the previous run, top outreach targets
- `history.jsonl`: one line per question, engine and run
- `latest.json`: machine-readable summary

Models can be changed with `GEO_OPENAI_MODEL` and `GEO_GEMINI_MODEL`.

## What to do with the outreach list

- **Neutral third parties** (comparison articles, directories, review portals, communities): get listed, contribute a useful article, or politely ask for inclusion.
- **Competitors** in the list show you which content format gets cited, typically honest buyer guides and FAQ pages. Build that format on your own site.
- **Do not buy links.** Paid do-follow links violate Google's spam policies and can cost you the rankings you are trying to build.

## Use as a Claude Code skill

Copy `skill/SKILL.md` into `~/.claude/skills/geo-source-audit/` and keep `geo_source_audit.py` next to it. Then ask Claude Code to "run a GEO source audit".

## Auf Deutsch, kurz

Das Werkzeug zeigt, welche Quellen ChatGPT und Gemini zitieren, wenn Ihre Kunden nach Empfehlungen fragen, und ob Ihre Marke dabei vorkommt. Die meistzitierten Fremdquellen sind Ihre Arbeitsliste für mehr Sichtbarkeit in KI-Antworten. Mehr zu KI-Agenten und Automatisierung für den Mittelstand: [KI-Agenten.shop](https://ki-agenten.shop/) · Ratgeber: [KI-Agent kaufen: worauf achten](https://ki-agenten.shop/wissen/ki-agent-kaufen-worauf-achten/).

## About

Built and used in production by [KI-Agenten.shop](https://ki-agenten.shop/) (Culturetek Pte. Ltd., Singapore), where we build AI agents, AI skills and automation for small and mid-sized businesses. MIT licensed. Issues and pull requests welcome.
