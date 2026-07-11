---
title: Validation System Consolidation Audit
status: pass
owner: harness-advisor
created_at: 2026-07-11
updated_at: 2026-07-11
kind: audit
scope:
  - bin/validators
  - tickets/scripts
  - skills/*/scripts
  - docs/features
  - docs/sources
---

# Validation System Consolidation Audit

## Request

Audit every validator-like Python script, identify duplicate or wrong-owner
logic, and recommend the leanest ticket-level validation API without adding
ticket metadata fields.

## Constraints

- Preserve deterministic proof and owner-local tests.
- Give agents one public ticket-validation entrypoint.
- Reuse existing ticket `phase`, status, QA flags, changed paths, and artifacts.
- Do not merge judgment-heavy QA or reviewer decisions into mechanical checks.
- Do not replace modular implementations with one monolithic validator file.

## Inventory

The reproducible scan below finds 48 Python files: 13 tests and 35 non-test
scripts. The 35 scripts are not 35 independent validators:

```bash
find bin/validators tickets/scripts skills docs -type f -name '*.py' \
  | rg '/(check|validate|sync|render)[^/]*\.py$|/[^/]*(check|validate|sync|render)[^/]*\.py$'
```

| Class | Count | Meaning |
| --- | ---: | --- |
| Tests | 13 | Proof for validators; never public validation commands. |
| Core/docs/ticket atomic validators | 14 | Deterministic repo, docs, or ticket checks. |
| Skill-local atomic validators | 11 | Domain artifact checks, credential probes, or packet checks. |
| Aggregators/dispatchers | 2 | `run_git_gate.py` and `check_skills.py`. |
| Generators/sync/workflow helpers | 8 | Some offer check mode, but are not generic validators. |

The counts overlap where an aggregator calls a generator in check mode. The
operator-visible problem is therefore invocation sprawl and unclear ownership,
not simply file count.

### Core And Ticket Decisions

| Unit | Decision | Ticket API role |
| --- | --- | --- |
| `run_git_gate.py` | keep + extract shared runner | Basis for selection, execution, and result types. |
| `check_changed_file_line_count.py` | keep | Git-only advisory; not a ticket completion default. |
| `check_doc_refs.py` | keep | Completion check when documentation paths change. |
| `check_doc_parity.py` | merge engine | Fold rule mechanics into one `docs.contracts` leaf. |
| `check_harness_invariants.py` | split + rewrite | Keep harness/agent rules; remove nested project validation. |
| `check_farplane_project_files.py` | keep + move owner | Register as `project.files`; run only on project/config paths. |
| `check_template_version_metadata.py` | keep | Run when watched templates change. |
| `check_ticket_closure_gate.py` | keep separate | Git/session detachment gate, not ticket proof validation. |
| `check_skill_capabilities.py` | split | Pure fixture validation stays; repair-ticket creation leaves validation. |
| `check_skill_surface_budget.py` | keep under suite | Child of `skills.check`. |
| `check_skill_todo_tiers.py` | keep under suite | Child of `skills.check`; separate hardcase-writing side effect. |
| `check_tier0_phase_protocol.py` | merge into suite | No independent public command needed. |
| `sync_skill_registry.py` | move under skill owner | Check mode remains child of `skills.check`. |
| `sync_template_registry.py` | move under template owner | Check mode remains a template/skill-suite child. |
| `render_product_index.py` | move under product owner | Check mode only when product paths change. |
| `template_usage.py` | keep helper | Shared library, not a validator. |
| `tickets/scripts/check_ticket_metadata.py` | keep | First-class single-ticket `ticket.metadata` leaf. |
| `docs/features/validate_features.py` | keep under docs owner | Feature/system registry check mode belongs in `docs.check`; write mode remains explicit. |
| `docs/sources/validate_sources.py` | keep under docs owner | Source provenance registry leaf in `docs.check` when source paths change. |

### Skill-Local Decisions

| Unit | Decision | Ticket API role |
| --- | --- | --- |
| `skill-maintenance/check_skills.py` | keep aggregator | One `skills.check` suite when skill paths change. |
| `impl-plan/validate_visual_companion.py` | keep | Always run at the planning gate. |
| `taste-loop/check_progress_hypothesis_cycles.py` | keep | Auto-select when packet files opt into hypothesis cycles. |
| `eval/check_eval_queries.py` | keep child | Already included by `skills.check`; never invoke twice. |
| `skill-creator/quick_validate.py` | demote | Fast package/create preflight only; not a ticket gate. |
| Feed Scout feed/profile validators | keep local | Run only when their artifact paths are supplied by existing QA obligations. |
| Instagram payload validator | keep local | Artifact-specific check requiring an explicit payload. |
| X payload validator | keep local | Artifact-specific check requiring an explicit payload. |
| Instagram/X metric validators | merge engine | Share one parameterized metric-snapshot engine; retain thin platform wrappers. |
| Instagram/X config checks | keep as probes | Credential readiness, not automatic repository validation. |
| `notion_pinned_read_check.py` | rename/declassify later | Stateful read planner/recorder, not validation. |
| CRM/front-end/skill plugin sync scripts | keep workflow-local | Generators or external sync; never automatic validation mutations. |
| Skill checklist sync | keep suite child | Check mode only; `--write` is forbidden in ticket validation. |
| Skill plugin sync | keep workflow-local/check child | `--check` may run when plugin packaging is in scope; write/install modes never run from validation. |

## Duplication And Ownership Findings

1. `skills.check` is already a large suite. It invokes checklist, both registry,
   tier, phase-protocol, surface-budget, capability, eval-query, and doc-ref
   checks (`skills/skill-maintenance/scripts/check_skills.py:443`). The pre-push
   config then invokes `skill_registry_check` again
   (`rules/git-review-gates.toml:30`), so the registry is checked twice.
2. `check_harness_invariants.py` calls the complete project-file validator
   internally (`bin/validators/check_harness_invariants.py:125`). This hides a
   large second suite behind one check ID and prevents path-aware selection.
3. Doc parity and harness invariants both implement the same required/forbidden
   substring rule engine (`bin/validators/check_doc_parity.py:88` and
   `bin/validators/check_harness_invariants.py:102`). Their rule data differs;
   the engine should not.
4. Ticket frontmatter, ticket closure, skill metadata, skill budgets, template
   versions, and template registries contain several independent parsers.
   Share parsers within ticket, skill, and template domains; do not invent one
   universal metadata parser.
5. Instagram and X metric snapshot validation is nearly identical. Constants
   and warnings vary, while traversal and error logic are duplicated
   (`skills/instagram-account/scripts/validate_metrics.py:31` and
   `skills/x-account/scripts/validate_metrics.py:31`).
6. `quick_validate.py` and `check_skills.py` overlap functionally. Preserve the
   former as a fast creation/package preflight, but make `skills.check` the only
   ticket-level skill suite.
7. Several filenames inflate the apparent validator count despite performing
   generation, installation, credential probing, or stateful workflow work.
   Reclassification and naming will reduce cognitive load without deleting
   useful behavior.
8. `check_skills.py` currently calls the tier checker with
   `--hardcase-on-failure` (`skills/skill-maintenance/scripts/check_skills.py:461`),
   which writes an eval artifact on failure. A ticket validator must use a pure
   mode and leave hardcase capture to the repair workflow.

## Options

1. **One monolithic validator file.** One command, but couples unrelated
   domains, destroys owner-local testing, and makes every change high blast
   radius. Reject.
2. **One ticket API over modular check families.** One agent-facing command,
   path/phase selection, no new metadata, one receipt, and owner-local leaves.
   Recommend.
3. **Keep Git gates and skill aggregators as the public surface.** Lowest
   implementation cost, but agents still need to infer which commands and
   artifact arguments apply. Reject as the long-term interface.

## Recommendation

Create one public API while retaining roughly eight internal check families:

```text
validate_ticket(ticket_path, target_phase, changed_paths?)
  -> selected_check_ids + results + receipt + exit_status

farplane validate ticket tickets/TASK-XXXX/ticket.md --phase planning
farplane validate ticket tickets/TASK-XXXX/ticket.md --phase complete
```

Selection inputs require no new ticket fields:

- explicit target phase supplied to the command;
- existing ticket phase/status and QA/demo flags;
- changed paths from an explicit base/ref or explicit path set; staged paths
  only when the caller explicitly chooses that source;
- existing Goal Packet/artifact presence;
- allowlisted validator commands already present in `QA Strategy`; unrecognized
  commands remain QA obligations and are never shell-evaluated.

In a shared worktree, the command must never silently infer all dirty files.
The receipt records `path_source`, base/ref when used, and the exact selected
paths. If no deterministic ticket-to-diff boundary is available, selection
fails or reports `changed_paths: unavailable` rather than widening scope.

Default families:

| Check family | Selection |
| --- | --- |
| `ticket.plan` | Planning phase: metadata, required companion, plan contract, required review receipt presence. |
| `ticket.complete` | Completion phase: planning invariants plus required QA/demo/reviewer evidence. Session detachment/archive is excluded. |
| `skills.check` | Skill, skill-registry, skill-template, or eval paths changed. |
| `docs.check` | README/architecture/docs paths changed: references, contract rules, feature/system registries, and source registry by subpath. |
| `templates.check` | Watched templates changed: version metadata plus template registry check mode. |
| `project.check` | Farplane project/config/product paths changed. |
| `packet.check` | Existing program/progress files declare an applicable packet contract. |
| `artifact.check` | Existing QA Strategy contains an allowlisted validator form and concrete artifact input. |

The API consolidates selection, execution, output capture, receipt writing, and
exit status. It must not absorb validator implementation or reviewer judgment.
The receipt belongs under `tickets/TASK-XXXX/artifacts/validation/` in JSON and
compact Markdown forms.

## Final Target Setup

Use one Farplane-wide validation subsystem and keep domain validators with
their skill owners:

```text
bin/farplane.py
  farplane validate ticket <ticket.md> --phase planning|complete
  farplane validate git --stage pre-commit|pre-push

bin/core/validation/
  __init__.py       # stable Python API
  models.py         # Check, Result, Receipt, Phase, PathBoundary
  registry.py       # allowlisted check IDs and callable registration
  select.py         # phase + explicit changed-path selection
  run.py            # timeout, output capture, warning/block, one exit status
  receipt.py        # deterministic JSON + compact Markdown evidence

bin/validators/
  farplane_checks.py       # consolidated repo-wide leaf check implementations
  test_farplane_checks.py  # leaf check regression tests
  validate.py              # temporary compatibility entrypoint only

rules/validation.toml
  # path selectors, phase defaults, warning/block policy; no raw ticket commands

skills/<owner>/scripts/
  # skill-specific validators remain here and register an allowlisted callable
```

`bin/validators/` stops being a shelf of public scripts. During migration it
may retain one compatibility entrypoint, `validate.py`, but the canonical API
is `farplane validate ...` and old wrappers are deleted once callers move.

Farplane-wide logic is consolidated by concern inside
`bin/validators/farplane_checks.py` rather than one script per old filename.
Shared orchestration remains in `bin/core/validation/`, matching the repo rule
that core helpers belong in `bin/core/` while validators and their tests belong
in `bin/validators/`:

```text
validate_ticket_contract(ticket, phase)
validate_docs(paths)
validate_templates(paths)
validate_project(paths)
validate_harness(paths)
```

These functions may share parsers and rule data. Generator/write behavior does
not move into validation: feature, source, template, skill, and product
generators retain explicit owner-local write commands, while their pure check
functions are imported by the Farplane validation subsystem.

Skill ownership examples:

```text
skills/impl-plan/scripts/validate_visual_companion.py
skills/feed-scout/scripts/validate_daily_feed.py
skills/x-account/scripts/validate_post_payload.py
```

The dispatcher calls those only through stable allowlisted registrations and
only when the phase, changed paths, packet, or explicit artifact input makes
them applicable. It never discovers and executes arbitrary scripts.

### Phase Behavior

```text
planning:
  ticket contract
  impl-plan visual companion
  plan proof/reviewer receipt presence

complete:
  planning checks
  Farplane checks selected from explicit changed paths
  applicable skill validators
  required QA/demo/reviewer receipt presence
  consolidated validation receipt

post-close Git gate:
  session detached
  ticket archived
  cheap staged/branch safeguards
```

### Intended Physical Result

- One public command instead of many validator scripts.
- One shared runner package under `bin/core/validation/` and one consolidated
  Farplane leaf-check module under `bin/validators/`.
- One rules file for phase/path selection.
- Skill-specific validators remain in their skills.
- Generator, sync, install, credential, repair, and hardcase workflows remain
  outside validation.
- Old `bin/validators/check_*.py` scripts are removed after all callers and
  tests move to the new Python API.

## Migration Shape

1. Extract reusable command/check/result selection from `run_git_gate.py` into
   a shared `bin/core` validation runner. Keep Git stages and ticket phases as
   separate callers of that engine.
2. Add `farplane validate ticket ... --phase planning|complete`; do not add
   frontmatter fields.
3. Register stable check IDs and path selectors in one repo-owned rules file.
   Registry commands must be pure during validation; mutation modes remain
   explicit workflow actions.
4. Make ticket metadata validation accept one ticket path efficiently and add
   planning/completion phase suites.
5. Register `check_skills.py` once as `skills.check`; delete the redundant
   pre-push `skill_registry_check` selection, and remove/isolate
   `--hardcase-on-failure` so validation is pure.
6. Merge the doc/harness substring rule engine, remove the nested full project
   validation call, and select `project.check` explicitly by paths.
7. Extract the shared Instagram/X metrics engine and keep platform wrappers.
8. Update `impl-plan`, `goal-advisor`, `qa`, and `close-ticket` to call the one
   ticket API at their phase boundary and consume its receipt. `close-ticket`
   runs completion validation before archive; the existing session/archive Git
   gate remains a separate post-close safeguard.
9. Preserve Git pre-commit/pre-push as cheap independent safeguards using the
   same runner; do not equate Git stage with ticket phase.

## Loss Check

Preserved:

- every deterministic invariant and its owner-local tests;
- package-local artifact validators requiring explicit inputs;
- Git/session closure protection;
- generation and repair workflows, but outside pure validation;
- QA and reviewer judgment as independent readiness gates.

Removed or consolidated:

- duplicate skill registry execution;
- duplicate substring engines;
- hidden nested project-suite execution;
- duplicate social metric traversal;
- manual agent responsibility for selecting repo-wide validators.

Residual risk: automatic path selection cannot infer arbitrary runtime artifact
arguments. Those remain grounded in existing `QA Strategy` commands and links
rather than new metadata.

## Proof Plan

- Unit-test phase and path selection, unknown check IDs, timeouts, output
  capture, warning/block modes, and receipt determinism.
- Golden tests for planning and completion tickets with no new metadata.
- Prove each existing Git-gate check maps to the shared runner without behavior
  loss.
- Prove `skills.check` runs once and retains all current child checks.
- Prove validation mode cannot invoke `--write`, install, repair-ticket, API,
  credential, hardcase-writing, or arbitrary shell paths.
- Prove path selection is deterministic from an explicit base/ref/path set and
  receipts record the exact boundary.
- Prove unrecognized QA Strategy commands are reported but never executed.
- Replay representative skill, docs, project, packet, and artifact tickets.
- Require independent reviewer judgment before accepting migration and compare
  old-vs-new selected checks for at least one branch.
