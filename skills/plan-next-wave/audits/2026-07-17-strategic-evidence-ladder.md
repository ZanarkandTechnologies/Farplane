---
title: Strategic evidence ladder skill audit
status: complete
owner: plan-next-wave
kind: skill-audit
updated_at: 2026-07-17
changed_paths:
  - skills/plan-next-wave/SKILL.md
  - .agents/skills/farplane-market-learning/SKILL.md
  - .agents/skills/farplane-ablation-proof/SKILL.md
  - .agents/skills/farplane-content-creation/SKILL.md
---

# Strategic evidence ladder skill audit

## Trigger

Plan Next Wave produced understandable-looking but strategically arbitrary
ideas. Proposals were not mechanically tied to Farplane's product bets, core
harness systems, current ICP pain, or the next missing evidence stage.

## Before / after

| First-load surface | Before | After | Delta |
|---|---:|---:|---:|
| `plan-next-wave/SKILL.md` | 119 | 135 | +16 |
| `farplane-market-learning/SKILL.md` | 47 | 49 | +2 |
| `farplane-ablation-proof/SKILL.md` | 61 | 63 | +2 |
| `farplane-content-creation/SKILL.md` | 316 | 320 | +4 |

The added first-load text is limited to strategic bindings, evidence-stage
routing, and rejection criteria. Research, ablation, and content procedures
remain in their owning skills; no new router, agent, hook, or workflow package
was added.

## Contract delta

```text
select_next(product_bet, evidence_state)
  -> market_learning | ablation_proof | content_creation | productization
```

- Product bets now cite canonical `system_refs` and `feature_refs`.
- Market-learning, ablation, and content calls bind `product_bet_ref`,
  `system_ref`, and `feature_refs`; productization retains its accepted-result
  contract.
- The response validator rejects strategic refs outside the named product bet.
- Market learning requires current direct ICP complaint/workaround evidence.
- Ablation isolates one core harness variable and ends in keep/modify/delete.
- Content preserves strategic and proof refs while leading with audience pain
  and a visible result rather than an internal feature name.

## Quality gates

- Positive and negative eval cases cover strategic routing, generic research,
  random feature rejection, and audience-led content.
- Skill-local QA checklists guard market learning and ablation.
- Harness validation resolves product-bet refs against system and feature
  registries at template version `0.5.3`.
- Independent review first found productization-contract ambiguity and missing
  system-to-feature coherence. Both were repaired and regression-tested; final
  re-review passed at TAS-A with no remaining contract blocker.

## Residual risk

The evidence ladder improves selection discipline but cannot guarantee taste.
Human review remains the delayed signal for whether an evidence-backed content
angle is actually interesting.

## Lean follow-up

Removed the `materializer_injects` planner field from every configured skill.
It duplicated two existing facts: planner calls contain exactly
`required_arguments`, while Pulse owns ticket creation. Optional `ticket?`
runtime parameters remain ordinary skill context and need no planner schema.
