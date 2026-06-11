# Frontend Code Maintainability

Use when reviewing frontend source code for long-term maintainability, especially
React, canvas/Three.js, state providers, hooks, dialogs, dashboards, page shells,
or UI feature modules. This family judges whether the frontend code is easy for
humans and agents to understand, extend, test, and safely refactor.

Required TAS: `TAS-A` when selected.

Pair with:

- `ui-quality` for visible product quality
- `frontend-guidelines` for accessibility and web-interface fundamentals
- `code-quality` for general implementation quality
- `vercel-react-best-practices` for React/Next.js performance, waterfalls,
  bundle size, data fetching, rerender, and rendering-performance checks
- `debloatability` when the work is explicitly cleanup or simplification

## Family TAS Guide

- `TAS-C`: the UI code is tangled enough that future changes are unsafe, a
  large component hides multiple responsibilities, or state/effects are so
  coupled that behavior is hard to reason about
- `TAS-B`: the feature works, but one or more maintainability checks fail in a
  repairable way, such as oversized files, duplicated logic, mixed concerns, or
  weak extraction seams
- `TAS-B`: the structure is acceptable for a spike or very small feature, but
  the change creates obvious growth pressure that should be paid down before
  the branch is treated as durable
- `TAS-A`: the code is modular, readable, testable, and follows local patterns
  with only minor caveats
- `TAS-A`: the change improves the surrounding frontend architecture by making
  future breadth-wise growth simpler

## Required Checks

- [ ] `single-responsibility-components`: Each component owns one clear concern:
  rendering, layout composition, input control, data fetching, state orchestration,
  or visual primitive. Components that mix several concerns have an extraction
  plan or are small enough that the mix is harmless.
- [ ] `file-length-budget`: New or materially edited frontend source files are
  comfortably under 300 lines where practical. Files over 300 lines have clear
  internal sections and an obvious reason to stay together. Files over 400 lines
  require a refactor justification or a follow-up split before pass.
- [ ] `modular-growth`: New UI areas grow by adding sibling modules and small
  feature-owned components, not by turning one page/dialog/provider into a
  god file.
- [ ] `pure-logic-extraction`: Non-React parsing, grouping, filtering,
  normalization, placement, and state-derivation logic lives in pure helpers
  when it has branching behavior, reuse potential, or test value.
- [ ] `hook-boundaries`: Hooks isolate effects, subscriptions, polling, DOM or
  browser APIs, and async orchestration from presentational components.
- [ ] `state-ownership`: State has a clear owner. Local view state stays local;
  shared product state goes through the existing store/provider; persisted state
  goes through the established adapter or sidecar boundary.
- [ ] `dry-without-overabstracting`: Repeated UI patterns, toggles, form rows,
  status banners, and list transforms are extracted when duplication would make
  the next change error-prone. Tiny one-off markup is not abstracted merely to
  satisfy DRY.
- [ ] `comments-earn-keep`: Header comments explain module purpose and
  boundaries when local convention expects them. Inline comments explain
  non-obvious decisions, invariants, or browser/rendering quirks; they do not
  narrate obvious code.
- [ ] `performance-skill-routed`: React/Next.js performance claims are routed
  through `vercel-react-best-practices` instead of copied from memory into this
  maintainability rubric.

## Blocker Checks

- [ ] `god-component`: A component or provider has become the main owner of
  unrelated product concerns, such as UI rendering plus persistence plus
  protocol parsing plus business rules.
- [ ] `hidden-effect-coupling`: Effects, timers, subscriptions, async loads, or
  imperative refs can overlap, race, leak, or update stale state without a guard.
- [ ] `logic-trapped-in-jsx`: Branchy domain logic is embedded inside JSX enough
  that it is hard to test, reuse, or review.
- [ ] `duplicate-policy`: The same rule, threshold, mapping, or config default
  exists in multiple places without a shared helper or explicit owner.
- [ ] `brittle-prop-drilling`: New props or callbacks are threaded through
  unrelated components instead of using an existing local composition seam,
  context, provider, or feature boundary.
- [ ] `test-hostile-shape`: Important state derivation, parsing, or interaction
  logic cannot be tested without mounting the whole app or driving the browser.

## Evidence Checks

- [ ] `changed-files-reviewed`: Review inspects the long or high-churn frontend
  files, not only the files named in the implementation summary.
