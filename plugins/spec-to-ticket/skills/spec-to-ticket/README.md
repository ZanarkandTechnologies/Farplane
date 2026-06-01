# Spec-to-Ticket

Turn one bounded spec slice into raw executable tickets.

## Purpose

Help agents convert product/spec intent into capability-first ticket truth while front-loading diagram-first approval summaries, testability, QA shape, and evidence expectations.
This is a Tier 3 Codexter coding-pipeline implementation of the generic
[`plan`](/Users/kenjipcx/coding-harness/Codexter/skills/plan/SKILL.md)
interface.
When an `Agent Testability Brief` exists, this skill should carry its surfaces
forward into the ticket contract instead of inventing them again.
When a repo has `docs/bootstrap-brief.md` with `Agent Experience / Testability`
defaults, this skill should also use those defaults to seed the first UI/game
ticket contract and matching `qa/cookbook` workflow entry when a richer
testability brief does not exist yet.

## Public API / Entrypoints

- `SKILL.md`: main planning contract
- `SKILL.md` Important Checklist: example natural-language todo template for slice decomposition
- `references/spec-template.md`: canonical spec structure
- `references/ticket-template.md`: ticket-writing reference
- `references/review.md`: planning review checklist
- `AGENTS.md`: maintenance rules for this module

## Minimal Example

1. Read the chosen SLC slice.
2. Use the `SKILL.md` Important Checklist when invoking the skill.
3. Start with the largest coherent self-contained feature ticket that still fits one build loop.
4. Split only when a real boundary trigger applies, then make the dependency order explicit from that boundary.
5. Add a compact diagram summary for material tickets and UI testability/evidence requirements when relevant.
6. If the repo has `qa/cookbook/` and the slice is UI-bearing or agentically
   hard, seed a matching cookbook workflow entry from the ticket contract.
7. Write the raw tickets into `tickets/` and stop before implementation.

## How to Test

- Confirm `SKILL.md` still says one slice per planning pass.
- Confirm capability-first packaging is the default and the split triggers are explicit.
- Confirm the `SKILL.md` Important Checklist reinforces planning/testability behaviors as plain natural-language checklist text without becoming a second ticket template.
- Confirm UI-bearing ticket requirements remain explicit.
- Confirm `Agent Testability Brief` guidance is preserved when present.
- Confirm bootstrap `Agent Experience / Testability` guidance is used as a
  fallback when there is no richer testability brief.
- Confirm the linked references exist and match the live ticket contract.
