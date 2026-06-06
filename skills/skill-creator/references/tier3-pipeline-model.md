# Tier 3 Pipeline Model

Use this when creating or refactoring a complex Tier 3 domain skill. The goal
is faster scanning, not mathematical ceremony.

## Core Algebra

```text
Tier3Pipeline := Model + MethodRegistry + TodoRecipe + Templates + Proof

Project := Brief + ComponentMatrix + MethodSet + Constraints + ExecutionPackets + ProofPlan

Component := Job + Claim + Inputs + Levers + CandidateMethods + ChosenMethod + OwnerSkill + Output + Proof

Method := id + use_when + avoid_when + inputs + outputs + cost + risk + proof

MethodSelection(component, methods, constraints) :=
  candidates = filter(methods, component, constraints)
  chosen = advise(top3(candidates))
  packet = ExecutionPacket(component, chosen, proof)
```

## Skill Package Shape

```text
SKILL.md               = first-load contract + Todo List + compact algebra prelude
references/model.md    = domain algebra and component matrix rules
references/*.json      = method registries when records are stable
templates/*.md         = output packet shapes
tests/*.json           = optional compact capability/smoke fixtures
```

Do not add `README.md` files to skill packages just to restate the model.
`SKILL.md` remains the entrypoint. Put longer notation in references.

## When To Use

Use this model when a Tier 3 skill:

- has a planning phase and execution phase
- decomposes work into sections, scenes, slides, campaign assets, screens, or
  similar components
- chooses from method records or effect/asset/layout levers
- needs per-component proof plus whole-output review

Avoid it for tiny skills, wrappers, or tools where a 5-step workflow is clearer
than component algebra.

## Component Matrix

Use a matrix as the planning object:

| Component | Job | Claim / Goal | Inputs | Candidate methods | Chosen method | Owner skill | Output | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

The matrix row is the unit of decision. Run `advise` on complete directions for
that row, not on isolated variables unless one variable is the real blocker.

Bad:

```text
advise headline
advise color
advise button
advise animation
```

Good:

```text
advise HeroDirection :=
  headline posture + layout + asset carrier + motion method + proof cue + CTA + QA
```

## Ticket Split Rule

Do not make every component a ticket. Keep components as matrix rows unless one
has a real split trigger:

- independent proof surface
- reusable foundation
- risky or blocked asset/dependency
- specialist owner can work independently
- QA instrumentation must exist before build
- runtime/service boundary

## First-Load Contract

The algebra must not replace the required `SKILL.md` contract. `SKILL.md` still
needs:

- trigger conditions
- 5-8 step workflow
- decision branches
- top gotchas
- judgement questions
- outcome contract

The model/reference exists to make complex domain choices faster to read.
