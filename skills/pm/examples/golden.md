# Synthetic calibration: a week with progress and an appealing course

Input: The user requests advice about the remaining week, with no write request.
The current pinned Plan Week says to finish a gripper experiment and protect
Friday afternoon for building. A newer ordinary task has a later edit time.
The gripper project is `Info Dumped`, but two experiment tasks are Done. A Done
meeting says a collaborator might help teach a workshop; no buyers are confirmed.
An older open invoice follow-up is linked from the weekly cashflow section.

Trace:

- N1 selects the pinned Plan Week by planning date, includes the older invoice
  follow-up, and reads the meeting body despite its Done status.
- N2 treats the gripper project as executing despite stale metadata. It keeps
  workshop assistance conditional and distinguishes revenue interest from money.
- N3 recommends the next gripper experiment plus the existing invoice follow-up;
  workshop buyer discovery is a proposed test, not a booked course. It preserves
  Friday's accepted building allocation and makes no capacity claims beyond it.
- N4 is not entered for writes: advice does not update pages or processed state.

Accepted output: source-linked advice with one bounded experiment, reuse of the
invoice task, and an explicit workshop uncertainty. No duplicate setup task,
assumed buyer, or processed receipt appears.

Generic/no-skill failure contrast (hypothetical, not measured): taking project
status literally hides execution; taking Done literally hides meeting actions;
ranking only likely revenue displaces protected work. The transferable rule is
to reconcile record semantics and evidence before choosing priorities.

Behavior proof requires actual candidate/no-skill runs over normal, hard, and
boundary fixtures in `../evals/evals.json`; this trace is not that proof.
