# Tech Impl Plan Prompt

<!--
Approval-first planning prompt.
Keep this focused on the next commit and the next ticket move, not on implementation detail.
-->

0a. Study `@docs/prd.md`.
0b. Study `@docs/specs/*`.
0c. Study the active ticket in `@tickets/review/*`; if none exists, inspect `@tickets/todo/*`.
0d. Study `@docs/MEMORY.md`.
0e. Study `@docs/TROUBLES.md` if present.
0f. Search the codebase first.

Plan only. Target the next commit.

Rules:

1. First decide: `one commit` or `split`.
2. If split, stop and ask before planning deeper.
3. Optimize for fast approval, not exhaustive explanation.
4. Put the highest-signal content first.
5. Use compact wording, symbols, and short labels where they improve scan speed.
6. Add appendix detail only if risk or novelty justifies it.
7. Before final handoff, run a plan-quality pass and tighten the plan until it passes.

Output shape:

<!--
This shape is intentionally short so the user can approve quickly.
If a plan needs a long appendix to make sense, the slice is probably too big or too risky.
-->

- `Pitch`
  - `Req`
  - `Bet`
  - `Win`
- `B -> A`
- `Delta`
- `Core Flow`
- `Proof`
- `Plan Review`
- `Ask`

Requirements:

- `B -> A` must appear near the top.
- `Core Flow` defaults to short pseudocode.
- Diagram only for new or risky paths.
- Proof must use concrete checks, not generic test categories.
- `Plan Review` must state:
  - which references were actually used,
  - whether scope is still one commit,
  - whether proof/risk/rollback are concrete enough,
  - any fixes made before handoff.
- `Delegation: Not needed` unless justified.
- If delegation is used, include:
  - exact ticket file path
  - delegated agent/skill
  - short task note
  - expected artifact
  - required write-back section in the ticket
- End with `Ready: yes/no`.
- Include `Ticket Move`:
  - where the ticket should live after planning,
  - whether any follow-up tickets should be spawned,
  - whether the ticket stays in `review/` or is ready for `building/`.

Do not implement.
