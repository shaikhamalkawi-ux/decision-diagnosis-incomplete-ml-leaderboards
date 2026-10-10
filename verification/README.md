# Verification and diagnostic scope — status replay, not numerical recertification

The exact constructions combine analytical arguments with exact-arithmetic implementation checks. The real-data opposite-answer witnesses are verified against disclosed values, declared score domains, aggregation bounds, valid ranks, exact ties, and file digests.

The diagnostic labels are deliberately conservative:
- one verified opposite-answer pair is sufficient to prove information limitation;
- certificate limitation requires an independent proof of semantic determination plus nonexistence of a valid certificate in the declared family;
- failure to find a witness is inconclusive unless semantic determination is separately established.

## Fixed-trace source ledgers

The three frozen source ledgers required by `code/verify_fixed_trace_qstar.py` are public in `verification/source_ledgers/`:

- `Phase2_FOLD_RUNS.csv` — SHA-256 `8f06784d4a4b2f2449f28eec229b50b558832fd914384671df7e9a3a865d36dc`
- `Phase6_TRACE_SUMMARY.json` — SHA-256 `0765fd72f53d71edd0fe98c9cbb041ac83a2686602e72e182b86ce2571d8a12b`
- `Phase8_TRACE_SUMMARY.json` — SHA-256 `425b0fa2309b47f2afafe2482215515457184db98829eb436ad2bdad162d125c`

Replay with:

```bash
python code/verify_fixed_trace_qstar.py \
  --phase2-fold-runs verification/source_ledgers/Phase2_FOLD_RUNS.csv \
  --phase6-trace-summary verification/source_ledgers/Phase6_TRACE_SUMMARY.json \
  --phase8-trace-summary verification/source_ledgers/Phase8_TRACE_SUMMARY.json \
  --output-csv verification/fixed_trace_Q_match_replay.csv
```

Expected result: 80 records, 0 identity mismatches, and `conditional_qstar_Q_matches = 47`. The 47 cases have Q-1 ambiguity witnesses, so q* is at least Q for their frozen orders; equality requires the original terminal positive-margin certificate. The public replay does not independently reconstruct mean-enclosure/rounding inequalities at Q.

The implementation checks are reproducibility checks, not blind external replication.

**Current numerical Q-certificate status: NOT RECOMPUTED.** The 364 archived-completion comparisons are a historical operation count, not 364 independent experiments. The original Phase-2 implementation, raw admitted fold losses, numerical margins, and error bounds are required to certify the terminal Q upper step.
