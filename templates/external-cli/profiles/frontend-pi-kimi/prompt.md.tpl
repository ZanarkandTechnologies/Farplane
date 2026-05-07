# Delegated Frontend Run

Profile: {{profile_name}}
Adapter: {{adapter}}
Model: {{model}}
Run ID: {{run_id}}
Ticket: {{ticket_ref}}

## Delegate System Rules

{{append_system}}

## Task

{{prompt}}

## Ticket Context

{{ticket_context}}

## Skill Bundle

Use these mounted skill paths when relevant. For UI-bearing work, use the
frontend skills for implementation. For media-heavy or Terminal-style landing
work, use the mounted inference.sh image/video/remotion skills during the asset
phase, then use `visual-qa`, `review`, and `web-design-guidelines` in the same
Pi thread before writing the handoff:

{{skill_list}}

## Attachments

These files are attached to this Pi prompt as additional context:

{{attachment_list}}

## Output Contract

Write the final handoff here:

```text
{{handoff_path}}
```

Follow the handoff template. Include changed files, behavior built,
verification commands/results, self-review results, visual-QA results, risks,
and follow-ups. When the run was launched with `--expect-output`, include the
`first_write.json` status and path.

Use these exact handoff section headings so Codexter can detect bounded phase
completion before timeout: `## Changed Files`, `## Verification`, and
`## Risks / Followups`. Put non-empty content under each heading, and mention
the expected owned output file inside `## Changed Files`.

For scroll-scrub or Terminal-style landing pages, the handoff must also include:

- the selected recipe/taste/effect-stack IDs,
- whether `window.__scrollScrubDebug` satisfies the full debug contract:
  `progress`, `phase`, `frame` or `mediaTime`, `active`, `ready`, and
  `reducedMotion`,
- asset strategy, asset manifest path, generated/rendered media count, and
  whether any `code-native-canvas` fallback is only a prototype path,
- the scrubbed stage selector,
- checkpoint states at 0%, 25%, 50%, 75%, and 95% scroll,
- scroll-scrub QA JSON/screenshot artifact paths plus the `verdict` and
  `hasRequiredDebugContract` score when the harness can run,
- `terminalVerdict` and `terminalFinalReady` for Terminal/Terminus-level final
  builds; a basic `verdict: PASS` is only mechanics proof.
- `maxCheckpointChangedRatio`, `meaningfulCheckpointDeltaCount`,
  `strongCheckpointDeltaCount`, and `midScrollDeltaCount` so Codexter can
  reject tiny or one-transition-only scrub deltas.
- `hasTerminalMediaPipeline`, `hasDominantHeroMedia`, and
  `hasDistributedScrubDeltas` when the page is meant to prove final premium
  industrial scroll quality.
- `hasStyleScrub`, `candidateChangeCount`, `hasSupportVideoDom`, and
  `hasMissionSupportVideos` when the page is meant to prove a premium
  industrial computer-vision surface.
- `hasMobileHeroPhraseSeparation` when the page has a multi-phrase hero
  headline on mobile.

## Boundaries

- Codexter remains final integrator and may audit your self-review.
- Preserve unrelated changes.
- Do not push, deploy, publish, or perform destructive actions.
- Do not claim final Codexter completion. Produce a builder plus self-review
  handoff.
