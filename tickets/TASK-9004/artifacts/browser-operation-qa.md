---
ticket_id: TASK-9004
artifact: browser-operation-qa
created_at: 2026-08-02
owner: qa_task_9004_browser
context_ref: tickets/TASK-9004/ticket.md
verdict: pass
---

# Browser Operation QA

## Claim

`skills/functional-ui/SKILL.md` plus
`skills/functional-ui/references/comparable-patterns.md` gives an executable
public `agent-browser` path that can inspect established functional references
without login bypass, capture observed screens/states/access limits, and
distinguish Pinterest-style taste from functional proof.

## Proof Policy

- Read `tickets/TASK-9004/ticket.md`, `skills/functional-ui/SKILL.md`,
  `skills/functional-ui/references/comparable-patterns.md`,
  `skills/functional-ui/qa_checklist.md`, `skills/agent-browser/SKILL.md`,
  `skills/qa/SKILL.md`, `skills/qa/qa_checklist.md`, and `docs/TASTE.md`.
- Load `agent-browser skills get core` before operation.
- Operate public Mobbin and Page Flows surfaces only; do not log in or bypass
  account walls.
- Capture exact commands, public URLs, observed states/sequences, screenshots,
  source blockers, adopt/adapt/reject observations, verdict, and residual risk.

## Runtime Target

- Runtime: external public browser targets, no local app runtime.
- Browser tool: `agent-browser` CLI 0.27.0 with Chrome for Testing
  148.0.7778.167.
- Bound source URLs:
  - `https://mobbin.com/browse/web/apps`
  - `https://pageflows.com/`
  - `https://pageflows.com/web/`
  - `https://pageflows.com/web/flows/`
  - `https://pageflows.com/post/desktop-web/onboarding/heygen/`

## Commands And Evidence

```bash
agent-browser skills get core
agent-browser doctor --offline --quick
agent-browser --session task9004-mobbin open https://mobbin.com/browse/web/apps
agent-browser --session task9004-mobbin wait --load networkidle
agent-browser --session task9004-mobbin snapshot -i -u
agent-browser --session task9004-mobbin click @e17
agent-browser --session task9004-mobbin wait --load networkidle
agent-browser --session task9004-mobbin snapshot -i -u
agent-browser --session task9004-mobbin click @e11
agent-browser --session task9004-mobbin wait 1000
agent-browser --session task9004-mobbin snapshot -i -u
agent-browser --session task9004-mobbin screenshot tickets/TASK-9004/artifacts/mobbin-public-flows.png
agent-browser --session task9004-pageflows open https://pageflows.com
agent-browser --session task9004-pageflows wait --load networkidle
agent-browser --session task9004-pageflows snapshot -i -u
agent-browser --session task9004-pageflows click @e30
agent-browser --session task9004-pageflows wait --load networkidle
agent-browser --session task9004-pageflows snapshot -i -u
agent-browser --session task9004-pageflows open https://pageflows.com/post/desktop-web/onboarding/heygen/
agent-browser --session task9004-pageflows wait --load networkidle
agent-browser --session task9004-pageflows snapshot -i -u
agent-browser --session task9004-pageflows screenshot tickets/TASK-9004/artifacts/pageflows-heygen-direct.png
agent-browser --session task9004-pageflows click @e80
agent-browser --session task9004-pageflows wait 1000
agent-browser --session task9004-pageflows snapshot -i -u
agent-browser --session task9004-pageflows screenshot tickets/TASK-9004/artifacts/pageflows-heygen-generating-answer.png
agent-browser --session task9004-pageflows open https://pageflows.com/web/flows/
agent-browser --session task9004-pageflows wait --load networkidle
agent-browser --session task9004-pageflows snapshot -i -u
agent-browser --session task9004-pageflows screenshot tickets/TASK-9004/artifacts/pageflows-web-flows-index.png
```

Screenshots:

