---
title: "Proof And Review"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - proof-and-review
refs:
  - docs/features/FEAT-0008-artifact-first-qa-and-completion-proof.md
  - skills/qa/SKILL.md
  - skills/review/SKILL.md
  - docs/review/rubrics
system_record_json: |
  {
    "id": "SYS-0005",
    "name": "Proof And Review",
    "status": "implemented",
    "summary": "The QA, review, completion, and adversarial testing surfaces that keep Farplane work evidence-backed instead of self-certified.",
    "owner_spec": "docs/systems/proof-review.md",
    "primary_feature_ref": "FEAT-0008",
    "feature_refs": [
      "FEAT-0008",
      "FEAT-0031",
      "FEAT-0034",
      "FEAT-0043"
    ],
    "refs": [
      "docs/features/FEAT-0008-artifact-first-qa-and-completion-proof.md",
      "skills/qa/SKILL.md",
      "skills/review/SKILL.md",
      "docs/review/rubrics"
    ],
    "last_verified": "2026-06-26"
  }
---

# Proof And Review

The QA, review, completion, and adversarial testing surfaces that keep Farplane work evidence-backed instead of self-certified.

## Role

Proof and Review is the anti-self-approval layer: QA artifacts, reviewer gates, behavior tests, evals, and completion proof.

## What Belongs Here

Done/Proof obligations, QA/review routing, agent behavior tests, adversarial QA, and system-prompt regression evidence.

## What Belongs Elsewhere

Planning and execution belong to Work Loop and Horizon Loop; skill-local eval definitions belong to Skill System when the eval is package-specific.

## Feature Docs

- [FEAT-0008 Artifact-first QA and completion proof](../features/FEAT-0008-artifact-first-qa-and-completion-proof.md)
- [FEAT-0031 Agent behavior test workflow](../features/FEAT-0031-agent-behavior-test-workflow.md)
- [FEAT-0034 Adversarial agent QA test skill](../features/FEAT-0034-adversarial-agent-qa-test-skill.md)
- [FEAT-0043 Project-level system prompt eval suite](../features/FEAT-0043-project-level-system-prompt-eval-suite.md)

## Maintenance

This system page owns only the system-level contract. Feature registry rows are authored as feature pages in `docs/features/` and generated into `docs/features/registry.jsonl`.
