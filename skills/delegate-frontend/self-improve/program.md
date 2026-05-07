# Self-Improve Program: delegate-frontend

## Objective
make external Pi/Kimi frontend delegation reliably produce Terminal-style scroll-scrub landing pages with measurable first-write, motion, visual-quality, and handoff evidence

## Current Contract
- Trigger: frontend implementation or polish should be delegated to an external
  CLI profile, currently `frontend-pi-kimi`.
- First-load workflow: read the target brief, route through `delegate-cli`,
  sync the frontend/media skill bundle, run dry-run/live with explicit owned
  files, then hand results back through QA, `visual-qa`, and `review`.
- Outcome: profile, prompt, handoff, first-write evidence, run logs, UI/asset
  artifacts, scroll-scrub QA proof, and review follow-up.
- Validation: `first_write.json`, strict scroll-scrub QA, visual checkpoint
  deltas, asset manifest quality, mobile/reduced-motion proof, and self-review
  handoff completeness.

## Eval Metric
- Primary: `skill_eval_pass_rate`
- Direction: higher
- Meaning: case-expectation pass rate. `accept` cases must pass all assertions;
  `reject` control cases must keep their fixture/provenance assertions passing
  while failing at least one quality gate. Raw assertion ratio is reported as
  `assertion_pass_rate` for diagnostics only.
- Minimum meaningful delta: one newly passing live Pi/Kimi first-write,
  completion, or final-quality experiment, or a new reject-control case that
  catches a real failure without lowering `skill_eval_pass_rate`.
- Simplicity guard: keep the public `SKILL.md` thin; put experiment machinery
  under `self-improve/` and keep prompt/profile rules specific to observed
  failures.

## Rubric
- First-write reliability
- Terminal/Terminus scroll-scrub mechanics
- Premium media / visual parity
- Handoff evidence completeness
- Bounded phase behavior without reference-chasing

## Durable Evals
- `evals/test_cases.jsonl`
- `evals/assertions.py`

