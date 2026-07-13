---
ticket_id: TASK-0044
status: active
---

# Provider source-gap fixture

## Summary

Verify a live provider observation.

## Scope

- In: provider observation plus independent local validation.

## Delta

The integration should expose the provider observation.

## Change Plan

Query the bound provider API and run the deterministic local check.

## Done

- A live provider observation or recorded provider export proves the claim.

## QA Strategy

API target: `https://provider.example/v1/observations`. Credentials and the
recorded export are unavailable. Preserve that source gap; the local check is
supporting evidence only.

## Docs Strategy

No docs change.

## Links

- `artifacts/local-check.log`