- `tickets/TASK-9004/artifacts/mobbin-public-flows.png`
- `tickets/TASK-9004/artifacts/pageflows-heygen-direct.png`
- `tickets/TASK-9004/artifacts/pageflows-heygen-generating-answer.png`
- `tickets/TASK-9004/artifacts/pageflows-web-flows-index.png`

`agent-browser doctor --offline --quick` passed: CLI, Chrome, state directory,
and daemons were healthy. No browser-tool blocker was observed.

## Operated Observations

### Mobbin

- Attempted URL: `https://mobbin.com/browse/web/apps`.
- Observed current URL/title: `https://mobbin.com/?redirect_to=%2Fdiscover%2Fapps%2Fweb`,
  `Mobbin -- UI & UX design inspiration for mobile & web apps`.
- Public state: marketing/landing surface with `Log in`, `Join for free`,
  `See our plans`, `Pricing`, `Awards`, and sections describing "Screens",
  "UI Elements", "Flows", and "Text in Screenshots".
- Interaction attempted:
  - Clicked footer/nav `Explore` link.
  - Clicked in-page `Flows` affordance.
- Result: no public app-flow index or individual flow was exposed from the
  attempted unauthenticated route. The route remained on the public marketing
  page with login/signup/pricing affordances.
- Access limit: public workflow inspection is currently limited without an
  account or plan. This is a source-access limit, not an `agent-browser`
  blocker.
- Evidence: `tickets/TASK-9004/artifacts/mobbin-public-flows.png`.
- Decision: `adapt` for source handling. Functional UI should still try Mobbin
  first when it is relevant, but receipts must record the public redirect/login
  wall and avoid inventing hidden flow states.

### Page Flows Web Index

- Attempted URL: `https://pageflows.com/`, then `https://pageflows.com/web/`
  and `https://pageflows.com/web/flows/`.
- Public state:
  - Homepage exposed search, platform tabs, `Explore Flows`, `Login`, and
    `Try 3 Days`.
  - Web page exposed `Products`, `Screens`, `UI Elements`, `Flows`, and public
    examples such as Lovable onboarding, HubSpot CRM onboarding, Claude
    onboarding, HeyGen onboarding, Asana upgrading account, and Etsy purchase.
  - Web flows index exposed categories such as `Onboarding`, `Upgrading
    Account`, `Inviting & Adding Friends`, `Purchasing & Ordering`, `Creating
    & Adding`, `Searching & Finding`, `Analyzing Stats`, `Deactivating &
    Deleting Account`, and `General Browsing`, plus product-specific flow
    links.
- Access limit: login and trial CTAs are present, but public flow indexes and
  many public flow pages were inspectable.
- Evidence: `tickets/TASK-9004/artifacts/pageflows-web-flows-index.png`.
- Decision: `adopt`. This satisfies the executable comparable-research shape:
  source URL, user job/query, public categories, concrete examples, and
  observed access limits.

### Page Flows HeyGen Flow

- Attempted URL:
  `https://pageflows.com/post/desktop-web/onboarding/heygen/`.
- Public state:
  - Page title: `HeyGen Onboarding Flow on Web | Page Flows`.
  - Heading: `Web Onboarding in HeyGen`.
  - Dated version control: `Version: October 2025`.
  - Related HeyGen flows: `Creating a folder`, `Creating an avatar`,
    `Creating a video`, `Updating your profile`, `Logging out`, `Changing
    password`, `Upgrading your account`, `Inviting people`, `Adding to
    favorites`, `General browsing`, `Help center`, `Deleting your account`.
  - Video player controls were present.
  - Timestamped sequence list was present, including `Home`, `Sign up`,
    `Enter code`, `Pricing & plans`, `Select number of people`, `Enter site
    URL`, `Get started`, `Add prompt`, `Submit`, `Generating answer`,
    `Loading`, `Enable new features`, `Generated AI`, `Download`, `Download
    complete`, `Select feedback`, `Onboarding tasks`, `Create video`,
    `Upload images`, `Select voice`, and return `Home`.
