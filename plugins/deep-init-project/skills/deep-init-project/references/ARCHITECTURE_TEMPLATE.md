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
- `docs/specs/README.md`: index of deeper behavior specs
- `tickets/README.md`: execution contract and ticket lifecycle

## Main Surfaces

- `docs/`: durable knowledge and specs
- `tickets/`: active work and archived history
- `src/` or runtime directories: implementation surface
- `tests/`: verification surface
- `scripts/`, `bin/`, or equivalent: operational helpers

## Read Order

1. `AGENTS.md`
2. `ARCHITECTURE.md`
3. `README.md`
4. `docs/specs/README.md`
5. active ticket and `tickets/README.md`

## Current Limits

List the most important boundaries or known non-goals so this file stays honest.
