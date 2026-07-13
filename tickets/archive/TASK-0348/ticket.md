---
template_id: ticket-template
template_version: "0.2.1"
ticket_id: TASK-0348
title: Prototype the human-readable report template
status: done
priority: high
created_at: 2026-07-13T21:00:00+08:00
updated_at: 2026-07-13T22:02:00+08:00
---

# TASK-0348: Prototype the human-readable report template

## Summary

Turn the accepted 37-skill report audit into one shared, tracked human-report
template and one representative Dogfood before/after prototype. Prove the
decision-first reading pattern on existing evidence before changing any live
report-producing skill or scaling the pattern across the inventory.

## Scope

- In: shared human-report template, reporting-doctrine update, template
  registry/discoverability and version-watch updates, one Dogfood
  after-prototype derived from the 2026-07-13 report, one proof-preserving
  machine receipt, comparison evidence, retained-hunk proof for overlapping
  user edits, deterministic validators, and independent review.
- Out: edits to `skills/dogfood-review/`, changes to live report generation,
  rollout to the other 36 report producers, deletion of source reports,
  automation changes, publishing, deployment, or external side effects.

## Delta

```text
overall_before:
  - report producers either invent their own shape or mix human decisions with receipts, workflow policy, empty tables, and exhaustive evidence.
  - the accepted audit recommends a shared spine but no reusable template or representative rendered proof exists.
overall_after:
  - one tracked template defines decision -> situation map -> material findings -> risks -> next action -> supporting evidence.
  - one Dogfood prototype proves the shape against real existing evidence while preserving the sole canonical no-action receipt separately.
why_now:
  - the operator accepted the audit and explicitly requested the first implementation wave.
first_principles_basis:
  objective: reduce report decision-find time without weakening proof or downstream machine state
  need: prove one honest report before editing 37 producer contracts
  assumptions: the 2026-07-13 Dogfood report is representative because it is long despite having no active experiment WIP
  root_cause: report bodies currently serve human reading, machine receipt, policy documentation, and evidence storage at once
  constraints: preserve current user changes, keep runtime behavior unchanged, retain exact authority/mutation/validation/stop proof
  first_viable_slice: one shared template plus one Dogfood rendered prototype
  proof_or_falsification: reject or revise if the shorter prototype loses a material decision, risk, source gap, next action, or canonical no-execution proof
  tradeoff: defer live Dogfood adoption and broad rollout until the prototype passes independent review
  non_goals: universal report renderer, migration automation, or report UI redesign
```

## Change Plan

```text
architecture_signatures:
  module_level:
    - human_report(source_evidence, report_kind, template) -> decision_report + supporting_evidence_refs
    - sync_template_registry(template_metadata, rules/template-registry.toml) -> docs/templates/registry.jsonl
  main_flow:
    - accepted audit -> shared template -> existing Dogfood evidence -> after prototype + canonical receipt -> comparison + review
  data_flow:
    - source report decisions/risks/actions -> human report body
    - source report authority/mutation/validation/stop fields -> linked canonical receipt
  builder_freeform_boundary:
    - exact prose and prototype table layout are builder-owned; reading order, proof preservation, no-live-rollout boundary, and template ownership are fixed.
```

### Change 1: Add the shared human-report owner

```text
fixes:
  - the accepted report spine has no reusable, discoverable template owner
before:
  - reporting.md owns metadata/indexing only and each producer owns its own shape
after:
  - docs/templates/HUMAN_REPORT_TEMPLATE.md owns the reusable human reading spine
  - reporting.md names the human body versus supporting receipt boundary
read:
  - docs/farplane-framework/reporting.md
  - docs/templates/README.md
  - rules/template-registry.toml
  - rules/template-version-watch.toml
  - docs/fundamentals/prompt-engineering.md
write:
  - docs/templates/HUMAN_REPORT_TEMPLATE.md
  - docs/farplane-framework/reporting.md
  - docs/templates/README.md
  - rules/template-registry.toml
  - rules/template-version-watch.toml
  - docs/templates/registry.jsonl
operation:
  - add a compact template with positive and negative examples, diagram rules, specialization points, and proof-preservation invariant
  - register the prototype consumer without claiming broad rollout
  - add the template to the high-impact version watch so metadata validation cannot silently skip it
signature_or_type_impact:
  - new template_id human-report-template@0.1.0
routes:
  docs: doc-advisor
  qa: template and doc validators
  review: reviewer
qa:
  - template registry write/check remains deterministic
  - template metadata validator includes HUMAN_REPORT_TEMPLATE.md through rules/template-version-watch.toml
  - existing reporting frontmatter/index contract remains unchanged
failure_modes:
  - template becomes another long policy document
  - template imports ticket execution machinery
  - generated registry overwrites unrelated user changes
```

### Change 2: Render one proof-preserving Dogfood prototype

