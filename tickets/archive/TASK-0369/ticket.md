---
template_id: ticket-template
template_version: "0.2.1"
feature_refs:
  - FEAT-0071
  - FEAT-0072
ticket_id: TASK-0369
title: Add persistent ICP and world memory to Feed Scout planning
status: done
created_at: 2026-07-14T09:26:43Z
updated_at: 2026-07-14T12:23:28Z
---

# TASK-0369: Add persistent ICP and world memory to Feed Scout planning

## Summary

Give Feed Scout one update-in-place Markdown memory for canonical ICP profiles,
current trends, notable observations, and source gaps. Feed the relevant memory
and per-area ICP contract into Plan Next Wave and ticket-owned artifact work so
Pulse proposes grounded, baseline-aware work rather than shallow ideas.

## Scope

- In: per-area ICP schema, Feed Scout memory template/validator/update contract,
  Plan Next Wave and Pulse retrieval, Farplane artifact-skill retrieval, live
  memory seed, focused evals, docs, install and automation synchronization.
- Out: snapshots, monthly ledgers, trend timelines, vector databases, new
  planners/Pulses/controllers, automatic publication, and silent mutation of
  canonical ICP definitions by external content.

## Delta

```text
overall_before:
  - Feed Scout produces dated feeds and reports, but Pulse has no compact persistent model of the ICP or current external context.
  - Areas carry planner instructions and metrics, but no explicit audience contract.
overall_after:
  - harness.areas.<area>.icp is canonical audience truth.
  - .farplane/feed-scout/memory.md is one compact, update-in-place world-context file read by Feed Scout, planning, and artifact work.
why_now:
  - Recent Pulse tickets satisfy mechanics but often lack ICP-specific stakes, credible baselines, and game-changing knowledge value.
first_principles_basis:
  objective: Increase the relevance and downstream value of every admitted artifact.
  need: Retain current audience/world context across daily runs without replaying raw feeds.
  assumptions: Markdown is sufficient when headings, provenance, and update rules are explicit.
  root_cause: External evidence is dated and fragmented while ICP meaning is implicit inside prose.
  constraints: Keep one planner, one Pulse, human gates, visible files, and no hidden runtime service.
  first_viable_slice: One memory file plus explicit ICP records and retrieval gates.
  proof_or_falsification: Validator fixtures and planner evals must reject shallow, ungrounded candidates and preserve local-only self-improvement paths.
  tradeoff: A compact mutable synthesis loses trend history, intentionally, in exchange for cheap current-context retrieval.
  non_goals: Trend analytics, snapshot diffs, or autonomous changes to the protected project charter.
```

## Reward

```yaml
kpi_rewards:
  - reward_id: accepted-evidence-cycles-world-memory
    kpi_id: accepted_evidence_cycles
    expected_reward: "one validated context loop that improves ticket grounding"
    check_in_at: "2026-07-21T09:26:43Z"
    actual_result:
    decision:
    evaluated_at:
    evaluation_key:
    supersedes_evaluation_key:
    evidence_refs: []
guard: "Memory context must improve grounding without becoming planning authority or a new controller."
```

## Change Plan

```text
architecture_signatures:
  module_level:
    - feed_scout(memory_ref, harness_areas, sources) -> daily_report + updated_memory + candidates
    - validate_memory(path) -> errors[]
  main_flow:
    - work_pulse(board_state, harness_areas_with_icp, world_memory_ref) -> grounded_ticket_specs
  data_flow:
    - harness.areas.<area>.icp -> Feed Scout memory ICP section -> planner audience_context -> ticket execution.inputs
  builder_freeform_boundary:
    - Wording and helper structure are builder-owned; ownership, schema, authority, and proof boundaries are fixed by this ticket.
```

### Change 1: Persistent memory contract

```text
fixes:
  - Feed Scout forgets synthesized audience and trend context between daily reports.
before:
  - Dated reports and a raw JSONL ledger are the only durable external-signal surfaces.
after:
  - One validated Markdown file is updated in place with ICPs, trends, notable things, and source gaps.
read:
  - path: skills/feed-scout
    reason: Owner of acquisition, synthesis, reports, and handoff.
write:
  - path: skills/feed-scout
    change: Add memory data contract, template, validator, tests, update rules, and evals.
operation:
  - Preserve useful synthesis, merge duplicates, cite sources, and replace superseded current understanding without append-only history.
signature_or_type_impact:
  - FeedScoutConfig gains memory; Feed Scout returns an update receipt.
routes:
  docs: update_docs
  qa: tests
  review: reviewer
qa:
  - Template validates; malformed/missing headings and source refs fail focused fixtures.
failure_modes:
  - Memory becomes uncited vibes, grows as a timeline, or rewrites canonical ICPs.
```

### Change 2: Grounded planning and execution handoff

