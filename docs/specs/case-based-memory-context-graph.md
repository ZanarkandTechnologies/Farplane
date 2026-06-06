# Case-Based Memory Context Graph

Status: seed design

Purpose: give Farplane a way to reason over prior decisions, shipped features,
operator corrections, source inspirations, tickets, and durable memories as
connected cases instead of scattered logs.

This is a navigation and consistency layer over existing records. It should not
replace `docs/MEMORY.md`, `docs/HISTORY.md`, `docs/TROUBLES.md`,
`docs/LESSONS.md`, `docs/features/registry.jsonl`,
`docs/sources/registry.jsonl`, tickets, or skill registries.

## Problem

Farplane is accumulating many local policies, skills, features, and corrective
lessons. The individual ledgers are useful, but agents need a fast way to ask:

- have we made a similar decision before?
- which user correction caused this rule?
- which feature introduced this behavior?
- which ticket or source proves it?
- does this proposed change contradict an older invariant?
- is this a repeated case that should become a policy, skill, validator, or
  ticket template change?

## Recommendation

Build case-based memory as a generated context graph, not as another manual
registry.

Use existing artifacts as source nodes:

- `MEM-*`: durable invariant nodes from `docs/MEMORY.md`
- `HISTORY` events: timeline nodes from `docs/HISTORY.md`
- `TROUBLES` rows: raw correction, blocker, and miss case nodes from
  `docs/TROUBLES.md`
- `LESSONS` rows: distilled prevention-rule case nodes from `docs/LESSONS.md`
- `FEAT-*`: harness feature nodes from `docs/features/registry.jsonl`
- `SRC-*`: source provenance nodes from `docs/sources/registry.jsonl`
- `TASK-*`: ticket nodes from `tickets/**/ticket.md`
- `skills/*`: skill package nodes from `docs/skills/registry.jsonl`
- `docs/specs/*`: contract/spec nodes

Then generate derived edges:

- `introduced_by`: feature -> ticket/history/source
- `constrained_by`: feature/skill/spec -> memory
- `corrected_by`: memory/policy -> trouble or lesson case
- `implemented_in`: feature -> surfaces
- `proved_by`: feature/ticket -> evidence refs
- `routes_to`: skill/spec/policy -> owning workflow
- `contradicts_candidate`: proposed change -> older invariant or known limit

## Case Shape

```json
{
  "case_id": "CASE-0001",
  "summary": "External skill self-healing should not edit installed skill bodies",
  "trigger": "Notion-context repair directly patched an installed skill",
  "decision": "Mirror, ticket, or wrap external skills unless the operator explicitly approves direct edit",
  "nodes": ["MEM-0107", "FEAT-0024", "docs/specs/skill-self-healing.md"],
  "evidence": ["docs/TROUBLES.md", "docs/LESSONS.md", "tickets/TASK-0164/ticket.md"],
  "reuse_when": ["skill self-healing", "external skill maintenance"],
  "avoid_when": ["operator explicitly requests a specific external skill edit"]
}
```

Cases should be generated or curated from existing ledgers. They are retrieval
objects for consistency checks, not a fourth place to maintain raw truth.

## First Useful Checks

1. `policy_consistency`: given a proposed policy edit, retrieve related
   `MEM-*`, `FEAT-*`, trouble cases, lesson cases, and owner specs before editing.
2. `feature_duplicate_check`: given a proposed feature, retrieve matching
   feature rows and prior source decisions.
3. `correction_pattern_check`: given a user complaint, retrieve similar trouble
   rows, distilled lessons, and any promoted memories.
4. `skill_boundary_check`: given a skill maintenance task, retrieve source
   ownership rules and external-boundary cases.

## Non-Goals

- No hosted database in the first pass.
- No new always-on daemon.
- No replacing existing ledgers.
- No hand-maintained giant graph file.
- No hidden autonomy decisions from graph similarity alone.

## Minimal Implementation Path

1. Add this seed spec and registry links.
2. Add a small extractor that reads existing ledgers into normalized nodes.
3. Generate a local JSON graph under `experiments/context-graph/` while the
   shape is still unstable.
4. Add a query helper for `similar cases for <topic>`.
5. Feed the helper into `harness-advisor`, `skill-maintenance`, and `review`
   only after the retrieved cases prove useful.

## Placement

- `docs/specs/case-based-memory-context-graph.md`: graph model and rollout
  contract.
- `docs/features/registry.jsonl`: feature row for dedupe and status.
- Future `bin/*`: deterministic extraction and query helpers.
- Future `skills/*`: only after the workflow becomes repeatable enough to need
  an agent-facing playbook.
