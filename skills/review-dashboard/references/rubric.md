# Dashboard Review Rubric

Ten criteria. Grade each `0 unknown | 1 absent | 2 partial | 3 effective` and
quote the evidence. The mistakes listed are the ones agent-built dashboards
make most; check for them by name.

## D1 · One question, answered on top

The screen exists for one or two questions from its stories, and the answer
sits top-left of the first screen in words and a number.

- **Signals:** the first heading names the answer, not the data source; the
  answer is visible without scrolling at 1440×900; analysis opens with a
  plain-English verdict sentence ("Version B is winning, 96% likely to be
  best") before its tables.
- **Mistakes:** a banner about a pipeline error takes the top third; a row of
  every metric comes before the one that's red; a picker of all projects comes
  before the project's own state.
- **Before → After:** `Top: 11 project chips, then 5 metric tiles` →
  `Top: "Revenue is behind: 40% of this month's target · see its tests"`, project
  picker moved to the title's dropdown.
- **3** the answer is the first thing read · **2** visible but competing ·
  **1** below the fold or absent.

## D2 · Each fact once

A number, item or status appears once per screen, and one set of items lives
on one screen.

- **Signals:** the same metric in a tile strip, a goal list and a heatmap; two
  metrics that always read the same value; two screens whose cards are the same
  items.
- **Mistakes:** "metrics", "goals" and "weekly status" sections each listing the
  same two metrics; a reach metric that equals one platform's views; a Library
  and a Mood board showing the same eight saves.
- **Before → After:** three sections × the same metric → one row per metric with
  its value, target, trend and status.
- **3** no repeats · **2** one repeat with a purpose (e.g. trend vs detail) ·
  **1** repeats with no new information.

## D3 · The operator's words

Labels, statuses and empty states use the words the operator says out loud.

- **Signals:** no internal ids (`biz_…`, ticket hashes), file paths, ISO
  timestamps, seconds counts, pipeline verbs (emitted, rollup, projection,
  sync), tier or template codes, or a paragraph explaining where the data comes
  from; labels in sentence case, with letter-spaced capitals kept for one small
  eyebrow per group; dates relative in feeds (`2 days ago`) and short in tables
  (`4 Oct`).
- **Mistakes:** `last read 2026-10-04T00:00:00.000Z`; `The final 61,204 seconds
  are uncovered`; `TEMPLATE STALE` on 91 rows; a footer showing a folder path.
- **Before → After:** `last read 2026-10-04T00:00:00.000Z` → `read this
  morning`; `Where client memory comes from` section → a `?` that opens it.
- **3** none · **2** a few in secondary text · **1** in headings or statuses.

## D4 · Red means act

One status vocabulary with a word and a colour, and red only for what the
operator should act on now.

- **Signals:** statuses are words (On track · Behind · Not read · No goal), not
  colour alone; `Blocked` only when something is blocked; most items are not
  red; every headline number carries its comparison (`↑ 14% on last week`, `of
  3,000`); masked money still leaves a readable status or trend.
- **Mistakes:** every card says `Blocked` because each is a little behind pace;
  every eval row is red; a cash screen that is a grid of `******` with no trend
  word when money is hidden.
- **Before → After:** four red `Blocked` cards → cards sorted by how far behind,
  `Behind · 87% of pace` in amber, red kept for below a set floor.
- **3** calibrated · **2** right words, too much red · **1** colour-only or
  mislabelled.

## D5 · Empty is a sentence

No data reads as one sentence saying what's missing and the one action that
fills it.

- **Signals:** no chart of all zeros, no single-point chart, no grid of zero
  counters, no `[no snapshot]` repeated in every row, no axis labelled
  `0.05` for a count.
- **Mistakes:** four "needs you" tiles all reading 0; a subscriptions chart with
  a flat zero line and a 0–0.1 axis; a table column of `[no snapshot]`.
- **Before → After:** four zero tiles → `Nothing needs you`; zero chart →
  `No subscriptions yet · first one shows here`.
- **3** every empty state is a sentence with its action · **2** some drawn
  empties · **1** empties dominate the screen.

## D6 · Fits without cutting the point

The primary label, goal or title is never truncated; long real data still fits.

- **Signals:** no `…` in a title, goal, metric name or status; ellipsis only on
  secondary text with the full text on hover or click; the layout holds with
  the longest real names and the most items.
- **Mistakes:** the quarter's goal cut to `SIGN THREE PILOT CUSTO…`; metric
  names cut to `Monthly revenue (30 d…`; sticky notes cut mid-word.
- **Before → After:** fixed-size sticky with ellipsis → sticky that grows, or a
  shorter label written for the space.
- **3** nothing primary cut · **2** secondary cuts only · **1** primary cut.

## D7 · Detail behind a click

The first screen fits a density budget; the rest is one click away inside the
same screen (drawer, row expand, detail page).

- **Signals (from `scripts/screen_stats.mjs`):** words above the fold ≤ ~150,
  controls ≤ ~12, font sizes ≤ 4, competing big numbers ≤ 6; an index is a list
  or table with detail in a side panel, not cards of paragraphs; a media card
  carries at most one overlay on its image.
- **Mistakes:** every eval run's failing tasks inline; a paragraph summary on
  every card; six stat tiles of harness jargon above the list.
- **Before → After:** 335 words above the fold → the headline, a 5-row table,
  and failures in a row drawer.
- **3** within budget · **2** one dimension over · **1** two or more over.

## D8 · One component per job, app-wide

Each job uses the app's one shared component and the app's visual language.

- **Signals:** underline or segmented tabs for views, chips only for filters;
  one stat tile, one card, one chart, one table, one date format, one empty
  state; one primary action, top-right of the screen's header, and one
  page-level date range beside it; one graph node grammar (shape encodes kind,
  fill encodes status, corners match the app's: square apps use square nodes;
  entity graphs elsewhere mostly use circles, catalog maps icon rects, so say
  which you follow and why).
- **Mistakes:** tabs drawn as square buttons on one screen, pills on another,
  a vertical list on a third; one graph with square icon nodes and another with
  circles; dates as ISO, `Oct 4, 2026, 12:00 AM` and `4 Oct` on neighbouring
  screens; a serif face or handwriting font for body text.
- **Before → After:** three tab styles → the shared segmented control; circle
  wiki nodes → the square icon nodes the capability map uses.
- **3** shared components only · **2** one stray style · **1** several.

## D9 · Matches the closest real product, or says why not

The screen's structure matches what the closest real products do for the same
question, or the difference earns its place.

- **Signals:** the reference's first-screen answer, hidden detail and controls
  are recorded; each deviation has a reason tied to a story.
- **Mistakes:** a client list as long prose cards where CRMs use a table with a
  side drawer; an analytics page with one chart at a time where analytics tools
  show a grid; a menu of seventeen text cards where launchers show a few pinned
  items and search.
- **3** matches or deviates on purpose · **2** partly · **1** ignores it.

## D10 · Earns its place

The screen serves a story the operator runs at a cadence, and is reachable in
two clicks from where that story starts.

- **Signals:** at least one story with a cadence; no other screen serves it;
  it isn't the same panel opened with a different filter under a second name.
- **Mistakes:** a "Skill Rollout" screen that is Skill OS with a filter; a
  "Clients" screen that is the graph on a lens; four screens that each list
  saved links; an explainer section that nobody returns to.
- **Before → After:** two menu entries for one panel → one entry whose filter
  is a chip.
- **3** unique and used · **2** overlaps another screen · **1** no story or a
  duplicate.
