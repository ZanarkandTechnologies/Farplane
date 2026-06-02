# Notes

## Before
The delegated frontend profile could pass scroll mechanics after local repair,
but the output was not Terminal/Terminus-level. The visual deltas were tiny and
the asset manifest declared `code-native-canvas` with no generated media.

## After
The self-improve suite now measures:

- first-write evidence,
- strict debug contract,
- scroll-scrub pass/fail,
- fake-scroll rejection,
- mobile/reduced-motion proof,
- checkpoint screenshot changed ratio,
- generated/rendered asset presence.

The profile now tells Pi/Kimi to write the owned file first, avoid reference
chasing when the prompt supplies constraints, and reject code-native canvas as
final Terminus quality.

The eval runner now replays captured candidate outputs and live-run summaries,
prints `METRIC skill_eval_pass_rate=0.948276`, and exits cleanly so
autoresearch can compare variants without treating an expected quality gap as a
broken command.

The delegate CLI first-write gate now accepts only changed regular files.
Directories, symlinks, unchanged existing files, and timeout-zero runs without a
changed expected file produce failed `first_write.json` evidence.

The local replay suite now has 14 cases and scores
`skill_eval_pass_rate=0.804054`. The lower score is intentional: the suite now
catches stubbed specs after first-write, missing generated media, weak
first-viewport geometry, and Pi startup/no-session failures.

`scroll_scrub_qa.cjs` now emits `visualGeometry`, and
`self-improve/scripts/artifact_summary.py` turns run directories, specs, asset
manifests, and scroll QA JSON into replay rows. The suite now has 15 cases and
scores `skill_eval_pass_rate=0.806452`. The current warehouse page produced
`first_viewport_blank_ratio=0.3083`, so it fails geometry while still passing
scroll mechanics.

`artifact_summary.py` now rejects untouched handoff templates as placeholder
evidence. Replay rows that claim phase completion declare a `summary_source`,
and `test_candidate_output_provenance.py` regenerates their semantic summaries
from artifact-shaped run directories. The hardened 15-case baseline is now
`126/155`, `skill_eval_pass_rate=0.812903`.

The next-run prompt path is now local and testable. `phase_prompt_compiler.py`
creates bounded phase prompts with first-write wording, selected route IDs, one
phase boundary, and owned outputs. `startup_probe.py` builds a minimal
delegate-cli startup probe; its dry-run command rendered successfully. The
suite now has 16 cases and scores `136/165`,
`skill_eval_pass_rate=0.824242`.

Live startup probe evidence:

- `delegate-frontend-startup-probe-live-1`: high-thinking default with a 45s
  first-write gate produced a session but failed to write `PROBE.md`.
- `delegate-frontend-startup-probe-live-2-low`: low thinking with a 90s
  first-write gate passed. It wrote `PROBE.md` after ~15s, produced one session
  file, and wrote a non-placeholder startup handoff.

The sanitized success fixture is now part of the replay suite. The suite has
17 cases and scores `149/178`, `skill_eval_pass_rate=0.837079`.

The metric now separates expected accept/reject outcomes from raw assertion
ratio. Bad fixtures such as stub specs, missing generated assets, no-session
startup, and weak viewport geometry are marked `expected_outcome: reject`, so
their quality-gate failures count as correct rejection behavior. Current score:
`skill_eval_pass_rate=1.000000` for 17/17 expected outcomes, with
`assertion_pass_rate=0.843434` retained as the raw diagnostic.

Additional hardening after final review:

- startup probe default artifact and probe paths are derived from `--run-id`,
  so changing the run id no longer overwrites prior evidence,
- short regular probe outputs can complete a startup phase,
- handoff summaries include required section flags, and positive
  `--expect-output` fixtures now include `First-Write Evidence`.

Live compiled spec evidence:

- `delegate-frontend-compiled-spec-live-1`: low-thinking compiled spec prompt
  passed first-write at roughly 28s, wrote a complete 10,633-byte `SPEC.md`,
  and produced a non-placeholder handoff with first-write proof.
- The wrapper exited `124` at the total timeout, so the phase remains a rejected
  case even though startup, first-write, and spec-content gates pass.
- The sanitized fixture is now
  `fixtures/delegate-runs/compiled-spec-live-timeout/`, and the suite has 18
  cases with `18/18` expected outcomes, `skill_eval_pass_rate=1.000000`, and
  `assertion_pass_rate=0.863436`.

Review-blocker fixes:

- Prose-only stub specs no longer produce fake route IDs. `artifact_summary.py`
  now requires explicit labels such as `Recipe ID:` or `**Recipe ID:**`.
- Provenance tests now derive the expected output marker from each
  `summary_source` and verify that marker against the matching test case's
  `must_contain` rule.
- After these fixes the suite still has 18 cases with `18/18` expected
  outcomes, `skill_eval_pass_rate=1.000000`, and
  `assertion_pass_rate=0.859031` (`195/227` raw assertions passing).

Clean phase-completion detector:

- `delegate_cli_agent.py` now has an opt-in
  `--complete-when-output-and-handoff` flag for bounded phases.
- When an expected regular output changes and the managed handoff no longer has
  placeholder markers, the wrapper can terminate the external process with
  success instead of waiting for the total timeout.
- Unit coverage now includes direct first-write-gate early termination,
  placeholder handoff rejection, and public `command_run` behavior.
- The self-improve suite remains 18/18 expected outcomes with
  `skill_eval_pass_rate=1.000000` and `assertion_pass_rate=0.859649`
  (`196/228` raw assertions passing).

Live compiled spec success:

- `delegate-frontend-compiled-spec-live-2-complete` ran with
  `--complete-when-output-and-handoff`, passed first-write at ~29s, wrote a
  16,625-byte `SPEC.md`, and exited `0` before the 300s timeout.
