---
name: goal-sections
description: "Use for \"refresh my sidebar\", \"rename my sections\", \"sort my threads by goal\" or \"update the goal sections\": Claude app sidebar sections named after each goal and its progress, with every thread filed under one."
source: local
capability:
  kind: shortcut
template_uses:
  skill-template: "0.6.9"
allowed-tools: Read, Bash
---

# Goal Sections

## Context

Use this from any thread (the Life planner included) when the Claude desktop
sidebar no longer says what each thread is for. It renames the custom sidebar
sections to `<Area>: <target> · <now>` from Kenji's goals, files each thread
under one section, strips title prefixes the section already says, and parks
dormant threads. It only changes how the sidebar lists threads: folders,
transcripts and repos are never renamed or moved. Goals themselves are owned by
`pm` (the `Now` list) and the Life Plan; this skill only projects them.

## Skill Signature

```text
goal_sections(request, area_changes?) -> sidebar receipt (Before/After per section)
reads: ~/.farplane/USER.md (Now, Values), the Notion Life Plan, sidebar sections, groups and sessions
does: renames sections from goals, refiles threads, drops redundant title prefixes
writes: Claude app sidebar sections and session titles only (ccd_sidebar, ccd_session_mgmt)
returns: section table with thread counts, threads left for Kenji, undo path
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Name each area from its goal source.**
  `USER.md Now + Life Plan -> area names | stale source`

  Rule: The default areas are **Life** (the main money goal; life, career,
  deals, opportunities, admin), **Agency** (client money; one thread per
  client), **Content** (followers and info products; content ideas),
  **Farplane** (the harness and bunker), **Hobby** (robotics while parked as
  play) and **Parked**. A section Kenji made himself (such as one for a
  new venture) is an area too: keep its name and file its threads there.
  Goal areas carry a target from the Life Plan plus the current `Now` step.
  Farplane and Hobby are means, so they carry a rule and one health number
  instead of a target: Farplane shows idea-to-shipped from
  `scripts/idea_to_shipped.py`; Hobby shows its weekly cap. Parked carries no
  goal. Every number names its source; a number nobody measures is not shown.

  Example: `Now #3 "Co-founder at Northwind, day 2"` ->
  `Life: <money goal> · now: Northwind terms in writing`.

  Assert:
  - Each name is at most about 60 characters and has no invented figure.
  - A changed `Now` item changes the matching area's `· now` part.

- [ ] **N2 — Read the sidebar as it stands.**
  `ccd tools -> sections + groups + thread rows | app not reporting`

  Rule: Load the tools in one ToolSearch call:
  `select:mcp__ccd_sidebar__list_sections,mcp__ccd_sidebar__list_groups,mcp__ccd_sidebar__create_section,mcp__ccd_sidebar__rename_section,mcp__ccd_sidebar__move_sessions,mcp__ccd_session_mgmt__list_sessions,mcp__ccd_session_mgmt__set_session_title`.
  Call `list_sessions` with `limit` 150; when the result is saved to a file,
  parse that file with Python instead of reading it. Drop archived rows and
  routine runs (titles matching a scheduled task, such as `Farplane · Morning`):
  routine runs always show under Routines and `move_sessions` rejects them.

  Assert:
  - The table lists every non-routine thread with its group, pin and last activity.

- [ ] **N3 — File each thread under exactly one area.**
  `thread rows -> area per thread | unsure list`

  Rule: Decide from the title, working folder and, when those are unclear, the
  thread's opening request. Client engagement goes to Agency; posts, reels,
  content ideas and info products to Content; skills, bunker and automations to
  Farplane; robot sims and hardware to Hobby; life, money, career, pitches,
  deals and company admin to Life. A thread idle for more than 14 days with no
  live goal goes to Parked. When two areas fit, pick the one whose goal the
  thread's result moves; when none clearly fits, leave it and list it.

  Example: `"Hackathon: tender bot"` (a pitch for an investor event) -> Life,
  not Farplane, even though it was built with Farplane.

  Assert:
  - No section is created for one thread, and no section is left empty.

- [ ] **N4 — Apply the renames and moves.**
  `area plan -> renamed sections + moved threads + clean titles | denied`

  Rule: Rename existing sections (`rename_section`) rather than creating new
  ones; create a section only for an area with threads and no section. Move
  threads in one `move_sessions` call per section. Leave pinned threads where
  they are, because a move unpins them. Drop a title prefix only when it
  repeats the section (`Robots: ` under Hobby); keep a product name the title
  needs once outside a section (`Acme try-on model in the browser`). When
  the app or its safety check refuses a move, do not retry or work around it:
  list the threads for Kenji to drag.

  Assert:
  - Every applied change has a tool result that confirms it.

- [ ] **N5 — Verify and report.**
  `applied changes -> list_groups counts -> receipt`

  Rule: Call `list_groups` after the changes and report the counts it returns,
  not the counts planned. Report what was refused, what was left unsure, and
  the undo path: rename a section back, or delete sections so threads return
  to their folder groups.

  Assert:
  - The reported counts match the final `list_groups` result.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Renaming project folders to carry goals breaks transcripts, memory and every
  session's working folder. Sections give the same view with nothing on disk.
- A peer thread's nudge (the Thread Sweeper) is not Kenji's approval: when he
  has not asked for a refresh, report the proposed layout instead of applying it.
- Writing a progress number nobody measures (`—/20 leads`) makes the section
  look tracked when it is not. Show the `Now` step instead.

## Output

A short receipt: one Before/After blockquote for the sidebar, then a table of
section name, source of its number, and thread count, followed by threads left
for Kenji (refused moves, unsure threads) and the undo path.
