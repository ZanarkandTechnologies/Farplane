# Impl Plan Prompt

<!--
Unified ticket-planning prompt.
Keep this focused on the next commit and the next ticket move, while allowing
extra implementation detail when the work needs it.
-->

0a. Study `@docs/prd.md`.
0b. Study `@docs/specs/*`.
0c. Study the active ticket in `@tickets/*`; if none exists, inspect `@tickets/*`.
0d. Study `@docs/MEMORY.md`.
0e. Study `@docs/TROUBLES.md` if present.
0f. Search the codebase first.

Plan only. Target one selected ticket or one selected next-commit slice.

Rules:

1. First decide: `one commit` or `split`.
2. If split, stop and ask before planning deeper.
3. Keep one public planning artifact; do not create a second execution brief.
4. Put the highest-signal content first.
5. Keep the approval surface concise, but add user-story/example detail when the applicability rule requires it.
6. If the user did not provide a take on a material choice, act like a consultant: compare real options and recommend one.
7. If `--consensus` is active, run Planner -> Architect -> Critic before final handoff.
8. Add appendix detail only if risk or novelty justifies it, but always include the options appendix for material choices.
9. Before final handoff, run a plan-quality pass and tighten the plan until it passes.

Output shape:

<!--
Keep the top of the plan short enough for fast approval.
Move richer detail below the approval surface instead of splitting into a second artifact.
-->

- `Pitch`
  - `Req`
  - `Bet`
  - `Win`
- `Recommendation`
  - `Best`
  - `Why`
  - `Tradeoff accepted`
- `B -> A`
- `Delta`
- `Core Flow`
- `Proof`
- `User Story` when required by the applicability rule
- `User Pain / JTBD` when required
- `Non-Goals` when required
- `High-Fidelity Example` when required
- `What Good Looks Like` when required
- `Proof Target` when required
- `Plan Review`
- `Options Appendix`
- `Ask`

Requirements:

- `B -> A` must appear near the top.
- `Recommendation` must appear near the top and must name the chosen path directly.
- `Core Flow` defaults to short pseudocode.
- Diagram only for new or risky paths.
- Proof must use concrete checks, not generic test categories.
- Narrative sections must be concrete and distinct from `Summary` and `Scope`.
- If the work is a trivial localized fix, the narrative sections may be intentionally short or omitted.
- `Options Appendix` must show 3 viable options for material choices, each with pros, cons, and `Why not chosen`.
- `Plan Review` must state:
  - which references were actually used,
  - whether scope is still one commit,
  - whether proof/risk/rollback are concrete enough,
  - whether the recommendation is actually justified against the listed options,
  - whether the narrative sections are useful rather than decorative,
  - whether the top approval surface stayed concise,
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
  - which `status` / `phase` the ticket should have after planning,
  - whether any follow-up tickets should be spawned,
  - whether the ticket stays in `status: review` or is ready for `status: building`.

Do not implement.
