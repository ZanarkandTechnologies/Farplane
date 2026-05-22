# Todos

Generic active todo surface for multi-ticket or `batch-work` passes.

## Active

- [ ] `TASK-0170`: add profile-driven project planning.
- [ ] `TASK-0167`: apply Tier 3 pipeline model to `social-content`.
- [ ] `TASK-0168`: apply Tier 3 pipeline model to `video-production`.
- [ ] `TASK-0169`: apply Tier 3 pipeline model to `product-photography`.
- [ ] `TASK-0159`: add Codexter local telemetry event ledger.
- [ ] `TASK-0160`: instrument Codexter hooks and add telemetry status CLI.
- [ ] `TASK-0161`: add Aikage Codexter event ingest.
- [ ] `TASK-0162`: add Aikage Codexter telemetry dashboard panel.
- [ ] `TASK-0163`: add Codexter skill usage and prune candidate report.

## Completed Skill-Capability Batch

- [x] `TASK-0155`: add skill capability checker.
  - [x] Add `tests/notion-context/tasks_this_week.json`.
  - [x] Add `bin/check_skill_capabilities.py`.
  - [x] Add tests for fixture validation and scoring.
  - [x] Document `tests/<skill>/` fixture paths.
  - [x] Run ticket proof checks.
- [x] `TASK-0156`: create skill failure repair tickets.
- [x] `TASK-0157`: score missing high-value skill capabilities.

## Notes

- Keep ticket-local plans and evidence in `tickets/TASK-*/ticket.md`.
- Use this file only for the active cross-ticket checklist that should survive
  outside chat.
- Use `blockers.md` for blockers that should not stop the rest of a batch.
