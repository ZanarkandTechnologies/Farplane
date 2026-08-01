---
name: self-improve
description: "Optimize one existing skill through a Goal-backed harden-then-refine loop over a frozen eval suite."
tier: 3
group: self-improvement
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.2.0"
eval: evals/evals.json
planner_contract:
  required_arguments: ["target_skill", "performance_metric", "feedback_class", "failure_evidence"]
---

# Self Improve

## Context

Use this when an existing skill has a measurable behavior gap and should improve
over multiple bounded turns. Native Goal is the sole continuation engine. Each
invocation instantiates [the reusable Goal program](references/goal-program-template.md)
into the owning ticket's ordinary Goal Packet:

```text
tickets/TASK-XXXX/
  ticket.md
  program.md
  hypothesis-tree.json
  progress.md
  artifacts/native-goal-prompt.md
```

The target keeps its live `SKILL.md` and canonical `evals/evals.json`. Eval
owns execution and generated evidence under `.farplane/evals/runs/`. Do not
create target-local lifecycle state or another decision engine.

## Skill Signature

```text
self_improve(target_skill, performance_metric, feedback_class, failure_evidence,
             owning_ticket?, eval_suite?, guards?, intervention_catalog?, budgets?)
  -> approved_goal_packet + shortest_verified_passing_candidate + eval_evidence

state:
  reads(target SKILL.md, canonical evals/evals.json, owning ticket, program
        policy, hypothesis-tree.json, progress.md learnings, generated Eval
        evidence)
  writes(ticket program.md, ticket hypothesis-tree.json, ticket progress.md,
         native Goal prompt, accepted target-skill change)

gates:
  target_exists; owning_ticket_exists; metric_named; suite_frozen;
  baseline_recorded; guards_named; phase_budgets_named; source_stage_grounded;
  hypothesis_tree_bound;
  packet_approved

routes: leverage-advisor | goal-advisor | eval | metric-advisor | skill-maintenance |
  agent-qa-test | review

fails:
  taste_only_optimization; mutation_before_baseline; changing_suite_mid_goal;
  refinement_before_target; behavior_for_length_trade; unmeasured_promotion;
  target_local_loop_state; adversary_self_approval
```

## Mandatory Composition

Every Goal Packet and active-turn decision must make this named composition
explicit:

```text
source_stage(local failures + supplied sources + Feed Scout signals?)
  -> techniques + mechanisms + variables
leverage_advisor(source synthesis) -> initial hypothesis candidates + first selection
campaign.initialize_tree(initial hypothesis candidates)
goal_advisor(ticket.md + program preset + hypothesis-tree.json + progress.md)
  -> approved Goal Packet
leverage_advisor(program.md policy + pending tree leaves + progress.md learnings
                 + current Eval evidence + remaining phase budget) -> next experiment
eval(next experiment, frozen complete suite) -> evidence
update_tree(result + insight + bounded diagnostic children?)
progress.md.append(selection + tree mutation + evidence + next_action)
native_goal(updated packet state) -> continue | transition | block | complete
```

Goal Advisor is only the packet/native-Goal compiler. Leverage Advisor is the
only harden/refine experiment selector. Do not replace either named owner with
anonymous equivalent logic, and do not select a candidate directly before the
Leverage Advisor checkpoint.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read the target `SKILL.md`, canonical `evals/evals.json`, and owning
  ticket. Route an obvious deterministic repair to direct maintenance instead
  of creating an optimization Goal.
- [ ] 2. Bind the performance metric, passing target, guards, editable search
  space, length metric, and separate harden/refine `max_rounds` plus patience.
  Use `metric-advisor` only when an honest metric cannot be stated directly.
- [ ] 3. Run the source stage and seed the hypothesis tree before freezing the
  Goal.
   - [ ] Start from local failures and scored history.
  - [ ] Add supplied references, configured Feed Scout signals, or bounded
    practitioner, paper, or book research through
    `skill-maintenance:upgrade_skill_from_sources`; keep the source packet out
    of the Goal state and record `adopt | adapt | reject | defer` decisions.
   - [ ] Extract only applicable techniques, mechanisms, variables, failure
     conditions, and source refs. Generate initial intervention hypotheses with
     expected observations, falsifiers, expected compounding rewards, and short
     reward bases in ticket-local `hypothesis-tree.json`.
   - [ ] Route adversarial cases through `agent-qa-test`; a separate evidence
     reviewer must accept a case before Eval does. The tester cannot approve its
     own case.
   - [ ] Use [leverage-advisor](../leverage-advisor/SKILL.md) for one ordinal
     compounding-leverage comparison over eligible leaves and the first proof.
     Do not use a pairwise tournament, persistent score table, or invented lift.
- [ ] 4. Invoke `goal-advisor` to instantiate
  `references/goal-program-template.md` into the ticket's `program.md`, create
  or update `hypothesis-tree.json` and `progress.md`, and compile a compact
  Files-listed native Goal prompt. Material packets remain pending until the
  operator approves the current ticket, program, tree, progress scaffold, and
  prompt together.
- [ ] 5. Freeze the complete suite for the Goal and record the baseline before
  editing. If an accepted case changes the suite later, stop and regenerate a
  fresh packet and baseline; never change cases mid-comparison.
