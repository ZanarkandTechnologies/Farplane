---
ticket_id: TASK-0213
title: Add Farplane lifecycle docs and semantic graph
phase: complete
status: done
owner: codex
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-06-23T23:22:07+0800
updated_at: 2026-06-24T00:09:00+0800
next_action: amend the lifecycle graph commit with the flattened core graph; optional follow-up ticket for Farplane UI rendering
last_verification: 2026-06-24T00:09:00+0800 - py_compile, lifecycle graph unit tests, and generator JSON/JS --check passed after graph flattening
---

# TASK-0213: Add Farplane lifecycle docs and semantic graph

## Summary

Create one friendly end-to-end Farplane framework surface and one machine-readable
semantic lifecycle graph. The human docs should help a new user understand init,
project files, Horizon, Goal Advisor, Pulse, Steer, hooks, drains, memory
compression, and ticket-to-Goal execution without reading every underlying spec.

The graph implementation should reuse the existing skill and harness graph
machinery where useful, but add a focused lifecycle graph that parses skill
signatures, file read/write state, routes, hooks, framework files, and finite
state projections into a UI-consumable JSON artifact.

## Scope

- In:
  - Add `docs/farplane-framework/lifecycle.md` as the friendly lifecycle hub.
  - Add `docs/farplane-framework/graph-contract.md` describing node and edge
    types, extraction rules, and finite-state projections.
  - Add `docs/farplane-framework/hooks-and-runtime.md` or an equivalent sibling
    page for Codex hooks/runtime surfaces consumed by the lifecycle graph.
  - Update `docs/farplane-framework/README.md` so new users can find the
    lifecycle hub and graph contract first.
  - Implement a focused lifecycle graph generator under
    `skills/skill-maintenance/scripts/`.
  - Generate `skills/skill-maintenance/graph/farplane-lifecycle-graph.json` and
    optional `.js` wrapper for UI use.
  - Parse obvious `SKILL.md` signature fields: `state reads(...)`,
    `writes(...)`, `routes:`, `gates:`, and front matter.
  - Include known framework file nodes such as `farplane/goals.md`,
    `farplane/steer.config.toml`, `farplane/pm.json`, `.farplane/state/*`,
    ticket Goal Packet files, reports, hooks, and docs.
  - Add finite-state projections for at least:
    - project initialization
    - automation activation
    - ticket-to-native-Goal execution
    - memory/drain upkeep
  - Add focused tests for parser behavior, generated graph shape, and FSA
    projection shape.
- Out:
  - No Farplane UI rendering implementation in this ticket.
  - No hidden scheduler, daemon, or live automation activation.
  - No broad rewrite of existing framework specs.
  - No automatic compaction of durable memory/docs from hooks.
  - No attempt to perfectly parse every prose sentence in every Markdown file.
  - No unrelated cleanup of existing dirty worktree changes.

## Delta

- `Before:` Farplane has good individual docs for framework files, Deep Init,
  Pulse/Steer, Goal Packets, filesystem lifecycle, and graph generation, but no
  single beginner-friendly lifecycle hub and no semantic lifecycle graph that
  connects skills to the Farplane state files they read/write.
- `After:` New users start from one lifecycle page, then follow links to deeper
  specs. The repo also emits a focused lifecycle graph JSON with typed nodes,
  directional edges, and FSA projections that future UI work can render.
- `Why now:` The operator wants one quick surface for explaining Farplane
  end-to-end and a programmatic graph that can become reusable context for
  agents and the harness UI.
- `First-principles basis:`
  - `objective:` make the framework legible to humans and inspectable by tools.
  - `need:` reduce repeated oral explanation of init, goals, loops, drains, and
    file lifecycle.
  - `assumptions:` local docs and skill signatures are reliable enough for a
    conservative first parser; ambiguous edges can be explicitly curated.
  - `root_cause:` current reference graphs show local links, not semantic
    reads/writes/routes over Farplane state.
  - `constraints:` keep docs reader-friendly, keep graph schema small, preserve
    existing docs as source owners, and avoid inventing a new orchestration
    runtime.
  - `first_viable_slice:` docs hub + graph contract + parser for obvious
    signatures + four FSA projections + tests.
  - `proof_or_falsification:` graph generator and tests pass; docs refs pass;
    generated graph contains expected nodes and directional edges for Deep Init,
    Horizon, Goal Advisor, Pulse, Steer, hooks, and drains.
  - `tradeoff:` accept conservative parsing plus explicit curated nodes rather
    than a brittle universal Markdown parser.
  - `non_goals:` UI rendering, live automation creation, broad doc rewrite,
    hidden runtime, automatic memory compaction.

## Program