```text
fixes:
  - Pulse can admit technically valid artifacts with no precise ICP, baseline, or belief/behavior delta.
before:
  - Planning sees optional dated reports and prose-only area definitions.
after:
  - Complete area records include ICP; outward candidates bind current memory evidence, baseline, and decision-changing value; ticket inputs carry those refs into artifact skills.
read:
  - path: skills/plan-next-wave, skills/pulse-update, .agents/skills/farplane-*
    reason: Planning, materialization, and artifact-production seams.
write:
  - path: farplane/harness.yaml, skills/plan-next-wave, skills/pulse-update, .agents/skills/farplane-*
    change: Add retrieval and quality gates without another planner or global prompt rule.
operation:
  - Use ticket-provided context first; direct skill calls fall back to configured memory; local harness evidence remains valid for self-improvement.
signature_or_type_impact:
  - Area records gain icp; ticket specs gain audience_context and stable evidence inputs.
routes:
  docs: update_docs
  qa: agent_qa_test
  review: reviewer
qa:
  - Planner eval accepts a grounded ICP/baseline candidate and rejects a shallow trend-name candidate.
failure_modes:
  - Memory is treated as authority, stale items are presented as fresh, or every internal ticket is forced to cite external trends.
```

visual_companion:
  path: tickets/archive/TASK-0369/diagrams.md
  generated_by: inline diagramming from the accepted architecture boundary
  blocks_approval: false
  canonical_contract: ticket.md

## Gap Analysis

- Current state: daily acquisition, dedupe, reports, ticket history, and area
  instructions exist; persistent synthesized external context and explicit ICP
  records do not.
- Production expectation: current audience context is cheap to retrieve,
  provenance-bound, clearly separated from canonical strategy, and passed to
  downstream work.
- Missing gaps: memory shape, update semantics, validation, planner consumption,
  artifact handoff, and live initialization.
- Comparable implementations: local Farplane file/memory doctrine and current
  Feed Scout/Pulse contracts; no external service is required for this slice.
- Recommendation: land the smallest Markdown loop now and evaluate ticket
  relevance before considering semantic retrieval or richer storage.

## Done

```text
done_when:
  - Every harness area has a validated ICP profile and init templates expose the same optional standard.
  - Feed Scout owns one configured Markdown memory with required ICPs, Trends, Other Notable Things, and Source Gaps sections.
  - A daily run reads existing memory, updates it in place with provenance, and emits a memory receipt before planner handoff.
  - Plan Next Wave and Pulse load the memory once, bind relevant refs to outward candidates, and reject shallow no-baseline/no-belief-delta proposals.
  - Farplane artifact skills consume ticket-owned audience/world context first and configured memory as a direct-call fallback.
  - Live memory is seeded, source/install surfaces are synchronized, focused tests/evals pass, and an independent reviewer returns pass-ready.
```

## QA Strategy

```text
qa_strategy:
  proof_weight: agent_qa
  checks:
    - Run Feed Scout memory validator unit tests and validate the seeded file.
    - Run project-file validator tests for the ICP schema.
    - Run focused Feed Scout, Plan Next Wave, and Pulse eval validation.
    - Run skill registry/docs/install checks affected by changed skill contracts.
  manual:
    - Inspect the seeded memory for compactness, provenance, and no timeline/snapshot semantics.
  delegated_lanes:
    - Native reviewer checks architecture placement, prompt quality, and ticket Done / Proof.
  review:
    - rubric: harness-change, prompt-quality, ticket-opportunity-quality
      required_tas: pass-ready
  evidence:
    - tickets/archive/TASK-0369/artifacts/qa/verification.md
    - tickets/archive/TASK-0369/artifacts/review/completion-review.md
  goal_advisor_inputs:
    proof_route: focused tests + eval schema checks + live artifact validation
    final_evidence: tickets/archive/TASK-0369/artifacts/qa/verification.md
    final_checkpoint: independent reviewer receipt before awaiting_review
  residual_risk:
    - Actual relevance improvement still requires observing later Pulse waves and Reward outcomes.
```

## Docs Strategy

```text
docs_strategy:
  outcome: update_docs
  doc_targets:
    - docs/features/FEAT-0071-project-work-pulse.md
    - docs/systems/source-sidecar-systems.md
    - skills/feed-scout/references/data-model.md
    - docs/farplane-framework/project-files.md
  validation:
    - feature, doc-ref, skill, and project-file validators
```

## State

- Current: implemented, independently reviewed TAS-A, and ready to archive.
- Blockers: none.
- Final evidence: 45 focused tests, strict live/template/eval-fixture memory
  validation, unspoiled planner eval A, deterministic admitted-spec replay,
  project/docs/feature validators, installed-skill parity, and live automation
  readback.
- Handoff: evaluate Reward `accepted-evidence-cycles-world-memory` at
  `2026-07-21T09:26:43Z` against a real later Pulse wave; this delayed product
  outcome does not reopen implementation completion.
- Last verification: 2026-07-14T12:23:28Z.

## Links

- [Visual companion](diagrams.md)
- [QA verification](artifacts/qa/verification.md)
- [Final TAS-A review](artifacts/review/completion-review.md)
- [Feature contract](../../../docs/features/FEAT-0072-persistent-icp-and-world-memory.md)

## Notes

- Placement: primary lever is the Feed Scout skill/file-memory contract.
  Secondary synchronization belongs in the project harness schema, planner,
  Pulse, artifact skills, and deterministic validators. Root/global prompts,
  subagents, and hooks are intentionally not primary surfaces.
- Closeout: no commit was created because this checkout contains extensive
  unrelated and overlapping operator work; the ticket-scoped evidence and
  explicit validation boundary are the handoff surfaces.
