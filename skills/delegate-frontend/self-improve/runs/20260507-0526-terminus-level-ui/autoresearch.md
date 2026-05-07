# Autoresearch: Terminus-Level Frontend Delegation

## Goal
Improve `delegate-frontend` and the `frontend-pi-kimi` profile so delegated
frontend runs reliably produce Terminal/Terminus-style landing pages with
measurable first-write, scroll-scrub, asset, and visual-parity evidence.

## Scope
- Target skill: `skills/delegate-frontend`
- Target profile: `templates/external-cli/profiles/frontend-pi-kimi`
- Supporting harness: `bin/delegate_cli_agent.py`
- QA harness: `skills/landing-page/scripts/scroll_scrub_qa.cjs`

## Metric
- Primary: `skill_eval_pass_rate`
- Direction: higher
- Verify: `python3 skills/delegate-frontend/self-improve/evals/runner.py`
- Autoresearch contract: runner prints `METRIC skill_eval_pass_rate=<number>`
  and exits `0`; failing assertions lower the metric instead of failing the
  experiment command.

## Binary Metrics
- `first_write.json` exists and records `pass` or intentional `dry_run`.
- Strict debug contract is present: `progress`, `phase`, `frame` or
  `mediaTime`, `active`, `ready`, `reducedMotion`.
- Scroll-scrub QA verdict is `PASS`.
- Prior fake-scroll page remains `FAIL`.
- Maximum checkpoint screenshot changed ratio is at least `0.15` for final
  Terminal/Terminus visual parity.
- `assets/asset-manifest.json` has generated/rendered media or frame/video
  assets; `code-native-canvas` is prototype-only.

## Baseline
- Initial self-improve baseline: `0.944444`
- Failures:
  - current warehouse page max changed ratio below `0.15`,
  - `asset_strategy: code-native-canvas`,
  - zero final media assets.

## Experiments
- H1: Add explicit final-quality rejection of code-native canvas.
  - Result: pass rate `0.947368`.
  - Keep: yes.
- H2: Require first external tool call to write the owned file stub.
  - Result: pass rate `0.949153`; Pi experiment 002 crossed first-write.
  - Keep: yes.
- H3: Prevent reference-chasing after first-write when prompt already supplies
  recipe/taste/effect IDs and QA requirements.
  - Result: pass rate `0.951613`; Pi experiment 002 diagnosis supports it, but
    follow-up experiments hit startup flakiness before a session file appeared.
  - Keep: yes, but continue testing.
- H4: Make eval cases replay captured candidate outputs and live-run summaries
  instead of reading whatever happens to exist in `.harness`.
  - Result: pass rate `0.948276` across 7 cases; remaining failures are the
    intended asset and large visual-delta gates.
  - Keep: yes.
- H5: Require `--expect-output` evidence to be a changed regular file and keep
  `first_write.json` even when the early timeout is set to `0`.
  - Result: delegate CLI unit coverage expanded to 27 tests.
  - Keep: yes.
- H6: Add local phase gates for spec completion, phase completion, asset
  manifest quality, visual geometry, and startup reliability before more live
  Pi/Kimi attempts.
  - Result: suite expanded from 7 to 14 cases; pass rate reset from `0.948276`
    to the harder baseline `0.804054`.
  - Keep: yes. The drop is intentional because the suite now catches known
    real failures instead of only measuring the older softer gates.
- H7: Add mechanical producers for visual geometry and delegate run summaries.
  - Result: `scroll_scrub_qa.cjs` emits `visualGeometry`, and
    `artifact_summary.py` emits `startup`, `phase_completion`, `spec`,
    `asset_manifest`, and `visual_geometry` summaries from real artifacts.
  - Keep: yes. The current warehouse page now fails a produced blank-band
    geometry check while still passing scroll mechanics.
- H8: Reject placeholder handoffs and verify replay-row provenance.
  - Result: `artifact_summary.py` ignores the prefilled "pending live external
    CLI run" handoff template, and `test_candidate_output_provenance.py`
    regenerates declared `summary_source` rows from artifact-shaped run
    directories. The hardened baseline is `0.812903` across 15 cases.
  - Keep: yes. Phase-completion rows can be trusted as producer-backed local
    replay evidence; no live Pi/Kimi completion is claimed yet.
- H9: Compile phase prompts and prepare a minimal startup probe before another
  live Pi/Kimi attempt.
  - Result: `phase_prompt_compiler.py` produces a first-write-oriented spec
    prompt with selected recipe/taste/effect IDs and phase boundaries;
    `startup_probe.py --dry-run --execute --json` rendered the delegate-cli
    startup probe command and mounted frontend skill bundle. The replay suite
    is now `0.824242` across 16 cases.
  - Keep: yes. The next live run can be a cheap startup probe, then a compiled
    spec phase if startup produces a session and first-write evidence.
