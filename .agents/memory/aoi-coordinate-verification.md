# AOI coordinates: OGIM terminal records are offshore loading points

Date: 2026-10-04 · Tool: devin · Repo: veio

AST-0014 (José complex) was anchored on an OGIM "SHIPPING TERMINAL" record
(-64.646, 10.216) flagged OFFSHORE — a loading point ~29 km from the
industrial complex. METHOD-0002 then reported 122 hotspots "at José" that
belonged to another location; the real complex (OSM centroid -64.864,
10.069) has 750. A similar dead AOI broke the METHOD-0004 Lagunillas test.

**Trap:** using the nearest dataset point as an asset AOI without checking
what that record actually is (onshore/offshore flag, facility type, name).

**Fix:** before any method run, verify each AOI against a second source
(OSM / named place record) and check the ON_OFFSHORE field; record the
coordinate source in `registry/assets.csv` (`location_source`).
