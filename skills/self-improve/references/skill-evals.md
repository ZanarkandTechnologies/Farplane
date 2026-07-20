# Skill Eval Use

[Eval](../../eval/SKILL.md) owns clean execution, grading, comparison, and
generated run artifacts. `self-improve` owns the ordered harden/refine policy.

Keep the canonical suite at `skills/<target>/evals/evals.json`. Before target
mutation, run the full suite and record the baseline in ticket `progress.md`.
Use the same frozen suite, metric, repetitions, and guards for every harden and
refine candidate.

```text
eval(candidate, current_best, frozen_suite)
  -> performance + guards + length + run_reference
```

Use a smoke subset only for cheap rejection; a retained candidate requires the
complete frozen suite. Do not weaken assertions to make a candidate win.

Adversarial agents may propose realistic break cases, but the tester cannot
approve them. A separate evidence reviewer and Eval owner decide acceptance.
Accept cases before a Goal starts. A case accepted mid-Goal requires stopping,
regenerating the packet, and establishing a new baseline.

Source research is similarly bounded: start from a measured failure slice,
route practitioner, paper, or book inputs through the existing source-upgrade
method, and test only `adopt` or `adapt` candidates. Raw source prose never
becomes Goal state.
