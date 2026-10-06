"""VEIO documentation drift check (stdlib only, run in CI).

Fails (exit 1) when the public docs drift from the repo:

  1. Registry <-> files: every registry row's note_path exists; every
     docs/datasets/DS-*.md and docs/assets/AST-*.md is registered.
  2. Method notes <-> dashboard: every docs/methods/METHOD-*.md is listed in
     STATUS.md and STATUS.es.md; STATUS/PLATFORM EN+ES pairs exist.
  3. Derived observations: every `**Derived**` line in a dossier cites a
     METHOD-#### that has a method note (and a manifest path).
  4. Bilingual orphans: a `X.es.md` without its `X.md` sibling.
  5. No generated artifacts in the repo (ADR-001): no committed raster/figure.
  6. Asset × Evidence matrix lists every asset and every method (EN + ES).

Usage: py -3 scripts/check_docs.py
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []


def read(p):
    return p.read_text(encoding="utf-8")


def csv_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def check_registry(csv_rel, prefix, folder, id_col="id"):
    reg = ROOT / csv_rel
    rows = csv_rows(reg)
    registered = set()
    for r in rows:
        note = (r.get("note_path") or "").strip()
        if not note:
            errors.append(f"{csv_rel}: row {r.get(id_col)!r} has no note_path")
            continue
        registered.add(note)
        if not (ROOT / note).exists():
            errors.append(f"{csv_rel}: note_path missing on disk: {note}")
    for f in (ROOT / folder).glob(f"{prefix}-*.md"):
        rel = f.relative_to(ROOT).as_posix()
        if rel not in registered:
            errors.append(f"{folder}/{f.name} is not registered in {csv_rel}")


def check_methods():
    methods = sorted((ROOT / "docs" / "methods").glob("METHOD-*.md"))
    status = ROOT / "docs" / "methods" / "STATUS.md"
    status_es = ROOT / "docs" / "methods" / "STATUS.es.md"
    for p in (status, status_es, ROOT / "docs" / "foundation" / "PLATFORM.md",
              ROOT / "docs" / "foundation" / "PLATFORM.es.md"):
        if not p.exists():
            errors.append(f"missing required doc: {p.relative_to(ROOT).as_posix()}")
    text_en = read(status) if status.exists() else ""
    text_es = read(status_es) if status_es.exists() else ""
    for m in methods:
        key = m.stem  # METHOD-0002
        if key not in text_en:
            errors.append(f"{key} not listed in docs/methods/STATUS.md")
        if key not in text_es:
            errors.append(f"{key} not listed in docs/methods/STATUS.es.md")


def check_derived():
    notes = {f.stem for f in (ROOT / "docs" / "methods").glob("METHOD-*.md")}
    for d in sorted((ROOT / "docs" / "assets").glob("AST-*.md")):
        for i, line in enumerate(read(d).splitlines(), 1):
            if "**Derived**" not in line and "**Derived " not in line:
                continue
            ids = re.findall(r"METHOD-\d{4}", line)
            if not ids:
                errors.append(f"{d.name}:{i}: Derived observation cites no METHOD-####")
            for mid in ids:
                if mid not in notes:
                    errors.append(f"{d.name}:{i}: cites {mid} with no method note")
            if "manifest" not in line.lower() and "data/derived" not in line:
                errors.append(f"{d.name}:{i}: Derived observation cites no manifest path")


def check_orphans():
    for f in ROOT.rglob("*.es.md"):
        if any(part in {".git", "node_modules", "data"} for part in f.parts):
            continue
        base = f.with_name(f.name[: -len(".es.md")] + ".md")
        if not base.exists():
            errors.append(f"orphan Spanish doc (no English twin): {f.relative_to(ROOT).as_posix()}")


GENERATED_SUFFIXES = {".png", ".tif", ".tiff", ".jpg", ".jpeg"}
SKIP_PARTS = {".git", "node_modules", ".venv", "__pycache__", "data"}


def check_no_generated_artifacts():
    """ADR-001: no generated artifact (raster/figure) may be committed."""
    for f in ROOT.rglob("*"):
        if not f.is_file():
            continue
        rel = f.relative_to(ROOT)
        if any(part in SKIP_PARTS for part in rel.parts):
            continue
        if f.suffix.lower() in GENERATED_SUFFIXES:
            errors.append(f"generated artifact in repo (ADR-001): {rel.as_posix()} "
                          "(generate locally under data/ instead)")


def check_evidence_matrix():
    """Every asset and every method must appear in the matrix (EN + ES)."""
    ids = {r["id"] for r in csv_rows(ROOT / "registry" / "assets.csv")}
    methods = {f.stem for f in (ROOT / "docs" / "methods").glob("METHOD-*.md")}
    for name in ("EVIDENCE-MATRIX.md", "EVIDENCE-MATRIX.es.md"):
        p = ROOT / "docs" / "assets" / name
        if not p.exists():
            errors.append(f"missing required doc: docs/assets/{name}")
            continue
        text = read(p)
        for aid in sorted(ids):
            if aid not in text:
                errors.append(f"docs/assets/{name}: asset {aid} missing")
        for mid in sorted(methods):
            if mid not in text:
                errors.append(f"docs/assets/{name}: method {mid} missing")


def main():
    check_registry("registry/datasets.csv", "DS", "docs/datasets")
    check_registry("registry/assets.csv", "AST", "docs/assets")
    check_methods()
    check_derived()
    check_orphans()
    check_no_generated_artifacts()
    check_evidence_matrix()
    if errors:
        print(f"DOCS DRIFT: {len(errors)} problem(s)")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("docs drift check: OK")


if __name__ == "__main__":
    main()
