# METHOD-0003 — SAR infrastructure & vessel monitoring (Sentinel-1)

**Bottom line:** Hypothesis-method: S1 time series detects infrastructure changes and vessel presence under cloud cover (Apr–Jul optical gap). Highest complexity — last to implement.

## Hypothesis
- S1 GRD IW backscatter change (DS-0002, ~10 m, 2014–2026; constellation gap 2022–2024) detects infrastructure modifications at asset AOIs; bright-target detection identifies vessels at terminals.
- Expected signal: structural change signatures; vessel counts at TAECJAA/La Salina consistent with reported queues (Apr 2025).

## Validation plan (before execution)
- Reference events: Alula platform arrival at Lagunillas 2025-09 (documented, visible target); TAECJAA tanker queue 2025-04 (Reuters).
- Controls: open-water AOIs away from lanes; expected FP: wind roughening, layover at fixed structures, aquaculture.
- Acceptance: Alula arrival detected ±2 weeks; vessel counts correlate (directionally) with reported queue; else negative finding recorded.

## Parameters (pinned 2026-10-05, from a documented discovery pass)
- Product/geometry: Sentinel-1 **RTC** gamma0, VV, **S1A descending relative orbit 171** (constant geometry across both windows; 18 scenes 2025-06..12). Grid EPSG:4326 at 0.0001° (~11 m), nearest resampling. Composite = per-scene median in dB.
- Water mask: pre-window median < −15 dB.
- New persistent object: per-scene bright = VV ≥ −8 dB; **≥90%** of post-window scenes bright and **0%** of pre-window scenes bright; connected component 4–2000 px (~0.05–24 ha).
- Windows: pre 2025-06-01..2025-08-20 (7 scenes) / post 2025-09-01..2025-12-30 (11 scenes).
- Supplementary (not scored): cross-check in ascending geometry (track 4); independent eastern-lake screening at ~55 m.

## v0.1 pre-registration (2026-10-05, committed before execution)
| Test | AOI (box) | Role | Pass criterion |
|---|---|---|---|
| T-Alula | Lagunillas lake/terminal, −71.40..−71.20 / 10.00..10.20 | positive | ≥1 qualifying new persistent bright object; first-bright in 2025-09-01..2025-10-31 (reported install month + margin) |
| C-water-1 | Southern Lake Maracaibo, −71.30..−71.10 / 9.60..9.80 | control | 0 qualifying objects |
| C-water-2 | Western Lake Maracaibo, −71.60..−71.40 / 10.05..10.25 | control | 0 qualifying objects |

- Validated **only** for the tested statement ("a new persistent radar-bright object appears over pre-window dark water in the Lagunillas box in the reported month") if T-Alula passes **and** both controls pass. Identity (vessel vs structure vs rig) and open-water platform detection are **not** claimed.
- Expected false positives: near-shore/port clutter, moored vessels, seasonal wind roughening, construction; partial swaths at box edges.
- Known limitations: radar does not reveal flag/operator/identity; a target moving between acquisitions is removed by the median; the 2022–2024 constellation gap does not affect 2025 coverage.

## Status
- Pre-registered 2026-10-05 (design committed before execution). No derived product exists yet.
