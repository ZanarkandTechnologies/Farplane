---
title: Golden compact configured skill call
status: active
owner: plan-next-wave
kind: golden-example
updated_at: 2026-07-17
---

# Bind evidence to an existing project skill

## Accepted output

```yaml
call_id: content-from-accepted-ablation
title: Transform the accepted recovery ablation across social formats
skill_ref: farplane-content-creation
area_id: adoption_and_distribution
arguments:
  problem_ref: operational_visibility
  system_ref: SYS-0005
  feature_refs: [FEAT-0008]
  source_or_idea: tickets/TASK-9001/artifacts/accepted-ablation.md
  audience: technical agent builders
  content_goal: teach the reproducible recovery delta and invite a Farplane trial
  channels: all_configured
expected_artifact: one approved skeleton, optimized exemplar, and video/carousel/X/LinkedIn transformation pack
current_alternative: separate generic posts that restate autonomy claims without the accepted comparison
why_now: the source ablation is accepted and no content transformation exists
```

It passes because it chooses an allowed skill at the accepted-proof stage,
binds one stable problem and coherent system/feature refs, names one finished result
and contrast, and leaves the content workflow inside the skill.

## Tempting negative

```yaml
title: Create a viral autonomy campaign system
workflow: research trends, design a new content framework, make videos, run tests
```

It fails because no configured skill is selected, its inputs are unbound, and
it invents a workflow.

## Transferable invariants

- Select an existing configured skill; never create a work category.
- Bind its required arguments from cited evidence.
- Bind outward work to one configured stable problem and canonical, coherent system and feature refs.
- Make the artifact and alternative understandable without copying the workflow.
- Keep objective, authority, falsifier, dedupe, and ranking evidence compact.
- Store each call once and refer to it by `call_id` after selection.

Fixture IDs, paths, audience, source, wording, and channel values are not reusable facts.
