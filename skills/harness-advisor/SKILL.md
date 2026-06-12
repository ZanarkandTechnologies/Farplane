---
name: harness-advisor
description: "Turn a Farplane improvement idea into a recommended owner surface across policy, templates, skills, agents, hooks, tickets, docs, or validators."
tier: 2
source: local
skill_template_version: "0.2.0"
feature_refs:
  - FEAT-0023
  - FEAT-0040
  - FEAT-0048
---

# Harness Advisor

## Context

Use this when the operator asks how to improve Farplane itself and the right
surface is not obvious. This skill chooses where a harness improvement belongs;
it does not implement hidden stateful work in chat.

Default doctrine lives in `docs/specs/harness-engineering-doctrine.md`. Use
`references/algebra-adapter.md` when the decision needs loss terms, quality
levers, mini-harness decomposition, accept/hold/rollback gates, or generated
harness-map reasoning. Load the full `docs/specs/harness-algebra.md` only for
deep algebra, eval-design, decomposition, or manifest/schema decisions.

This is a Tier 2 workflow surface. It may use Tier 1 primitives directly, then
hand implementation to a Tier 3 skill such as `skill-maintenance`, `impl-plan`,
`impl`, `qa`, `demo`, or another Farplane application skill.

## Skill Signature

```text
harness_place(gap_or_request, evidence?) -> placement_decision
state: reads(harness doctrine, feature registry, skill registry, relevant surfaces); writes(ticket? handoff?)
gates: failure_named; owner_surface:named; rejected_surfaces:named; proof_path:named
routes: gap-analysis | eval | self-improve | skill-maintenance | impl-plan | spec-to-ticket | direct-answer
fails: defaults to AGENTS.md; creates new skill before checking registry; recommends hooks for judgment-heavy work
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. State the improvement request as one concrete harness failure or
   capability gap; route to `gap-analysis` first when the observed-versus-
   expected gap is still fuzzy.
- [ ] 2. Ground the current state with the smallest relevant evidence.
   - [ ] Use [reference-grounding](../reference-grounding/SKILL.md) for compact
     local evidence before recommending a surface.
   - [ ] Read `docs/specs/harness-engineering-doctrine.md` for placement rules.
   - [ ] Check `docs/features/registry.jsonl` for an existing or partial
     harness feature before proposing a new feature.
   - [ ] Check `docs/skills/registry.jsonl` for an existing skill, method,
     source owner, or consolidation target before proposing a new skill.
- [ ] 3. Choose the decision depth.
   - [ ] 1. Normal placement: use doctrine, registries, and
     [placement axes](references/placement-axes.md).
   - [ ] 2. Algebraic or high-blast-radius placement: also use
     [algebra adapter](references/algebra-adapter.md).
   - [ ] 3. Graph-wide or dependency placement: inspect the generated skill
     graph or future harness map for backlinks, owner clusters, and surprising
     dependencies.
- [ ] 4. Compare realistic owner surfaces.
   - [ ] Consider repo `AGENTS.md`, `templates/global/AGENTS.md`, generated
     project templates, `docs/specs/*`, `skills/*`, `agents/*.toml`, hooks or
     scripts under `bin/`, ticket contracts, validators, feature registry,
     skill registry, and generated harness-map metadata.
   - [ ] When skills and subagents are candidates, separate actor-prompt
     ownership from reusable skill-contract ownership.
   - [ ] When material review behavior is a candidate, place rubric routing in
     the calling skill or ticket `Done / Proof`, reviewer execution in
     `agents/reviewer.toml`, and TAS/rubric definitions in `skills/review`.
- [ ] 5. Use [advise](../advise/SKILL.md) to compare exactly three viable
   placement options when three realistic options exist.
- [ ] 6. Recommend one primary owner and secondary sync points.
   - [ ] Name rejected surfaces and why they should not own the change now.
   - [ ] Route proof by type: judgment to review, repeatable behavior to eval,
     deterministic invariant to validator/hook, task-local evidence to
     `Done / Proof`, and context-drift/self-review risk to reviewer subagent.
   - [ ] Define accept, hold, rollback, or follow-up conditions for material
     harness deltas.
- [ ] 7. Hand implementation to the relevant Tier 3 workflow, ticket, or
   visible artifact instead of doing hidden stateful work in chat.
   - [ ] Use `optimize-harness` when the user
     wants the full diagnose-place-prove-change-review loop owned end to end.
- [ ] 8. Review readiness before treating a material placement decision as
   ready.
   - [ ] Use the [review protocol](../review/SKILL.md) for material recommendations.
   - [ ] Confirm the decision is grounded, names one owner, avoids root-prompt
     bloat, includes proof, and preserves source ownership.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Decision spine:

```text
failure -> loss_term -> candidate_surface -> proof_plan -> accept_or_hold
```

Material decision output:

```text
Decision:
Primary owner:
Rejected surfaces:
Proof / validation:
Next ticket or owner:
```

## Guardrails

- Do not default to root `AGENTS.md`; prefer the smallest surface that fixes
  the failure.
- Do not read the full harness algebra spec every invocation. Use the packaged
  adapter first, then load the full spec only when the decision needs it.
- Do not create a new skill before checking the existing skill registry.
- Do not create a new feature row before checking the feature registry.
- Do not use a hook or validator for judgment-heavy work that is not
  deterministic.
- Do not treat a generated harness map as source of truth. It should summarize
  canonical specs, skills, registries, agents, hooks, templates, and tickets.

## Gotchas

- A good placement decision can still be wrong if it optimizes the wrong loss
  term. Name the failure mode before choosing surfaces.
- Full-spec context can make normal advice slower and noisier. Load
  `docs/specs/harness-algebra.md` only when the adapter is insufficient.
- A generated harness map is navigation and evidence, not a new desired-state
  language.
- `TAS-B` is not a pass. Hold or revise material changes until required review
  gates pass.

## Reference Map

- [references/algebra-adapter.md](references/algebra-adapter.md) - packaged
  distilled harness algebra for placement decisions, quality levers,
  mini-harnesses, and harness-map reasoning.
- [references/placement-axes.md](references/placement-axes.md) - material
  placement scoring across context budget, reuse, ownership, determinism,
  evidence, duplication, discoverability, and maintenance cost.
- `docs/specs/harness-engineering-doctrine.md` - canonical Farplane placement
  doctrine and smallest-lever rules.
- `docs/specs/harness-algebra.md` - full research spec for deep algebra,
  decomposition, eval, or manifest/schema decisions.
- `docs/features/README.md` and `docs/features/registry.jsonl` - feature
  dedupe, provenance, status, and evidence.
- `docs/skills/README.md` and `docs/skills/registry.jsonl` - generated skill
  inventory and skill selection guide.

## Output

Return a compact placement decision:

- `Decision`
- `Current evidence`
- `Existing feature/skill match`
- `Failure/loss term`
- `Options`
- `Recommendation`
- `Tradeoff accepted`
- `Primary owner`
- `Rejected surfaces`
- `Secondary sync points`
- `Proof / validation`
- `Next ticket or owner`
