---
title: "Fundamentals"
status: active
owner: doc-governance
created_at: 2026-06-12
updated_at: 2026-06-12
tags:
  - farplane
  - fundamentals
  - harness
refs:
  - docs/specs/README.md
  - README.md
---

# Fundamentals

This folder holds Farplane's conceptual foundations: the principles, mental
models, and best-practice contracts that explain how to think about the harness.

Use this folder for docs that are reusable across many surfaces but are not
themselves implementation specs, schemas, runtime contracts, or ticket flows.

## Current Docs

- `harness-algebra.md` - operational model for optimizing harness behavior:
  loss terms, coordinates, proof signals, and accept/hold/rollback rules.
- `harness-engineering-doctrine.md` - placement doctrine for deciding where a
  harness change belongs.
- `prompt-engineering.md` - shared prompt contract for prompt-like templates,
  examples, output shapes, and proof expectations.

## Boundary

- Put foundational thinking, reusable doctrine, and cross-surface best
  practices here.
- Put buildable behavior contracts, schemas, lifecycle specs, execution loops,
  runtime adapters, and proof gates in `docs/specs/`.
- Put operational workflows in `skills/`.
- Put machine-readable rule files in `rules/`.
