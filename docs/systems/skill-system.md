---
title: "Skill System"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - skill-system
refs:
  - docs/skills/README.md
  - docs/skills/system.md
  - docs/skills/templates/SKILL_TEMPLATE.md
  - skills/skill-maintenance/SKILL.md
system_record_json: |
  {
    "id": "SYS-0006",
    "name": "Skill System",
    "status": "implemented",
    "summary": "The reusable expertise layer: skill tiers, packaging, templates, evals, QA checklists, registry intelligence, and maintenance constraints.",
    "owner_spec": "docs/systems/skill-system.md",
    "primary_feature_ref": "FEAT-0022",
    "feature_refs": [
      "FEAT-0022",
      "FEAT-0024",
      "FEAT-0030",
      "FEAT-0033",
      "FEAT-0044",
      "FEAT-0047",
      "FEAT-0053",
      "FEAT-0054",
      "FEAT-0057",
      "FEAT-0058",
      "FEAT-0059",
      "FEAT-0062",
      "FEAT-0064"
    ],
    "refs": [
      "docs/skills/README.md",
      "docs/skills/system.md",
      "docs/skills/templates/SKILL_TEMPLATE.md",
      "skills/skill-maintenance/SKILL.md"
    ],
    "last_verified": "2026-06-26"
  }