```text
signature:
  farplane_lifecycle_docs_and_graph(repo_docs, skill_signatures, hooks_config)
    -> lifecycle_docs + semantic_graph + fsa_projections + validation_evidence

vars:
  docs_owner = docs/farplane-framework/
  graph_owner = skills/skill-maintenance/graph/
  generator_owner = skills/skill-maintenance/scripts/
  ticket = tickets/TASK-0213/ticket.md
  program = tickets/TASK-0213/program.md
  progress = tickets/TASK-0213/progress.md

program:
  ground_existing_surfaces(vars)
    -> current_docs + graph_scripts + memory_constraints

  write_lifecycle_docs(current_docs)
    -> lifecycle.md + graph-contract.md + hooks-and-runtime.md + README links

  implement_graph_generator(skill_signatures, framework_refs)
    -> farplane-lifecycle-graph.json + farplane-lifecycle-graph.js

  add_tests(generator)
    -> parser_tests + graph_shape_tests + fsa_projection_tests

  verify(done_when, proof)
    -> command_results + generated_artifacts + progress_entries
```

## Map

- `Touch:`
  - `docs/farplane-framework/README.md`
  - `docs/farplane-framework/lifecycle.md`
  - `docs/farplane-framework/graph-contract.md`
  - `docs/farplane-framework/hooks-and-runtime.md`
  - `skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py`
  - `skills/skill-maintenance/scripts/farplane_lifecycle_graph.py`
  - `skills/skill-maintenance/scripts/farplane_lifecycle_catalog.py`
  - `skills/skill-maintenance/scripts/test_generate_farplane_lifecycle_graph.py`
  - `skills/skill-maintenance/graph/README.md`
  - `skills/skill-maintenance/graph/farplane-lifecycle-graph.json`
  - `skills/skill-maintenance/graph/farplane-lifecycle-graph.js`
- `Inspect:`
  - `AGENTS.md`
  - `README.md`
  - `ARCHITECTURE.md`
  - `docs/MEMORY.md`
  - `docs/TROUBLES.md`
  - `docs/LESSONS.md`
  - `docs/specs/filesystem-lifecycle.md`
  - `docs/specs/doc-governance.md`
  - `docs/specs/steer-pulse-automation.md`
  - `docs/specs/goal-loop-contract.md`
  - `docs/farplane-framework/deep-init-critical-path.md`
  - `docs/farplane-framework/project-files.md`
  - `hooks.json`
  - `skills/deep-init-project/SKILL.md`
  - `skills/horizon-advisor/SKILL.md`
  - `skills/goal-advisor/SKILL.md`
  - `skills/pulse-update/SKILL.md`
  - `skills/steer-update/SKILL.md`
  - `skills/update-memory/SKILL.md`
  - `skills/skill-maintenance/SKILL.md`
  - `skills/learning-drain/SKILL.md`
  - `skills/eval/SKILL.md`
  - `skills/knowledge-tidier/SKILL.md`
  - `skills/skill-maintenance/scripts/generate_harness_graph.py`
  - `skills/skill-maintenance/scripts/generate_skill_graph.py`
- `Signature delta:`
  - `parse_skill_signature(markdown) -> reads + writes + routes + gates`
  - `build_lifecycle_graph(repo_root, curated_refs?) -> nodes + edges + fsa`
  - `write_lifecycle_graph(graph, json_path, js_path?) -> artifacts`
- `Type Sketch:`

```text
LifecycleNode = {
  id: string,
  kind: skill | file | state | hook | automation | report | ticket | doc | fsa_state,
  label: string,
  path?: string,
  owner?: string,
  tags: string[]
}

LifecycleEdge = {
  source: string,
  target: string,
  type: reads | writes | routes_to | triggers | guards | updates | documents | contains | transition,
  evidence_ref: string,
  confidence: explicit | parsed | curated
}

FsaProjection = {
  id: string,
  states: LifecycleNode[],
  transitions: LifecycleEdge[],
  start: string,
  terminal: string[]
}
```

- `Diagram:`

```mermaid
flowchart LR
  docs["Framework docs"] --> parser["lifecycle graph generator"]
  skills["SKILL.md signatures"] --> parser
  hooks["hooks.json"] --> parser
  parser --> graph["farplane-lifecycle-graph.json"]
  graph --> ui["future Farplane UI"]
  graph --> fsa["FSA projections"]
  fsa --> init["init lifecycle"]
  fsa --> goal["ticket-to-Goal"]
  fsa --> loops["Pulse/Steer"]
  fsa --> drains["memory/drain upkeep"]
```

## Done / Proof

