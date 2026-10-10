# TabArena provenance — source-admission boundary

This paper reports an admitted historical subset of **51 tasks**, **14 prespecified methods**, and **816 paired fold-loss vectors**. Four disclosure policies, ten seeds and two total-variation settings (2/51 and 4/51) produce 80 overlapping, nonindependent traces. A disclosure is the method-loss vector for one task/fold.

The admitted task and method identifiers are in [TABARENA_SCOPE.json](TABARENA_SCOPE.json).

## Corrected hash inventory

| File or object | SHA-256 | What is actually verified |
|---|---|---|
| Public Phase-2 stopping-status ledger `verification/source_ledgers/Phase2_FOLD_RUNS.csv` | `8f06784d4a4b2f2449f28eec229b50b558832fd914384671df7e9a3a865d36dc` | **Byte digest of the public Phase-2 ledger**, which contains trace-level stopping results, not 816 raw fold-loss vectors |
| Phase-6 frozen trace-summary ledger | `0765fd72f53d71edd0fe98c9cbb041ac83a2686602e72e182b86ce2571d8a12b` | Public ledger byte digest |
| Phase-8 frozen witness-summary ledger | `425b0fa2309b47f2afafe2482215515457184db98829eb436ad2bdad162d125c` | Public ledger byte digest |
| Original admitted raw 816-fold-loss-vector object | **not verified / no certified raw-object digest available here** | Do not use the Phase-2 digest as a substitute |
| Legacy transcript identity | `feddd565bc543dbc34dba2f19853c74f0ba030da55a3dab9a948f920563b3564` | Historic recorded identity; source bytes not supplied in this release |
| Legacy checkpoint-record identity | `a02a7077feb527498325a85fd09ffaba4dc13a6104a0a9f726cd3527fa83694f` | Historic recorded identity; source bytes not supplied in this release |

The old `source_fold_csv_sha256` JSON field was mislabeled. It referred to `Phase2_FOLD_RUNS.csv`; the corrected scope JSON names that object `phase2_stopping_ledger_sha256` and places `null` in `raw_paired_fold_vectors_sha256`. **No new raw-data hash was invented.**

## Upstream candidate retrieval, not automatic source admission

Official TabArena upstream: https://github.com/autogluon/tabarena

Official export documentation: https://github.com/autogluon/tabarena/blob/main/examples/README.md

Official script: https://github.com/autogluon/tabarena/blob/main/examples/plots/run_export_results_per_split.py

The upstream exporter can generate per-split results locally from hosted results. The latest live leaderboard may differ from this study's historical input. An independently generated upstream CSV is **candidate input only** until the original TabArena artifact version/commit, methods and configurations, task/fold mapping, loss direction, missing/imputed/failed-row policy, order, and the frozen admitted-file digest are positively matched. Otherwise leave the 816-fold reconstruction on HOLD.

Do not silently substitute new live leaderboard outputs, impute failures, or assign unknown raw scores.

## Public reproducibility scope

- [verification/README.md](../verification/README.md) explains identity-level checks.
- [verification/FIXED_TRACE_QSTAR_SUMMARY.json](../verification/FIXED_TRACE_QSTAR_SUMMARY.json) is a summary of conditional matches, **not** recomputed numerical Q certificates.
- [verification/Q_CERTIFICATE_CLOSURE_PROTOCOL.md](../verification/Q_CERTIFICATE_CLOSURE_PROTOCOL.md) lists the missing artifacts and acceptance gate.
- [results/primary_summary.csv](../results/primary_summary.csv) contains publication-facing descriptive counts.

Third-party raw data are not redistributed without a documented applicable license. The exact proof constructions are separately executable; the empirical Q certificate is not independently recertified by the public status-ledger replay.