```text
fixes:
  - the shared spine is unproved against a real verbose report
before:
  - .farplane/reports/dogfood-review/2026-07-13T060328+0800.md is 1,990 words with 14 headings
after:
  - one ticket-local prototype exposes the decision, map, material findings, risks, and next action first
  - one linked receipt preserves the authority, mutation, validation, and stop state
read:
  - .farplane/reports/dogfood-review/2026-07-13T060328+0800.md
  - .farplane/reports/report-skill-audit/2026-07-13-audit.md
write:
  - tickets/archive/TASK-0348/artifacts/prototype/dogfood-after.md
  - tickets/archive/TASK-0348/artifacts/prototype/dogfood-receipt.json
  - tickets/archive/TASK-0348/artifacts/prototype/comparison.md
  - tickets/archive/TASK-0348/artifacts/prototype/pre-existing-overlap.md
operation:
  - derive both artifacts from the same source report without changing canonical experiment or ticket state
  - map source receipt fields exactly: authority is report_only; Goal packets, experiment tickets, and recovery tickets created are 0; experiment/check-in, Pulse/worker, reward mutation, and completion-learning receipt recreation are false; every source capacity/ordering guard remains true; the stop receipt remains exactly `no implementation, Goal, Pulse, worker, check-in, promotion, rollback, external action, or experiment-ticket creation invoked`
  - compare reading-path length, heading count, empty sections, repeated receipt prose, and retained decision/evidence coverage
signature_or_type_impact:
  - prototype only; no live Dogfood signature or output-contract change
routes:
  docs: ticket_artifact
  qa: focused artifact checks
  review: reviewer
qa:
  - every material source decision/risk/action maps to the prototype or receipt
  - JSON parsing fails the check when any mapped field is missing, changed, or invented
  - prototype has one compact diagram and no empty section
  - original source report remains untouched
  - pre-existing reporting.md CRM-source and registry MANIFEST_TEMPLATE@2.0.3 hunks remain present after edits
failure_modes:
  - concise report hides a source gap or weakens the no-execution boundary
  - prototype silently becomes a live template migration
```

## Done

```text
done_when:
  - the shared human-report template is tracked, discoverable, concise, diagram-aware, and explicit about supporting evidence.
  - reporting doctrine distinguishes human body, supporting evidence, and canonical machine receipt without changing report-card metadata.
  - the Dogfood prototype and receipt derive from the same real source report and leave that source unchanged.
  - comparison evidence shows what was retained, moved, and removed without claiming broad rollout.
  - focused validators pass and independent documentation/evidence review returns TAS-A.
```

## QA Strategy

```text
qa_strategy:
  proof_weight: prototype + deterministic checks + review
  checks:
    - python3 bin/validators/sync_template_registry.py --write
    - python3 bin/validators/sync_template_registry.py --check
    - python3 bin/validators/check_template_version_metadata.py --all
    - python3 bin/validators/check_doc_refs.py
    - python3 docs/features/validate_features.py
    - compare source/prototype word and heading counts with wc and rg
    - parse dogfood-receipt.json and assert authority.write_policy == report_only; all three created counts == 0; experiment/check-in, Pulse/worker, reward mutation, and completion-learning receipt recreation == false; all eight source ordering/capacity guards == true; and stop.no_execution_receipt exactly equals the source string
    - before editing, record the existing reporting.md CRM-source hunk and registry MANIFEST_TEMPLATE@2.0.3 hunk in pre-existing-overlap.md; after editing, assert those exact semantic lines remain in the working diff/files
  manual:
    - map every material source decision, risk, gap, and next action to the prototype or receipt
    - verify no live Dogfood skill/template/runtime file changed
  delegated_lanes:
    - reviewer judges implementation-plan readiness before execution
    - reviewer judges documentation-quality and evidence-quality before completion
  review:
    - rubric: implementation-plan + evidence-quality
      required_tas: TAS-A
    - rubric: documentation-quality + evidence-quality + integration-readiness
      required_tas: TAS-A
  evidence:
    - tickets/archive/TASK-0348/artifacts/prototype/
    - tickets/archive/TASK-0348/artifacts/review/
  goal_advisor_inputs:
    proof_route: deterministic checks plus reviewer
    final_evidence: comparison.md and final review receipt
    final_checkpoint: TAS-A completion review after all checks
  residual_risk:
    - one report proves the reading pattern, not generality across all report families
```

## Docs Strategy

```text
docs_strategy:
  outcome: update_docs
  doc_targets:
    - docs/farplane-framework/reporting.md
    - docs/templates/README.md
    - docs/templates/HUMAN_REPORT_TEMPLATE.md
  no_docs_reason:
  validation:
    - python3 bin/validators/check_doc_refs.py
    - python3 bin/validators/sync_template_registry.py --check
```

## Links

- `program:` none — direct bounded prototype is preferred
- `progress:` none — one-turn local execution with ticket evidence
- `visual companion:` `tickets/archive/TASK-0348/diagrams.md`
- `artifacts:` `tickets/archive/TASK-0348/artifacts/`
- `review:` `tickets/archive/TASK-0348/artifacts/review/`
- `refs:` `.farplane/reports/report-skill-audit/2026-07-13-audit.md`, `.farplane/reports/report-skill-audit/2026-07-13-review.md`

## Notes

- Minimal implementation claim: this is the `1` in `1 -> 10 -> 100`; live
  Dogfood adoption belongs to the next accepted wave.
- Existing service fit: `docs/farplane-framework/reporting.md` and the template
  registry are the existing owners; no new skill, renderer, hook, or service is
  introduced.
- Grounding evidence: local-only because this ticket implements an accepted
  Farplane-specific report contract using canonical local templates and real
  report evidence.
- Preserve unrelated current edits in `docs/farplane-framework/reporting.md`
  and generated registry inputs/outputs.
- Completion receipt: TAS-A across documentation quality, evidence quality,
  and integration readiness. Strongest evidence:
  `artifacts/prototype/comparison.md`, `artifacts/prototype/verification.md`,
  and `artifacts/review/completion-review.md`.
- Closeout validation: `artifacts/validation/complete.md` and
  `artifacts/validation/complete.json`; all six blocking checks passed.
