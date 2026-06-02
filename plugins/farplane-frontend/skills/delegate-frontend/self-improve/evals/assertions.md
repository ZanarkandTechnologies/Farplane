# Delegate Frontend Self-Improve Assertions

Primary metric: `skill_eval_pass_rate`.

`skill_eval_pass_rate` is a case-expectation metric:

- `expected_outcome: "accept"` means every assertion should pass.
- `expected_outcome: "reject"` means fixture/provenance assertions should pass
  and at least one quality gate should fail.

The runner also reports `assertion_pass_rate` as a diagnostic. It is allowed to
stay below 1.0 because reject-control fixtures intentionally fail quality gates.

The suite converts "Terminus-level frontend delegation" into binary gates:

- external CLI run evidence includes `first_write.json` when `--expect-output`
  is used,
- Terminal-style pages pass the strict scroll-scrub QA harness,
- generated pages expose the full debug contract: `progress`, `phase`,
  `frame` or `mediaTime`, `active`, `ready`, and `reducedMotion`,
- desktop/mobile/reduced-motion QA artifacts stay replayable,
- the old fake-scroll page fails the scroll-scrub harness,
- a Terminus-level page has large visual delta across scrub checkpoints, not
  just tiny canvas label changes,
- a Terminus-level page uses premium media assets or frame/video artifacts, not
  only `code-native-canvas`.
- `visual_geometry` summaries should come from
  `skills/landing-page/scripts/scroll_scrub_qa.cjs` when screenshots exist.
- `startup` and `phase_completion` summaries should come from
  `self-improve/scripts/artifact_summary.py` when delegate run artifacts exist.
- `phase_completion.handoff_path` is valid only when the handoff is not the
  prefilled template. Rows that claim producer-backed summaries should declare a
  `summary_source` and pass `test_candidate_output_provenance.py`.
- `compiled_prompt` summaries should come from
  `self-improve/scripts/phase_prompt_compiler.py` and prove first-write,
  selected-route, phase-boundary, and anti-reference-chasing constraints before
  another live Pi/Kimi run.

Current baseline is expected to pass mechanics and fail the Terminus-level
visual proxy until the external agent reliably produces generated/photoreal
media and stronger scroll checkpoint deltas.