- Interaction attempted:
  - Opened the direct flow URL.
  - Clicked `01:08 Generating answer`.
  - Re-snapshotted and captured the state.
- Result: the public page preserved a timestamped sequence and exposed enough
  structured states to support workflow comparison. The click did not create a
  visible accessibility-tree delta in the captured snapshot, but it exercised
  an actual flow-step control and kept the current flow context.
- Access limit: repeated `Try 3 Days` links appeared next to many screenshots;
  bulk download/save and deeper media assets are trial/account-gated.
- Evidence:
  - `tickets/TASK-9004/artifacts/pageflows-heygen-direct.png`
  - `tickets/TASK-9004/artifacts/pageflows-heygen-generating-answer.png`
- Decision: `adopt` for workflow sequencing and state vocabulary; `adapt` for
  media/screenshot extraction because trial-gated assets should be recorded as
  access limits.

## Pinterest / Taste Boundary

The operated Page Flows pages exposed a Pinterest social link in the footer:
`https://www.pinterest.com/pageflowsdesign/_created`. The Functional UI skill
and comparable-patterns reference correctly classify Pinterest and similar
gallery/taste surfaces as visual inspiration only. This QA run did not count
that link as functional proof because the proof-worthy Page Flows evidence came
from operated product-flow pages with platform/category navigation, concrete
flow URLs, timestamped sequence states, and access-limit observations.

Decision: `reject` Pinterest-style boards as functional workflow proof;
`adapt` them only as taste inputs for `visual-design` or source-discovery inputs
for `ingest-content`.

## Obligation Reconciliation

| Obligation | Verdict | Evidence |
| --- | --- | --- |
| Load current `agent-browser` core instructions before operation | PASS | `agent-browser skills get core` succeeded and was applied. |
| Use public Mobbin/Page Flows or closest current URLs | PASS | Mobbin public redirect and Page Flows public indexes/flow page operated. |
| Capture observed screens/states/access limits without login bypass | PASS | Screenshots plus observed login/trial limits recorded for both sources. |
| Capture actual sequence/state evidence, not just web search/docs | PASS | Page Flows HeyGen flow exposed timestamped state list and related flow URLs. |
| Distinguish aesthetic/Pinterest-style taste from functional proof | PASS | Pinterest/social-gallery route explicitly rejected for functional proof. |
| Provide adopt/adapt/reject observations | PASS | Decisions recorded per source and boundary. |

## Failure Check

The most relevant falsifier was an access wall or static gallery masquerading
as operated workflow evidence.

- Mobbin currently redirected the attempted public browse URL to a marketing
  page with account and plan CTAs. The result was recorded as an access limit,
  not treated as hidden workflow evidence.
- Page Flows contained both trial CTAs and public flow pages. The run separated
  publicly observable flow structure from trial-gated save/download/media
  affordances.
- Pinterest-style surface was not used to satisfy the comparable-evidence
  requirement.

## Verdict

PASS for the requested browser-operation QA claim.

The Functional UI skill and comparable-patterns reference are executable with
current `agent-browser` commands and produce the intended evidence distinction:
operate public workflow references where possible, record access limits when
sources gate deeper inspection, and keep gallery/taste sources out of
functional proof.

## Blockers

None for the claim.

Source-specific limits:

- Mobbin public browse route did not expose workflow examples unauthenticated
  during this run.
- Page Flows save/download/deeper media affordances are trial/account-gated.

## Residual Risk

- Source access and URLs can change; future skill runs should preserve the
  inspected date, exact URL, and access state.
- This run proves the browser-operation path and source classification, not
  every possible Mobbin/Page Flows feature or authenticated account behavior.
- The clicked Page Flows timestamp did not show a detectable accessibility-tree
  change, so future high-stakes workflow proof should add video position or
  screenshot-diff evidence when the exact frame transition matters.

QA_RESULT: verdict=pass evidence=tickets/TASK-9004/artifacts/browser-operation-qa.md reason=public browser operation proved the executable comparable-evidence route and access-limit/taste-boundary handling
