---
name: delegate-frontend
version: 0.1.0
description: Delegate frontend implementation or design-polish work to the configured external CLI frontend profile, currently frontend-pi-kimi via delegate-cli, while preserving Codexter ticket, QA, visual review, and integration authority.
allowed-tools: Read, Grep, Glob, Bash
---

# Delegate Frontend

Use this profile skill when frontend implementation, page/component polish, or
visual craft should be built by an external CLI profile instead of the current
Codex lane.

## Trigger Conditions

- The user explicitly asks to delegate frontend work to another CLI/model.
- A ticket says the frontend builder should be external.
- `frontend-craft`, `visual-design`, or `landing-page` planning exists and the
  next step is implementation through a configured external agent.

## Workflow

1. Read the ticket or frontend brief.
2. Confirm the work is frontend build/polish, not UX-only planning or final
   visual QA.
3. Load `delegate-cli`.
4. Use profile `frontend-pi-kimi`.
5. For Terminal-style, cinematic, generated-media, or premium landing pages,
   delegate one phase at a time: `spec`, `assets`, `implementation`, then
   `visual-review`. Do not combine all phases in one live prompt.
   For self-improve or Terminus-level runs, compile the phase prompt with
   `skills/delegate-frontend/self-improve/scripts/phase_prompt_compiler.py`
   so the run has selected recipe/taste/effect IDs, owned outputs, first-write
   wording, and phase-specific acceptance criteria before Pi starts.
6. For implementation or repair phases, name the expected output file(s) and
   require a first-write checkpoint before broad review. If the external run
   reads for minutes without creating the requested file, kill it and record the
   handoff as failed rather than widening the prompt.
7. Run `python3 bin/sync_frontend_pi_skills.py --json` or
   `python3 bin/delegate_cli_agent.py setup --profile frontend-pi-kimi --json`
   so the managed Pi profile receives the curated frontend/media skill bundle.
8. Run `doctor`, then `run --dry-run`. Before another live Pi/Kimi spec or
   implementation attempt, run the lightweight startup probe plan:
   `python3 skills/delegate-frontend/self-improve/scripts/startup_probe.py --dry-run --json`.
   Run it live only when model spend is intentionally allowed.
9. Run live only after credentials/spend/filesystem gates are satisfied. For
   implementation and repair phases, pass each owned file with
   `--expect-output <relative/path>` so `first_write.json` records whether the
   external agent created or modified an expected regular file before the
   timeout. For bounded spec, asset, or implementation phases that are expected
   to finish by writing the managed handoff, also pass
   `--complete-when-output-and-handoff` so the wrapper can stop cleanly once the
   owned output and non-placeholder handoff exist.
   After an asset phase, run
   `python3 skills/delegate-frontend/self-improve/scripts/asset_manifest_lint.py <asset-manifest>`
   and do not start implementation unless it passes.
10. Send any resulting UI changes back through Codexter QA, `visual-qa`, and
    `review`.

## Core Decision Branches

- `workflow unclear` -> run `functional-ui` or `frontend-craft` first.
- `visual taste unclear` -> run `visual-design` before delegation.
- `landing page narrative` -> run `landing-page` before delegation.
- `cinematic landing build` -> require a `SPEC.md` or landing brief, then split
  the external run by phase and file ownership.
- `asset-heavy frontend` -> rely on the mounted inference.sh skills
  `image-generation`, `video-generation`, `remotion`, and `remotion-render`;
  do not require Codex-native `imagegen` in the external Pi profile.
- `Terminal/Terminus-level final build` -> require generated/rendered media or
  frame/video assets in `assets/asset-manifest.json`; treat `code-native-canvas`
  as a prototype fallback unless the user explicitly asks for a no-asset mock.
- `asset phase complete` -> lint `assets/asset-manifest.json`; if it lacks
  four local generated/rendered assets, source prompts, mobile/reduced-motion
  fallbacks, zero broken refs, and zero paths escaping the declared asset root,
  stay in the asset phase.
- `asset phase timed out after valid manifest` -> run a no-spend
  asset-finalization phase against the existing manifest. Require first-write
  readiness proof, canonical handoff headings, and the manifest linter before
  treating implementation as unblocked.
