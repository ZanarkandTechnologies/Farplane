---
template_id: ticket-template
template_version: "0.1.5"
feature_refs:
  - FEAT-0007
  - FEAT-0008
ticket_id: TASK-0253
title: Lean SMART goal KPI snapshot model
phase: complete
status: done
owner: codex
claimed_by:
priority: high
depends_on:
  - TASK-0249
blocked_by: []
ready: true
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-07-01T00:00:00Z
updated_at: 2026-07-01T03:07:00+08:00
next_action: complete; optional follow-up is Farplane UI adapting to daily_diff/current readings
last_verification: 2026-07-01 focused tests, skill checks, snapshot smoke, and diff check passed; X provider currently blocked with 401 source gap
---

# TASK-0253: Lean SMART goal KPI snapshot model

## Summary
Simplify Farplane's KPI standards so goals are readable by humans and agents,
while metric snapshots stay structured enough for charts. The selected model is:
SMART goals live inline under each goal axis, agents use `update_hint` plus
available provider skills to fetch data, and daily snapshots store metric
readings keyed by stable KPI names with optional item breakdowns.

This replaces the emerging table-heavy, registry-heavy shape with one agentic
loop: read goals and ops memory, call the right skills, write daily readings,
derive chart diffs/cumulative views for the UI.

## Scope
- In:
  - Update the Farplane project-file standard for `farplane/goals.md`.
  - Prefer YAML-readable goal axes with inline `smart_goals`.
  - Remove the need for a separate human-authored tracked KPI registry when the
    same information can be derived from `smart_goals[*].kpis`.
  - Simplify metric source bindings into a provider catalog without `enabled`.
  - Standardize daily source snapshots around metric readings:
    `metrics.<kpi>.value` plus optional `items`.
  - Preserve content item breakdowns without polluting KPI names with content
    IDs.
  - Update interval/init/update guidance so agents find missing feedback
    mechanisms and create instrumentation tickets when needed.
- Out:
  - No deterministic parser for `farplane/ops-memory.md`.
  - No new `distribution.md` or `projects.md` surface.
  - No hidden scheduler or daemon.
  - No dashboard-specific chart config unless a metric truly needs an exception.
  - No per-content dynamic KPI names such as
    `video_17966345906934171_instagram_views`.

## Delta

```text
overall_before:
  - KPI axes, tracked KPI tables, metric source bindings, social content items,
    and UI chart semantics are drifting into several overlapping structures.
  - `manual_x_account` / `manual_instagram_account` naming makes skill-produced
    snapshots look like human manual files.
  - The proposed SMART tracker table duplicated goal-axis information and was
    hard to read.
overall_after:
  - Each goal axis owns its SMART goals inline.
  - Each SMART goal names stable KPI keys and an agent-readable update hint.
  - Metric providers are a simple catalog of available skills/files.
  - Daily snapshots store one reading per KPI and optional item breakdowns.
  - UI derives daily diffs and current/cumulative trend views from readings.
why_now:
  - X and Instagram account skills can now fetch real data, exposing the need
    for a lean durable contract before the UI and interval loop hard-code the
    wrong model.
problems:
  - before: Goal axes appeared as KPIs with `provider_missing`.
    after: Goal axes have inline SMART goals; providers belong to KPI readings.
    why_now: The UI needs a clear difference between strategic goals and chart
      metrics.
  - before: Content IDs were candidates for metric-key names.
    after: KPI names stay stable; content IDs live under metric item breakdowns.
    why_now: Multiple videos/posts may be tracked over time without exploding
      the metric namespace.
  - before: `enabled` flags and manual source names implied a rigid control
      panel.
    after: Providers are available coordinates; failed fetches create snapshot
      gaps.
    why_now: The interval agent should reason agentically, not rely on brittle
      config switches.
first_principles_basis:
  objective: Make goals measurable without making goals.md unreadable.
  need: Agents need enough hints to fetch/update metrics; UI needs stable keys
    and dated values.
  assumptions: The agent can semantically read goals and ops memory; chart
    derivation can be deterministic once daily snapshots exist.
  root_cause: Earlier structure optimized for deterministic registries before
    deciding the human/agent-readable goal contract.
  constraints: Keep files lean; avoid new project/distribution surfaces; do not
    parse ops memory deterministically.
  first_viable_slice: Change standards/docs and adapt the metric snapshot
    generator to support compact reading snapshots while keeping existing
    snapshots compatible.
  proof_or_falsification: A Farplane daily snapshot can render goal KPI charts
    and content breakdowns from the new shape without losing current KPI data.
  tradeoff: More agent responsibility in the update loop, less rigid schema.
  non_goals: Full BI semantics, broad analytics warehouse, provider-specific UI
    config, or strict parsing of all Markdown memory.
```

