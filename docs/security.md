# Security — VEIO

Living document; changes to it require an ADR when they alter the model.

## Threat model (light, MVP)
Assets: public Atlas users, contributors, reviewers/maintainers, the platform itself, upstream data providers.
Principal risks: (1) leakage of RESTRICTED data through public endpoints or logs; (2) unauthorized writes via public API; (3) malicious uploads; (4) supply-chain compromise of a public repo; (5) exposure of sensitive infrastructure locations; (6) defacement/misinformation of a public evidence platform.

## Access levels and matrix
Levels per AGENTS.md §7: PUBLIC (Atlas), RESEARCH (working analysis), RESTRICTED (`veio-internal`, sensitive locations/agreements).

| Capability | Anonymous | Contributor | Reviewer | Maintainer/Admin |
|---|---|---|---|---|
| Read PUBLIC layers/API | ✓ | ✓ | ✓ | ✓ |
| Read RESEARCH docs | ✓ | ✓ | ✓ | ✓ |
| Read RESTRICTED | — | — | — | ✓ (via internal repo) |
| Submit contribution | — (MVP) | ✓ | ✓ | ✓ |
| Review/validate contribution | — | — | ✓ | ✓ |
| Manage users/datasets config | — | — | — | ✓ |
| Write to data stores | — | — | — | via pipelines only |

- **Check:** negative tests per row boundary (anonymous → RESTRICTED = 403/absent; contributor → admin endpoint = 403).
- All authorization server-side through the single choke point (engineering rule 2). Hiding UI elements is not access control.

## Sensitive locations policy
Only infrastructure locations that are already public (published datasets, official maps) appear in PUBLIC layers. Anything else (exact coordinates of critical assets provided privately, security-relevant detail) is RESTRICTED. When in doubt → RESTRICTED.

## Uploads and spatial queries
Uploads: size cap, content-type sniffing, XML external entities disabled (KML), no execution of uploaded content. Spatial queries: bbox area cap, feature-count cap, vertex cap (engineering rule 4) to prevent resource-exhaustion via expensive geometry requests.

## Secrets and keys
Env vars only; `.env` git-ignored; `.env.example` placeholders; fail fast on placeholder secrets in production; admin keys header-only + constant-time compare; tokens never in URLs (fragment if unavoidable); no secrets in logs (mask emails/IDs).

## Headers, transport, rate limits
CSP, X-Frame-Options DENY, X-Content-Type-Options nosniff, Referrer-Policy strict-origin-when-cross-origin, Permissions-Policy; HTTPS everywhere in production; rate limits on auth, write and tile endpoints; CORS allowlist for write endpoints (public reads may be open).

## Incident response
1. Detect: audit log monitoring, alert on anomalous 403/5xx patterns, gitleaks/secret-scanning alerts.
2. Contain: disable affected accounts/tokens; revoke leaked credentials immediately (tokens are user-managed and revocable).
3. Eradicate: rotate secrets, patch, remove malicious content with a documented tombstone (community history is never silently deleted).
4. Recover: restore from tested backups; verify integrity via checksums/manifests.
5. Notify: affected users; authorities if legal duty applies.
6. Learn: post-incident note in `.agents/memory/` + ADR if the model changed.

## Data protection
No personal data beyond contributor accounts (name, email). Contributions are pseudonymous by default; public attribution only with explicit consent. No biometric data, ever. Audit log records writes and sensitive reads with ID-only metadata (no payloads).

## Vulnerability reporting
See `SECURITY.md` (private GitHub security advisories). Do not open public issues for vulnerabilities.