- `implementation ready` -> call `delegate-cli --profile frontend-pi-kimi` with
  `--expect-output` for the files the phase owns.
- `repair ready` -> compile a `repair` phase prompt with one owned output and
  explicit QA gates. The prompt must tell Pi not to read `scroll_scrub_qa.cjs`
  or broad references before patching, and must name the observable
  `hasStyleScrub`, `candidateChangeCount`, `hasSupportVideoDom`, and
  `hasMissionSupportVideos` scores when those are acceptance criteria.
- `large generated implementation needs media repair` -> prefer a small loaded
  sidecar script or CSS patch as the owned output instead of asking Pi to edit a
  40KB+ generated JS file directly. The sidecar should use known selectors from
  the prompt, wire generated media from the manifest, and avoid reading the
  large implementation before first complete output.
- `phase prompt has a managed handoff` -> add
  `--complete-when-output-and-handoff` so complete phase runs do not burn the
  full timeout after the handoff is written.

## Judgement Questions

Use `advise` when deciding whether the UI work is ready for external build, or
whether Codexter should first produce a stronger UX/visual brief.

## Top Gotchas

1. Do not use this skill for final visual judgment; use `visual-qa`.
2. Do not bypass `delegate-cli`; this is a profile skill, not a second platform.
3. Do not call the frontend profile a general solution for all CLIs.
4. Do not attach gold-reference screenshots to broad implementation prompts
   after the spec exists; summarize the reference in the spec and reserve
   screenshots for visual-review prompts.
5. Do not accept a timed-out partial external run as a successful handoff.
6. Do not add Codex-native `imagegen` to the Pi profile bundle; Pi should use
   the repo-owned inference.sh asset skills for repeatable external CLI work.
7. Do not let repair prompts start by rereading the whole page. Give the profile
   one owned file, the required debug contract, and the exact QA command; broad
   visual critique belongs after the first runnable artifact exists.
8. Do not skip `first_write.json` when the work is a live implementation phase;
   it is the machine-readable proof that the external CLI actually crossed from
   planning into regular-file production.
9. When a prompt includes a first-write requirement, say that the first external
   tool call must create or modify the named file with a valid stub before
   reading references. Directory creation and symlink creation are not enough.
10. If the prompt supplies the selected recipe/taste/effect IDs and acceptance
    criteria, tell the external profile to finish the owned artifact from those
    constraints before optional reference reading. Reference-chasing after the
    first write is a timeout risk.
11. Use clean completion only for bounded phases with a managed handoff. Do not
    use `--complete-when-output-and-handoff` for open-ended research, broad
    review, or tasks where the external process must continue after writing an
    initial handoff.
12. Clean completion requires more than headings. The handoff must have
    non-empty changed-files, verification, and risks/followups bodies, and
    changed-files must mention the expected owned output.
13. Asset manifests must not reference files outside the declared asset root.
    Reject absolute out-of-root paths, `../` escapes, symlinks, remote URLs, and
    existing unrelated local files.
14. Repair runs that only make a first-write stub and then read broad files are
    failed experiments. Convert the next attempt into a compiler-generated
    `repair` phase prompt with a micro-patch boundary and explicit observable
    QA scores.
15. Repair runs that pass DOM metrics by replacing a built page with a tiny
    dark text stub are failed experiments. Preserve the existing surface or
    start a new implementation output path instead of destructive simplification.
16. Mobile landing-page repair needs typography proof, not just scroll proof.
    When a multi-phrase hero title uses explicit breaks, require
    `hasMobileHeroPhraseSeparation` or an equivalent screenshot check so
    hidden `<br>` rules do not glue the headline together.
17. Repair first-write on existing files must be non-destructive. If Pi
    overwrites an existing built page or large script with a tiny stub and then
    stalls, kill the run, restore from backup or session evidence, and retry
    with a sidecar-owned output or smaller patch boundary.

## Outcome Contract

Return:

- profile used: `frontend-pi-kimi`,
- ticket or brief supplied,
- dry-run/live status,
- `first_write.json` status when live implementation was run,
- handoff/log paths,
- required QA and review follow-up.

## References

- [architecture.md](references/architecture.md)
- [workflows.md](references/workflows.md)
- [gotchas.md](references/gotchas.md)
