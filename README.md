# Decision Diagnosis for Incomplete Machine-Learning Leaderboards

Public reproducibility materials for the manuscript:

**A Decision-Diagnostic Framework for Incomplete Machine Learning Leaderboards: Evidence Ambiguity versus Certificate Failure under Task Reweighting**

Authors: Ghassan Malkawi, Ahmed Elsayed, Mohammed Alhagyan, and Bakeel Hussein.

## Research question

When an incomplete multi-task machine-learning leaderboard cannot yet support a decision, is the limiting factor the **available evidence** or the **certificate/reasoning mechanism** used to establish the decision?

The framework distinguishes four states:

1. **Information-limited** — verified compatible completions yield opposite decisions.
2. **Certificate-limited** — the decision is proved fixed and nonexistence of a valid certificate in the declared family is proved.
3. **Certified/resolved** — the declared certificate establishes the fixed decision.
4. **Inconclusive** — the available checks do not establish any of the three conditions above.

A failed witness search is not treated as proof of agreement, and a failed certificate search is not treated as proof of certificate nonexistence.

## Locked reported results

- exact 4-task nonuniform obstruction;
- exact 68-task uniform-center obstruction;
- 65,780 canonical states;
- 789,360 exact ordered support comparisons;
- TabArena study: 51 tasks, 14 methods, 816 paired fold vectors;
- 80 fixed overlapping disclosure traces;
- 480 prespecified checkpoints;
- zero earlier stopping for the tested certificate strengthening;
- 47/80 information-limited immediate pre-stopping prefixes;
- 39/40 at epsilon = 2/51;
- 8/40 at epsilon = 4/51;
- 33 traces remain inconclusive;
- fixed-trace decision point q*=Q on the same 47 witnessed traces;
- Q range among those 47 traces: 726–816 disclosures;
- 1,120 candidate-completion trials;
- 14,560 candidate support comparisons;
- 364 archived-completion comparisons.

## Repository structure

- `manuscript/` — current LaTeX manuscript source and Highlights. Technical proof and witness material is integrated as Appendices A-C; there is no separate Supplementary Material file in the active submission candidate.
- `code/` — exact-obstruction replay, figure generation, and fixed-trace verification scripts.
- `proofs/` — explicit analytical proof details.
- `data/` — admitted-scope and provenance notes for the TabArena analysis.
- `results/` — publication-facing result summaries.
- `verification/` — machine-readable verification summaries and the frozen source ledgers required by the fixed-trace verifier.

## Empirical-data boundary

The trace counts are descriptive and are not population-frequency estimates. Logical completions are defined by declared numerical domains and are not claimed to be realizable by retraining the named methods. The fixed-trace q*=Q result is specific to the recorded disclosure order and is not an optimization over alternative query orders.

Third-party raw TabArena artifacts are not redistributed where redistribution rights are unclear. The repository records scope, provenance, derived summaries, and code needed to inspect the reported claims without republishing restricted third-party raw artifacts.

## Reproduction

For the exact synthetic obstruction checks:

```bash
python code/replay_exact_obstructions.py
```

For the fixed-trace verification, use the frozen ledgers in `verification/source_ledgers/`; the exact command and source hashes are recorded in `verification/README.md`.

Figure-generation scripts are included in `code/`.

## Citation

Citation metadata are provided in `CITATION.cff`.

## Active manuscript structure

The KBS submission candidate is self-contained: the former supplementary proof and witness material has been consolidated into Appendices A-C of the main manuscript. Reproducibility code, exact proof records, result summaries, and verification artifacts remain in this repository.

## Permanent archive

A DOI-bearing archival snapshot has not yet been assigned. A Zenodo release can be created after the final submission lock; its DOI should then be added here and to `CITATION.cff` without changing the scientific results.