## Reward

```text
moves:
  - Reduces KPI/config bloat before Farplane UI and interval-update depend on it.
  - Makes missing feedback mechanisms visible without blocking ambitious goals.
  - Keeps distribution/social content tracking compatible with many content
    items over time.
win_signal:
  - A human can read the Farplane goals file and understand goals, SMART
    targets, KPI names, update hints, and missing feedback mechanisms in one
    pass.
  - UI chart data can be derived from daily readings: bar = daily diff,
    line/current = reading value.
guard:
  - Do not reintroduce a table-heavy KPI registry unless implementation proves
    the agentic model cannot support charts or provider gaps.
```

## Proposed Data Contract

### `farplane/goals.md`

Use one readable YAML block or YAML-like fenced block for goals:

```yaml
goals:
  distribution_from_evidence:
    question: Can Farplane turn real harness evidence into audience, users, and research authority?
    evidence_hints:
      - evidence-backed content shipped
      - qualified attention
      - serious conversations
      - pilot users
    smart_goals:
      - id: evidence_distribution_q3
        target: 100000 evidence-backed views by 2026-09-30
        kpis:
          - instagram_views
          - x_views
          - posts_published
          - qualified_replies
        update_hint: >
          Use available social account skills and ops-memory tracked content.
          Aggregate relevant content item readings into stable KPI keys.
          Record missing providers or unavailable retention as gaps.

  quality_and_proof:
    question: Do long-running agents preserve quality, proof, and operator control?
    evidence_hints:
      - sufficient proof
      - validator pass rate
      - false completion incidents
      - proof closure rate
    smart_goals:
      - id: proof_quality_q3
        target: 90% of completed material tickets have sufficient proof by 2026-09-30
        kpis:
          - proof_closure_events
          - review_pass_rate
          - false_completion_incidents
        update_hint: >
          Derive available proof readings from rewards, ticket Done/Proof
          blocks, review receipts, and validator results. Record feedback gaps
          for missing review pass rate or false-completion tracking.
```

Required per SMART goal:

```text
id
target
kpis
update_hint
```

Optional per SMART goal:

```text
status: available | proxy | setup_required | missing
notes
```

### `farplane/bindings.md`

Metric bindings are a provider catalog, not a rigid on/off control plane:

```yaml
metric_providers:
  x-account:
    credentials: FARPLANE_X
    writes: .farplane/metrics/sources/x_account_metrics/latest.json
    provides:
      - x_followers
      - x_views
      - x_likes
      - x_retention_score

  instagram-account:
    credentials: FARPLANE_INSTAGRAM
    writes: .farplane/metrics/sources/instagram_account_metrics/latest.json
    provides:
      - instagram_followers
      - instagram_views
      - instagram_likes
      - instagram_retention_score

  pulse_reward_ledger:
    path: .farplane/automation/rewards.jsonl
    provides:
      - accepted_harness_improvements
      - proof_closure_events
```

Provider availability is observed at fetch time. A missing token, missing file,
or unavailable API metric becomes a source gap in the snapshot, not an
`enabled: false` precondition.

### Daily Source Snapshot

