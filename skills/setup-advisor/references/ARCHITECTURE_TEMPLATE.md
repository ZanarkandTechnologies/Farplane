# Architecture

Current-state system map for the repo.

Use this file after `AGENTS.md` to explain the major surfaces and where the
canonical truth for each concern lives.

## Purpose

Describe what this repo is for and what the main moving parts are.

## Canonical Surfaces

- `AGENTS.md`: operational map loaded every loop
- `ARCHITECTURE.md`: top-level system map
- `README.md`: product story and setup
- `docs/prd.md`: product requirements and current slice
- `tickets/README.md`: execution contract and ticket lifecycle

## Main Surfaces

- `docs/`: durable knowledge and specs
- `tickets/`: active work and archived history
- `src/` or runtime directories: implementation surface
- `tests/`: verification surface
- `scripts/`, `bin/`, or equivalent: operational helpers

## Systems

One row per durable system; there is no separate systems or feature-spec
folder. The owner column names where each contract lives.

| System | Purpose | Boundary (what belongs elsewhere) | Owning code / docs |
| --- | --- | --- | --- |

## Read Order

1. `AGENTS.md`
2. `ARCHITECTURE.md`
3. `README.md`
4. `docs/prd.md`
5. active ticket and `tickets/README.md`

## Current Limits

List the most important boundaries or known non-goals so this file stays honest.
