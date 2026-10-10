# G2–KBS V22 — exact source-realized rank-convexification gaps

This **draft research branch** adds source-safe **derived rank-only** certificates for four experimentally discovered 4-method × 4-task TabArena subbenchmark states, with exactly one original fold masked in each case. It is stacked on the V21 branch and **does not update `main`**.

## Run exact rank-only verification

Requires Python 3.10+ and no additional packages:

```bash
python code/v22/verify_v22_rank_only.py --certificates verification/v22/V22_RANK_ONLY_SADDLE_CERTIFICATES.json
```

Expected: 4/4 exact saddle certificates and 192 label-permutation assertions. The independently checked rank-code cases each have semantic completion-aware minimum margin **+1/48**, best fixed single-action margin **−1/24**, and optimal completion-independent joint-mixture margin **0**, with explicit matching rational primal/dual witnesses. Four cases emerge from a **post hoc exploratory** 26,880-source-state screen; 26,880 disjoint-model/task held-out source cases showed **0** additional gaps; 28,000 BenchPress 4×4 complete benchmark-row masks showed **0 semantically fixed-negative cases**. None of these are prevalence estimates or tests of a real deployment.

## Evidence gates, legal scope, and reproduction limitations

**This public branch DOES NOT contain source TabArena raw scores** or masked-fold source-verification machinery. The source-gated proof that each exact legal rank pattern can arise from the recorded source's disclosed fold vectors is in the **restricted author-side V22 audit**, not this public rank-only verifier. Therefore this repository branch is NOT a complete independent public reproduction of the original-score discovery. It also does not independently establish the full historical 51-task×14-model TabArena V19/V21 80/80 result.

The new convex-hull characterization is an application of classical minimax to the declared finite weak-order completion set, **not a claim to have invented minimax theory**. The four gap cases are *real-score-anchored under exploratory selection*; all are four-method/four-task slices rather than the full 51-task matrix. No robust real-world noise/stability or prospective evaluation-cost advantage follows. Avoid interpreting these selected cases as a rate of certificate failure.

The journal-facing V22 draft is a 42-page, one-file manuscript with embedded Appendices A–F on the authorized project Google Drive. The earlier V21 and main branches are retained. Human author review and third-party data-license/attribution signoff are required before merge or publication.

## File inventory
- `code/v22/verify_v22_rank_only.py`: pure-stdlib Fraction verifier.
- `verification/v22/V22_RANK_ONLY_SADDLE_CERTIFICATES.json`: four source-derived **rank-only** numerical witnesses, no original raw fold-score table.
- `verification/v22/V22_RANK_ONLY_VERIFICATION.json`: independent checker output.

The BenchPress no-gap comparator and full source-code for source-gated TabArena scans are in the separate audited V22 bundles; no inference should be made from their absence here.
