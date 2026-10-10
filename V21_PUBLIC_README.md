# G2--KBS V21 verified scientific extension (author-review branch)

This branch preserves the historical default branch. It contains an independently executed source-safe numerical subset of V21, not a completed journal submission or a full public release of restricted TabArena inputs.

From the **repository root** after installing numpy and pandas, run:

```bash
python code/v21/replay_four_task_exact.py
python code/v21/replay_full_uniform_obstruction_independent.py
python code/v21/benchpress_external_diagnostic.py
python code/v21/verify_benchpress_diagnostic_independent.py
```

Checks: six four-task admissible rank types; 65,780 states and 789,360 exact comparisons for the 68-task obstruction; 72 BenchPress complete-case benchmark-row disclosure scenarios with 64 explicit opposing decisions and eight conservative certificates (three certified D=0, five certified D=1). A second verifier independently checks all 72.

The 11-by-10 score matrix is from Microsoft's BenchPress source archive; CSV SHA-256 `b13854563618794e44dfa9d98e001765b0049cd023613b836964de3be631a605`. Official data https://huggingface.co/datasets/microsoft/benchpress-score-matrix, **CDLA-Permissive-2.0**, authors Y. Zeng and D. Papailiopoulos (2026).

**Important source boundary:** This branch has no TabArena third-party raw fold scores, no private Q certificates and no new private completion fills. The 80/80 TabArena and 585/756/636 source-gated findings were rerun in a separate restricted author audit; they cannot be reproduced from this public branch alone. It does not claim independent human replication, universal algorithm completeness, reduced evaluation costs, natural real-data certificate-limited cases, or statistical generalization.

Current integrated V21 manuscript (single PDF with Appendices A–E) and separate source-safe/private packages are in the project author's Google Drive V21 folder. Do not merge this branch or reuse V13 default-branch claims as current V21 without author review.