capability_records_json: |
  [
    {
      "id": "FEAT-0022",
      "name": "Skill tier leverage classes",
      "status": "implemented",
      "category": "skills",
      "surfaces": [
        "templates/global/AGENTS.md",
        "docs/skills/system.md",
        "skills/plan",
        "skills/reference-grounding",
        "skills/prototyping",
        "skills/research",
        "skills/review",
        "docs/review/rubrics",
        "docs/skills/README.md",
        "bin/validators/sync_skill_registry.py",
        "bin/validators/check_skill_todo_tiers.py",
        "bin/validators/check_tier0_phase_protocol.py"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0098",
        "docs/specs/harness-techniques.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md"
      ],
      "known_limits": "Depends on skill maintainers keeping Markdown links accurate; numeric tiers describe compound upgrade priority while first-load todo links enforce loading boundaries; Tier 0 is a universal phase protocol rather than a skill tier, plan is a planning prompt-template rather than the phase itself, execute remains a deprecated compatibility wrapper, and concrete coding skills such as spec-to-ticket, impl-plan, goal-advisor, and close-ticket must not be treated as universal generic workflows.",
      "metrics": [],
      "last_verified": "2026-06-23",
      "capability_role": "primary",
      "public": true
    },
    {
      "id": "FEAT-0024",
      "name": "Skill capability sanity tests",
      "status": "partial",
      "category": "skills",
      "surfaces": [
        "bin/validators/check_skill_capabilities.py",
        "tests/notion-context/tasks_this_week.json",
        "tests/value-signals",
        "docs/specs/self-improvement-contracts.md",
        "docs/skills/README.md"
      ],
      "source_refs": [
        "docs/fundamentals/harness-engineering-doctrine.md",
        "docs/skills/README.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "bin/validators/check_skill_capabilities.py",
        "docs/skills/README.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "Capability fixtures, repair-ticket generation, and value-signal scoring exist; generated skill registry rows do not yet expose compact capability handles. Installed or external skills can be mirrored by fixtures, but self-healing must target local wrappers, registry/test metadata, or visible repair tickets unless the operator explicitly approves a specific external-skill edit.",
      "metrics": [
        "skill_capability_sanity_pass_rate",
        "repeat_skill_failure_count",
        "false_autofix_count",
        "manual_interventions_saved"
      ],
      "last_verified": "2026-05-22",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0030",
      "name": "On-demand skill plugin packaging",
      "status": "implemented",
      "category": "skills",
      "surfaces": [
        "skills/skill-maintenance/scripts/sync_skill_plugins.py",
        "skills/skill-maintenance/scripts/install_selected_skills.py",
        "install.sh",
        "README.md"
      ],
      "source_refs": [
        "skills/skill-maintenance/scripts/sync_skill_plugins.py",
        "skills/skill-maintenance/scripts/install_selected_skills.py",
        "install.sh",
        "docs/HISTORY.md"
      ],
      "external_refs": [
        "https://developers.openai.com/codex/plugins",
        "https://developers.openai.com/codex/plugins/build"
      ],
      "evidence_refs": [
        "skills/skill-maintenance/scripts/test_install_selected_skills.py",
        "skills/skill-maintenance/scripts/test_sync_skill_plugins.py",
        "docs/HISTORY.md"
      ],
      "known_limits": "Generated plugin packages are no longer tracked in source. Farplane keeps `skills/*` as the source of truth; skill-maintenance owns the implementation, and install.sh now calls the owner script directly. Official self-serve public Plugin Directory publishing, icons, screenshots, apps, MCP servers, and hooks are not included yet.",
      "metrics": [
        "selected_skill_installer_tests_pass",
        "skill_plugin_generation_pass"
      ],
      "last_verified": "2026-06-24",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0033",
      "name": "Embedded skill checklist install",
      "status": "implemented",
      "category": "skills",
      "surfaces": [
        "install.sh",
        "skills/skill-maintenance/scripts/install_selected_skills.py",
        "templates/global/AGENTS.md",
        "docs/skills/README.md"
      ],
      "source_refs": [
        "tickets/TASK-0181/ticket.md",
        "docs/MEMORY.md#MEM-0114"
      ],
      "external_refs": [],
      "evidence_refs": [
        "tickets/TASK-0181/ticket.md",
        "skills/skill-maintenance/scripts/test_install_selected_skills.py"
      ],
      "known_limits": "Rendered installed skills must be refreshed by rerunning install after source skill edits; the renderer improves first-load checklist visibility but does not persist checklist state or inspect hidden reasoning. install.sh calls skills/skill-maintenance/scripts/install_selected_skills.py directly; old top-level bin wrapper was removed in TASK-0218.",
      "metrics": [
        "rendered_skill_todo_embedding_pass"
      ],
      "last_verified": "2026-06-24",
      "capability_role": "implementation_detail",
      "public": false
    },
    {
      "id": "FEAT-0044",
      "name": "Validator-triggered hardcase capture",
      "status": "implemented",
      "category": "skills",
      "surfaces": [
        "bin/validators/check_skill_todo_tiers.py",
        "skills/skill-maintenance/scripts/check_skills.py",
        "experiments/hardcases",
        "docs/skills/README.md"
      ],
      "source_refs": [
        "docs/LESSONS.md",
        "docs/specs/filesystem-lifecycle.md",
        "docs/HISTORY.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "bin/validators/check_skill_todo_tiers.py",
        "skills/skill-maintenance/scripts/check_skills.py",
        "skills/eval/examples/farplane-global-harness/tasks.json",
        "docs/HISTORY.md"
      ],
      "known_limits": "The validator writes deduplicated hardcase artifacts only when todo-tier checks fail. It does not fix the violation or create runnable eval rows by itself.",
      "metrics": [
        "skill_todo_tier_violation_hardcase_capture_pass"
      ],
      "last_verified": "2026-06-07",
      "capability_role": "implementation_detail",
      "public": false
    },
    {
      "id": "FEAT-0047",
      "name": "Deliberative advice council workflow",
      "status": "implemented",
      "category": "skills",
      "surfaces": [
        "skills/deliberative-advice",
        "skills/advise",
        "docs/specs/context-and-handoff-policy.md",
        "templates/global/AGENTS.md",
        "agents/reviewer.toml",
        "agents/qa-tester.toml",
        "agents/planner-agent.toml",
        "docs/skills/README.md"
      ],
      "source_refs": [
        "skills/deliberative-advice/SKILL.md",
        "docs/fundamentals/harness-engineering-doctrine.md",
        "docs/specs/context-and-handoff-policy.md"
      ],
      "external_refs": [
        "https://github.com/karpathy/llm-council",
        "https://deepwiki.com/karpathy/llm-council/1-overview"
      ],
      "evidence_refs": [
        "skills/deliberative-advice/SKILL.md",
        "skills/deliberative-advice/references/llm-council-model.md",
        "skills/deliberative-advice/eval_task.json"
      ],
      "known_limits": "Skill-contract workflow only; actual independent perspective collection depends on the invoking agent and available native subagent or lane tooling. Council mode now requires a durable context packet when prior discussion, options, evidence, or constraints matter, but it is still prompt-and-eval enforced rather than a hidden daemon, majority-vote system, or automatic multi-model router.",
      "metrics": [
        "deliberative_advice_skill_validation_pass",
        "council_context_packet_pass"
      ],
      "last_verified": "2026-06-13",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0053",
      "name": "Skill behavior gap analysis interface",
      "status": "implemented",
      "category": "skills",
      "surfaces": [
        "skills/gap-analysis",
        "docs/skills/README.md",
        "docs/skills/registry.jsonl"
      ],
      "source_refs": [
        "docs/skills/system.md",
        "docs/HISTORY.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "skills/gap-analysis/SKILL.md",
        "docs/skills/README.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "Diagnostic skill contract only; it produces grounded gap reports and owner recommendations, but the actual remediation still requires the target skill edit, eval addition, self-improvement loop, harness-advisor placement pass, or deliberative advice when the remediation choice is high-stakes.",
      "metrics": [
        "skill_gap_report_usefulness"
      ],
      "last_verified": "2026-06-10",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0054",
      "name": "Modular skill-local eval tasks",
      "status": "implemented",
      "category": "skills",
      "surfaces": [
        "skills/eval/scripts/run_evals.py",
        "skills/eval/SKILL.md",
        "skills/eval/eval_task.json",
        "docs/skills/templates/SKILL_TEMPLATE.md",
        "docs/skills/system.md",
        "docs/skills/best-practices.md"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0145",
        "docs/HISTORY.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "skills/eval/eval_task.json",
        "skills/eval/tests/test_run_evals.py",
        "docs/HISTORY.md"
      ],
      "known_limits": "The runner discovers `skills/*/eval_task.json` as a modular suite, but it does not yet enforce every skill having one or validate skill-local eval coverage quality beyond the existing task JSON schema and judge prompts.",
      "metrics": [
        "skill_local_eval_discovery_pass"
      ],
      "last_verified": "2026-06-11",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0057",
      "name": "Skill-local QA checklist artifacts",
      "status": "implemented",
      "category": "skills",
      "surfaces": [
        "skills/skill-maintenance/qa_checklist.md",
        "skills/skill-maintenance",
        "skills/skill-creator",
        "docs/skills/system.md",
        "docs/skills/best-practices.md",
        "docs/skills/README.md"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0150",
        "docs/fundamentals/harness-algebra.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "skills/skill-maintenance/qa_checklist.md",
        "skills/skill-maintenance/audits/2026-06-23-qa-checklist-preflight-review.md"
      ],
      "known_limits": "Markdown artifact standard only; no dedicated qacheck runner, renderer, or subagent fanout script exists yet. Agents now read skill-local checklists as preflight guardrails, apply them again at finish, and route independent reviewer lanes for material checklist conformance through skill-maintenance, skill-creator, and recorded audit/proof notes.",
      "metrics": [
        "skill_qa_checklist_application_pass"
      ],
      "last_verified": "2026-06-23",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0058",
      "name": "Skill template intelligence artifact",
      "status": "implemented",
      "category": "skills",
      "surfaces": [
        "skills/skill-maintenance/scripts/generate_template_intelligence.py",
        "skills/skill-maintenance/graph/skill-template-intelligence.json",
        "skills/skill-maintenance/templates/archive",
        "docs/skills/templates/SKILL_TEMPLATE.md"
      ],
      "source_refs": [
        "tickets/archive/TASK-0202/ticket.md",
        "docs/skills/system.md",
        "docs/skills/README.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "tickets/archive/TASK-0202/ticket.md",
        "skills/skill-maintenance/scripts/test_generate_template_intelligence.py"
      ],
      "known_limits": "Template evals are representative heuristic research signals, not universal skill quality rankings; UI consumers must preserve the caveat and Farplane remains the source of truth.",
      "metrics": [
        "skill_template_rollout_visibility",
        "skill_template_eval_signal_pass"
      ],
      "last_verified": "2026-06-14",
      "capability_role": "implementation_detail",
      "public": false
    },
    {
      "id": "FEAT-0059",
      "name": "Template-owned skill feature metadata",
      "status": "implemented",
      "category": "skills",
      "surfaces": [
        "docs/skills/templates/SKILL_TEMPLATE.md",
        "skills/skill-maintenance/scripts/migrate_skill_surfaces.py",
        "bin/validators/sync_skill_registry.py",
        "skills/skill-maintenance/scripts/generate_template_intelligence.py",
        "docs/skills/system.md",
        "docs/skills/README.md"
      ],
      "source_refs": [
        "docs/skills/system.md",
        "docs/skills/README.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "bin/validators/test_sync_skill_registry.py",
        "skills/skill-maintenance/scripts/test_generate_template_intelligence.py"
      ],
      "known_limits": "Template-level feature metadata is authoritative for structural template features; skill rows declare only local eval, QA checklist, and skill UI surfaces. Existing skills are not automatically marked current for a new template version unless their structure is verified.",
      "metrics": [
        "skill_surface_metadata_coverage",
        "template_feature_inference_pass"
      ],
      "last_verified": "2026-06-15",
      "capability_role": "implementation_detail",
      "public": false
    },
    {
      "id": "FEAT-0062",
      "name": "Budget-aware refactoring and hardening workflows",
      "status": "implemented",
      "category": "skills",
      "surfaces": [
        "skills/refactoring",
        "skills/hardening",
        "skills/init-advisor/references/PROJECT_RULES_TEMPLATE.md",
        "docs/skills/registry.jsonl"
      ],
      "source_refs": [
        "tickets/TASK-0224/ticket.md"
      ],
      "external_refs": [
        "https://docs.sonarsource.com/sonarqube-server/user-guide/code-metrics/metrics-definition",
        "https://eslint.org/docs/latest/rules/max-lines-per-function",
        "https://github.com/semgrep/semgrep",
        "https://martinfowler.com/articles/workflowsOfRefactoring/fallback.html",
        "https://csrc.nist.gov/projects/ssdf",
        "https://owasp.org/www-project-application-security-verification-standard/"
      ],
      "evidence_refs": [
        "skills/refactoring/SKILL.md",
        "skills/hardening/SKILL.md",
        "skills/refactoring/eval_task.json",
        "skills/hardening/eval_task.json",
        "tickets/TASK-0224/progress.md"
      ],
      "known_limits": "Reference-driven workflows and eval rows only; no analyzer aggregation script or automatic project tool installation exists yet. Stack-specific tooling remains optional and must be adopted by each project through PROJECT_RULES or a setup ticket.",
      "metrics": [
        "skill_registry_validation_pass",
        "skill_eval_query_lint_pass",
        "quality_tooling_slots_present"
      ],
      "last_verified": "2026-06-25",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0064",
      "name": "Skill compounding score",
      "status": "implemented",
      "category": "skills",
      "surfaces": [
        "docs/specs/skill-compounding-score.md",
        "docs/skills/system.md",
        "skills/taste-loop",
        "farplane/automations.md",
        "docs/skills/registry.jsonl"
      ],
      "source_refs": [
        "docs/farplane-framework/lifecycle.md",
        "docs/skills/system.md",
        "farplane/products.md",
        "skills/skill-maintenance/graph/README.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "skills/taste-loop/SKILL.md",
        "skills/taste-loop/templates/heartbeat-prompt.md",
        "skills/taste-loop/eval_task.json"
      ],
      "known_limits": "Official ranking contract only; the current implementation is prompt-consumed by Taste Loop and generated graph data. No standalone scorer, UI renderer, hidden scheduler, or automatic skill mutation is shipped.",
      "metrics": [
        "skill_compounding_score_traceability_pass",
        "taste_loop_score_breakdown_pass",
        "skill_registry_validation_pass"
      ],
      "last_verified": "2026-06-26",
      "capability_role": "subcapability",
      "public": false
    }
  ]
---

# Skill System

The reusable expertise layer: skill tiers, packaging, templates, evals, QA checklists, registry intelligence, and maintenance constraints.

## Role

This system spec is the authored source for one public Farplane system and its internal capability handles. The generated registries expose the same data as `docs/systems/registry.jsonl` and `docs/features/registry.jsonl`.

## Public Capability

- `FEAT-0022` - Skill tier leverage classes

## Capability Handles

- `FEAT-0022` `primary` - Skill tier leverage classes
- `FEAT-0024` `subcapability` - Skill capability sanity tests
- `FEAT-0030` `subcapability` - On-demand skill plugin packaging
- `FEAT-0033` `implementation_detail` - Embedded skill checklist install
- `FEAT-0044` `implementation_detail` - Validator-triggered hardcase capture
- `FEAT-0047` `subcapability` - Deliberative advice council workflow
- `FEAT-0053` `subcapability` - Skill behavior gap analysis interface
- `FEAT-0054` `subcapability` - Modular skill-local eval tasks
- `FEAT-0057` `subcapability` - Skill-local QA checklist artifacts
- `FEAT-0058` `implementation_detail` - Skill template intelligence artifact
- `FEAT-0059` `implementation_detail` - Template-owned skill feature metadata
- `FEAT-0062` `subcapability` - Budget-aware refactoring and hardening workflows
- `FEAT-0064` `subcapability` - Skill compounding score

## Maintenance Notes

- Edit the `system_record_json` and `capability_records_json` blocks in this file, then run `python3 docs/features/validate_features.py --write`.
- Keep public docs focused on the system and primary capability; use subcapability rows for compatibility, dedupe, rollout, and evidence tracking.