- H10: Run the compiled startup probe live with settings that minimize first
  tool-call latency.
  - Result: `delegate-frontend-startup-probe-live-1` created a session but
    failed first-write with high thinking and a 45s gate.
    `delegate-frontend-startup-probe-live-2-low` passed with `--thinking low`
    and a 90s first-write gate, writing `PROBE.md` after roughly 15s and
    producing a non-placeholder handoff. Replay suite is now `0.837079` across
    17 cases.
  - Keep: yes. Treat session-only startup as insufficient; use low-thinking
    startup probe before compiled spec phases.
- H11: Fix metric semantics and evidence-contract edge cases found in final
  review.
  - Result: reject-control cases now use `expected_outcome: reject`, so
    `skill_eval_pass_rate` measures 17/17 expected accept/reject outcomes and
    `assertion_pass_rate=0.843434` remains the raw diagnostic. Startup probe
    artifact/probe paths derive from `--run-id`; short probe files can complete;
    positive phase handoffs include `First-Write Evidence` sections.
  - Keep: yes. The headline metric now describes skill behavior instead of
    penalizing intentionally failing quality gates.
- H12: Run the compiled spec prompt live and preserve process timeout as a
  reject-control.
  - Result: `delegate-frontend-compiled-spec-live-1` passed startup and
    first-write, wrote a complete 10,633-byte `SPEC.md`, and produced a
    non-placeholder handoff. The wrapper still exited `124`, so phase
    completion remains rejected. Replay suite is 18/18 expected outcomes,
    `skill_eval_pass_rate=1.000000`, `assertion_pass_rate=0.863436`.
  - Keep: yes. The spec prompt is viable; the next hypothesis should target
    clean stop-after-handoff behavior before asset or implementation phases.
- H13: Fix review-blocked parser and provenance gaps.
  - Result: prose-only stub specs now leave route IDs empty, and provenance
    tests derive marker text from each declared source before comparing the
    corresponding `must_contain` rule. Replay suite remains 18/18 expected
    outcomes, `skill_eval_pass_rate=1.000000`, `assertion_pass_rate=0.859031`.
  - Keep: yes. The self-improve loop should fail on stale marker text or route
    IDs inferred from absence prose before another live run.
- H14: Add wrapper-side clean completion for bounded phase handoffs.
  - Result: `delegate_cli_agent.py` gained opt-in
    `--complete-when-output-and-handoff`. Unit tests prove it terminates early
    after an expected output plus completed handoff, rejects placeholder
    handoffs, and works through the public command path. Replay suite remains
    18/18 expected outcomes, `skill_eval_pass_rate=1.000000`,
    `assertion_pass_rate=0.859649`.
  - Keep: yes. The next live compiled spec retry should use the flag to turn
    timeout-after-complete-spec into a clean phase completion.
- H15: Retry the compiled spec phase live with clean-completion support
  available.
  - Result: `delegate-frontend-compiled-spec-live-2-complete` passed
    first-write, wrote a 16,625-byte complete spec, produced a non-placeholder
    handoff, and exited `0` before timeout. The wrapper did not need to
    force-stop the process; the accepted fixture raises the replay suite to
    19/19 expected outcomes, `skill_eval_pass_rate=1.000000`,
    `assertion_pass_rate=0.875486`.
  - Keep: yes. The spec phase is live-proven. Move next to an asset-manifest
    phase with manifest linting before implementation.
- H16: Run the compiled asset phase live with generated media and manifest
  linting.
  - Result: `delegate-frontend-assets-live-1d` passed first-write in roughly
    7s, generated 4 videos, 1 image, desktop/mobile frame sequence endpoints,
    a poster fallback, and a 10-asset manifest. The manifest passed
    `asset_manifest_lint.py` with 0 errors and 0 warnings. The run still exited
    `124`, so the sanitized fixture is an expected reject. The replay suite is
    20/20 expected outcomes, `skill_eval_pass_rate=1.000000`, and
    `assertion_pass_rate=0.882979`.
  - Keep: yes. Asset generation is live-proven enough to preserve as evidence,
    but implementation must not consume it as a completed phase until the
    wrapper observes clean process completion or explicit clean completion.
- H17: Retry asset finalization without spending on additional media.
  - Result: `delegate-frontend-assets-finalize-live-1` wrote
    `ASSET_PHASE_READY.md` as first-write in roughly 8s, ran
    `asset_manifest_lint.py`, wrote canonical `Changed Files`, `Verification`,
    and `Risks / Followups` handoff sections, and the wrapper stopped it with
    `completion_reason=expected_output_and_handoff`. The replay suite is 21/21
    expected outcomes, `skill_eval_pass_rate=1.000000`, and
    `assertion_pass_rate=0.892508`.
  - Keep: yes. Use this no-spend finalization pattern to turn a generated
    media package into implementation-ready evidence before the build phase.
