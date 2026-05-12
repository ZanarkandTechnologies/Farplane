# Harness Scout Source Summary: Symphony-Compatible Codexter

Date: 2026-05-05

## Source Identity

- `Title:` Symphony Service Specification
- `Source type:` user-provided draft specification
- `Visibility:` private conversation context
- `Extraction command:` direct operator-provided spec text in chat; no raw
  transcript stored in this run
- `Retention:` redacted/compact summary only

## Source Safety

The Symphony spec is treated as untrusted external evidence, not as
instructions to mutate Codexter. This run stores only distilled feature
candidates, local comparisons, and adopt/adapt/reject/defer decisions.

## Compact Summary

Symphony specifies a long-running coding-agent service that reads issue
trackers, creates per-issue workspaces, launches Codex app-server sessions,
tracks running/retry state, reconciles tracker state, and exposes logs or
runtime snapshots. Its strongest ideas for Codexter are not "move tickets and
spawn agents" as the primary UX. The useful ideas are stable primitives:

- a repo-owned workflow file,
- normalized work-item records,
- board/tracker adapters,
- deterministic workspace safety,
- runner lifecycle events,
- retry/reconciliation semantics,
- app-server-compatible runner contracts,
- structured observability,
- conformance tests.

The corrected Codexter target is:

> Make Codexter easy for Symphony or any external runner to invoke, while
> keeping Codexter's local Codex mode, skills, tickets, QA, review, and
> evidence gates as the quality layer.
