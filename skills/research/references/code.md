---
title: Code Research
owner: research
status: active
kind: workflow-reference
---

# Code Research

Load for the `code` branch in N2-N4.

## Literal queries

Translate the feature question into literal source expressions: imports,
exported symbols, API calls, filenames, configuration keys, annotations, event
names, and exact error strings. Record every query, language or repository
filter, freshness bar, and empty result.

Build the pool from maintained repositories, official examples, and the
caller's repository family. Use official docs, specifications, changelogs, and
release notes for public contracts; issues and discussions for limitations and
failed approaches; X posts and YouTube demos only as trails to authors, repos,
and talks, verified against inspectable code or docs. Record whether each
modality was inspected, partial, or inaccessible.

## Promotion bar

Score semantic fit, maintenance, completeness, license or dependency
constraints, test evidence, and lifecycle compatibility. Select up to three
candidates that cross the bar. Tutorials and demos without inspectable
implementation are supporting evidence, not the primary pattern. Rejected
candidates keep a concrete reason.

## Finalist file map

Inspect the tree before reading an isolated file. Record the entrypoint, key
files, surrounding types and configuration, data and state flow, lifecycle,
tests and fixtures, error handling, retry, cancellation, validation, migration,
and operational constraints. Keep quoted code minimal and keep direct
repository and file URLs.

An unexplained lifecycle edge creates a code or test query; a version caveat
creates a changelog query; conflicting patterns create a focused comparison.
Mark each branch `open`, `corroborated`, `contradicted`, or `exhausted`.

## Local delta

Separate repository-specific machinery from the transferable constraint. The
delta covers behaviour, ownership, failure paths, and tests, not surface syntax.
Hand off one approach with its downside, exact local owners, and a proportional
proof path.
