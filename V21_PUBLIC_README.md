# G2--KBS V21 public verification (no restricted TabArena rows)

Requires Python 3.10+, numpy, pandas. Use the self-contained ZIP from Google Drive for a one-command folder layout. For this GitHub branch, scripts under code/v21 expect data under inputs/; copy the two inputs/v21 CSVs into inputs/ before running (or use the ZIP). From a prepared directory run:

    python code/v21/replay_four_task_exact.py
    python code/v21/replay_full_uniform_obstruction_independent.py
    python code/v21/benchpress_external_diagnostic.py
    python code/v21/verify_benchpress_diagnostic_independent.py

Expected: six admissible four-task patterns; 65,780 canonical 68-task states and 789,360 exact candidate-rival supports; 72 BenchPress benchmark-row disclosure cases (64 ambiguity witnesses, 8 positive decision certificates); all checks pass. These are separate source-level checks, not blind independent human replication.

The 11x10 `inputs/v21/benchpress_primary_complete_case_scores.csv` and normalized rank matrix are retained from the independently archived source, not a substitution for the current living upstream dataset. BenchPress source Microsoft, Y. Zeng and D. Papailiopoulos (2026), https://huggingface.co/datasets/microsoft/benchpress-score-matrix; dataset license **CDLA-Permissive-2.0**, https://huggingface.co/datasets/microsoft/benchpress-score-matrix/tree/main/data. Source CSV SHA-256 b13854563618794e44dfa9d98e001765b0049cd023613b836964de3be631a605.

The original TabArena fold losses, Phase-2/Phase-8 transcript files, private witness score fills, and verification scripts requiring them are absent. Public proof code alone does **not** reproduce the full TabArena 80/80 trace result. This remains conditional on restricted author-side input. No task weights were empirically calibrated and no prospective evaluation savings were observed.
