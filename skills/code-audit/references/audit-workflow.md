---
title: Code Audit Workflow
owner: code-audit
status: active
kind: reference
---

# Audit Workflow

Use this reference before inspecting architecture or ranked modules. The audit
flows from whole-system structure to local module details so local cleanup does
not outrun the real product boundary.

## Architecture Pass

```text
architecture_audit(context, inventory)
  -> boundary_findings + cross_cutting_risks + module_audit_targets
```

Check:

- Ownership boundaries: each workflow has an obvious home, and helpers are not
  scattered across unrelated packages.
- Dependency direction: low-level modules do not import product policy, UI
  modules do not own backend rules, and shared utilities do not become dumping
  grounds.
- Public contracts: exported APIs, CLI commands, schemas, config keys, and
  generated artifacts match docs and call sites.
- State flow: data moves through named boundaries rather than hidden globals,
  ad hoc files, or transcript-only state.
- Side effects: filesystem, network, subprocess, database, cache, and external
  service calls are isolated at edges.
- Observability: important lifecycle failures leave useful logs, receipts,
  evidence artifacts, or validator output.
- Recovery: partial failures have a retry, rollback, cleanup, or clear
  residual-risk note.
- Test strategy: critical paths have characterization, smoke, integration,
  eval, QA, or review proof appropriate to their behavior.

## Module Pass

```text
module_audit(component)
  -> findings + owner_routes + proof_routes
```

Check:

- Responsibility: one module owns one coherent job or explicitly composes
  smaller owners.
- Size and complexity: large files, long functions, nested conditionals, and
  repeated branches are justified by the domain or routed to `refactoring`.
- Interfaces: input/output types, exceptions, return values, and public names
  are clear enough for callers and tests.
- Security and resilience: unsafe inputs, secrets, permissions, dependency
  failure, concurrency, resource exhaustion, and unsafe configuration route to
  `hardening`.
- Tests and proof: missing proof for claimed behavior becomes a test or
  proof-advisor follow-up, not a speculative patch.
- Dead or stale surfaces: unused code, compatibility shims, legacy names, and
  stale docs are classified as delete/consolidate/document tickets when
  supported by evidence.

## Finding Classification

Use one primary route per finding:

- `refactor`: behavior is known; shape is slowing future work.
- `harden`: working behavior has abuse, failure, security, resilience, or
  operational risk.
- `runtime-debugging`: a concrete defect or reproducible failure exists.
- `testing`: behavior is plausible but unproved.
- `document`: implementation is acceptable, but durable docs mislead future
  work.
- `delete`: evidence shows the surface is stale, unused, or duplicated.
- `split-ticket`: the finding crosses independent proof or ownership
  boundaries.
- `no-action`: the apparent smell is justified or not valuable enough now.

Do not combine multiple primary routes in one ticket unless the same proof
surface naturally covers them.
