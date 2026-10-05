# Scalability — VEIO

> Structural limits and trigger thresholds. **No measurements exist yet** — no benchmarks, no production logs, no load tests. Every number below is a reasoned structural limit, not a measurement. Update after first real deployment.

## What the MVP architecture supports (reasoned)
Static-ish Atlas + PostGIS + object storage for rasters, modest instance:
- **Users:** read-heavy, bursty (news-driven spikes around publications). A single instance + CDN-cached tiles handles low thousands of concurrent readers.
- **Data volume:** the heavy growth is raster/point-cloud storage (object storage, cheap), not rows. PostGIS holds assets/observations (thousands–low millions of rows) — comfortable if indexed.
- **Real first bottleneck:** correctness and data quality, not scale.

## Structural limits (ordered by which is hit first)
| # | Limit | Nature | Manifests as |
|---|---|---|---|
| 1 | Missing spatial/attribute indexes | Structural, preventable from day 1 | Slow dossier/layer queries |
| 2 | Unbounded spatial queries (bbox/vertex) | Preventable (rule 4) | Memory/CPU spikes per request |
| 3 | Synchronous heavy processing in request path | Architectural | Timeouts during change-detection runs |
| 4 | Single instance | Architectural | Deploy = downtime |
| 5 | Raster serving without tile cache/CDN | Architectural | Slow maps under load |
| 6 | Unbounded observation/audit growth | Structural | Table bloat |

## Trigger thresholds — instrument before scaling decisions
| Metric | Threshold | Action |
|---|---|---|
| p95 page/tile response | > 1000 ms sustained | Profile queries; check indexes; add tile cache |
| Slowest query | > 200 ms | Index or denormalize |
| DB size | > 5 GB | Partition observations/audit; archive |
| Connection pool usage | > 70% sustained | Pooler (PgBouncer) |
| CPU / RAM instance | > 70% / > 80% sustained | Scale vertically first |
| 5xx rate | > 0.5% | Investigate before scaling |
| Concurrent users | > 100 | Second instance + load balancer |
| Processing job duration | > 60 s | Move to queue + worker |
| Object storage monthly cost | threshold set with funding reality | Lifecycle policies; reprocess on demand |

## Scaling stages
| Stage | Users | Architecture | Main bottleneck | Trigger to next |
|---|---|---|---|---|
| 0 | dev | Monolith + PostGIS in compose | Correctness | Pilot deployable |
| 1 | 0–1k | 1 instance + managed PostGIS + object storage + CDN + backups | Indexes, sync processing | >100 concurrent · job >60 s |
| 2 | 1k–20k | + queue/worker for processing, read replicas if needed | Raster processing throughput | Funding + demand |
| 3 | >20k | Multi-instance, regional CDN, partitioned tables | Cost/ops maturity | Only with partners/funding |
