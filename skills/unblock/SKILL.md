---
name: unblock
description: "Use for \"before we start this goal\", \"I'm blocked\", \"it's stuck on X\" or \"what else can I do\": a checked goal start, or the next move when a block hits, with one ask only when no work is left."
source: local
template_uses:
  skill-template: "0.6.9"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Unblock

## Context

Use this before any goal or unattended run, and whenever work stops on
something outside the thread. A block ends one bet, never the goal. A bet is
one thing to try. On a block with no goal, start at N4 and treat the current
step as the only bet; N1-N3 are for goals and unattended runs. A replay of 83
night stops found 32 with a real next move, 40 with only housekeeping, and 11
with nothing left. The diagram is [the map](references/map.md).

This skill owns start checks and what to do next. `goal-advisor` owns the Goal
Packet, `choose_next` owns ranking inside a packet, `ml-autoresearch` owns the
hypothesis tree, and `notify` delivers the ping.

## Skill Signature

```text
unblock(goal, block?, repo?) -> start_sheet | next_move | one_ping
reads: thread notes, Goal Packet or hypothesis tree if any, <repo>/docs/unblock.md
does: checks a goal can run, or picks the next move past a block
writes: ## Bets in the thread notes; in a packet, ## Current Goal state or the tree
returns: finish line, ranked bets, blocks table, touch test result, or next move
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Set a finish line and at least three bets.**
  `goal -> finish line + ranked bets | one question`

  Rule: A finish line is a check a thread can run. In a hand-set goal, turn a
  wish such as "perfect" into a provisional pass/fail test and say so. In a
  packet, a missing metric stays with `goal-advisor`, which never invents one.
  Write the budget and the exit: finish line met, budget spent, or every bet
  waiting after N6. Rank bets by gain times chance, divided by cost, starting
  at the biggest bottleneck. Keep one bet that avoids the riskiest service, and
  one that explores a new idea. Keep one list: a tree keeps its own statuses.

  Assert:
  - The finish line can fail, and each bet names its gain, cost and proof.
  - A material goal with no metric asks one question if the user is present.
- [ ] **N2 — Write the blocks table before starting.**
  `bets + repo history -> next 5 steps + likely block + Plan B`

  Rule: List what could stop each of the next 5 steps, using
  `<repo>/docs/unblock.md` and recent failures. Give each block a Plan B the
  thread can run alone. Do not simulate a whole conversation: it guesses, and
  the touch test finds out.

  Assert:
  - Every block has a Plan B or names what only the user can do.
- [ ] **N3 — Run the touch test.**
  `blocks table -> pass | fixed | swapped bet | asks for the user`

  Rule: Run after approval, in a packet's first turn. Run the repo's preflight,
  then make one cheap real call to every paid service the bets need, and check
  each device and login. A set key or a balance does not prove a call works.
  Run the first step for real if it is reversible and in budget. Bring anything
  only the user can do to them before they leave, all at once, then start.

  Assert:
  - Each check shows its real result, and the run starts on a bet that passed.
  - The test stays inside the task's spend, deploy and publish limits.
- [ ] **N4 — Classify a block and take the next move.**
  `block -> status + next move`

  Rule: Program stops, budget, a stale packet and evaluator drift win over this
  table. Otherwise use it, after any matching row in the repo's file. Mark the
  bet `waiting: <what>`, `lost` or `tool broke`, then take the next move in the
  same turn. Use `lost` only for an idea a real test failed; a provider or tool
  fault says nothing about the idea. While bets are open, a repeated stop hook or goal check gets a new
  move, never the same block again.

  | Block | Next move | Ping? |
  | --- | --- | --- |
  | Provider out of credit or refusing | An approved provider or saved answers | No |
  | Login, password, OAuth, CAPTCHA, payment | Mark waiting, next bet | Final ask |
  | Phone walk or hand test | Recorded walk, replay or simulator | Final ask |
  | Job, CI or another thread running | Background it, next bet, check at its limit | No |
  | Reversible choice in the same direction | Take the option worth most, write the undo | No |
  | Different direction or product choice | Mark waiting, next bet | Final ask |
  | Blocked before prod | Ship to dev if the task allows it, next bet | No |
  | Idea fails its kill rule, or 3 tries with none | Mark lost, next bet | No |
  | Tool, network or environment broke | Retry once, other route, next bet | No |
  | No bets left | N5 | No |
  | Public post, over the spend cap, losing the user's data | Ping now, keep working elsewhere | Yes |

  Assert:
  - The reply names the status and the move already started.
  - Plan B stays inside the task's spend, deploy and publish limits.
- [ ] **N5 — Refill an empty list before calling anything a blocker.**
  `no open bets + finish line -> new bets | truly empty`

  Rule: Measure the gap to the finish line, split it by cause, and write at
  least two bets for the biggest cause. Retry `waiting` bets whose cause has
  cleared. Truly empty means no in-scope cause is left, or one refill found no
  bet worth its cost. Stay inside the task's limits and an ML kill rule.

  Assert:
  - New bets aim at a named gap, not at nearby tidying.
- [ ] **N6 — Leave one ask, then end the turn.**
  `truly empty -> Waiting on Kenji line | Yes row -> one notify message`

  Rule: When the list is truly empty, write the goal, what was done and every
  waiting bet, then make the last line `Waiting on Kenji: <the one action that
  frees the most work>`; pick one even when several remain. Thread Sweeper delivers it, held until morning; outside
  the Claude app, send it with `notify`. A row marked Yes uses `notify` with
  intent `blocker` straight away.

  Assert:
  - The turn holds every ask, and its last line is the one action.
  - No row marked No sends a message.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- "Waiting for X" with a full bet list is not a stop.
- A Plan B that hides a quality drop must say so in the log.
- Housekeeping does not count as a next move when a real bet is open.

## Reference Map

- [map](references/map.md) - the loop as a diagram, for a reader.
- `<repo>/docs/unblock.md` - each repo's own blocks and Plan Bs.

## Output

Keep only the lines that apply. A job with no goal needs only the block and the
next move.

```text
Finish line: <check>
Bets: <ranked, with status>
Touch test: <check -> result>
Block: <row> -> <status>
Next move: <started now>
Ask: none | Waiting on Kenji line | notify receipt
```
