---
name: delegate-frontend
version: 0.1.0
description: Delegate frontend implementation or design-polish work to the configured external CLI frontend profile, currently frontend-pi-kimi via delegate-cli, while preserving Codexter ticket, QA, visual review, and integration authority.
tier: 3
group: frontend
source: local
allowed-tools: Read, Grep, Glob, Bash
---

# Delegate Frontend

Use this when frontend work should be handed to the external Pi/Kimi frontend
agent instead of being implemented directly in the Codex lane.

## Job

Run a bounded external-CLI phase with the mounted frontend skills, collect the
handoff, and let Codexter integrate or reject the result.

## Default Profile

- Adapter: `pi`
- Model: `openrouter/moonshotai/kimi-k2.6`
- Profile root: `.harness/external-cli/profiles/frontend-pi-kimi`
- Run root: `.harness/external-cli/runs`

## Phase Types

- `spec`: produce or refine `LANDING_SPEC.md`; no implementation.
- `assets`: generate, collect, render, or manifest assets; no page build.
- `implementation`: edit the target frontend from an approved spec.
- `repair`: fix a named visual, motion, asset, or QA failure.
- `visual-review`: run same-thread review/visual-QA and produce findings.

## Required Inputs

- phase name
- run id
- owned output paths
- first-write path
- target page/spec path
- design brief path or explicit reason no durable design brief is needed
- stack facts: framework/router, Tailwind version, package availability,
  shadcn config, registry/theme plan
- acceptance criteria
- handoff path under `.harness/external-cli/runs/<run-id>/handoff.md`

## Command Pattern

Write the prompt to `.harness/external-cli/runs/<run-id>/prompt.md`, then run:

```bash
pi \
  --session-dir .harness/external-cli/runs/<run-id>/sessions \
  --model openrouter/moonshotai/kimi-k2.6 \
  --thinking low \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/frontend-craft \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/functional-ui \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/visual-design \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/landing-page \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/best-of-worlds \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/brainstorm \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/frontend-design \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/image-generation \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/video-generation \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/product-photography \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/agent-browser \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/visual-qa \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/review \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/web-design-guidelines \
  -p @.harness/external-cli/runs/<run-id>/prompt.md
```

Add other mounted skills only when the phase needs them.

## Rules

- Do not delegate vague "make it better" work. Convert it into a phase,
  owned files, and acceptance criteria first.
- Delegate prompts must include the design brief path, stack facts, registry or
  theme plan, and expected component-state proof when the phase touches reusable
  UI. If any item is unavailable, the prompt must say why.
- First external write must touch the named first-write path before broad
  reading or implementation.
- For premium landing pages, delegate only after the landing spec has research
  synthesis, best-of-worlds decisions, unique take, asset evidence, motion, and
  QA gates.
- For `spec` or `spec-research` phases, forbid reading `qa/**`, prior session
  JSONL, screenshots, videos, frame folders, and large generated assets unless
  the prompt explicitly requests visual review. Finish the owned planning
  artifact and handoff before optional artifact dives.
- For product, device, hardware, or equipment landing pages, mount and use the
  `product-photography` skill during the asset phase when available. Require
  realistic product shots/renders and assembly, disassembly, exploded-view, or
  feature-detail media instead of generic infographics.
- For premium product pages, require explicit product-clarity/accessibility QA:
  the hero and primary demo must keep the product inspectable, section text
  contrast must be readable, focus/skip-link affordances must exist, all images
  need alt text plus width/height attributes, and the handoff must report a
  `product_clarity_score`.
- For product teardown or exploded-view media, require a disassembly score:
  object continuity across states, component specificity, clean separation,
  product clarity, studio lighting, and no baked readable text or alphanumeric
  quality labels in generated pixels.
- For premium landing-page visual carriers, do not ask the delegated agent to
  create custom SVG illustrations, SVG diagrams, or SVG overlay art. Require
  generated/real raster media, or real WebGL/Three.js when a procedural visual
  is warranted.
- For cinematic hero scroll scrub, require a long authored media plan instead
  of a short decorative loop: 8-15+ seconds of seekable video or a 96+ frame
  sequence, at least five named beats, and a synchronized effect layer using
  GSAP, WebGL, Three.js, or HTML beat panels. The handoff must include debug
  evidence for media time, active beat, and effect-layer state.
- When the phase requests generated video, the delegated run must actually use
  the mounted `video-generation` skill and a video app/model. `Seedream` or
  other image-generation output plus local `ffmpeg` assembly is a frame
  sequence, not generated video. The handoff and manifest must record
  `skillsActuallyUsed` including `video-generation` plus `videoModel`,
  `videoProvider`, `sourceVideo`, or equivalent video provenance; otherwise
  Codexter must reject the handoff or downgrade the result to prototype.
- Require the handoff to list changed files, skills loaded, skills actually
  used, commands/results, risks, and next recommendation.
- Require implementation and repair handoffs to report stack facts observed,
  package or registry commands run, theme/preset changes, reusable component
  state coverage, and QA evidence for responsive, reduced-motion, focus,
  contrast, and overflow checks when UI changed.
- Codexter owns final verification and integration. Pi/Kimi does not claim final
  completion.

## Outcome Contract

After a delegate run, Codexter should have:

- `prompt.md`
- `command.json`
- `session_files.json` when available
- `handoff.md`
- the owned output files
- clear keep/repair/reject decision
- stack facts and design-brief traceability
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
   owned output and non-placeholder handoff exist. For sidecar or repair phases
   that can otherwise pass with a stub/no-op, add `--expect-output-min-bytes`
   and repeat `--expect-output-contains` for required contract strings such as
   `window.__scrollScrubDebug`, `mediaTime`, and any phase-specific marker.
   After an asset phase, run
   `python3 skills/delegate-frontend/self-improve/scripts/asset_manifest_lint.py <asset-manifest>`
   and do not start implementation unless it passes.
10. Send any resulting UI changes back through Codexter QA, `visual-qa`, and
    `review`. For runnable delegated UI, require the Pi profile to use the
    mounted `agent-browser` skill so page snapshots, screenshots, console logs,
    and page errors are captured in the same thread as the builder handoff.

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
- `browser-runnable UI` -> use mounted `agent-browser` inside the delegated
  thread for page-open, snapshot, screenshot, console, and error evidence before
  handoff; use specialized scroll-scrub QA in addition for Terminal-style
  pages.
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
- `Terminal first viewport lacks visible offer copy` -> require
  `hasInitialHeroOfferVisible` in QA and repair the owned sidecar/CSS so the
  primary headline or offer is visible before scroll; dominant media alone is
  not final readiness.
- `micro-repair keeps missing first-write` -> shrink to a compact prompt with a
  phase-scoped skill bundle and, when safe, give the external CLI an exact first
  command that modifies only the owned file.
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
18. Do not assume browser QA happened because the page renders locally. For
    delegated UI work, the handoff should name the `agent-browser` or visual QA
    artifacts that were actually captured.

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