## Experiment Log
| Date | Run | Hypothesis | Result | Keep? | Lesson |
| --- | --- | --- | --- | --- | --- |
| 2026-05-06 | setup | Create skill-local memory | Baseline memory surface created | yes | Future runs should record durable lessons here. |
| 2026-05-07 | 20260507-0526-terminus-level-ui | Make first-write, debug, visual-delta, and asset-quality gates mechanical | Pass rate moved from `0.944444` to `0.951613`; live Pi reached first-write only after stronger first-tool-call wording, then timed out from reference-chasing | yes | Keep `--expect-output`, strict debug contract, and no-reference bounded prompts; the remaining output gap is generated media plus large cinematic deltas. |
| 2026-05-07 | review-fix | Make the metric replayable and less gameable | Pass rate is now `0.948276` across 7 captured-output cases and the runner emits `METRIC skill_eval_pass_rate=...` with exit 0 | yes | Candidate prompt rules, live Pi first-write logs, Terminal gold QA, fake-scroll failure, and current prototype QA are now evaluated from captured rows instead of live filesystem peeks. |
| 2026-05-07 | first-write-proof-fix | Tighten `--expect-output` evidence to changed regular files | Delegate CLI tests now cover created, modified, unchanged, directory, symlink, public command-run, and timeout-zero evidence paths | yes | Timeout `0` disables early kill only; it still emits `first_write.json` and fails if the expected regular file never changes. |
| 2026-05-07 | local-phase-gates | Add local replay gates for spec completion, phase completion, asset manifest quality, visual geometry, and startup reliability | Harder suite now has 14 cases, `119/148` assertions passing, `skill_eval_pass_rate=0.804054` | yes | The lower score is the new baseline; it catches first-write stubs, missing generated media, weak first-viewport geometry, and no-session startup failures before another live Pi/Kimi build. |
| 2026-05-07 | artifact-summary-producers | Add mechanical producers for geometry, startup, and phase summaries | `scroll_scrub_qa.cjs` now emits `visualGeometry`; `artifact_summary.py` turns delegate run artifacts into summaries; suite now has 15 cases, `125/155` assertions passing, `skill_eval_pass_rate=0.806452` | yes | New gates are no longer only hand-curated summaries; current page fails generated geometry on blank-band ratio while still passing scroll mechanics. |
| 2026-05-07 | placeholder-handoff-provenance-fix | Reject prefilled handoff templates and prove replay rows from artifact sources | Artifact summary tests now cover placeholder handoffs; candidate provenance tests compare declared `summary_source` rows against `artifact_summary.py`; suite scores `126/155`, `skill_eval_pass_rate=0.812903` | yes | A non-empty handoff is not completion evidence if it still contains the template's pending markers; positive phase rows must be sourced from artifact-shaped run directories until a live Pi/Kimi completion exists. |
| 2026-05-07 | phase-prompt-compiler | Compile bounded phase prompts and dry-run a startup probe command | Added `phase_prompt_compiler.py`, `startup_probe.py`, and prompt provenance tests; suite now has 16 cases, `136/165` assertions passing, `skill_eval_pass_rate=0.824242` | yes | The next live Pi/Kimi attempt should start from a compiled phase prompt and a startup probe rather than a broad natural-language ask. |
| 2026-05-07 | live-startup-probe-low-thinking | Verify Pi/Kimi startup with the compiled probe path | First live probe with high thinking/45s first-write failed after producing a session but no file; retry with low thinking/90s first-write passed, wrote `PROBE.md`, and produced a non-placeholder handoff; suite now has 17 cases, `149/178`, `skill_eval_pass_rate=0.837079` | yes | Startup probe should run low-thinking with a 90s first-write gate before expensive phase prompts; session creation alone is not enough. |
| 2026-05-07 | metric-semantics-and-contract-fix | Make reject-control cases first-class and harden probe/handoff evidence | Runner now reports `skill_eval_pass_rate=1.000000` for 17/17 expected accept/reject outcomes and `assertion_pass_rate=0.843434`; startup probe defaults are run-id-derived; short probe outputs can complete; positive handoffs prove first-write evidence sections | yes | Do not optimize against raw assertion ratio when reject fixtures are supposed to fail quality gates. |
| 2026-05-07 | compiled-spec-live-timeout | Test the compiled spec prompt against live Pi/Kimi | Pi/Kimi wrote a complete `SPEC.md` and non-placeholder handoff with first-write proof, but the wrapper exited `124`; suite now has 18 cases, `18/18` expected outcomes, `skill_eval_pass_rate=1.000000`, `assertion_pass_rate=0.863436` | yes | The spec prompt is good enough to produce structured planning output; the next failure is clean phase termination after handoff, not spec content quality. |
| 2026-05-07 | parser-and-provenance-review-fix | Fix review blockers in spec parsing and candidate-output provenance | Prose-only stub specs now leave route IDs empty, and provenance tests derive expected marker text from each declared source; suite remains 18/18 expected outcomes with `assertion_pass_rate=0.859031` | yes | Evidence rows must not infer route IDs from prose, and eval marker text must be tied to source provenance instead of only mutable free-form output. |
| 2026-05-07 | clean-phase-completion-detector | Stop bounded phase runs after owned output plus completed managed handoff | Delegate CLI now supports `--complete-when-output-and-handoff`; unit tests cover early successful termination, placeholder rejection, and public command-run behavior; suite remains 18/18 expected outcomes with `assertion_pass_rate=0.859649` | yes | The next live compiled spec run should use the completion detector so a finished spec handoff does not wait for the total timeout. |
| 2026-05-07 | live-compiled-spec-success | Retry compiled spec with the clean-completion path available | Pi/Kimi produced a 16 KB complete spec, first-write proof, and a non-placeholder handoff, then exited `0`; accepted fixture raises the suite to 19/19 expected outcomes with `assertion_pass_rate=0.875486` | yes | The spec phase is now live-proven; proceed to an asset phase only after carrying forward the wrapper first-write appendix and manifest linter gates. |
| 2026-05-07 | live-asset-manifest-timeout | Run the compiled asset phase with live generation and manifest linting | Pi/Kimi generated real image/video/frame assets, wrote a manifest that passes `asset_manifest_lint.py`, and produced a handoff; process exit was still `124`, so the new fixture is an expected reject and the suite is 20/20 with `assertion_pass_rate=0.882979` | yes | Asset quality is now live-proven, but process completion remains a separate gate. Broaden handoff heading recognition and keep timeout rows rejected until the wrapper sees exit `0` or an explicit clean completion. |
| 2026-05-07 | live-asset-finalization-success | Retry asset finalization without spending on media | Pi/Kimi wrote a readiness file as first-write, ran the manifest linter, used canonical handoff headings, and the wrapper observed `completion_reason=expected_output_and_handoff`; accepted fixture raises the suite to 21/21 with `assertion_pass_rate=0.892508` | yes | The asset package is now cleanly finalizable without another media-generation run; implementation can use the manifest only after this finalization evidence exists. |
| 2026-05-07 | review-blocker-fix-path-and-handoff | Fix review-found false positives in asset paths and handoff completion | Asset manifests now count/reject unsafe out-of-root refs; handoffs must have non-empty required section bodies; wrapper clean-completion requires the changed-files body to mention the expected output; unsafe-ref reject-control raises the suite to 22/22 with `assertion_pass_rate=0.897590` | yes | First-write and phase-completion proof must be hard to spoof: headings alone are not completion, and existing local files outside the asset package are not valid generated assets. |
| 2026-05-07 | implementation-repair-loop | Run seeded implementation and bounded V4 repair experiments | Seeded V4 output passes scroll/media/style/support-video QA but timed out without managed handoff; first mobile repair failed the 60s first-write gate; retry with a 120s gate cleanly patched mobile typography and raised the suite to 29/29 with `assertion_pass_rate=0.901852` | yes | Treat seeded partial UI as useful artifact evidence but failed phase completion; use one-file micro-repairs with clean handoff completion for polish, and score mobile hero phrase separation mechanically. |

