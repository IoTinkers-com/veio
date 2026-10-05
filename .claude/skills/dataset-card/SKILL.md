---
name: dataset-card
description: Discover, verify and register a public dataset for VEIO - writes a dataset card with verified license/redistribution and a row in registry/datasets.csv.
argument-hint: "[url | topic]"
---

Follow AGENTS.md (evidence rules §5, licensing gate §6).

## Procedure
1. If a topic: search authoritative providers; prefer open licenses and API access. If a URL: fetch and confirm it works; record access date.
2. Dedupe against `registry/datasets.csv` (URL/title).
3. Next `DS-####` = max + 1. Verify from the provider page: license, attribution, modification and redistribution rights, coverage, resolution, update frequency, format, API, known limitations. Never assume "public on the internet" = redistributable.
4. Write `docs/datasets/DS-####.md` from `templates/dataset-card.md` (≤150 words). Unclear redistribution → status `DISPLAY ONLY / RESTRICTED`, note in card.
5. Append the row to `registry/datasets.csv` (quoted fields, UTF-8). Score relevance to the MVP (0–5) with one-line justification.

## Output
- Card + CSV row; chat: one line per dataset (ID, license, status) + paths. LOG entry via `task-close`.

## Checklist
- License fields filled or flagged; URL verified with date; no invented coverage.