Store provider readings keyed by stable KPI names. Content IDs belong in item
breakdowns under a KPI, not in the KPI name.

```json
{
  "date": "2026-07-01",
  "source": "instagram_account_metrics",
  "status": "available",
  "metrics": {
    "instagram_followers": {
      "value": 921
    },
    "instagram_views": {
      "value": 2180,
      "items": [
        {
          "id": "instagram:17966345906934171",
          "value": 2180,
          "kind": "carousel_album",
          "url": "https://www.instagram.com/..."
        }
      ]
    },
    "instagram_retention_score": {
      "value": null,
      "items": [
        {
          "id": "instagram:17966345906934171",
          "value": null,
          "gap": "retention_requires_reel"
        }
      ]
    }
  },
  "gaps": []
}
```

Snapshot rule:

```text
metrics.<kpi>.value = provider reading on that date.
```

Chart rule:

```text
bar = today's reading - previous reading
line/current = today's reading
target progress = today's reading / target when target exists
```

For ratios or scores, daily diff is still useful but cumulative/target display
may be metric-specific:

```text
retention_score: 42 today, +3 points from previous reading
```

## Change Plan
Filled by `impl-plan(ticket)` after approval. Expected implementation units:

```text
architecture_signatures:
  module_level:
    - farplane/goals.md / goal_axis.smart_goals(input): agent-readable KPI contract
    - farplane/bindings.md / metric_providers(input): provider catalog
    - source_snapshot.metrics[kpi].value(input): daily reading
    - farplane_metrics.generate_metric_snapshots(project_root, date): ui/latest.json
  main_flow:
    - interval agent reads goals + ops memory -> calls providers -> writes source snapshots -> runs metric snapshot -> reports diffs/gaps
  data_flow:
    - goals.smart_goals[*].kpis -> expected metric keys
    - provider snapshot.metrics -> dated readings
    - source-snapshots/*/*.json -> ui metric series with daily_diff
  builder_freeform_boundary:
    - Implementation may choose the smallest parser/compat layer, but must not
      parse ops-memory as a deterministic database or reintroduce duplicated
      KPI tables.
```

## Gap Analysis
- Current state:
  - `farplane/goals.md` has KPI axes plus a table-style tracked KPI registry.
  - `farplane/bindings.md` has table-style sources with `enabled` flags and
    `manual_*` source names.
  - Account skills currently emit `observations` and `content_items`.
  - `bin/core/farplane_metrics.py` expects table-defined metric definitions and
    observation lists.
- Production expectation:
  - Goals are readable by the operator and useful to an interval agent.
  - Metric snapshots are structured enough to render trends and explain item
    breakdowns.
  - Missing feedback mechanisms are explicit and actionable.
- Missing gaps:
  - No lean SMART goal field under goal axes.
  - No compact reading snapshot contract accepted by the KPI generator.
  - No chart derivation rule for daily diffs from point readings.
  - Social provider names and source naming still imply manual entry.
  - Interval/update guidance has not been updated to use goal update hints plus
    provider skills.
- Comparable implementations:
  - Local Farplane KPI pipeline from TASK-0249.
  - X/Instagram skill snapshots from TASK-0249 social API work.
- Recommendation:
  - Land standards and compatibility first, then migrate current Farplane goals
    and social snapshots to the lean model.

## Done

```text
done_when:
  - `farplane/goals.md` or its template supports inline `smart_goals` under
    each goal axis with `id`, `target`, `kpis`, and `update_hint`.
  - `farplane/bindings.md` or its template describes metric providers without
    `enabled` as a required concept.
  - Daily source snapshots can use the compact `metrics.<kpi>.value` reading
    shape with optional `items`.
  - KPI UI snapshot generation derives daily diffs from readings and preserves
    current/line values.
  - Existing TASK-0249 observation-list snapshots remain readable during the
    migration window or have a clear compatibility wrapper.
  - Interval/update guidance says agents read goals and ops memory
    semantically, call available provider skills, write source gaps for missing
    feedback mechanisms, and avoid deterministic ops-memory parsing.
```