- [ ] 6. Harden first. Before each turn, invoke Leverage Advisor on the
  `program.md` policy, pending tree leaves, `progress.md` learnings, current
  Eval evidence, and remaining harden budget to choose one eligible bounded instruction
  experiment. Verify that one complete round fits the remaining budget; never
  assume an unstated budget or candidate prerequisite. Run the complete frozen
  suite and retain it only when behavior improves and every guard passes.
  Update the selected node, add only program-bounded diagnostic children for a
  surprising or causally ambiguous result, then append the selection, tree
  mutation, evidence, learning, decision, and next action;
  include rejected alternatives only when they materially explain the
  selection. Enter refinement only after the full target passes. Exhausting
  harden patience or `max_rounds` blocks without refinement.
- [ ] 7. Refine second. Before each turn, use the same evidence-updated
  selection step to choose one removal, merge, or condensation experiment.
  Retain only candidates that preserve the hardened performance floor and every
  guard while reducing length; otherwise restore the shortest passing
  candidate. Stop on refine patience or `max_rounds`.
- [ ] 8. Run the frozen suite once more on the shortest passing candidate,
  append final evidence to ticket `progress.md`, obtain required Agent QA and
  review, then promote the accepted skill change through `skill-maintenance`.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Execution Boundary

The objective is lexicographic:

```text
maximize required behavior until target passes
then minimize instruction length subject to that exact behavior floor
```

One Goal owns both phases. A phase budget is a safety bound, not a competing
controller. Candidate files may remain temporary; keep only the accepted skill
change, ticket progress, and generated evidence.

Leverage Advisor is the existing decision owner for choosing the next
experiment. `program.md` owns source/search and replan policy;
`hypothesis-tree.json` owns current hypotheses, results, and insights;
`progress.md` owns chronological receipts. Before every harden or refine round,
Leverage Advisor rereads all three plus current evidence and remaining budget. It
does not execute Eval, mutate the target, compile the Goal, or create an
experiment ticket.

External research is optional and evidence-triggered, not an automatic web
search. Adversarial agents strengthen the eval boundary before a Goal or force
a new frozen Goal; they do not mutate or approve the suite during a run.

The reusable Goal program is a compact `program.md` preset only. Limit it to
metric and frozen-suite bindings, source/search policy, phase budgets,
accept/transition/stop rules, and tree/progress writeback shapes. Do not copy editable scope, detailed
round procedures, proof lanes, completion workflow, or promotion policy from
the ticket and skills. The ticket owns scope and proof; `progress.md` owns
observations; `goal-advisor` separately compiles the Files-listed native
launcher.

## Reference Map

- [Goal program template](references/goal-program-template.md) — instantiate
  for every material self-improvement Goal.
- [Leverage Advisor](../leverage-advisor/SKILL.md) — use at setup and every
  experiment checkpoint to choose the next pending tree leaf from current evidence.
- [Goal Packet ownership](references/skill-memory.md) — load when compiling or
  repairing state surfaces.
- [Skill eval use](references/skill-evals.md) — load for suite, metric,
  adversarial, or held-out decisions.
- [Optimization workflow](references/workflows.md) — load for the full loop.
- [Architecture boundary](references/architecture.md) — load for ownership.
- [Gotchas](references/gotchas.md) — load for leakage, overfitting, or bloat.
- [Bounded source upgrades](../skill-maintenance/references/upgrade-skill-from-sources.md)
  — load only when local evidence is insufficient.
- [Adversarial agent proof](../agent-qa-test/SKILL.md) — load when a proposed
  case needs separate tester and evidence-review lanes.

## Output

- approved ticket Goal Packet, ticket-local hypothesis tree, and compact native
  Goal prompt
- append-only ticket `progress.md` observations and Eval evidence
- shortest discovered candidate that passes the frozen target and guards
- accepted target-skill change or an evidence-backed blocked result
- optional source dispositions and separately reviewed adversarial cases

For an active turn or audit, make the decision replayable without another
helper. Report:

```text
Packet: owning ticket + program + hypothesis tree + progress + approval/freshness + frozen suite
Phase: baseline | harden | refine
Budget: harden max_rounds/patience + refine max_rounds/patience
Observation: performance + guards + length + evidence ref
Selector: eligible pending leaves + Leverage Advisor selection rationale
Decision: retain | reject | transition_refine | blocked | complete
Diagnostic: bounded children + preserved sibling ids + repair/reject/defer/backtrack branches, when evidence is ambiguous
Writeback: tree mutation + observation + evidence + learned constraint + next action
Writeback order: hypothesis-tree.json then progress.md
Next action: one bounded next turn or stop reason
```

When asked to show an active turn, render the compact `progress.md` writeback
with `observation`, `evidence`, `decision`, `learning`, and `next_action`
instead of merely saying it will be appended. If the remaining budget,
eligibility, or evidence is unknown, make resolving that value the next action
rather than inventing it.

When asked to seed from supplied sources, render the extracted source refs,
techniques, mechanisms, variables, and concrete initial nodes. Each node names
its expected observation, falsifier, expected reward, reward basis, and source
refs before one ordinal Leverage Advisor selection. For an ambiguous miss,
the `Diagnostic` and `Writeback order` lines above are mandatory even when the
answer is brief; list preserved sibling IDs and all four outcome branches.

Always report the configured limits for both phases, even when one phase is
inactive. For every retained or rejected candidate, the writeback names the
hypothesis, complete frozen-suite evidence reference, performance, guards,
length, and decision; never invent a missing evidence reference.
When explaining budget use or exhaustion, restate that one round is one bounded
target edit followed by the complete frozen eval so the limit is auditable.
