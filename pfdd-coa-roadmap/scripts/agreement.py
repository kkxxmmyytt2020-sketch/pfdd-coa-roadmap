#!/usr/bin/env python3
"""Inter-coder agreement for qualitative coding QA (FDA PFDD Guidance 2, App. 4).

Two CSVs with columns: segment_id, code  (one code per segment; extra columns ignored).
Typically: primary.csv = human/primary coder; blind.csv = blind-coder agent output.

Reports: n matched segments, percent agreement, Cohen's kappa, per-code agreement
(one-vs-rest kappa), and the most frequent disagreement pairs — the code definitions most in
need of sharpening. Kappa finds definitions that don't separate concepts; it is not a pass/fail gate.

    python3 agreement.py primary.csv blind.csv [--json]
"""
import argparse
import csv
import json
import sys
from collections import Counter


def load(path):
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows or not {"segment_id", "code"} <= set(rows[0]):
        sys.exit(f"{path}: needs columns segment_id, code")
    return {r["segment_id"].strip(): r["code"].strip() for r in rows}


def cohen_kappa(pairs):
    n = len(pairs)
    if n == 0:
        return float("nan"), float("nan")
    po = sum(a == b for a, b in pairs) / n
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    kappa = 1.0 if pe == 1 else (po - pe) / (1 - pe)
    return po, kappa


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("primary")
    ap.add_argument("second")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    a, b = load(args.primary), load(args.second)
    common = sorted(set(a) & set(b))
    pairs = [(a[s], b[s]) for s in common]
    po, kappa = cohen_kappa(pairs)

    codes = sorted({x for p in pairs for x in p})
    per_code = {}
    for c in codes:
        bin_pairs = [(x == c, y == c) for x, y in pairs]
        n_c = sum(1 for x, y in bin_pairs if x or y)
        _, k = cohen_kappa(bin_pairs)
        per_code[c] = {"segments_involving": n_c, "kappa_one_vs_rest": round(k, 3)}

    confusions = Counter(tuple(sorted(p)) for p in pairs if p[0] != p[1]).most_common(5)
    result = {
        "n_segments": len(common),
        "only_in_primary": len(set(a) - set(b)),
        "only_in_second": len(set(b) - set(a)),
        "percent_agreement": round(po, 3),
        "kappa": round(kappa, 3),
        "per_code": per_code,
        "top_disagreements": [{"codes": list(k), "count": v} for k, v in confusions],
    }
    if args.json:
        json.dump(result, sys.stdout, indent=2)
        print()
        return 0

    print(f"Segments compared: {result['n_segments']} "
          f"(unmatched: {result['only_in_primary']} primary-only, {result['only_in_second']} second-only)")
    print(f"Percent agreement: {po:.1%}   Cohen's kappa: {kappa:.3f}")
    print("\nPer code (one-vs-rest kappa):")
    for c, d in per_code.items():
        print(f"  {c:<30} kappa={d['kappa_one_vs_rest']:>6}  segments={d['segments_involving']}")
    if confusions:
        print("\nMost frequent disagreements (sharpen these definitions):")
        for (x, y), v in confusions:
            print(f"  {x}  <->  {y}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
