---
name: geo-source-audit
description: Measure brand visibility in AI search answers (ChatGPT web search, Gemini grounding). Use when the user asks which sources AI assistants cite for their market, whether their brand is mentioned, or wants a GEO / AI-visibility outreach list.
---

# GEO source audit

1. Ask the user for: their domain(s), brand names, and 3 to 8 real buyer questions without brand names. Write them to `projects.json` in the format of `projects.example.json`.
2. Check that `OPENAI_API_KEY` and/or `GEMINI_API_KEY` are set. Never print key values.
3. Run `python3 geo_source_audit.py --config projects.json --project all`.
4. Read `geo-audit/latest.json` and the newest `geo-audit/*_geo-audit.md`. Report per project: mentioned x/n, cited x/n, change vs. previous run.
5. Turn the outreach targets into actions: separate neutral third parties (directories, comparison articles, review portals, communities) from competitors. For each neutral target, find how to get listed or contribute. For competitors, name the content format that gets cited.
6. Never recommend buying links.
