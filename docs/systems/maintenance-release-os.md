---
title: "Maintenance And Release OS"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - maintenance-release-os
refs:
  - docs/specs/doc-governance.md
  - docs/specs/filesystem-lifecycle.md
  - docs/farplane-framework/harness-maintenance.md
  - docs/templates/registry.jsonl
system_record_json: |
  {
    "id": "SYS-0009",
    "name": "Maintenance And Release OS",
    "status": "implemented",
    "summary": "The registries, lifecycle rules, manifests, rollout checks, adoption scans, and docs validators that keep Farplane coherent as it evolves.",
    "owner_spec": "docs/systems/maintenance-release-os.md",
    "primary_feature_ref": "FEAT-0060",
    "feature_refs": [
      "FEAT-0060",
      "FEAT-0041",
      "FEAT-0049",
      "FEAT-0055",
      "FEAT-0061"
    ],
    "refs": [
      "docs/specs/doc-governance.md",
      "docs/specs/filesystem-lifecycle.md",
      "docs/farplane-framework/harness-maintenance.md",
      "docs/templates/registry.jsonl"
    ],
    "last_verified": "2026-06-26"
  }
capability_records_json: |
  [
    {
      "id": "FEAT-0060",
      "name": "High-impact template feature registry",
      "status": "implemented",
      "category": "context-routing",
      "surfaces": [
        "docs/templates/registry.jsonl",
        "docs/templates/README.md",
        "rules/template-registry.toml",
        "rules/template-version-watch.toml",
        "bin/validators/sync_template_registry.py",
        "templates/global/AGENTS.md",
        "docs/skills/templates/SKILL_TEMPLATE.md",
        "docs/skills/templates/METHOD_REFERENCE_TEMPLATE.md",
        "tickets/templates/ticket.md",
        "tickets/templates/goal-loop/program.md",
        "skills/harness-creator/templates/project-harness.md"
      ],
      "source_refs": [
        "docs/features/registry.jsonl",
        "rules/template-registry.toml"
      ],
      "external_refs": [],
      "evidence_refs": [
        "bin/validators/test_sync_template_registry.py"
      ],
      "known_limits": "Tracks high-impact prompt-shaped templates and the docs-owned skill/method template standards. Broader documentation versioning and low-impact scaffold templates are intentionally deferred until they have a clear consumer.",
      "metrics": [
        "template_feature_registry_validation_pass"
      ],
      "last_verified": "2026-06-24",
      "capability_role": "primary",
      "public": true
    },
    {
      "id": "FEAT-0041",
      "name": "Filesystem lifecycle and drain routing",
      "status": "implemented",
      "category": "memory",
      "surfaces": [
        "docs/specs/filesystem-lifecycle.md",
        "ARCHITECTURE.md",
        "docs/specs/harness-techniques.md"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0136",
        "docs/specs/filesystem-lifecycle.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md"
      ],
      "known_limits": "Router contract only; owner docs still define detailed local rules and agents must not treat experiments as canonical memory.",
      "metrics": [],
      "last_verified": "2026-06-06",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0049",
      "name": "Artifact-first Markdown front matter standard",
      "status": "implemented",
      "category": "memory",
      "surfaces": [
        "templates/global/AGENTS.md",
        "docs/specs/filesystem-lifecycle.md",
        "docs/MEMORY.md"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0137",
        "docs/specs/filesystem-lifecycle.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "templates/global/AGENTS.md",
        "docs/specs/filesystem-lifecycle.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "Prompt-and-spec standard only; no validator currently enforces front matter on every new Markdown artifact, and existing Markdown files are not retrofitted by default.",
      "metrics": [],
      "last_verified": "2026-06-09",
      "capability_role": "implementation_detail",
      "public": false
    },
    {
      "id": "FEAT-0055",
      "name": "Mechanical local reference checks",
      "status": "implemented",
      "category": "proof",
      "surfaces": [
        "bin/validators/check_doc_refs.py",
        "bin/validators/test_check_doc_refs.py",
        "skills/skill-maintenance/scripts/check_skills.py",
        "docs/specs/harness-techniques.md"
      ],
      "source_refs": [
        "docs/specs/filesystem-lifecycle.md",
        "docs/specs/doc-governance.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "bin/validators/check_doc_refs.py",
        "bin/validators/test_check_doc_refs.py"
      ],
      "known_limits": "Default validation scans active docs, registries, and root entrypoints to avoid noisy examples, tests, tickets, and historical artifacts. Use `python3 bin/validators/check_doc_refs.py --all` for broader cleanup audits that may require triage.",
      "metrics": [
        "local_doc_ref_validation_pass"
      ],
      "last_verified": "2026-06-12",
      "capability_role": "implementation_detail",
      "public": false
    },
    {
      "id": "FEAT-0061",
      "name": "Farplane adoption tracker CLI",
      "status": "implemented",
      "category": "proof",
      "surfaces": [
        "bin/farplane.py#adoption scan",
        "bin/core/farplane_adoption.py",
        "bin/tests/test_farplane_adoption.py",
        "docs/features/registry.jsonl"
      ],
      "source_refs": [
        "experiments/decisions/2026-06-24-project-harness-rollout-feature/decision.md",
        "tickets/TASK-0216/ticket.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "bin/tests/test_farplane_adoption.py"
      ],
      "known_limits": "Local CLI resolver only. It reads explicit project roots, roots files, or known ~/.farplane state files; it does not crawl the whole computer, mutate project manifests, or render Office UI directly.",
      "metrics": [
        "farplane_adoption_scan_pass",
        "feature_adoption_drift_count"
      ],
      "last_verified": "2026-06-24",
      "capability_role": "subcapability",
      "public": false
    }
  ]
---

# Maintenance And Release OS

The registries, lifecycle rules, manifests, rollout checks, adoption scans, and docs validators that keep Farplane coherent as it evolves.

## Role

This system spec is the authored source for one public Farplane system and its internal capability handles. The generated registries expose the same data as `docs/systems/registry.jsonl` and `docs/features/registry.jsonl`.

## Public Capability

- `FEAT-0060` - High-impact template feature registry

## Capability Handles

- `FEAT-0060` `primary` - High-impact template feature registry
- `FEAT-0041` `subcapability` - Filesystem lifecycle and drain routing
- `FEAT-0049` `implementation_detail` - Artifact-first Markdown front matter standard
- `FEAT-0055` `implementation_detail` - Mechanical local reference checks
- `FEAT-0061` `subcapability` - Farplane adoption tracker CLI

## Maintenance Notes

- Edit the `system_record_json` and `capability_records_json` blocks in this file, then run `python3 docs/features/validate_features.py --write`.
- Keep public docs focused on the system and primary capability; use subcapability rows for compatibility, dedupe, rollout, and evidence tracking.
