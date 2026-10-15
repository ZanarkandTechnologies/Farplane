# Goal Program Contract Review

Use this family when Goal Advisor, an issue's `## Goal program`, a generated
native Goal launcher, Goal packet references, or completion routing changes.

Required TAS: `TAS-A`

## TAS Guide

- `TAS-A`: objective, execution path, references, branches, proof, and stop
  conditions form one coherent issue-backed program that a fresh agent can run.
- `TAS-B`: one repairable binding, reference, recovery path, or proof closure
  still requires executor inference.
- `TAS-C`: the program can pursue the wrong outcome, load scope-expanding or
  contradictory context, stop with unsupported Done claims, or drift without a
  recoverable owner.
- `TAS-D`: ticket, program, launcher, or required evidence is unavailable.

## Required Checks

- [ ] `objective-fidelity`: The program advances the ticket's valuable outcome
  and does not substitute an easier metric, proxy, or neighboring task.
- [ ] `path-coherence`: Compiled Execution Path respects Contract Diagram
  dependencies and maps every material Change Plan unit to exit assertions and
  proof observations.
- [ ] `reference-necessity`: Every non-core file has a named consumer and
  purpose. Orphan, stale, redundant, and just-in-case references are absent.
- [ ] `assertion-closure`: Every Done assertion maps to executable proof,
  evidence ownership, and a status that cannot silently default to pass.
- [ ] `branch-completeness`: Material failures lead to bounded repair,
  diagnosis, feedback, rollback, or a named blocker.
- [ ] `stop-soundness`: `complete` is impossible while closure rows are pending,
  unsupported, stale, or contradicted by stronger evidence.
- [ ] `reconstructability`: A fresh agent can name current state, next eligible
  move, why it is eligible, and what will prove it from the issue body, the
  newest Goal turn comments within 80 lines, and listed files alone; a
  reviewer can rebuild the change from the issue without chat.
- [ ] `ownership-consistency`: Ticket sections own scope/proof, `## Goal
  program` owns instantiated loop policy, Goal turn comments own observations,
  `## Current Goal state` holds only the latest checkpoint, and the launcher
  remains a compact compiler output.

## Blocker Checks

- [ ] `contradictory-order`: Program order violates a ticket dependency or
  attempts proof before the state it observes can exist.
- [ ] `scope-by-reference`: A listed file silently expands executable scope.
- [ ] `premature-stop`: Progress, tests, or executor confidence can bypass an
  unsupported Done assertion or required independent review.
- [ ] `stale-binding`: Ticket/design/proof changed after compilation without a
  packet regeneration gate.
- [ ] `self-approval`: Material judgment is assigned to the executor that
  produced the candidate.

## Evidence Checks

- [ ] One coherent representative packet passes.
- [ ] One plausible-but-incoherent packet fails for semantic reasons rather
  than missing keywords.
- [ ] Hardcases cover irrelevant references, contradictory order, unmapped Done
  assertions, stale UI design, failure recovery, and premature completion.
- [ ] Validators check only mechanical shape; semantic findings cite
  ticket/program/launcher relationships.

## Finding Cues

- A polished launcher repeats policy while leaving actual moves vague
- References copied from older packets without named consumers
- Done mapped to “run tests” when the claim is an operated workflow
- UI completion cites `design.md` without comparing observed state IDs
- Recovery loops indefinitely instead of repairing or blocking