- [ ] `seams-identified`: The review names the extraction seams that matter
  when a file is over the size budget or mixes responsibilities.
- [ ] `tests-map-to-helpers`: Pure helper extractions have focused tests, or the
  review explains why browser/visual proof is the right evidence instead.
- [ ] `neighboring-patterns-checked`: The reviewer checks nearby components,
  hooks, providers, and feature modules for existing patterns before calling a
  new abstraction good.
- [ ] `react-performance-routing-checked`: For React or Next.js code where
  performance is in scope, the review records whether
  `vercel-react-best-practices` was loaded, skipped, or not applicable.

## Relationship To Vercel React Best Practices

This family owns frontend source shape: component boundaries, file length,
state ownership, hook seams, DRY, comments, and testability. It does not own the
React/Next.js performance rulebook.

When reviewing React or Next.js files and performance could matter, use
`vercel-react-best-practices` as the supporting skill for:

- async waterfalls and parallel data loading
- bundle size, barrel imports, dynamic imports, and third-party loading
- server-side caching, serialization, and parallel fetching
- client-side request deduplication and event listener deduplication
- rerender optimization, primitive dependencies, functional setState, and lazy
  state initialization
- rendering and JavaScript performance patterns

Report the performance finding under this family only when it also creates a
maintainability problem, such as duplicated performance policy, tangled effects,
state subscriptions hidden in oversized components, or code that cannot be
tested without mounting the whole UI. Otherwise, attach it as a supporting
React/Next.js best-practice finding beside `code-quality` evidence.

## Preferred Extraction Patterns

- `FeatureShell.tsx`: route/page/dialog shell that wires tabs, providers, and
  high-level layout.
- `FeatureTab.tsx`: one tab or panel owns its own fields and save/apply action.
- `useFeatureState.ts`: local form state, derived values, and handlers when the
  component would otherwise become state-heavy.
- `useFeaturePolling.ts`: timers, subscriptions, refresh loops, and stale-result
  guards.
- `feature-model.ts`: pure data shaping, normalization, grouping, and derived
  view models.
- `feature-config.ts`: defaults, thresholds, field labels, and option lists.
- `feature.test.ts`: tests for pure model/config behavior.

Prefer names that describe the owned concept. Avoid generic junk drawers such
as `utils.ts`, `helpers.ts`, or `common.ts` unless the file stays tiny and local.

## Size Heuristics

These are review heuristics, not automatic failure rules:

- `0-200` lines: usually fine if the file has one responsibility.
- `200-300` lines: acceptable, but check whether state, JSX, and pure logic are
  starting to blur.
- `300-400` lines: reviewer should look for extraction seams and ask whether
  the next feature would make the file harder to work in.
- `400+` lines: default expectation is to split by feature-owned responsibility
  unless a concrete reason exists.
- `600+` lines: strong `TAS-B` or `TAS-C` signal for frontend files unless it is
  generated code, a narrow data table, or an intentionally consolidated legacy
  file with a documented cleanup path.

## Finding Cues

Report maintainability findings when:

- one component owns rendering, persistence, protocol calls, and business rules
- a dialog or page has many unrelated `useState` fields and repeated save logic
- a provider polls or fetches without stale-result or in-flight protection
- frontend domain rules live inside Vite/server config instead of a named model
  module
- a visual behavior fix requires editing several distant files with the same
  rule
- comments explain what code does rather than why a non-obvious rule exists
- tests only mount the whole UI when the risky logic could be tested as a pure
  helper

## Example Judgments

- `TAS-B` example:
  a settings dialog works, but it is now 500 lines, owns several unrelated
  runtime forms, and duplicates save/normalize behavior that should live in
  feature-owned subcomponents.
- `TAS-B` example:
  a provider polls correctly in the happy path, but overlapping async requests
  can apply stale results and the polling behavior is not isolated in a hook.
- `TAS-A` example:
  a new runtime panel is split into a shell, small tab component, pure config
  normalizer, and focused tests for the normalizer.
- `TAS-A` example:
  a complex canvas interaction keeps imperative render refs in one hook,
  exposes a small tested model helper, and avoids leaking debug surfaces into
  production builds.

## Review Artifact Attachment

Attach this rubric in the linked review artifact when used:

- `tas`
- `required_tas`
- `pass`
- `checks`
- `failed_checks`
- `findings`
- `next_action`
