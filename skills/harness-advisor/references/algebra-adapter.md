# Harness Algebra Adapter

Use this reference when a placement decision needs the compact algebra model
without loading the full `docs/specs/harness-algebra.md`.

This file is packaged with the `harness-advisor` skill during install. It is a
distilled adapter, not a second source of truth. Load the full spec only when
the decision needs deeper decomposition, eval design, or manifest/schema work.

## Core Decision Model

```text
failure -> loss_term -> task_slice -> harness_coordinate
        -> owner_surface -> quality_lever -> proof_plan
        -> accept | hold | rollback
```

`harness-advisor` exists to choose the smallest surface that can improve the
objective while preserving proof, ownership, and context budget.

## Harness Coordinates

```text
theta =
  system_prompt_policy
+ skill_policy
+ subagent_policy
+ hook_policy
+ mcp_policy
+ memory_policy
+ filesystem_policy
+ eval_policy
+ automation_policy
+ routing_policy
+ verification_policy
+ budget_policy
```

Common owner surfaces:

```text
system_prompt_policy -> repo AGENTS.md or templates/global/AGENTS.md
skill_policy -> skills/* or docs/skills/registry.jsonl
subagent_policy -> agents/*.toml
hook_policy -> bin/* hooks or validators
memory_policy -> docs/MEMORY.md, docs/LESSONS.md, docs/TROUBLES.md, ledgers
filesystem_policy -> specs, tickets, artifacts, registries, templates
eval_policy -> skills/eval, .codex/evals, .claude/evals
verification_policy -> skills/review, ticket Done / Proof, QA, completion gates
```

## Quality Lever Routing

```text
judgment-heavy quality claim -> review
repeatable behavioral claim -> eval
task-local evidence obligation -> proof_contract
deterministic structure/invariant -> validator
deterministic boundary event -> hook
self-review or context-drift risk -> reviewer subagent
final sufficiency claim -> completion gate
```

Do not use hooks or validators for judgment-heavy work. Do not use review prose
for deterministic invariants that a validator can check.

## Harness Advisor Decision

```text
HarnessAdvisorDecision = {
  improvement_request,
  failure_mode,
  loss_term,
  task_slice,
  candidate_coordinates,
  owner_surface,
  rejected_surfaces,
  quality_lever,
  proof_plan,
  accept_rule,
  rollback_rule,
  secondary_sync_points
}
```

Use this shape when the decision is material, ambiguous, or likely to affect
multiple surfaces.

## Decomposable Harnesses

For broad task distributions:

```text
D = A + B
H_D ~= H_A + H_B + Compose(H_A, H_B)
```

Do not optimize one huge harness when the work can be tested as smaller
mini-harnesses.

```text
MiniHarness = {
  id,
  owner,
  task_family,
  task_slice,
  selected_skills,
  tools,
  state_files,
  proof_contract,
  eval_cases,
  review_families,
  composition_edges
}
```

Use local skill or workflow evals for `H_A`; use composition evals or
integration review for `Compose(H_A, H_B)`.

Do not decompose when the task is one-off, low-risk, or already fits in one
context without pollution. Decomposition has coordination cost.

## Compounding ROI

Default prior:

```text
ROI(Tier1_delta) >= ROI(Tier2_delta) >= ROI(Tier3_delta)
```

This is a leverage prior, not permission to increase blast radius.

High-compounding updates:

```text
update(review) -> improves every workflow that uses review gates
update(advise) -> improves placement and tradeoff decisions
update(skill-creator) -> improves future skill quality
update(skill-maintenance) -> improves skill graph health and rollout
write_eval(skill_policy) -> makes skill extraction safer
write_eval(harness-advisor) -> makes placement recommendations measurable
```

Escalate up the tier graph only when:

```text
repeated_failures_across_multiple_owners
OR registry_or_graph_evidence_shows_broad_duplication
OR local_fix_failed_and_failure_is_structural
OR one_high_severity_global_failure_requires_always_loaded_policy
```

Otherwise, fix the local owner.

## Accept, Hold, Rollback

```text
Accept(Delta theta) :=
  score_improves
  AND required_review_families_are_TAS_A
  AND eval_or_regression_evidence_supports_claim
  AND integration_readiness_is_TAS_A
  AND cost <= budget
  AND prompt_size <= limit
  AND no_safety_regression
  AND no_test_regression
  AND heldout_score_does_not_regress
  AND no_scope_overreach
```

```text
promote:
  repeated pass
  AND no hard-gate failures
  AND integration proof exists

hold:
  local pass
  AND workflow_or_composition_proof_missing

rollback:
  regression
  OR weak evidence
  OR composition failure
  OR safety regression
```

## Harness Map Direction

Long term, `harness-advisor` should consume a generated harness map, not read
every skill or doc.

```text
HarnessMap(repo_state) -> surfaces
                        + ownership
                        + edges
                        + proof_routes
                        + validation_status
```

Candidate generated fields:

```text
schema_version
generated_at
source_inputs
surfaces
owners
edges
coordinates
proof_routes
mini_harnesses
known_limits
validation
```

Keep the map generated from canonical source files. Do not make it a second
hand-authored source of truth or a Terraform-style desired-state language until
evals prove a real need.

## Counterexamples

```text
local skill bug
  -> wrong: root prompt update
  -> better: owning skill contract or skill eval

judgment-heavy review failure
  -> wrong: hook
  -> better: review rubric routing or Done / Proof contract

eval added without baseline or heldout cases
  -> wrong: claim improvement from one case
  -> better: baseline + representative cases + heldout split

local skill eval passes but workflow fails
  -> wrong: promote skill change globally
  -> better: hold until composition eval or integration review passes

reviewer returns TAS-B
  -> wrong: treat as pass
  -> better: revise or hold until required TAS gates pass

mini-harness split adds coordination cost without clearer proof
  -> wrong: over-decompose
  -> better: keep one state file or one workflow eval
```
