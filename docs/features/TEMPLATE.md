---
title: "Feature Name"
status: designed
owner: feature-registry
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
tags:
  - farplane
  - feature
  - sys-0000
refs: []
feature_id: FEAT-####
system_id: SYS-####
category: category
public: true
surfaces: []
source_refs: []
external_refs: []
evidence_refs: []
known_limits: "What this feature deliberately does not claim yet."
metrics: []
last_verified: YYYY-MM-DD
experimental: false
superseded_by: false
track: false
---

# Feature Name

One plain-English paragraph that says what the feature does, who or what uses
it, and why it earns a stable `FEAT-*` handle. A reader should understand the
feature before seeing paths, metrics, or implementation detail.

```text
feature_name(input, state?) -> user_visible_result + evidence + state_delta
```

## At A Glance

- Feature ID: `FEAT-####`
- System: [System Name](../systems/README.md)
- Status: `designed`
- Category: `category`
- Primary user: agent | operator | maintainer | project
- Job: the job this feature makes possible

## Problem

Describe the concrete pain this feature solves. Name the weak prior state,
reader/user impact, and why the feature exists now.

## What It Does

State the behavior as a short contract. Prefer concrete verbs and observable
outcomes over internal labels.

- The feature accepts or reads:
- The feature produces or changes:
- The feature refuses or escalates when:

## User Stories

- As a `role`, I can `do the thing` so that `outcome`.
- As a `role`, I can `inspect proof/state` so that `trust outcome`.

## Operating Contract

Explain how the feature works when it is already part of Farplane. Include
named concepts, state transitions, input/output shape, and ownership boundaries
only as far as a future maintainer needs to preserve behavior.

## Feature Flow

```mermaid
flowchart TD
  classDef keep fill:#f3f4f6,stroke:#6b7280,color:#111827
  classDef changed fill:#fef3c7,stroke:#b45309,color:#111827
  classDef added fill:#dcfce7,stroke:#15803d,color:#111827
  classDef retired fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d,stroke-dasharray: 5 3

  trigger["trigger or caller"]:::keep
  feature["docs/features/FEAT-####.md<br/>feature_id, status, experimental, track"]:::changed
  policy["farplane/harness.yaml<br/>Feature Policy"]:::keep
  surface["owner surface<br/>key variables"]:::changed
  output["created/updated artifact<br/>evidence, report, state_delta"]:::added

  trigger --> feature
  policy --> feature
  feature --> surface
  surface --> output
```

Legend:

- `gray = existing input or policy`
- `amber = feature owner or changed behavior`
- `green = created or updated artifact`
- `red dashed = retired or superseded handle`

## Surfaces

- Owner surfaces:
  - `path/to/owner`
- Supporting surfaces:
  - `path/to/support`
- Generated surfaces:
  - `path/to/generated-output`

## Proof And Quality

- Evidence:
  - `path/to/proof`
- Required checks:
  - `command or validator`
- Acceptance signals:
  - observable behavior or registry state that proves the feature is working

## Rollout And Maintenance

- Update path:
- Rollback path:
- Compatibility notes:
- Maintenance owner:

## Limits And Non-Goals

- This feature does not:
- Known weak spot:
- Delete or merge this feature when:

## Alternatives Considered

- Option:
  Decision: adopt | adapt | reject | defer
  Reason:

## Change History

- YYYY-MM-DD: Created.
