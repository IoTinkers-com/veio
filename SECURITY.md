# Security Policy — VEIO

## Reporting a vulnerability
Report privately via **GitHub Security Advisories** ("Report a vulnerability" on this repository) or by contacting the maintainers directly (see `veio-internal` contacts / repository owner). Do **not** open public issues for vulnerabilities.

Please include: affected component/endpoint, reproduction steps, impact, and any proof-of-concept. We aim to acknowledge within 72 hours.

## Scope
- The future Atlas web application and its public API (from Sprint 2).
- CI/CD and repository configuration.
- Data publication pipeline (leakage of RESTRICTED material is in scope).

## Out of scope (report to the provider instead)
- Vulnerabilities in upstream data providers' platforms.
- Social engineering of personnel.

## Safe harbor
We will not pursue action against good-faith research that avoids privacy violations, service degradation and data destruction, and reports findings privately.

## Current state
Sprint 0: no runtime application exists yet. The security model is defined in `docs/security.md`; the engineering baseline in `docs/engineering-rules.md`.
