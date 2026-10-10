#!/usr/bin/env python3
"""Replay frozen Phase-2/6/8 identities, NOT terminal Q inequality certificates.

The 47 entries with compatible opposite decisions at Q-1 establish a
fixed-order lower bound (q* >= Q) under the declared completion model.
A numerical Q upper certificate is not recomputed here; equality q*=Q
therefore remains CONDITIONAL on the original finite-target and
mean-enclosure/positive-margin assumptions. No external raw folds are read.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path

EXPECTED_SHA256 = {
    "phase2": "8f06784d4a4b2f2449f28eec229b50b558832fd914384671df7e9a3a865d36dc",
    "phase6": "0765fd72f53d71edd0fe98c9cbb041ac83a2686602e72e182b86ce2571d8a12b",
    "phase8": "425b0fa2309b47f2afafe2482215515457184db98829eb436ad2bdad162d125c",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key(seed, policy, radius_units):
    return int(seed), str(policy), Decimal(str(radius_units))


def unique_index(rows, key_func, source):
    by_key = {}
    for row in rows:
        k = key_func(row)
        if k in by_key:
            raise ValueError(f"Duplicate key in {source}: {k}")
        by_key[k] = row
    return by_key


def replay(p2: Path, p6: Path, p8: Path, output_csv: Path):
    digests = {"phase2": sha256(p2), "phase6": sha256(p6), "phase8": sha256(p8)}
    for name, actual in digests.items():
        if actual != EXPECTED_SHA256[name]:
            raise ValueError(f"Frozen {name} SHA-256 mismatch: {actual}")

    with p2.open("r", encoding="utf-8", newline="") as stream:
        rows2 = list(csv.DictReader(stream))
    rows6 = json.loads(p6.read_text(encoding="utf-8"))
    rows8 = json.loads(p8.read_text(encoding="utf-8"))
    m2 = unique_index(rows2, lambda r: key(r["seed"], r["policy"], r["task_mass_units"]), "Phase2")
    m6 = unique_index(rows6, lambda r: key(r["seed"], r["policy"], r["task_mass_units"]), "Phase6")
    m8 = unique_index(rows8, lambda r: key(r["seed"], r["policy"], r["units"]), "Phase8")
    if len(m6) != 80 or len(m8) != 80:
        raise ValueError("Expected 80 Phase-6/8 records")

    out = []
    for k, r in sorted(m8.items()):
        a, b = m2.get(k), m6.get(k)
        if a is None or b is None:
            raise ValueError(f"Missing Phase2/Phase6 record for {k}")
        q = int(r["Q"])
        valid = (
            int(r["q"]) == q - 1
            and int(a["fold_vectors_used"]) == q
            and a["status"] == "preference_dependence"
            and a["trace_sha256"] == r["trace_sha256"]
            and int(b["Q"]) == q
            and b["terminal_reproduced"] is True
            and b["trace_sha256"] == r["trace_sha256"]
        )
        if not valid:
            raise ValueError(f"Frozen identity/status mismatch for {k}")
        witnessed = r["status"] == "SUCCESS"
        if witnessed and not (r["fixed_trace_ambiguity_witness"] is True
                              and r["conditional_fixed_trace_Q_lower_upper_match"] is True):
            raise ValueError(f"Successful record missing conditional witness flags: {k}")
        out.append({
            "seed": r["seed"], "policy": r["policy"], "tv_radius": f'{r["units"]}/51',
            "Q": q, "Q_minus_1": int(r["q"]),
            "opposite_answer_witness_at_Q_minus_1": witnessed,
            "conditional_qstar_Q_match": witnessed,
            "terminal_Q_numerical_certificate_recomputed": False,
            "trace_sha256": r["trace_sha256"],
            "Q_minus_1_prefix_sha256": r["prefix_sha256"],
        })

    successes = [r for r in out if r["conditional_qstar_Q_match"]]
    if (len(out), len(successes)) != (80, 47):
        raise ValueError(f"Unexpected counts: records={len(out)}, conditional={len(successes)}")
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    return {
        "ledger_identity_status": "PASS",
        "terminal_Q_numerical_certificate": "NOT_RECOMPUTED",
        "records": len(out),
        "conditional_qstar_Q_matches": len(successes),
        "independently_recertified_qstar_equals_Q": None,
        "Q_816_among_conditional": sum(r["Q"] == 816 for r in successes),
        "Q_below_816_among_conditional": sum(r["Q"] < 816 for r in successes),
        "distinct_trace_sha256_among_conditional": len({r["trace_sha256"] for r in successes}),
        "source_sha256": digests,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase2-fold-runs", type=Path, required=True)
    ap.add_argument("--phase6-trace-summary", type=Path, required=True)
    ap.add_argument("--phase8-trace-summary", type=Path, required=True)
    ap.add_argument("--output-csv", type=Path, required=True)
    args = ap.parse_args()
    print(json.dumps(replay(args.phase2_fold_runs, args.phase6_trace_summary,
                            args.phase8_trace_summary, args.output_csv),
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