- H18: Fix review-found false positives in path and handoff completion gates.
  - Result: `asset_manifest_lint.py` now rejects absolute out-of-root files and
    parent-directory escapes, `artifact_summary.py` counts `unsafe_refs`, and
    wrapper clean-completion requires non-empty required handoff bodies plus a
    changed-files reference to the expected output. The new unsafe-ref fixture
    is an expected reject. The replay suite is 22/22 expected outcomes,
    `skill_eval_pass_rate=1.000000`, and `assertion_pass_rate=0.897590`.
  - Keep: yes. These blockers were real false-positive risks; the suite now
    catches them mechanically.
- H19: Seed implementation from the best existing artifact instead of asking
  Pi/Kimi for another full build from scratch.
  - Result: `delegate-frontend-implementation-live-5-seeded` copied/adapted a
    V4 page with generated media, GSAP/ScrollTrigger, mission support videos,
    style scrub, and large desktop/mobile screenshot deltas. Desktop and
    mobile scroll QA pass. The run still exited `124` and left the managed
    handoff placeholder, so it is an expected reject-control rather than a
    phase-complete implementation.
  - Keep: yes. Seeded implementation is a better artifact strategy than broad
    greenfield prompts, but phase completion remains a hard gate.
- H20: Add a mobile hero typography metric after visual QA found glued heading
  phrases.
  - Result: `scroll_scrub_qa.cjs` now emits `hasMobileHeroPhraseSeparation`
    based on hero title break visibility at mobile widths. The metric catches
    hidden `<br>` rules that visually glue phrases together while scroll
    mechanics still pass.
  - Keep: yes. This turns a taste/legibility miss into a repeatable binary
    check.
- H21: Try a one-file mobile CSS repair with a short first-write gate.
  - Result: `delegate-frontend-repair-v4-mobile-polish` opened a Pi/Kimi
    session but failed to edit the owned CSS file before the 60s first-write
    timeout.
  - Keep: yes as a reject-control. Session creation is still insufficient for
    repair progress.
- H22: Retry the same one-file repair with a longer first-write gate.
  - Result: `delegate-frontend-repair-v4-mobile-polish-2` edited
    `styles.css`, wrote a canonical handoff, exited through
    `completion_reason=expected_output_and_handoff`, and preserved desktop and
    mobile scroll QA. Mobile QA now passes `hasMobileHeroPhraseSeparation`.
    The replay suite is 29/29 expected outcomes,
    `skill_eval_pass_rate=1.000000`, and `assertion_pass_rate=0.901852`.
  - Keep: yes. Use bounded one-file repairs for polish, and allow one longer
    first-write retry before rejecting a micro-patch prompt.

## Live Pi/Kimi Run Evidence
- `terminus-self-improve-spec-exp-001`: failed first-write after 60s; Pi read
  references before creating `SPEC.md`.
- `terminus-self-improve-spec-exp-002`: first-write passed at ~24s; run timed
  out at 240s after broad reference reads and path mistakes; `SPEC.md` remained
  a stub.
- `terminus-self-improve-spec-exp-003`: failed first-write at 45s with no
  session file; timeout likely too aggressive or startup flake.
- `terminus-self-improve-spec-exp-003b`: failed first-write at 120s with no
  session file; startup/model/CLI flake remains a separate reliability issue.
- `delegate-frontend-startup-probe-live-2-low`: passed first-write and startup
  with low thinking and a 90s first-write gate.
- `delegate-frontend-compiled-spec-live-1`: passed first-write and wrote a
  complete spec, but total process timeout produced exit `124`.
- `delegate-frontend-compiled-spec-live-2-complete`: passed first-write, wrote
  a complete spec, produced a non-placeholder handoff, and exited `0`.
- `delegate-frontend-assets-live-1d`: passed first-write, generated real media,
  wrote a manifest that passes the asset linter, produced a complete handoff,
  but exited `124` at the wrapper timeout.
- `delegate-frontend-assets-finalize-live-1`: reused the existing manifest,
  did not call `belt`, wrote readiness proof, ran the linter, produced a
  canonical handoff, and exited `0` through the wrapper clean-completion path.
- `delegate-frontend-implementation-live-4`: crossed first-write but timed out
  with only a tiny scaffold and placeholder handoff.
- `delegate-frontend-implementation-live-5-seeded`: produced the strongest V4
  artifact and scroll QA pass evidence but timed out without managed handoff
  completion.
- `delegate-frontend-repair-v4-mobile-polish`: failed the 60s first-write gate
  despite session creation.
- `delegate-frontend-repair-v4-mobile-polish-2`: patched mobile hero
  typography, wrote a complete handoff, exited `0` through clean completion,
  and preserved scroll-scrub QA.

## Next Direction
The next experiment should split implementation into seeded slices instead of a
single broad build: scaffold/copy, media wiring, motion/debug, proof sections,
and mobile polish. Each slice should own one or a few files, use first-write and
clean handoff completion, then run `scroll_scrub_qa.cjs`, visual geometry,
visual QA, review, and `web-design-guidelines` proof before any Terminus-level
parity claim.