- The clean-completion detector was available but did not need to force-stop
  the process; `first_write.json` has no `completion_reason`, which means Pi
  exited on its own after writing the full spec and handoff.
- The sanitized positive fixture is now
  `fixtures/delegate-runs/compiled-spec-live-success/`, with wrapper
  first-write evidence appended to the handoff.
- The suite now has 19 cases with `19/19` expected outcomes,
  `skill_eval_pass_rate=1.000000`, and `assertion_pass_rate=0.875486`
  (`225/257` raw assertions passing).

Live asset manifest evidence:

- `delegate-frontend-assets-live-1d` ran the compiled asset phase and crossed
  first-write in roughly 7 seconds.
- Pi/Kimi generated 4 videos, 1 image, desktop/mobile frame sequence endpoints,
  a poster fallback, and a 10-asset manifest with source prompts, mobile
  fallback, reduced-motion fallback, and no broken refs.
- `asset_manifest_lint.py` passed with 0 errors and 0 warnings.
- The handoff used live headings such as `Changed / Produced Files` and
  `Self-Review Findings`; parsers now accept these as semantic equivalents
  while the profile asks for canonical completion headings going forward.
- The wrapper still exited `124`, so the sanitized fixture is an expected
  reject even though the asset quality gates pass.
- The suite now has 20 cases with `20/20` expected outcomes,
  `skill_eval_pass_rate=1.000000`, and `assertion_pass_rate=0.882979`
  (`249/282` raw assertions passing).

Live asset finalization success:

- `delegate-frontend-assets-finalize-live-1` reused the existing generated
  asset package and explicitly did not call `belt`.
- Pi/Kimi wrote `ASSET_PHASE_READY.md` as first-write, ran
  `asset_manifest_lint.py`, and wrote a handoff with canonical `Changed Files`,
  `Verification`, and `Risks / Followups` headings.
- The wrapper recorded `completion_reason=expected_output_and_handoff` and
  returned exit `0`, proving the clean-completion path works for a bounded
  asset finalization phase.
- The accepted fixture is now
  `fixtures/delegate-runs/compiled-assets-finalize-live-success/`.
- The suite now has 21 cases with `21/21` expected outcomes,
  `skill_eval_pass_rate=1.000000`, and `assertion_pass_rate=0.892508`
  (`274/307` raw assertions passing).

Review-blocker fixes:

- Asset manifests now report `unsafe_refs` and the linter rejects absolute
  out-of-root paths plus `../` escapes, even when the referenced media file
  exists and has a valid signature.
- Handoff summaries no longer treat arbitrary non-placeholder text as complete;
  required changed-files, verification, and risks/followups sections need
  non-empty bodies.
- Wrapper clean-completion no longer accepts heading-only handoffs and requires
  the changed-files body to mention the expected owned output.
- The contradictory compiled-spec success handoff now states that
  `first_write.json` passed under `--expect-output`.
- The new unsafe-ref fixture is
  `fixtures/delegate-runs/asset-unsafe-ref-phase/`.
- The suite now has 22 cases with `22/22` expected outcomes,
  `skill_eval_pass_rate=1.000000`, and `assertion_pass_rate=0.897590`
  (`298/332` raw assertions passing).

Implementation and V4 repair loop:

- A fresh greenfield implementation prompt still failed first-write, confirming
  that broad implementation is too large for Pi/Kimi as one phase.
- A tiny scaffold phase succeeded, but the follow-on implementation timed out
  with only an 836-byte scaffold and a placeholder handoff.
- The seeded V4 run copied/adapted the best existing page into
  `.harness/warehouse-cv-scrollscrub-pi-kimi-v4/`. Codex-side QA reports
  desktop and mobile `PASS`, generated/support video DOM, GSAP/ScrollTrigger,
  style scrub, and large visual deltas, but the wrapper exited `124` with a
  placeholder handoff, so it remains an expected reject-control.
- Visual inspection found a mobile hero typo/spacing problem:
  `See every trailer.Know every dock.Automate every gate.`. The QA harness now
  reports `hasMobileHeroPhraseSeparation`.
- The first one-file mobile repair failed the 60s first-write gate. The second
  run with a 120s gate edited `styles.css`, completed through
  `expected_output_and_handoff`, preserved scroll QA, and mobile QA now passes
  `hasMobileHeroPhraseSeparation`.
- The suite now has 29 cases with `29/29` expected outcomes,
  `skill_eval_pass_rate=1.000000`, and `assertion_pass_rate=0.901852`.

## Live Experiments
Experiment 002 proved the first-tool-call wording can make Pi write the target
file. It still timed out before completing the spec, so the next bottleneck is
post-stub scope control and Pi startup reliability.

The compiled spec live run moved the bottleneck forward: Pi/Kimi can now
produce the complete spec from a bounded prompt, but the process still needs a
clean stop-after-handoff or wrapper-side completion detector before later
phases should rely on it.

The compiled asset run moved the bottleneck again: Pi/Kimi can generate real
media and a lint-clean manifest, but process-level completion and canonical
handoff headings still need to be hardened before the implementation phase is
treated as unblocked.

The no-spend finalization run closed that specific gap. The seeded V4 and
mobile repair runs moved the bottleneck again: Kimi can improve a seeded page
through a bounded repair, but full implementation still needs smaller
seeded-slice prompts and clean handoffs before parity can be trusted.

## Remaining Risk
No live Pi/Kimi run has yet produced a complete Terminus-level UI end to end.
The current loop can detect that failure mechanically. A seeded V4 artifact now
passes scroll/media/style/support-video QA and a bounded mobile repair passes
clean completion, but final visual QA, source-level web-design review, and
full parity remain unproven.
