---
name: review-dashboard
description: "Review a dashboard screen, or a whole app's dashboards, against ten clarity and consistency criteria and the closest real products, then return a keep, fix, merge or cut verdict with Before/After changes."
source: local
department: operations
template_uses:
  skill-template: "0.6.3"
allowed-tools: Read, Glob, Grep, Bash, WebSearch, WebFetch
---

# Review Dashboard

## Context

Use this skill before building, after building, or when an operator says a
screen is confusing, overloaded or inconsistent. It judges a dashboard by the
question it exists to answer, measures what the first screen actually shows on
real data, compares it with the closest real products, and returns the smallest
change set. It reviews; it does not redesign the visual system (that is
`visual-design`) or diff a build against an accepted board (that is
`visual-qa`).

## Skill Signature

```text
review_dashboard(screens, stories?, references?, scope = screen | portfolio)
  -> screen_reviews + portfolio_findings? + verdicts
reads: each screen's code and data route, captures on real data, the operator's stories
does: grades ten criteria from captured evidence and picks keep | fix | merge | cut
writes: captures and stats under the caller's scratch folder; the review only when asked
returns: per-screen review cards, cross-screen findings, and ranked Before/After changes
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Name the question each screen answers, and who asks it when.**
  `screen code + entry points -> story card | no_story`

  Rule: Write each screen's stories as `When <moment>, I want <answer or
  action>, so <outcome>`, with a cadence (daily, weekly, when something breaks).
  The question comes from the operator's moment, not from the data the screen
  happens to read. A screen with no story is a cut candidate, not a fix.

  Example: `CEO desk -> "When I start the day, I want the one red number and its
  next step, so I unblock it before anything else" (daily)`.

  Assert:
  - Every screen has 1–3 stories or is marked `no_story`.
  - Two screens serving the same story are flagged as a merge pair.

- [ ] **N2 — Capture the first screen on real data and measure it.**
  `running app -> first-screen + full captures + stats.json`

  Rule: Capture at the operator's usual size (default 1440×900) with real data
  and the default state (masked money stays masked). Run
  `node scripts/screen_stats.mjs <url> <root-selector>` for words, controls,
  font sizes, colours and radii above the fold. Fixtures are evidence only when
  the screen has no real data yet, and the review says so.

  Assert:
  - Each screen has a first-screen capture, a full capture and its stats.
  - Error, empty and loading states seen during capture are recorded as findings.

- [ ] **N3 — Find the closest real products' version of the screen.**
  `story card -> 1–3 reference screens + what they put first`

  Rule: Pick products whose user asks the same question (Stripe home for a
  business's day, PostHog for a chart grid, Attio for a client list). Use
  Refero searches, the products' docs or public demos; never log in, sign up or
  get around a block (Mobbin refuses automation). Record what their first
  screen answers, what they hide behind a click and which controls they use.

  Assert:
  - Each reference names product, screen and source link or capture path.
  - Missing references are `unknown`, not invented from memory.

- [ ] **N4 — Grade the ten criteria from the evidence.**
  `captures + stats + references -> criterion grades`

  Rule: Load [references/rubric.md](references/rubric.md). Grade each criterion
  `0 unknown | 1 absent | 2 partial | 3 effective`, quoting the label, number
  or capture that proves it. Do not sum grades into a score.

  Assert:
  - Every grade of 1 or 2 cites visible evidence (quoted text, stat or capture).
  - Repeated facts, truncated primary labels and jargon are quoted verbatim.

- [ ] **N5 — Pick the verdict and the smallest change set.**
  `criterion grades + stories -> keep | fix | merge | cut + Before/After`

  Rule: Fix the criterion closest to the screen's question first. Prefer
  removing, folding or reusing a shared component over adding a new one. A
  merge names the surviving screen; a cut names where its one useful part goes.

  Example: `Library and Mood board list the same eight saves -> merge: Mood board
  becomes Library's "Parts" view; Before two menus, After one`.

  Assert:
  - Each change has Before, After and the criterion it fixes.
  - No change adds a screen, a tab or a component that a shared one covers.

- [ ] **N6 — For a portfolio, run the cross-screen pass.**
  `all screen reviews -> component inventory + duplicates + navigation map`

  Rule: List every style used for the same job across screens (tabs, filter
  chips, stat tiles, cards, charts, tables, graph nodes, date formats, empty
  states, status words). Any job with two or more styles is a finding with the
  one style to keep. Group the dashboard menu by the operator's moments
  (start of day, weekly review, when something breaks), not by data source.

  Assert:
  - The inventory names, per job, the kept style and every screen that diverges.
  - The navigation proposal shows at most seven top-level entries.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Redesigning before naming the question: a prettier CEO desk that still shows
  the same metric three times fails D1 and D2. Write the story first.
- Judging fixtures or the unmasked state: the operator sees real data with money
  hidden. A screen that reads only `******` when masked has no signal (D4).
- Treating a requested metaphor as the defect: a cork board or brass plaques the
  operator asked for stay; judge the legibility, type scale and status words
  inside them (D6, D8).
- Fixing overload by adding a tab or a new screen: move detail behind a click
  inside the same screen, or merge screens that serve one story.

## Output

Return a **Dashboard Review** per screen and, for a portfolio, a summary:

- **Screen card:** id, stories with cadence, closest products, the ten grades
  with evidence, verdict (`keep | fix | merge into <id> | cut`), and the ranked
  Before/After changes.
- **Portfolio:** the component inventory with the style to keep per job,
  duplicate screens, the regrouped dashboard menu, and the five changes with
  the most reach (screens touched × how often the operator opens them).
