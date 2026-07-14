---
kind: skill-example
skill: farplane-content-creation
scenario: approved-skeleton-variations
updated_at: 2026-07-14
---

# Approved Skeleton To Controlled Variations

```yaml
approved_skeleton:
  audience: serious builders evaluating agent harnesses
  promise: distinguish installation from real activation
  core_angle: installed is not activated
  narrative_or_teaching_spine:
    - installation creates files
    - invocation proves discoverability
    - artifact creation proves useful execution
    - review and evidence make the result trustworthy
  proof_spine:
    - activation proof artifact
    - independent review verdict
  format_engine: one activation stage per carousel card
  invariants: [audience, promise, activation stages, proof refs, honest limitations]
  variable_axes: [hook, metaphor, proof order, CTA]
  prohibited_claims: [universal reliability, zero-supervision autonomy]
```

| Variant | Changed axes | Preserved | Expected learning | QA results | Rank | Rationale |
| --- | --- | --- | --- | --- | --- | --- |
| V01 | hook | all invariants | Whether a contrarian opening improves clarity | claim/invariant/format/rights/channel: pass | 1 | Clearest hook without proof drift |
| V02 | metaphor | all invariants | Whether the runway metaphor improves recall | claim/invariant/format/rights/channel: pass | 3 | Memorable but less direct |
| V03 | proof order | all invariants | Whether proof-first framing increases trust | claim/invariant/format/rights/channel: pass | 2 | Strongest evidence-first opening |

The internal production matrix contains ten rows in this shape. The separate
handoff contains only selected artifacts:

```yaml
distribution_handoff:
  selected_artifact_refs: [V01, V03, V02]
  publication: gated
```

QA keeps the other seven rows as internal search evidence; it does not place
them in the handoff or publish them.
