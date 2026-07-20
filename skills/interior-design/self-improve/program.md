---
status: legacy
runtime_role: none
---

# Legacy Self-Improve Notes: interior-design

Historical experiment notes only. The active `self-improve` workflow does not
read, write, generate, parse, or migrate this file as Goal state.

## Objective

Make interior-design reliably produce coherent, operator-approved virtual
interiors instead of technically valid but aesthetically rejected local fixes.

## Current Contract

- Trigger: room, office, studio, shop, control-room, or navigable interior
  composition and repair.
- Outcome: evidence inventory, interior program, composition options,
  blockout hypotheses, review artifact, and operator verdict.
- Validation: skill-local evals plus human acceptance of the resulting spatial
  artifact.

## Eval Metric

- Primary live signal: `operator_artifact_acceptance` on a real default-camera
  render (`approve` or A/B passes).
- Skill-behavior guard: `skill_eval_pass_rate` must remain 1.0 on the five-case
  owner suite when reusable lessons change live skill behavior.
- Direction: more accepted artifacts in fewer whole-room cycles without
  weakening evidence integrity, owner boundaries, or engineering guards.
- Simplicity guard: at most 10 top-level todos, 5 QA items, and 5 eval cases.
- Human gate: an eval pass does not prove that the operator likes the rendered
  office; only review of the actual blockout can provide that evidence.

## Rubric

- Whole-room focal hierarchy is legible from the default camera.
- Occupied mass, purposeful circulation, dead space, and decorative clutter are
  visibly distinct.
- Architecture, furniture, materials, scale, repetition, and lighting read as
  one interior system.
- Implementation proof uses the real renderer rather than concept art alone.
- Skill writeback requires a reusable measured lesson, not a one-off preference.

## Durable Evals

- `evals/test_cases.jsonl`
- `evals/assertions.md`

## Experiment Log

| Date | Run | Result | Keep? | Lesson |
| --- | --- | --- | --- | --- |
| 2026-07-14 | ownership correction | Spatial workflow moved out of visual-design into an interior-specific latest-template package. | pending proof | Room planning, circulation, furniture grammar, and spatial coherence need a dedicated owner. |
| 2026-07-14 | supported-model smoke | Office F-reset case exercised the new owner. | B; all composition behavior passed, but evidence status omitted lighting availability. | Make the evidence-status dimensions explicit on first load. |
| 2026-07-14 | candidate-v2 | Five-case owner suite. | 1/5 A; construction boundary passed, office and density were near misses, dashboard failed owner stop, and one answer exposed hidden skill-file grounding. | Add immediate non-interior stop, exact evidence matrix, measurable targets, and hide harness internals. |
| 2026-07-14 | candidate-v3 | Five-case owner suite after owner and evidence repairs. | 4/5 A; all product cases passed, construction was B because the conceptual-versus-licensed scope was implied rather than explicit. | Put the exact professional-scope statement in the first todo gate. |
| 2026-07-14 | release-v2 | Five-case owner suite on supported `gpt-5.4` agent and judge. | 5/5 A; keep. | Mandatory owner/safety handoffs plus explicit interior output fields made the behavior reliable across office reset, density, missing-reference, UI-boundary, and construction-boundary cases. |
| 2026-07-14 | Central Command Commons live loop | Operator selected the central-commons concept and granted implementation autonomy with screenshot feedback each cycle. | active; keep local until real-render verdict | Treat concept acceptance as the execution brief, require real renderer evidence each cycle, and promote only reusable feedback through skill-maintenance. |

## Accepted Learnings

- Engineering metrics are guardrails, not aesthetic acceptance.
- Repeated local polish failures trigger a whole-interior composition reset.
- Operator acceptance of the blockout precedes broad implementation.
- Concept art establishes direction but cannot substitute for an app-faithful
  blockout and default-camera verdict.

## Rejected Ideas

- Treating compile, reachability, collision, or an LLM visual score as
  aesthetic acceptance.
- Updating the live skill after every isolated preference instead of waiting
  for repeated failure or an operator-approved reusable pattern.

## Next Hypothesis

- Replacing three-sided 5x5 destination rails with a central anchor, compact
  desk neighborhoods, and shallow two-wall bays will turn the live Office3D
  scene from an empty tray into the accepted Central Command Commons.
