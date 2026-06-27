---
title: "Invocation Runtime"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - systems
  - invocation-runtime
refs:
  - docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md
  - skills/farplane-invocation/SKILL.md
  - bin/farplane_invocation.py
system_record_json: |
  {
    "id": "SYS-0004",
    "name": "Invocation Runtime",
    "status": "implemented",
    "summary": "The explicit invocation, board adapter, compute selector, and external-runner boundary that keep Farplane an invocation/proof layer rather than a hidden daemon.",
    "owner_spec": "docs/systems/invocation-runtime.md",
    "primary_feature_ref": "FEAT-0015",
    "feature_refs": [
      "FEAT-0015"
    ],
    "refs": [
      "docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md",
      "skills/farplane-invocation/SKILL.md",
      "bin/farplane_invocation.py"
    ],
    "last_verified": "2026-06-26"
  }
---
# Invocation Runtime

The explicit invocation, board adapter, compute selector, and external-runner boundary
that keep Farplane an invocation/proof layer rather than a hidden daemon. This page is
the product-layer owner for that subsystem: it explains what belongs here, which feature
specs make up the stack, and where adjacent responsibilities should move.

```text
invocation_runtime(change, repo_state?) -> owned_feature_set + boundary_decision + maintenance_signal
```

## At A Glance

- System ID: `SYS-0004`
- Status: `implemented`
- Primary feature: `FEAT-0015`
- Owner spec: `docs/systems/invocation-runtime.md`
- Feature count: `1`

## Role

Invocation Runtime owns the boundary where work enters Farplane: explicit triggers,
board adapters, compute decisions, run envelopes, and proof packets. It keeps Farplane
an invocation/proof layer rather than an ambient scheduler.

## Feature Docs

- [FEAT-0015 Symphony-compatible Farplane invocation contract](../features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md)

## What Belongs Here

Run envelopes, proof packets, compute selectors, board adapter contracts, runtime state
placement, and future external-runner compatibility.

## What Belongs Elsewhere

Ticket execution belongs in Work Loop; long-running cadence belongs in Horizon Loop;
artifact review belongs in Proof And Review.

## Operating Contract

- Work starts from an explicit trigger or envelope.
- Runtime state lives in `.farplane/` or the owning ticket.
- External adapters carry proof obligations back to Farplane.
- No hidden polling or scheduler behavior is introduced without a new accepted feature.
- Feature-level behavior belongs in `docs/features/FEAT-*.md`; this page owns the system boundary and feature grouping.
- Registry data is generated from system and feature docs, not edited by hand.
- When a capability no longer deserves a feature page, fold its current truth into the best owner and remove active refs.

## Surfaces

- `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md`
- `skills/farplane-invocation/SKILL.md`
- `bin/farplane_invocation.py`

## Proof And Maintenance

- Registry proof: `python3 docs/features/validate_features.py`.
- Link proof: `python3 bin/validators/check_doc_refs.py`.
- Update this system page when product-layer boundaries or feature membership changes.
- Update feature pages when capability behavior changes.
- Regenerate registries and commit generated outputs with the source docs.

## Change History

- 2026-06-27: Migrated into the reader-first system-spec shape.
