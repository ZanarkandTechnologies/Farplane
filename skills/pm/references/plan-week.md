# Plan Week (interactive)

Use when the operator asks to plan, review, or reset the week. Interactive, not
automated. Weekly reporting across projects belongs to `report-gen`.

```text
plan_week(Life Plan + last Plan Week + goals + leverage ranking) -> negotiated week + saved Plan Week
```

## Inputs

- `Life Plan` page and the current quarter's goals with their critical path.
  Quarter goals are set once a quarter on the Farplane bunker's Mission board
  (`Farplane-UI-v2/docs/prd.md`, "The quarter loop"); read them from there and do
  not add a second goal-setting ritual to Plan Week.
- Last week's pinned `Plan Week`, plus what actually got done.
- Latest ranked leverage plays (`strategy/` leverage ranking) and open questions.
- Fixed dates this week: trips, meetings, deadlines. Ask once if unknown.

## Procedure

1. **Review last week.**
   - Outcomes planned versus done, with the reason for each miss.
   - Score the Great Work Check (0-2 per row). Name the lowest row.
2. **Choose the critical path.** One chain that everything else depends on this
   week. Say what slips if it slips.
3. **Set at most four outcomes,** each with a number or a done-when. Keep at most
   three active tracks; freeze the rest with one line on why.
4. **Protect a quiet day.** One block with no meetings or new ideas, used only
   for the critical-path item.
5. **Map the days for flow.** Assign kinds of work to days or blocks: outreach,
   building, filming, review. Do not mix them inside one block.
6. **Plan fun at three scales.** One small item this week, check that one medium
   item exists this month, and one large item this quarter.
7. **Triage carryover and new ideas** against the Life Plan guardrails; kill,
   park, or test with the cheapest test.
8. **Negotiate, then write.** After the operator accepts, create or update
   `Plan Week <Sunday date>` and pin it. Build it by carrying the previous
   Plan Week's whole body forward (Todos, Reflections, Positioning, Plan with
   Today / This Week / Long Term, Principles, Path, Personal Brand) and making
   minor edits only: keep the operator's wording and mark additions with a date
   tag such as `[30 Sep]`. Never regenerate the page from scratch. Read back
   every write.

## Rules

- Keep a `Pointers` section at the top of Plan Week: links or paths to the Life
  Plan, the ranked plays, the project list, and the ranked content backlog, plus
  the current critical path. Follow those pointers instead of re-deriving; keep
  detail in the owner and only pointers and this week's decisions on the page.

- New goals, changed obligations, and other people's actions stay proposals until
  accepted.
- Business targets follow the Farplane operating loop split (`Farplane-UI-v2/docs/prd.md`,
  "The operating loop"). Inputs (videos posted, DMs sent, offers shipped, buyer
  meetings) get a quarter target and a Monday quota of (target - done) / weeks left.
  Outputs (revenue, views, replies, sales) get no quarter forecast, only "better than
  last week". Do not write revenue forecasts as weekly targets.
- Price and cashflow items name a buyer and a number, or are marked door-openers.
- Unknown capacity and income targets stay unknown.
- Update the Life Plan in the same turn if the week changes direction.
- After saving, rewrite the `Now` section of `~/.farplane/USER.md`: at most 5
  live goals or problems, highest value first, each with deadline, target,
  floor, and a path or link to its owner. Replace finished or dropped items;
  never append. Read it back.