## Accepted Learnings
- A Terminal/Terminus page is not final quality when `asset_strategy` is
  `code-native-canvas` with zero assets, even if scroll mechanics pass.
- The first-write proof must be file creation/modification, not directory
  creation or agent activity.
- Pi/Kimi obeys first-write more reliably when the prompt says the first tool
  call must write a stub before reading references.
- Broad skill/reference reading after first-write can consume the run budget;
  phase prompts should supply selected IDs and acceptance criteria up front.
- Dry-run first-write evidence is useful for setup smoke tests but must not
  satisfy live Pi/Kimi reliability eval cases.
- First-write proof is a changed regular file. Directories, symlinks, unchanged
  pre-existing files, and broad agent activity are failed evidence.
- First-write is necessary but not sufficient. A phase must also produce a
  completion summary that is not a stub.
- Terminal-level visual parity needs geometry gates in addition to scroll
  mechanics: object scale, blank-band ratio, nav containment, and deliberate
  mobile crop.
- Pi startup/no-session failures are a separate reliability class and should
  not be diagnosed as prompt-quality failures.
- Visual geometry should be produced from scroll QA artifacts when screenshots
  exist; delegate startup and phase completion should be produced from run
  artifacts rather than inferred from prose.
- Placeholder handoffs with "pending live external CLI run" or "none reported
  yet" do not count as phase completion. The self-improve replay rows that
  claim phase completion need a declared `summary_source` and a provenance test
  that can regenerate their semantic summary.
- Use the phase prompt compiler before live Terminus-style Pi/Kimi phases. It
  makes first-write, selected-route IDs, owned outputs, anti-reference-chasing,
  and phase boundaries mechanical enough to test before spending another run.
- For Pi/Kimi startup probes, prefer `--thinking low` and a `90s`
  first-write gate. The earlier high-thinking `45s` probe created a session
  but failed to write; the low-thinking retry crossed first-write in roughly
  15 seconds and completed the handoff.
- Treat bad-fixture evals as `expected_outcome: reject`, not as raw score
  failures. The headline metric is whether accept cases pass and reject cases
  are rejected; `assertion_pass_rate` is only a diagnostic that should stay
  below 1.0 while known-bad controls remain in the suite.
- A live compiled spec phase can produce useful output and still be a failed
  handoff when the process exits `124`. Keep process completion separate from
  first-write and content-completeness evidence.
- Spec artifact parsers must require explicit labels such as `Recipe ID:` or
  `**Recipe ID:**`; prose like "no selected recipe, taste profile, effect
  stack" is evidence of absence, not a route-field value.
- Candidate-output rows that use produced artifacts must have marker text
  derived from their declared source, so `must_contain` checks cannot pass from
  stale hand-edited prose alone.
- For bounded external CLI phases, a changed owned output plus a non-placeholder
  managed handoff is a clean completion signal. Use the opt-in wrapper flag for
  those phases; do not apply it to open-ended research or broad review runs.
- Generated assets are not enough to unblock implementation when the external
  CLI process exits `124`. The manifest can pass lint while phase completion
  remains rejected; keep that distinction in evals and ticket evidence.
- Pi/Kimi may write reasonable handoff headings such as
  `Changed / Produced Files` and `Self-Review Findings`. Accept those as
  semantic equivalents in parsers, but keep the profile asking for canonical
  `Changed Files`, `Verification`, and `Risks / Followups` headings.
- A handoff is complete only when changed-files, verification, and
  risks/followups sections have non-empty bodies. For wrapper clean-completion,
  changed-files must mention the expected owned output.
- Asset manifests must stay inside the declared asset project root. Existing
  absolute files or `../` escapes are unsafe even when they exist and have valid
  media signatures.
- A seeded implementation can produce a strong partial UI while still failing
  the phase when the managed handoff stays placeholder. Preserve the output as
  evidence, but keep the run rejected until phase completion is clean.
- Mobile hero typography needs a mechanical gate. When a multi-phrase hero
  title relies on `<br>`, require visible breaks or equivalent spacing through
  `hasMobileHeroPhraseSeparation` so QA does not miss glued phrases.
- Pi/Kimi repair passes can work when reduced to one owned file and a clean
  handoff target, but a 60s first-write gate can flake. Retry once with a
  longer gate before rejecting the micro-patch hypothesis.

## Rejected Ideas
- Prompt-only "make it cinematic" without binary QA; it allowed fake scroll and
  tiny HUD-only deltas.

## Next Hypotheses
- Run the implementation phase from the approved spec plus the finalized asset
  manifest, then require scroll-scrub QA, visual geometry, visual QA, review,
  and web-design-guidelines evidence before any UI parity claim.
- Keep `asset_manifest_lint.py` as the hard gate before implementation consumes
  any generated media.
- Keep the local visual-geometry gates strict enough to reject the current
  warehouse page until the generated media and scroll-scrub implementation are
  materially better than code-native canvas.
- Promote the successful V4 mobile-polish pattern into future repair prompts:
  one owned CSS/component file, first-write proof, clean handoff completion,
  desktop/mobile scroll QA, and explicit mobile phrase-separation proof.
