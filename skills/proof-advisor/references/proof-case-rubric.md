---
title: Proof Case Rubric
owner: skills/proof-advisor
status: active
kind: reference
updated_at: 2026-06-23
---

# Proof Case Rubric

Use this rubric to accept, revise, or reject candidate proof cases before they
become tests, eval rows, QA cases, or behavior-capture prompts.

```text
judge_proof_case(candidate_case, claim_or_behavior, owner_scope)
  -> accept | revise | reject + reason + smallest_fix
```

Only `accept` is ready for a durable suite.

## Dimensions

| Dimension | Accept | Revise | Reject |
| --- | --- | --- | --- |
| behavior_focus | Tests one visible behavior or decision. | Related bundle, but failure cause is blurry. | Vague quality, style, or "be better." |
| source_quality | Comes from real failure, trace, ticket, spec, or named synthetic gap. | Source is plausible but not tied to a risk. | Invented because more cases felt better. |
| uniqueness | Covers a distinct failure mode, persona, scenario, boundary, or oracle. | Some overlap with another case. | Near-duplicate of an existing case. |
| realism | Input sounds like a real user/operator/system event. | Too polished or too conveniently phrased. | Query teaches the expected behavior. |
| judgeability | Has visible success criteria and failure signal. | Criteria need sharpening. | Cannot be scored without hidden intent. |
| fixture_truth | Fixture state is available, safe, and stable. | Fixture needs setup detail. | Fixture is impossible, live-risky, or stale. |
| proof_surface_fit | Uses the cheapest reliable proof surface. | Proof surface plausible but heavy. | Uses LLM judgment for deterministic behavior, or code for subjective judgment. |
| diagnostic_value | Failure tells us what owner to fix. | Failure indicates a problem but owner is fuzzy. | Failure would only say "bad output." |
| anti_cheat | Expected answer lives in oracle/reference, not user input. | Lightly leading wording. | Leaks answer, policy, skill name, or reference points. |
| maintenance_cost | Small, reusable, and worth rerunning. | Useful but a bit broad or costly. | Adds noise, flake, or brittle maintenance burden. |

## Candidate Sources

Prefer these in order:

1. Real regression or user correction.
2. Production log, trace, support issue, or observed operator confusion.
3. Ticket/spec/skill contract behavior that is easy to regress silently.
4. Existing deterministic tests with missing edge cases.
5. Synthetic gap fill across named dimensions.
6. Benchmark-style difficult regression only when it has reusable proof value.

## Selection Rules

- First batch: usually `3-5` cases.
- Keep one ordinary success path, one known/likely failure, one boundary case,
  and one negative/anti-cheat control when the target is prompt-like.
- Prefer one case with a strong oracle over five cases with vague criteria.
- If two cases fail for the same reason and route to the same owner, keep the
  more realistic one unless the second covers a critical boundary.

## Output Shape

```text
case_review:
  accepted:
  revised:
  rejected:
  coverage_gaps:
  strongest_next_case:
  proof_surface_notes:
```
