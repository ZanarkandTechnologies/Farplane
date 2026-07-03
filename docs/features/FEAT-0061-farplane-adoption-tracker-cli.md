---
title: Farplane adoption tracker CLI
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0009
refs:
  - bin/core/farplane_adoption.py
  - bin/tests/test_farplane_adoption.py
  - docs/features/registry.jsonl
  - experiments/decisions/2026-06-24-project-harness-rollout-feature/decision.md
  - tickets/TASK-0216/ticket.md
feature_id: FEAT-0061
system_id: SYS-0009
category: proof
public: true
surfaces:
  - bin/core/farplane_adoption.py
  - bin/tests/test_farplane_adoption.py
  - docs/features/registry.jsonl
source_refs:
  - experiments/decisions/2026-06-24-project-harness-rollout-feature/decision.md
  - tickets/TASK-0216/ticket.md
external_refs: []
evidence_refs:
  - bin/tests/test_farplane_adoption.py
known_limits: Local CLI resolver only. It reads explicit project roots, roots files, or known ~/.farplane state files; it does not crawl the whole computer, mutate project manifests, or render Office UI directly.
metrics:
  - farplane_adoption_scan_pass
  - feature_adoption_drift_count
last_verified: 2026-06-24
---
# Farplane adoption tracker CLI

Farplane adoption tracker CLI exists to find where Farplane's declared conventions are
not adopted across active surfaces. It belongs to [Maintenance And Release
OS](../systems/maintenance-release-os.md) and keeps `FEAT-0061` as a stable capability
handle because the behavior has an owner, proof path, and maintenance boundary.

```text
scan_adoption(repo_state, feature_set) -> adoption_gaps + followup_tickets
```

## At A Glance

- Feature ID: `FEAT-0061`
- System: [Maintenance And Release OS](../systems/maintenance-release-os.md)
- Status: `implemented`
- Category: `proof`
- Primary user: maintainer and release reviewer
- Job: find where Farplane's declared conventions are not adopted across active surfaces.

## Problem

A harness can declare a policy in docs while templates, skills, tickets, or validators
still follow the old shape.

The adoption tracker CLI gives maintainers a repeatable way to scan drift and decide
whether to fix, defer, or retire a convention.

## What It Does

- Scans active repo surfaces for adoption of feature or documentation conventions.
- Reports mismatches between docs, templates, skills, registries, and validators.
- Separates real blockers from known transitional gaps.
- Creates or informs follow-up tickets when adoption requires more than a mechanical fix.
- Supports release hygiene before declaring a framework version stable.

## User Stories

- As a maintainer, I can see which surfaces still use old docs or feature patterns.
- As a release reviewer, I can require adoption evidence before calling a migration done.
- As an agent, I can turn scan findings into targeted tickets instead of broad cleanup.

## Operating Contract

Adoption scans prove policy rollout across active surfaces.

- Scans name the convention under test and the surfaces checked.
- Findings classify missing, stale, conflicting, or accepted transitional states.
- Mechanical fixes may be applied directly; ambiguous findings become tickets.
- The scan output is evidence for maintenance release decisions.

## Surfaces

Owner surfaces:

- `bin/core/farplane_adoption.py`
- `bin/tests/test_farplane_adoption.py`
- `docs/features/registry.jsonl`

CLI entrypoint:

- `python3 bin/farplane.py adoption scan`

Source context:

- `experiments/decisions/2026-06-24-project-harness-rollout-feature/decision.md`
- `tickets/TASK-0216/ticket.md`

Evidence:

- `bin/tests/test_farplane_adoption.py`

## Proof And Quality

Required checks:

- `python3 docs/features/validate_features.py`
- `python3 bin/validators/check_doc_refs.py`

Acceptance signals:

- The feature remains listed under exactly one owning system.
- The owner surfaces still exist and agree with this contract.
- Evidence refs support the current status.

## Rollout And Maintenance

- Update this feature page first when the capability contract changes.
- Then update owner surfaces and regenerate feature/system registries when metadata changes.
- Preserve the feature ID while active templates, skills, tickets, or docs still reference it.
- Maintenance owner: Maintenance And Release OS.

## Limits And Non-Goals

- This feature is not a universal linter for every repo file.
- This feature does not mutate policy by itself.
- This feature does not replace human release judgment.
- Known limit: Local CLI resolver only. It reads explicit project roots, roots files, or known ~/.farplane state files; it does not crawl the whole computer, mutate project manifests, or render Office UI directly.
- Delete or merge this feature only when its current truth has moved into a clearer owner and all active refs are removed.

## Metrics

- `farplane_adoption_scan_pass`
- `feature_adoption_drift_count`

## Alternatives Considered

- Keep this only as a registry row.
  Decision: reject.
  Reason: Farplane features must be readable specs, not opaque metadata entries.
- Fold this entirely into the owning system page.
  Decision: defer.
  Reason: keep the `FEAT-*` page while templates, skills, tickets, or proof surfaces need a stable capability handle.

## Change History

- 2026-06-26: Feature spec created.
- 2026-06-27: Migrated into the reader-first feature-spec shape.
