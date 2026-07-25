---
skill: ingest-content
date: 2026-07-24
change_type: behavior-and-contract
owner: TASK-0404
status: passed
before_ref: tickets/TASK-0404/ticket.md#delta
after_ref: skills/ingest-content/SKILL.md
review_route: reviewer
reasoning_basis: first-principles review plus operator-approved implementation plan
proof_artifacts:
  - tickets/TASK-0404/artifacts/qa/
  - tickets/TASK-0404/artifacts/review/
  - tickets/TASK-0404/diagrams.md
eval_required: yes; save-only and future-creation branches are behavioral contracts
---

# Compact Capture And Repurpose Ticket Audit

## Before Behavior

- Source understanding was described through fragmented analysis fields.
- Context-only observations could be stored as unpinned CreativeElements.
- A future-creation note produced a downstream suggestion but no durable
  content ticket.

## After Behavior

- A capture stores optional transcript separately from one freeform
  `analysisMarkdown` value.
- `should_store_element(value, note) = is_element(value) &&
  explicitly_selected_for_reuse(value, note)` is the active write boundary;
  every new element is selected and pinned, while a capture may contain zero
  elements.
- Future-creation intent creates or reuses a thin ticket that names the stable
  source URL or asset ID, intended output, operator details, and
  `content-impl-plan` as its first operation.
- The ingest result returns `tickets[]`; no reverse ingestion-job/task link is
  required.

## Structure Rubric

- `first_load_sufficiency`: pass — the signature, intent branches, ticket step,
  output, and finish gate are present in `SKILL.md`.
- `reference_load_precision`: pass — detailed storage and phase contracts stay
  in the two existing references.
- `missing_context_rate`: pass — the ticket handoff includes the stable source
  and operator intent rather than relying on chat memory.
- `noisy_context_rate`: pass — no provider, scheduler, or full production-plan
  procedure was added.
- `duplicated_instruction_count`: pass — short first-load rules are repeated
  intentionally; deeper detail has one reference owner per concern.
- `prompt_size_tokens`: unknown — no comparative token benchmark was run.
- `task_success_rate`: unknown — adversarial QA passed the file-level contract,
  but no runtime behavior trace was run.
- `review_tas_rate`: pass — the TASK-0404 completion reviewer returned TAS-A
  for skill-contract and every required family.
- `maintenance_locality`: pass — ingest owns capture/ticket routing and
  `content-impl-plan` remains the downstream expansion owner.
- `composition_clarity`: pass — the signature exposes capture, selected
  elements, `tickets[]`, storage effects, gates, and routes.

## Proof Run

- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- `python3 docs/features/validate_features.py --write`
- `python3 docs/features/validate_features.py`
- `python3 bin/validators/check_doc_refs.py`
- focused Farplane-UI Resource Bank tests

## Followups

- A live Convex deployment needs a separately approved
  snapshot/reset/reingest plan because the active analysis schema intentionally
  has no compatibility path.
- Reverse task linkage remains deferred until a real retrieval or reporting
  need proves it useful.
