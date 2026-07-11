---
title: Farplane-Style Code Audit Plan Example
owner: code-audit
status: example
kind: skill-example
---

# Example: Ranked Audit Plan

## Input

```text
Request: A new model came out. Audit this Farplane checkout and create the
first improvement tickets. Do not implement changes yet.
Context refs:
  - README.md
  - ARCHITECTURE.md
  - docs/features/README.md
  - tickets/README.md
  - skills/refactoring/SKILL.md
  - skills/hardening/SKILL.md
Budget: focused, ticket_limit=3
```

## Good Output Shape

```text
Target:
  codebase: Farplane checkout
  non_goals: no code rewrite; no broad modernization; no scanner install
  budget: focused, ticket_limit=3

Component Inventory:
  - tickets lifecycle: tickets/, tickets/scripts/check_ticket_metadata.py
  - skill system: skills/*/SKILL.md, docs/skills/*, registry validators
  - runtime hooks and CLI: bin/, config examples, install paths
  - proof surfaces: qa/, docs/review, evals/evals.json files

Ranked Audit Order:
  1. skill system
     priority: critical
     reason: high composition heat; every skill invocation depends on first-load
       sufficiency, reference routing, and validation.
     audit_depth: architecture
     confidence: high
  2. ticket lifecycle
     priority: high
     reason: tickets are the durable work memory and proof scoreboard.
     audit_depth: architecture
     confidence: high
  3. runtime hooks and CLI
     priority: high
     reason: install and execution paths can create high blast-radius failures.
     audit_depth: focused-module
     confidence: medium

Architecture Findings:
  - Finding: skill packages have validation and registry ownership, but new
    audit behavior lacks a dedicated skill.
    evidence: docs/skills/system.md; skills/refactoring/SKILL.md;
      skills/hardening/SKILL.md
    impact: broad codebase audit requests currently route to execution skills.
    route: impl-plan
    ticket: Create code-audit skill
    proof: skill validation plus behavior eval cases.
    residual_risk: no live audit run yet.

Ticket:
  id_or_status: proposed
  title: Run focused audit of skill-system architecture
  owner_skill: code-audit -> impl-plan
  scope_in:
    - docs/skills/system.md
    - docs/skills/best-practices.md
    - skills/skill-maintenance/scripts/check_skills.py
  scope_out:
    - no bulk skill edits
    - no validator rewrite unless evidence requires a follow-up
  done_when:
    - ranked findings have evidence, owner routes, and proof routes
    - top follow-up ticket is ready for goal-advisor
  proof:
    - python3 skills/skill-maintenance/scripts/check_skills.py --write
    - reviewer pass on audit artifact before implementation wave
  residual_risk:
    - audit may underweight runtime behavior without sample executions
  next_action:
    - Create the ticket and bind exact files before running the audit.
```

## Why This Is Good

- It ranks components by product and system importance before local file smell.
- It audits architecture before module tickets.
- It creates ticket-shaped outputs instead of patching the repo.
- It routes implementation to owner skills.
- It names residual risk and proof instead of trusting model confidence.
