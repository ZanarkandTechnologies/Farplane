# Self Improve Gotchas

- Do not mutate the target before recording the baseline.
- Do not change the eval suite during a Goal; regenerate the packet and
  baseline after accepted case changes.
- Do not optimize a judgment-only goal without an honest metric or rubric.
- Do not enter refinement before every required behavior and guard passes.
- Do not trade behavior or a guard for fewer words; length is secondary.
- Do not claim a global mathematical minimum; return the shortest verified
  passing candidate discovered within the refinement budget.
- Do not omit phase-local `max_rounds`; patience and maximum rounds bound both
  hardening and refinement.
- Do not persist every candidate; keep reversible diffs and retain only the
  current best plus evidence.
- Do not create a parser, event schema, counter file, runner, campaign,
  scheduler, or target-local lifecycle state. Native Goal owns continuation.
- Do not make web, paper, or book research mandatory. Use bounded source
  upgrades only when local evidence cannot resolve the method.
- Do not let an adversarial tester add or approve its own eval case. Separate
  tester evidence, evidence review, and Eval acceptance.