```text
done_when:
  - A new lifecycle hub explains Farplane end-to-end for new users and links to deeper details.
  - The docs explain why Farplane uses visible files, Goal Packets, two automation loops, explicit proof, and drain/update passes, grounded in current memory decisions.
  - A graph contract defines lifecycle node/edge types and FSA projection rules.
  - Hooks/runtime surfaces are documented as graphable surfaces without making hooks a judgment-heavy brain.
  - The generator emits a parseable lifecycle graph JSON and JS wrapper.
  - The graph includes directional skill-to-file/state edges for Deep Init, Horizon, Goal Advisor, Pulse, Steer, hooks, update-memory, skill-maintenance, learning-drain, eval, and knowledge-tidier.
  - FSA projections exist for init, automation activation, ticket-to-Goal execution, and memory/drain upkeep.
  - Tests cover parser extraction, graph shape, and FSA projection presence.
  - Existing reference graph and skill graph behavior are not regressed.

proof:
  checks:
    - `python3 -m py_compile skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py`
    - `python3 -m unittest skills/skill-maintenance/scripts/test_generate_farplane_lifecycle_graph.py`
    - `python3 skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py --check`
    - `python3 bin/validators/check_doc_refs.py`
  manual:
    - Inspect `docs/farplane-framework/lifecycle.md` for new-user readability.
    - Inspect `skills/skill-maintenance/graph/farplane-lifecycle-graph.json` for expected nodes, edge types, and FSA projections.
    - Confirm no graph edge claims confidence `explicit` without a source ref.
  review:
    - rubric: documentation-quality / framework-contract / graph-schema
      required_tas: TAS-A or explicit blocker
  evidence:
    - `tickets/TASK-0213/progress.md`
    - generated graph JSON
    - command summaries and any review artifact under `tickets/TASK-0213/artifacts/`
```

## Run Hints

- `Likely size:` large
- `Goal recommendation:` required
- `Budget hint:` one active local implementation window; no deploy, no push, no spend
- `Compute hint:` local_shared
- `Planning hint:` native Goal from this packet
- `Proof weight:` tests + review
- `Proof route:` mechanical checks first; reviewer for material docs/schema if available
- `Final evidence:` final response links changed docs, generated graph, tests/checks, and review or explicit review-unavailable note
- `Batchability:` single-ticket
- `Human inputs/assets:` none; operator explicitly asked to create the Goal and implement end-to-end
- `Credentials / external access:` none
- `Compute/runtime needs:` local Python only
- `Tooling gaps:` possible lack of reviewer lane; if unavailable, record explicit risk
- `QA risks:` parser may overclaim edges; use confidence levels and explicit curated refs
- `Human gates:` none for local docs/code implementation; stop for destructive git actions, deploy, external services, or secrets
- `Agent decision boundaries:` do not modify unrelated dirty files; do not make graph extraction a scheduler; do not auto-compact memory

## Goal Packet

- `Goal packet:` active
- `Program:` `tickets/TASK-0213/program.md`
- `Progress:` `tickets/TASK-0213/progress.md`
- `Files:`
  - `tickets/TASK-0213/ticket.md`
  - `tickets/TASK-0213/program.md`
  - `tickets/TASK-0213/progress.md`
  - `docs/farplane-framework/README.md`
  - `docs/farplane-framework/deep-init-critical-path.md`
  - `docs/farplane-framework/project-files.md`
  - `docs/specs/filesystem-lifecycle.md`
  - `docs/specs/doc-governance.md`
  - `docs/specs/steer-pulse-automation.md`
  - `docs/specs/goal-loop-contract.md`
  - `docs/MEMORY.md`
  - `docs/TROUBLES.md`
  - `docs/LESSONS.md`
  - `hooks.json`
  - `skills/skill-maintenance/scripts/generate_harness_graph.py`
  - `skills/skill-maintenance/scripts/generate_skill_graph.py`
  - `skills/skill-maintenance/graph/README.md`
- `Generated Goal prompt:` `tickets/TASK-0213/generated-goal-prompt.md`
- `Metric provider:` mechanical + review
- `Feedback preset:` none
- `Drift reviewer:` inline, reviewer before final completion if available
- `Heartbeat:` none
- `Stop condition:` complete when Done / Proof passes; blocked on parser ambiguity that cannot be represented with confidence levels, doc placement conflict, test failure, or unavailable required local files
- `Reflection:` append compact turn entries to `progress.md`
- `Refs:` `docs/specs/goal-loop-contract.md`,
  `tickets/templates/goal-loop/program.md`,
  `tickets/templates/goal-loop/progress.md`

## State

- `next_action:` start the native Goal with `tickets/TASK-0213/generated-goal-prompt.md`
- `blocked:` no
- `latest_verification:` none yet
- `result:` active Goal Packet prepared

## Links

- `program:` `tickets/TASK-0213/program.md`
- `progress:` `tickets/TASK-0213/progress.md`
- `artifacts:` `tickets/TASK-0213/artifacts/`
- `review:` pending
- `refs:`
  - `docs/specs/goal-loop-contract.md`
  - `docs/specs/steer-pulse-automation.md`
  - `docs/specs/filesystem-lifecycle.md`
  - `docs/specs/doc-governance.md`
  - `docs/farplane-framework/README.md`
  - `docs/farplane-framework/deep-init-critical-path.md`
  - `skills/skill-maintenance/graph/README.md`

## Notes

- `Blast radius:` framework docs and skill-maintenance graph generation only.
- `Risks / rollback:` if parser extraction is noisy, keep docs and schema while reverting generator/artifacts in this ticket scope.
- `Follow-ups:` Farplane UI rendering of the lifecycle graph belongs in a separate UI ticket.
- `Citations:` current memory decisions require ticket-backed Goal Packets, two-loop Pulse/Steer automation, artifact-first docs, and safe memory tidying.
