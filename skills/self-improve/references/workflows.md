# Self Improve Workflow

## 1. Prepare The Goal

1. Confirm this is measured optimization, not an obvious direct repair.
2. Read the target skill, canonical suite, and owning ticket.
3. Define performance target, guards, editable scope, length metric, and
   separate harden/refine `max_rounds` plus patience.
4. Strengthen coverage before freezing it:
   - local failures first;
   - optional bounded practitioner, paper, or book source upgrade when local
     evidence cannot choose a method;
   - adversarial cases from `agent-qa-test`, accepted only by a separate
     evidence reviewer and Eval owner.
5. Use `goal-advisor` to instantiate the reusable template into the ordinary
   ticket Goal Packet and obtain operator approval.
6. Freeze the full suite and record the baseline.

## 2. Harden

On each native Goal turn, make one bounded instruction change, run the complete
frozen suite, and retain the candidate only when performance improves without a
guard regression. Continue until the full target passes. If harden patience or
`max_rounds` is exhausted first, stop blocked and do not refine.

## 3. Refine

Starting from the passing hardened candidate, repeatedly remove, merge, or
condense instructions. Run the same complete suite after every candidate.
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
