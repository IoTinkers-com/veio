# Engineering rules — VEIO

Binding for all web/data code. Each rule states **how it is checked**. Derived from the development lessons of prior IoTinkers projects (SplitTrack, ZEAZE) and adapted to a public geospatial platform.

1. **Rules are verifiable.** Every rule here names its check (grep, compiler, CI). Aspirational rules are removed or instrumented. — *Check: review in PR.*
2. **Single authorization choke point.** All access checks (PUBLIC/RESEARCH/RESTRICTED) go through one module. No route, page or handler re-implements access logic. — *Check: `grep` for direct session/permission calls must hit only that module; negative tests per boundary.*
3. **Separate response schemas per level.** RESTRICTED fields never appear in public responses. — *Check: schema review + negative tests (anonymous → restricted field = absent/403).*
4. **Validate every input before the database.** Schema validation with `max_length` on strings, bounded pagination, numeric ranges — plus spatial bounds: bbox area cap, feature-count cap, geometry vertex cap. — *Check: validator coverage test; fuzz sample in CI.*
5. **Index every queried column in the same migration.** Every geometry column gets a GIST index. — *Check: migration review; query plan spot-checks.*
6. **Schema changes only via the migration tool**, with history. Never manual SQL or `push` against production. — *Check: CI applies migrations to an ephemeral DB; no raw SQL in app code.*
7. **Derived values are not persisted** unless the formula and its inputs are stored with them (provenance `processing_version`). — *Check: schema review.*
8. **Never invent data, formulas, benchmarks or coverage.** Unknowns are `[UNVERIFIED]`/`[GAP]` or configurable. — *Check: scientific-review skill.*
9. **One decision = one ADR.** Supersede with a new ADR; never edit the original. — *Check: ADR log review.*
10. **One task = one commit.** CHANGELOG and API docs updated in the same task that changes behavior. — *Check: commit review; `task-close` skill.*
11. **Quality gate before closing any task**, fixed order: typecheck → lint → test → build. CI runs the same order. — *Check: CI; `task-close` skill.*
12. **No infrastructure without a measured trigger** from `docs/architecture/scalability.md`. — *Check: ADR required for any infra addition.*
13. **One adapter per external service** (Copernicus, Earthdata, EDGAR, tile servers). No direct SDK imports elsewhere. — *Check: `grep` for SDK imports must hit only the adapter module.*
14. **No secrets in frontend or repo.** Admin keys header-only, constant-time compare, no default value. `.env` never committed; `.env.example` has placeholders only; fail fast on placeholder secrets in production. — *Check: gitleaks (pre-commit + CI); startup check.*
15. **Security headers and rate limits** on all endpoints (CSP, X-Frame-Options, nosniff, Referrer-Policy; stricter limits on auth/write/tile endpoints). Generic 5xx messages; details logged server-side only. — *Check: header integration test; rate-limit test.*
16. **Uploads are contained:** size cap, content-type sniffing, no XML external entities (KML), no server-side execution of uploaded content, virus-scan hook when available. — *Check: upload tests with malformed payloads.*
17. **Literal routes before parametric routes.** No sandbox/zombie pages in production builds. — *Check: route table review; build output audit.*
18. **Accessibility is part of the flow:** keyboard navigation, contrast, alt text for imagery — not a later phase. — *Check: a11y lint/tests in CI (from Sprint 2).*
19. **Pinned dependencies with lockfiles;** new dependencies published ≥7 days; dependency audit in CI. — *Check: lockfile diff review; audit job.*
20. **Public repo hygiene:** branch protection on `main`, secret scanning, `permissions: read-all` on workflows. — *Check: repo settings; CI config.*
