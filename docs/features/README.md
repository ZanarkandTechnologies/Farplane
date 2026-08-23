---
title: "Feature Docs"
status: active
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - features
  - generated-registry-source
refs:
  - docs/prd.md
  - docs/systems/README.md
  - docs/features/TEMPLATE.md
  - docs/features/registry.md
  - docs/features/registry.jsonl
  - docs/features/validate_features.py
---

# Feature Docs

Farplane feature docs are the spec files for first-class capabilities. Each
feature has one Markdown owner file. Experimental features are allowed here when
they describe a real capability or UX contract being dogfooded, not a minor
patch. If a `FEAT-*` handle is too small, stale, or
implementation-detail-shaped to deserve a page here, delete the handle and
remove its template, source, and ticket references.

The project-level feature policy lives in [`farplane/harness.yaml`](../../farplane/harness.yaml).
In short: a Farplane feature must be relevant to Farplane as an agentic
maintenance tool for harnesses. It should help an operator or agent maintain,
evaluate, steer, prove, report on, or productize harness behavior.

This folder is the authored source for feature specs and generated feature records:

```text
feature pages in docs/features/
  -> docs/features/registry.jsonl
  -> docs/features/registry.md
```

Systems stay in [`docs/systems/`](../systems/README.md). A system explains the product layer; its `feature_refs` point to feature specs that are worth maintaining as named capabilities. Do not create a second spec-folder truth shelf for feature behavior.

## Current Outputs

- Human registry: [`registry.md`](registry.md)
- Machine registry: [`registry.jsonl`](registry.jsonl)
- Feature template: [`TEMPLATE.md`](TEMPLATE.md)

Do not hand-edit generated registry files.

## Spec Shape

Each feature page starts with YAML front matter used directly by the generated
registries. Do not add a `feature_record_json` block; it duplicates the page
and makes the human contract harder to read.

```yaml
---
title: "Goal Advisor execution compilation"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0003
refs:
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
feature_id: FEAT-0032
system_id: SYS-0003
category: execution
public: true
surfaces:
  - skills/goal-advisor/SKILL.md
source_refs:
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
external_refs: []
evidence_refs:
  - skills/goal-advisor/evals/evals.json
known_limits: "Compiles visible execution prompts; it is not a hidden scheduler."
metrics:
  - goal_prompt_contract_pass
last_verified: 2026-06-26
experimental: false
superseded_by: false
track: false
---
```

The body must make the feature understandable before it lists owner paths.
Start from [`TEMPLATE.md`](TEMPLATE.md), whose shape is adapted from:

- Kubernetes KEPs: summary, motivation, goals, non-goals, risks, test plan,
  rollout, monitoring, and troubleshooting.
- Rust RFCs: motivation, guide-level explanation, reference-level explanation,
  drawbacks, alternatives, prior art, and unresolved questions.
- Atlassian PRDs: objectives, success metrics, assumptions, options, supporting
  docs, open questions, and explicit out-of-scope boundaries.
- GitLab description templates: repo-owned Markdown templates that make the
  right fields easy to fill at creation time.

Farplane adapts those into a smaller contract: problem, behavior, user stories,
operating contract, surfaces, proof, rollout, limits, alternatives, and change
history.

## Field Contract

- `feature_id`: stable `FEAT-####` identifier for this docs-worthy capability.
- `title`: short, unique feature name.
- `status`: `implemented`, `partial`, `proposed`, `designed`, `deferred`, or
  `retired`.
- `system_id`: owning `SYS-*` record from `docs/systems/*.md`.
- `category`: broad grouping such as `planning`, `proof`, `memory`,
  `source-ingestion`, `skills`, or `improvement-loop`.
- `public`: must be `true`. A feature file is a public/maintainable capability
  owner, not a private alias row.
- `surfaces`: repo paths that own the live behavior.
- `source_refs`: `SRC-*` records, local docs, tickets, memories, or feature
  specs that explain why the feature exists.
- `external_refs`: outside URLs, repos, videos, or standards that influenced
  the feature.
- `evidence_refs`: tickets, artifacts, commands, evals, or experiment outputs
  that support the current status.
- `known_limits`: one concise caveat future agents should preserve.
- `metrics`: metric names or scorecards associated with the feature.
- `last_verified`: date when the record was checked against live surfaces.
- `experimental`: `true` when the feature is real enough to dogfood but not yet
  globally stable; `false` when accepted as a normal Farplane capability.
- `superseded_by`: `false`, one `FEAT-*`, or a list of successor feature IDs
  when this feature's active contract has moved to a clearer capability.
- `track`: optional `false` or a compact review checklist consumed by tracking
  workflows such as `dogfood-review`. Use it to name what to read, the rubric
  to apply, allowed decisions, and the interval-summary output. Keep procedural
  logic, tool branching, and broad workflow instructions in the owning skill,
  not in feature frontmatter. Retired or superseded features must use
  `track: false`; successor features own active dogfood review.

Generated rows add `system_name` and `owner_spec`.

`experimental` and `superseded_by` are separate from `status`:

```text
implemented + experimental=true
  = working enough to dogfood, not globally stable

implemented + experimental=false
  = accepted normal Farplane capability

superseded_by=FEAT-#### | [FEAT-####]
  = the active contract is moving to clearer successor feature docs
```

## Update Rules

1. Start from [`TEMPLATE.md`](TEMPLATE.md) for a new first-class capability.
2. Add or update the feature page under this folder.
3. Add the feature ID to exactly one system file's `feature_refs`.
4. Update template/source/ticket refs only when they should still point at the
   surviving feature.
5. Run:

   ```bash
   python3 docs/features/validate_features.py --write
   python3 docs/features/validate_features.py
   ```

## Deletion Rule

Delete a `FEAT-*` handle when it no longer earns a feature spec page. Before
deleting, move any current truth into the owning system doc, feature spec, skill,
template, source record, or ticket. Then remove all active references to the
deleted ID and regenerate the registries.

When deletion retires a previously feature-backed contract and future agents
could plausibly recreate it, retain or convert its page into a concise
`status: retired` decision record. Name the decision, evidence, replacement
owner, and concrete reintroduction guard. Do not retain a live alias merely as
an archaeological record. Do not keep a retired alias just to preserve noise.
