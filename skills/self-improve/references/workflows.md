# Self Improve Workflow

## 1. Prepare The Goal

1. Confirm this is measured optimization, not an obvious direct repair.
2. Read the target skill, canonical suite, and owning ticket.
3. Define performance target, guards, editable scope, length metric, and
   separate harden/refine `max_rounds` plus patience.
4. Run the source stage before freezing it:
   - local failures first;
   - supplied references and configured Feed Scout signals when relevant;
   - bounded practitioner, paper, or book source upgrade for a named gap;
   - extract applicable techniques, mechanisms, variables, failure conditions,
     and source refs;
   - adversarial cases from `agent-qa-test`, accepted only by a separate
     evidence reviewer and Eval owner.
5. Seed `hypothesis-tree.json` with intervention hypotheses, expected
   observations, falsifiers, expected rewards, and reward bases. Use
   `leverage-advisor` for one ordinal compounding-leverage comparison when
   several credible initial leaves need judgment.
6. Use `goal-advisor` to instantiate the reusable template into the ordinary
   ticket Goal Packet and obtain operator approval.
7. Freeze the full suite and record the baseline.

## 2. Harden

On each native Goal turn, apply `choose_next` to the program policy, eligible
pending tree leaves, `progress.md` learnings, current Eval evidence, and
remaining harden budget. Invoke `leverage-advisor` only when several eligible
moves need judgment; execute a mechanically implied move directly.
Make the selected bounded instruction change, run the complete frozen suite,
and retain the candidate only when performance improves without a guard
regression. Continue until the full target passes. If harden patience or
`max_rounds` is exhausted first, stop blocked and do not refine.
When a result is surprising or causally ambiguous, add only program-bounded
diagnostic children; after diagnosis, repair, reject, defer, or backtrack.

## 3. Refine

Starting from the passing hardened candidate, replan from progress before each
round, then remove, merge, or condense the selected instruction boundary. Run
the same complete suite after every candidate.
Retain only a shorter candidate that preserves the hardened performance floor
and every guard. Otherwise restore the prior shortest passing candidate.

Stop on refine patience or `max_rounds`, run one final full-suite verification,
and return the shortest passing candidate discovered.

## 4. Handle New Evidence

Do not add a case during the frozen Goal. A newly accepted adversarial or source
case invalidates the comparison boundary: stop, update Eval, regenerate the
Goal Packet, and take a fresh baseline.

If the target lacks a clear trigger, workflow, or outcome contract, repair it
through `skill-maintenance` before optimization. If the signal requires delayed
real-world exposure, use the owning product experiment rather than expanding
this loop.
