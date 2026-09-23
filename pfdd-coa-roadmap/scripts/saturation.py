#!/usr/bin/env python3
"""Concept saturation grid (FDA PFDD Guidance 2, App. 4, Table 7).

Input CSV columns: interview_id, order, concept [, participant_id]
  - order: sequence number of the interview (1..N) — or of the focus group in --groups mode.
  - participant_id (optional): who endorsed the concept; defaults to interview_id.

Chunking:
  default   : interviews split into 25% chunks of the *planned* number (--planned N);
              interviews beyond N fall into an extra chunk ("beyond plan").
  --groups  : one chunk per focus group (interview_id = group), in 'order' — the Table 7 layout.

Cell = number of distinct participants in that chunk endorsing the concept; '*' marks the chunk
where the concept first appears. Saturation (G2 App. 4) = no new important concepts in the last
chunk AND a representative sample — this script can only check the first half.

    python3 saturation.py coded.csv --planned 24
    python3 saturation.py groups.csv --groups --json
"""
import argparse
import csv
import json
import math
import sys
from collections import OrderedDict, defaultdict


def load(path):
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    need = {"interview_id", "order", "concept"}
    if not rows or not need <= set(rows[0]):
        sys.exit(f"CSV needs columns {sorted(need)} (optional participant_id)")
    for r in rows:
        r["order"] = int(r["order"])
        r["concept"] = r["concept"].strip()
        r["participant_id"] = (r.get("participant_id") or r["interview_id"]).strip()
    return rows


def chunk_labels_default(rows, planned):
    size = planned / 4.0
    labels = {}
    for r in rows:
        o = r["order"]
        labels[r["interview_id"]] = "beyond plan" if o > planned else f"Q{min(4, math.ceil(o / size))}"
    order = ["Q1", "Q2", "Q3", "Q4"] + (["beyond plan"] if "beyond plan" in labels.values() else [])
    return labels, order


def chunk_labels_groups(rows):
    firsts = {}
    for r in rows:
        firsts.setdefault(r["interview_id"], r["order"])
    ordered = sorted(firsts, key=lambda g: firsts[g])
    labels = {g: f"Group {i}" for i, g in enumerate(ordered, 1)}
    return labels, [labels[g] for g in ordered]


def grid(rows, labels, chunks):
    cells = defaultdict(set)
    first_seen = {}
    concepts = OrderedDict()
    for r in sorted(rows, key=lambda r: r["order"]):
        c, ch = r["concept"], labels[r["interview_id"]]
        concepts.setdefault(c, None)
        cells[(c, ch)].add(r["participant_id"])
    for c in concepts:
        for ch in chunks:
            if cells.get((c, ch)):
                first_seen[c] = ch
                break
    table = {c: {ch: len(cells.get((c, ch), ())) for ch in chunks} for c in concepts}
    new_by_chunk = {ch: [c for c in concepts if first_seen[c] == ch] for ch in chunks}
    return table, first_seen, new_by_chunk


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--planned", type=int, help="planned number of interviews (default mode)")
    ap.add_argument("--groups", action="store_true", help="one chunk per focus group")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    rows = load(args.csv)
    if args.groups:
        labels, chunks = chunk_labels_groups(rows)
    else:
        if not args.planned:
            ap.error("--planned N is required unless --groups")
        labels, chunks = chunk_labels_default(rows, args.planned)

    table, first_seen, new_by_chunk = grid(rows, labels, chunks)
    last = chunks[-1]
    result = {
        "chunks": chunks,
        "grid": table,
        "first_seen": first_seen,
        "new_by_chunk": {k: v for k, v in new_by_chunk.items()},
        "no_new_in_last_chunk": len(new_by_chunk[last]) == 0,
        "note": "Saturation also requires a representative sample (G1 §II.D.3; G2 App. 4).",
    }
    if args.json:
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return 0

    w = max([len("Concept")] + [len(c) for c in table])
    print("Concept".ljust(w) + " | " + " | ".join(ch.rjust(11) for ch in chunks))
    print("-" * w + "-+-" + "-+-".join("-" * 11 for _ in chunks))
    for c, row in table.items():
        cells = []
        for ch in chunks:
            n = row[ch]
            s = "" if n == 0 else f"{n}{'*' if first_seen[c] == ch else ''}"
            cells.append(s.rjust(11))
        print(c.ljust(w) + " | " + " | ".join(cells))
    print("\n* = first mention.  New concepts per chunk: " +
          ", ".join(f"{ch}: {len(v)}" for ch, v in new_by_chunk.items()))
    print(("No new concepts in the last chunk" if result["no_new_in_last_chunk"]
           else f"New concepts still emerging in {last}: {', '.join(new_by_chunk[last])}") +
          " — check representativeness before concluding saturation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
