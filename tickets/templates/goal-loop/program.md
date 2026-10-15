---
template_id: goal-loop-program
template_version: "0.3.3"
kind: goal-program
title: Goal program section
status: draft
owner: goal-advisor
---

<!-- Paste everything below this comment into the GitHub issue body, after the
ticket sections and before `## Current Goal state`. Subsections use `###`.
The first-load output (body + newest Goal turn comments within 80 lines; see
goal-advisor `references/prompt-templates.md`) stays within the 300-line target
and 400-line hard limit. Instantiate only applicable branches. The launcher is
a separate `**Goal launcher**` comment, not part of the body. -->

## Goal program

### Goal Mode

```yaml
trigger: native_goal | heartbeat | rollout | feedback | direct
files: []
compiled_from_ticket_sha:
budget:
approval: pending | approved | revise | blocked
```

### Execution Contract

- Objective: inherit the valuable outcome and scope from the ticket sections.
- Mutable surface:
- Hard constraints:
- Evidence owner:
- Hypothesis tree: `.farplane/goal-advisor/issue-<n>/hypothesis-tree.json` or
  `none`; never duplicate its frontier here.

### Compiled Execution Path

<!-- Bind meaning rather than copying ticket prose. Every material diagram node,
Change Plan unit, and exit assertion must be covered or the packet is revise. -->

| Ticket diagram nodes | Change unit | Exit assertions | Proof observation |
| --- | --- | --- | --- |
|  |  |  |  |

### Reference Manifest

<!-- List only files needed by a named execution node, assertion, proof, or
drift decision. Remove references with no consumer. -->

| Reference | Used by | Purpose |
| --- | --- | --- |
|  |  |  |

### Completion Closure

<!-- Map every ticket Done assertion and screenshot complaint to executable proof
and its evidence owner. No unsupported row may reach complete. -->

| Closure item | Source image + exact complaint | Design state/viewport | Proof method | Evidence owner/path | Status |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | pending |

### Metric Provider

```yaml
provider: mechanical | eval | review | agent_qa | human_feedback | market | hybrid | none
primary:
direction: maximize | minimize | pass
guards: []
anti_metrics: []
minimum:
```

### Decision Backbone

```text
choose_next(objective, evidence, eligible_moves, remaining_budget)
  -> execute | diagnose | report_now | request_feedback | stop
```

1. `observe`: run the first-load command (issue body + newest Goal turn
   comments within 80 lines); load older comments or artifacts only to resolve
   a named gap.
2. `choose_next`: compare the best eligible move with the outside options.
   Apply goal-advisor `references/choose-next.md` only when several moves need judgment;
   execute a mechanically implied move directly.
3. `act`: the domain skill executes one bounded move. Advisors do not execute.
4. `verify`: use the declared metric and ticket proof without weakening guards.
5. `write_back`: post one Goal turn comment (evidence, learning, decision,
   remaining budget, `next_action`) and rewrite `## Current Goal state`; then
   continue, report, request feedback, or stop.

Role boundaries:

- Goal Advisor compiles or regenerates this packet; it does not choose every turn.
- Goal Advisor's metric card (`references/metrics.md`) is setup/repair only when
  the measurement contract is unclear.
- The choose-next comparison is a conditional method, not campaign state.
- The domain skill owns execution; the ticket owns scope and proof.

### Experiment Backbone

<!-- Keep only for causal/comparative work. -->

```yaml
baseline:
candidate_or_hypothesis:
expected_observation:
falsifier:
search_budget:
```

### Proof Policy

- Derived from: the ticket's Done and QA Strategy.
- Checks:
- Evidence paths:
- Drift owner: inline | reviewer | goal-drift-reviewer
- Final checkpoint: inline | reviewer | none

### After Each Turn

- Apply the Decision Backbone once.
- Preserve the best verified state and attributable evidence.
- Post one compact Goal turn comment before yielding.
- Continue only when the next move beats `report_now`, `request_feedback`, and
  `stop` within the remaining budget.

### Conditional Modes

<!-- Add only the block required by the selected trigger. -->

- Feedback: sample, decision rule, writeback, and waiting condition.
- Heartbeat: trigger, freshness check, no-op rule, and next wake condition.
- Delayed check-in: evidence refs plus `accept | kill | monitor` rule.
- Rollout: prototype, target set, checkpoints, and rollback rule.

### Stop Conditions

- `complete`: ticket Done/proof and required review pass; post one proof
  comment, then `gh issue close <n> --reason completed`.
- `complete` is invalid while any Completion Closure row is pending,
  unsupported, stale, or contradicted by evidence.
- A screenshot complaint row records source image, complaint, state, viewport,
  newer comparable evidence, and independent verdict. It remains blocking until
  that verdict passes or the operator records an explicit withdrawal.
- `report_now`: evidence is useful but further work has lower expected value.
- `request_feedback`: one material user judgment blocks a better decision.
- `blocked`: required input, authority, or proof is unavailable.
- `budget_limited`: no justified move fits the remaining budget.

### Binding Decisions

<!-- One line per rule that still binds, each linking its `Decision:` comment. -->

- <rule> (Decision: <comment link>)