## QA Strategy

```text
qa_strategy:
  proof_weight: tests
  checks:
    - Unit tests for reading compact metric snapshots.
    - Unit tests for deriving daily_diff from dated readings.
    - Regression test that current observation-list snapshots still produce
      usable UI metrics or are migrated by the compatibility layer.
    - Snapshot smoke command:
      `python3 bin/farplane.py metrics snapshot --project-root . --date <date> --json`.
    - Skill metadata/docs check if templates or skill docs change:
      `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
    - `git diff --check`.
  manual:
    - Inspect generated `.farplane/metrics/ui/latest.json` for daily diff,
      current reading, target progress, and source gaps.
    - Inspect goals file for readability; reject if it becomes table-heavy or
      duplicates SMART goal data elsewhere.
  delegated_lanes:
    - reviewer for final data-contract and docs-readability review if this
      changes project templates or interval skill behavior.
  review:
    - rubric: data_contract_readability_and_backcompat
      required_tas: pass
  evidence:
    - ticket progress log with command outputs
    - example source snapshot before/after
    - generated UI latest JSON
  goal_advisor_inputs:
    proof_route: focused tests plus manual data-shape inspection
    final_evidence: test output, snapshot paths, reviewer receipt
    final_checkpoint: QA evidence review plus reviewer-lane completion review
  residual_risk:
    - Too much agent freedom could make provider calls inconsistent; mitigate
      with provider skill examples and snapshot validators rather than a heavy
      KPI registry.
```

## Docs Strategy

```text
docs_strategy:
  outcome: update_docs
  doc_targets:
    - farplane/goals.md
    - farplane/bindings.md
    - docs/farplane-framework/project-files.md
    - docs/farplane-framework/pulse-and-interval-loop.md
    - skills/interval-update references/templates as needed
    - social account skill metric snapshot references if output shape changes
  no_docs_reason:
  validation:
    - docs and generated registries/checks pass
```

## Agent Contract
Not a UI/browser ticket. The agent-facing contract is the data flow:

```text
Open: none
Test hook: `python3 bin/farplane.py metrics snapshot --project-root . --date <date> --json`
Stabilize: use temporary source snapshots under a test project root for unit tests
Inspect:
  - `farplane/goals.md` readability
  - `farplane/bindings.md` provider catalog
  - `.farplane/metrics/source-snapshots/*/*.json`
  - `.farplane/metrics/ui/latest.json`
Key screens/states: Farplane UI KPI cockpit may consume the output, but UI work is separate
Design baseline: none needed
QA cookbook: none yet
Expected artifacts: source snapshot sample, UI latest sample, focused test output
Delegate with: this ticket path plus TASK-0249 runbook context
```

## Run Hints
- Start with a compatibility design so existing source snapshots still work.
- Avoid adding a new DSL. YAML-like fields are for humans and agents first.
- Keep ops-memory semantic; do not write deterministic code that depends on its
  Markdown structure.
- Treat the new snapshot contract as the deterministic boundary:
  `metrics.<kpi>.value`.

## Links
- Parent / predecessor: [TASK-0249](../TASK-0249/ticket.md)
- Social API setup runbook:
  [2026-06-30-social-api-setup-runbook.md](../TASK-0249/artifacts/2026-06-30-social-api-setup-runbook.md)
- Current metric generator: [bin/core/farplane_metrics.py](../../bin/core/farplane_metrics.py)
- Current goals: [farplane/goals.md](../../farplane/goals.md)
- Current bindings: [farplane/bindings.md](../../farplane/bindings.md)

## Notes
- User preference from design discussion:
  - Goals should read naturally in YAML, with SMART goals directly under goal
    axes.
  - No duplicated tracked KPI registry unless implementation proves it is
    necessary.
  - No `enabled` binding switch as a core concept.
  - Daily snapshots should store readings; charts derive diffs.
  - Stable KPI names stay boring; content IDs live under item breakdowns.
