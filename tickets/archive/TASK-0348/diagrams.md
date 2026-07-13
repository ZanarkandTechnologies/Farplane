---
status: companion
source: ticket.md
blocks_approval: false
canonical_contract: ticket.md
generated_by: diagramming
generation_lane: delegated subagent when available; inline fallback allowed; impl-plan waits for validation
---

# Visual Plan

## Reading Order

- Start with `Before` to see why current reports are difficult to scan.
- Check `After` to see the bounded template-and-prototype proof path.
- Use `What Changed` for the compressed old-to-new summary.
- Give feedback against `Feedback Guide`.

## Before: Human decisions and machine proof compete in the same report

Report producers currently invent their own shapes and mix several audiences in
one body. The accepted audit identifies a shared reading spine, but there is no
reusable template or rendered proof yet.

```mermaid
flowchart TD
  classDef keep fill:#f8fafc,stroke:#cbd5e1,color:#334155
  classDef problem fill:#fff5f5,stroke:#dc2626,color:#991b1b

  evidence["source evidence"]:::keep
  producers["report producers<br/>invent report shape"]:::problem
  mixed["one report body<br/>decisions + policy + receipts + evidence"]:::problem
  reader["reader searches<br/>for decision and next action"]:::problem
  audit["accepted audit<br/>shared spine recommended"]:::keep
  missing["no shared template<br/>no rendered prototype"]:::problem

  evidence --> producers --> mixed --> reader
  audit --> missing
  missing -. leaves recommendation unproved .-> mixed
```

Legend:

- red = current problem, missing owner, or unproved recommendation
- gray = existing evidence or accepted context that stays

## After: One template proves a decision-first report without changing live producers

The shared template owns the human reading spine while supporting proof stays
linked and canonical. One Dogfood prototype tests the boundary against real
evidence before any live skill or broad rollout changes.

```mermaid
flowchart TD
  classDef keep fill:#f8fafc,stroke:#cbd5e1,color:#334155
  classDef added fill:#ecfdf5,stroke:#10b981,color:#065f46
  classDef changed fill:#fffbeb,stroke:#f59e0b,color:#92400e

  audit["accepted 37-skill audit"]:::keep
  template["shared human-report template<br/>human_report(evidence, kind) → report + refs"]:::added
  doctrine["reporting doctrine + registry<br/>body ↔ evidence ↔ receipt"]:::changed
  source["existing Dogfood report<br/>source remains untouched"]:::keep
  prototype["ticket-local Dogfood prototype<br/>decision → map → findings → risks → action"]:::added
  receipt["canonical JSON receipt<br/>authority + mutation + validation + stop"]:::added
  comparison["comparison + deterministic checks"]:::added
  review["independent TAS-A review"]:::keep
  deferred["live adoption + 36-skill rollout<br/>explicitly deferred"]:::keep

  audit --> template --> doctrine
  source --> prototype
  source --> receipt
  template --> prototype
  prototype --> comparison
  receipt --> comparison --> review
  review -. later accepted wave .-> deferred
```

Legend:

- green = added template, prototype, receipt, or proof artifact
- amber = changed doctrine, ownership, or discoverability
- gray = accepted input, unchanged source, review, or deferred scope

## What Changed

Diagram intent: show the two bounded replacements this prototype must prove.

```mermaid
flowchart LR
  classDef before fill:#fff5f5,stroke:#dc2626,color:#991b1b
  classDef after fill:#ecfdf5,stroke:#10b981,color:#065f46
  classDef changed fill:#fffbeb,stroke:#f59e0b,color:#92400e

  oldShape["before: each producer<br/>invents report shape"]:::before
  newOwner["after: shared template<br/>owns human reading spine"]:::changed
  oldBody["before: human decisions<br/>mixed with machine receipt"]:::before
  newBody["after: concise human report<br/>links canonical receipt"]:::after
  recommendation["before: audit recommendation<br/>without rendered proof"]:::before
  proof["after: Dogfood prototype<br/>comparison + TAS-A review"]:::after

  oldShape --> newOwner
  oldBody --> newBody
  recommendation --> proof
```

Legend:

- red = current or unproved behavior being replaced
- amber = changed ownership or reporting boundary
- green = added human-readable or proof artifact

## Short Notes

- `ticket.md` remains the canonical scope and approval contract.
- The source Dogfood report and all live report-producing skills remain unchanged.
- The prototype must retain every material decision, risk, gap, next action, and
  no-execution proof across the human report or linked receipt.
- Broad rollout is a later decision; this ticket proves only the first
  representative slice.

## Feedback Guide

- Is the before diagram honest about the mixed-audience report problem?
- Is the human-body versus canonical-receipt boundary clear in the after diagram?
- Does the bounded Dogfood prototype prove the pattern without implying live rollout?
- Are the colored boxes enough to scan what changed even with the legends alone?
- Is there a scope change that must go back into `ticket.md`?
