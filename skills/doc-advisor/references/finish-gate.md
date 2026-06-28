---
template_uses:
  skill-method-reference: "0.1.0"
---

# Finish Gate

Use this reference before claiming material documentation work is ready.

```text
documentation_finish_gate(target_file, claim, evidence?) -> doc_quality_result + review_route
state: reads(target doc, qa_checklist.md, selected owner docs, validation output); writes(proof note or review handoff)
gates: checklist_applied; claims_grounded; validators_run_or_deferred; review_route_named
fails: validator-only confidence; scalar doc score; unreviewed policy change
```

## Use When

- The doc is canonical, public, cross-surface, policy-bearing, or a completion
  claim.
- Links, refs, metadata, generated registries, or owner boundaries changed.
- The final response needs to name proof rather than just describe the edit.

## Inputs

```text
input_packet:
  required:
    target_file:
    claim:
  optional:
    changed_refs:
    validator_output:
    review_required:
  source_refs:
    - skills/doc-advisor/qa_checklist.md
    - docs/review/rubrics/documentation-quality.md
```

## Workflow

1. **Apply checklist.** Run `qa_checklist.md` as inspection evidence, not as a
   numeric score.
2. **Run focused checks.** Use targeted `rg` searches and validators that match
   the edit; do not run broad checks for ceremony.
3. **Choose review route.** Use `review` with `documentation-quality` when a
   readiness verdict matters; pair `evidence-quality` or
   `integration-readiness` when claims or neighboring contracts changed.
4. **Report repair context.** Summaries should name failed checks, fixes,
   deferrals, and remaining risk.

## Output Shape

```text
doc_quality_result:
  checklist_result:
  validators:
  review_route:
  fixed:
  deferrals:
  remaining_risk:
```

## Quality Gates

- Validators pass or failures are explicitly deferred.
- Material docs have review route or a reason review stayed inline.
- Numeric score language does not replace failed checks and repair hints.

## Bad Output

- "Docs are high quality" with no target checks or evidence.
- Passing links while leaving a doc misplaced or ungrounded.
