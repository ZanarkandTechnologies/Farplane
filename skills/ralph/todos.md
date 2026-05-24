# Todos

- [ ] Read `tickets/README.md`, active tickets, `docs/MEMORY.md`, and `docs/TROUBLES.md`.
- [ ] Run the read-only selector and inspect skipped-ticket reasons.
- [ ] Stop on human gates, unresolved blockers, unresolved dependencies, claims, missing tools, or missing permissions.
- [ ] Decide whether the next safe work unit is one ticket or a low-risk related tiny-ticket batch.
- [ ] For any batch, require same module/workflow, same setup, compatible proof surface, no conflicting write scope, and no separate human gate.
- [ ] Hand the selected work unit to [$work](../work/SKILL.md); let `$work` choose `impl-plan`, `$impl`, `close-ticket`, direct local work, reslice, or autoresearch.
- [ ] For a batch, require one proof row per ticket plus one batch-level regression row before completion.
- [ ] After each work unit, reread the board before selecting again.
- [ ] Apply the three-ring QA policy before deciding whether to continue the board drain.
- [ ] End with `RALPH_RESULT: status=... selected=... reason=...`.
