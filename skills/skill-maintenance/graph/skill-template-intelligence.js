window.SKILL_TEMPLATE_INTELLIGENCE = {
  "caveats": [
    "Template evals are hidden research signals until real eval-run artifacts can be joined to template release windows.",
    "Git mining is a recovery path; future template changes should archive snapshots at change time.",
    "Skill-applicable capabilities remain owned by docs/systems/skill-system.md metadata; generated system and feature registries are output.",
    "Template-level features are declared by the versioned skill template; skill rows expose local eval, QA checklist, and UI surfaces."
  ],
  "current_template_version": "0.3.2",
  "epochs": [
    {
      "changed_sections": [
        "Context",
        "Gotchas",
        "Output",
        "Phase Boundary",
        "Phase Contract",
        "Reference Map",
        "Skill Signature",
        "Templates",
        "Todo List"
      ],
      "introduced_at": "2026-06-24",
      "section_count": 9,
      "sections": [
        "Context",
        "Skill Signature",
        "Phase Contract",
        "Phase Boundary",
        "Todo List",
        "Templates",
        "Gotchas",
        "Reference Map",
        "Output"
      ],
      "snapshot_path": "skills/skill-maintenance/templates/archive/skill-template-0.3.2-a55523040aca.md",
      "source_commit": "a55523040aca",
      "summary": "chore(skills): upgrade skill creator workflows",
      "version": "0.3.2"
    },
    {
      "changed_sections": [],
      "introduced_at": "2026-06-24",
      "section_count": 9,
      "sections": [
        "Context",
        "Skill Signature",
        "Phase Contract",
        "Phase Boundary",
        "Todo List",
        "Templates",
        "Gotchas",
        "Reference Map",
        "Output"
      ],
      "snapshot_path": "skills/skill-maintenance/templates/archive/skill-template-0.3.3-b8f67d0311ce.md",
      "source_commit": "b8f67d0311ce",
      "summary": "Introduce proof advisor workflow inference",
      "version": "0.3.3"
    },
    {
      "changed_sections": [],
      "introduced_at": "2026-06-26",
      "section_count": 9,
      "sections": [
        "Context",
        "Skill Signature",
        "Phase Contract",
        "Phase Boundary",
        "Todo List",
        "Templates",
        "Gotchas",
        "Reference Map",
        "Output"
      ],
      "snapshot_path": "skills/skill-maintenance/templates/archive/skill-template-0.3.3-d8abb67693a6.md",
      "source_commit": "d8abb67693a6",
      "summary": "working tree current template",
      "version": "0.3.3"
    }
  ],
  "eval_definitions": [
    {
      "behavior": "routing",
      "expected_signals": [
        "description uses verb/input/output/call-condition guidance",
        "trigger catalogs stay out of frontmatter"
      ],
      "id": "routing_clarity",
      "title": "Routing clarity"
    },
    {
      "behavior": "todo_executability",
      "expected_signals": [
        "top-level todos use visible numbered checkbox actions",
        "policy prose is not treated as a top-level todo"
      ],
      "id": "todo_executability",
      "title": "Todo executability"
    },
    {
      "behavior": "phase_boundary",
      "expected_signals": [
        "phase-like skills are externalized only when their artifact is needed",
        "same-scope recursion is forbidden"
      ],
      "id": "phase_boundary",
      "title": "Phase boundary"
    },
    {
      "behavior": "proof_contract",
      "expected_signals": [
        "the finish gate names proof, blockers, or evidence",
        "output contract is explicit"
      ],
      "id": "proof_contract",
      "title": "Proof contract"
    },
    {
      "behavior": "eval_qa_sync",
      "expected_signals": [
        "eval_task.json is a first-class special file",
        "qa_checklist.md is a repeatable runtime guardrail only when warranted"
      ],
      "id": "eval_qa_sync",
      "title": "Eval / QA sync"
    }
  ],
  "evals": [
    {
      "behavior": "routing",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "routing_clarity",
      "expected_signals": [
        "description uses verb/input/output/call-condition guidance",
        "trigger catalogs stay out of frontmatter"
      ],
      "missing_signals": [],
      "source_commit": "a55523040aca",
      "template_version": "0.3.2",
      "title": "Routing clarity",
      "verdict": "pass"
    },
    {
      "behavior": "todo_executability",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "todo_executability",
      "expected_signals": [
        "top-level todos use visible numbered checkbox actions",
        "policy prose is not treated as a top-level todo"
      ],
      "missing_signals": [],
      "source_commit": "a55523040aca",
      "template_version": "0.3.2",
      "title": "Todo executability",
      "verdict": "pass"
    },
    {
      "behavior": "phase_boundary",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "phase_boundary",
      "expected_signals": [
        "phase-like skills are externalized only when their artifact is needed",
        "same-scope recursion is forbidden"
      ],
      "missing_signals": [],
      "source_commit": "a55523040aca",
      "template_version": "0.3.2",
      "title": "Phase boundary",
      "verdict": "pass"
    },
    {
      "behavior": "proof_contract",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "proof_contract",
      "expected_signals": [
        "the finish gate names proof, blockers, or evidence",
        "output contract is explicit"
      ],
      "missing_signals": [],
      "source_commit": "a55523040aca",
      "template_version": "0.3.2",
      "title": "Proof contract",
      "verdict": "pass"
    },
    {
      "behavior": "eval_qa_sync",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "eval_qa_sync",
      "expected_signals": [
        "eval_task.json is a first-class special file",
        "qa_checklist.md is a repeatable runtime guardrail only when warranted"
      ],
      "missing_signals": [],
      "source_commit": "a55523040aca",
      "template_version": "0.3.2",
      "title": "Eval / QA sync",
      "verdict": "pass"
    },
    {
      "behavior": "routing",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "routing_clarity",
      "expected_signals": [
        "description uses verb/input/output/call-condition guidance",
        "trigger catalogs stay out of frontmatter"
      ],
      "missing_signals": [],
      "source_commit": "b8f67d0311ce",
      "template_version": "0.3.3",
      "title": "Routing clarity",
      "verdict": "pass"
    },
    {
      "behavior": "todo_executability",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "todo_executability",
      "expected_signals": [
        "top-level todos use visible numbered checkbox actions",
        "policy prose is not treated as a top-level todo"
      ],
      "missing_signals": [],
      "source_commit": "b8f67d0311ce",
      "template_version": "0.3.3",
      "title": "Todo executability",
      "verdict": "pass"
    },
    {
      "behavior": "phase_boundary",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "phase_boundary",
      "expected_signals": [
        "phase-like skills are externalized only when their artifact is needed",
        "same-scope recursion is forbidden"
      ],
      "missing_signals": [],
      "source_commit": "b8f67d0311ce",
      "template_version": "0.3.3",
      "title": "Phase boundary",
      "verdict": "pass"
    },
    {
      "behavior": "proof_contract",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "proof_contract",
      "expected_signals": [
        "the finish gate names proof, blockers, or evidence",
        "output contract is explicit"
      ],
      "missing_signals": [],
      "source_commit": "b8f67d0311ce",
      "template_version": "0.3.3",
      "title": "Proof contract",
      "verdict": "pass"
    },
    {
      "behavior": "eval_qa_sync",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "eval_qa_sync",
      "expected_signals": [
        "eval_task.json is a first-class special file",
        "qa_checklist.md is a repeatable runtime guardrail only when warranted"
      ],
      "missing_signals": [],
      "source_commit": "b8f67d0311ce",
      "template_version": "0.3.3",
      "title": "Eval / QA sync",
      "verdict": "pass"
    },
    {
      "behavior": "routing",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "routing_clarity",
      "expected_signals": [
        "description uses verb/input/output/call-condition guidance",
        "trigger catalogs stay out of frontmatter"
      ],
      "missing_signals": [],
      "source_commit": "d8abb67693a6",
      "template_version": "0.3.3",
      "title": "Routing clarity",
      "verdict": "pass"
    },
    {
      "behavior": "todo_executability",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "todo_executability",
      "expected_signals": [
        "top-level todos use visible numbered checkbox actions",
        "policy prose is not treated as a top-level todo"
      ],
      "missing_signals": [],
      "source_commit": "d8abb67693a6",
      "template_version": "0.3.3",
      "title": "Todo executability",
      "verdict": "pass"
    },
    {
      "behavior": "phase_boundary",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "phase_boundary",
      "expected_signals": [
        "phase-like skills are externalized only when their artifact is needed",
        "same-scope recursion is forbidden"
      ],
      "missing_signals": [],
      "source_commit": "d8abb67693a6",
      "template_version": "0.3.3",
      "title": "Phase boundary",
      "verdict": "pass"
    },
    {
      "behavior": "proof_contract",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "proof_contract",
      "expected_signals": [
        "the finish gate names proof, blockers, or evidence",
        "output contract is explicit"
      ],
      "missing_signals": [],
      "source_commit": "d8abb67693a6",
      "template_version": "0.3.3",
      "title": "Proof contract",
      "verdict": "pass"
    },
    {
      "behavior": "eval_qa_sync",
      "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
      "eval_id": "eval_qa_sync",
      "expected_signals": [
        "eval_task.json is a first-class special file",
        "qa_checklist.md is a repeatable runtime guardrail only when warranted"
      ],
      "missing_signals": [],
      "source_commit": "d8abb67693a6",
      "template_version": "0.3.3",
      "title": "Eval / QA sync",
      "verdict": "pass"
    }
  ],
  "features": [
    {
      "evidence_refs": [
        "docs/HISTORY.md"
      ],
      "id": "FEAT-0022",
      "known_limits": "Depends on skill maintainers keeping Markdown links accurate; numeric tiers describe compound upgrade priority while first-load todo links enforce loading boundaries; Tier 0 is a universal phase protocol rather than a skill tier, plan is a planning prompt-template rather than the phase itself, execute remains a deprecated compatibility wrapper, and concrete coding skills such as spec-to-ticket, impl-plan, goal-advisor, and close-ticket must not be treated as universal generic workflows.",
      "last_verified": "2026-06-23",
      "metrics": [],
      "name": "Skill tier leverage classes",
      "status": "implemented",
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
      ]
    },
    {
      "evidence_refs": [
        "bin/validators/check_skill_capabilities.py",
        "docs/skills/README.md",
        "docs/HISTORY.md"
      ],
      "id": "FEAT-0024",
      "known_limits": "Capability fixtures, repair-ticket generation, and value-signal scoring exist; generated skill registry rows do not yet expose compact capability handles. Installed or external skills can be mirrored by fixtures, but self-healing must target local wrappers, registry/test metadata, or visible repair tickets unless the operator explicitly approves a specific external-skill edit.",
      "last_verified": "2026-05-22",
      "metrics": [
        "skill_capability_sanity_pass_rate",
        "repeat_skill_failure_count",
        "false_autofix_count",
        "manual_interventions_saved"
      ],
      "name": "Skill capability sanity tests",
      "status": "partial",
      "surfaces": [
        "bin/validators/check_skill_capabilities.py",
        "tests/notion-context/tasks_this_week.json",
        "tests/value-signals",
        "docs/specs/self-improvement-contracts.md",
        "docs/skills/README.md"
      ]
    },
    {
      "evidence_refs": [
        "skills/skill-maintenance/scripts/test_install_selected_skills.py",
        "skills/skill-maintenance/scripts/test_sync_skill_plugins.py",
        "docs/HISTORY.md"
      ],
      "id": "FEAT-0030",
      "known_limits": "Generated plugin packages are no longer tracked in source. Farplane keeps `skills/*` as the source of truth; skill-maintenance owns the implementation, and install.sh now calls the owner script directly. Official self-serve public Plugin Directory publishing, icons, screenshots, apps, MCP servers, and hooks are not included yet.",
      "last_verified": "2026-06-24",
      "metrics": [
        "selected_skill_installer_tests_pass",
        "skill_plugin_generation_pass"
      ],
      "name": "On-demand skill plugin packaging",
      "status": "implemented",
      "surfaces": [
        "skills/skill-maintenance/scripts/sync_skill_plugins.py",
        "skills/skill-maintenance/scripts/install_selected_skills.py",
        "install.sh",
        "README.md"
      ]
    },
    {
      "evidence_refs": [
        "tickets/TASK-0181/ticket.md",
        "skills/skill-maintenance/scripts/test_install_selected_skills.py"
      ],
      "id": "FEAT-0033",
      "known_limits": "Rendered installed skills must be refreshed by rerunning install after source skill edits; the renderer improves first-load checklist visibility but does not persist checklist state or inspect hidden reasoning. install.sh calls skills/skill-maintenance/scripts/install_selected_skills.py directly; old top-level bin wrapper was removed in TASK-0218.",
      "last_verified": "2026-06-24",
      "metrics": [
        "rendered_skill_todo_embedding_pass"
      ],
      "name": "Embedded skill checklist install",
      "status": "implemented",
      "surfaces": [
        "install.sh",
        "skills/skill-maintenance/scripts/install_selected_skills.py",
        "templates/global/AGENTS.md",
        "docs/skills/README.md"
      ]
    },
    {
      "evidence_refs": [
        "bin/validators/check_skill_todo_tiers.py",
        "skills/skill-maintenance/scripts/check_skills.py",
        "skills/eval/examples/farplane-global-harness/tasks.json",
        "docs/HISTORY.md"
      ],
      "id": "FEAT-0044",
      "known_limits": "The validator writes deduplicated hardcase artifacts only when todo-tier checks fail. It does not fix the violation or create runnable eval rows by itself.",
      "last_verified": "2026-06-07",
      "metrics": [
        "skill_todo_tier_violation_hardcase_capture_pass"
      ],
      "name": "Validator-triggered hardcase capture",
      "status": "implemented",
      "surfaces": [
        "bin/validators/check_skill_todo_tiers.py",
        "skills/skill-maintenance/scripts/check_skills.py",
        "experiments/hardcases",
        "docs/skills/README.md"
      ]
    },
    {
      "evidence_refs": [
        "skills/deliberative-advice/SKILL.md",
        "skills/deliberative-advice/references/llm-council-model.md",
        "skills/deliberative-advice/eval_task.json"
      ],
      "id": "FEAT-0047",
      "known_limits": "Skill-contract workflow only; actual independent perspective collection depends on the invoking agent and available native subagent or lane tooling. Council mode now requires a durable context packet when prior discussion, options, evidence, or constraints matter, but it is still prompt-and-eval enforced rather than a hidden daemon, majority-vote system, or automatic multi-model router.",
      "last_verified": "2026-06-13",
      "metrics": [
        "deliberative_advice_skill_validation_pass",
        "council_context_packet_pass"
      ],
      "name": "Deliberative advice council workflow",
      "status": "implemented",
      "surfaces": [
        "skills/deliberative-advice",
        "skills/advise",
        "docs/specs/context-and-handoff-policy.md",
        "templates/global/AGENTS.md",
        "agents/reviewer.toml",
        "agents/qa-tester.toml",
        "agents/planner-agent.toml",
        "docs/skills/README.md"
      ]
    },
    {
      "evidence_refs": [
        "skills/gap-analysis/SKILL.md",
        "docs/skills/README.md",
        "docs/HISTORY.md"
      ],
      "id": "FEAT-0053",
      "known_limits": "Diagnostic skill contract only; it produces grounded gap reports and owner recommendations, but the actual remediation still requires the target skill edit, eval addition, self-improvement loop, harness-advisor placement pass, or deliberative advice when the remediation choice is high-stakes.",
      "last_verified": "2026-06-10",
      "metrics": [
        "skill_gap_report_usefulness"
      ],
      "name": "Skill behavior gap analysis interface",
      "status": "implemented",
      "surfaces": [
        "skills/gap-analysis",
        "docs/skills/README.md",
        "docs/skills/registry.jsonl"
      ]
    },
    {
      "evidence_refs": [
        "skills/eval/eval_task.json",
        "skills/eval/tests/test_run_evals.py",
        "docs/HISTORY.md"
      ],
      "id": "FEAT-0054",
      "known_limits": "The runner discovers `skills/*/eval_task.json` as a modular suite, but it does not yet enforce every skill having one or validate skill-local eval coverage quality beyond the existing task JSON schema and judge prompts.",
      "last_verified": "2026-06-11",
      "metrics": [
        "skill_local_eval_discovery_pass"
      ],
      "name": "Modular skill-local eval tasks",
      "status": "implemented",
      "surfaces": [
        "skills/eval/scripts/run_evals.py",
        "skills/eval/SKILL.md",
        "skills/eval/eval_task.json",
        "docs/skills/templates/SKILL_TEMPLATE.md",
        "docs/skills/system.md",
        "docs/skills/best-practices.md"
      ]
    },
    {
      "evidence_refs": [
        "skills/skill-maintenance/qa_checklist.md",
        "skills/skill-maintenance/audits/2026-06-23-qa-checklist-preflight-review.md"
      ],
      "id": "FEAT-0057",
      "known_limits": "Markdown artifact standard only; no dedicated qacheck runner, renderer, or subagent fanout script exists yet. Agents now read skill-local checklists as preflight guardrails, apply them again at finish, and route independent reviewer lanes for material checklist conformance through skill-maintenance, skill-creator, and recorded audit/proof notes.",
      "last_verified": "2026-06-23",
      "metrics": [
        "skill_qa_checklist_application_pass"
      ],
      "name": "Skill-local QA checklist artifacts",
      "status": "implemented",
      "surfaces": [
        "skills/skill-maintenance/qa_checklist.md",
        "skills/skill-maintenance",
        "skills/skill-creator",
        "docs/skills/system.md",
        "docs/skills/best-practices.md",
        "docs/skills/README.md"
      ]
    },
    {
      "evidence_refs": [
        "tickets/archive/TASK-0202/ticket.md",
        "skills/skill-maintenance/scripts/test_generate_template_intelligence.py"
      ],
      "id": "FEAT-0058",
      "known_limits": "Template evals are representative heuristic research signals, not universal skill quality rankings; UI consumers must preserve the caveat and Farplane remains the source of truth.",
      "last_verified": "2026-06-14",
      "metrics": [
        "skill_template_rollout_visibility",
        "skill_template_eval_signal_pass"
      ],
      "name": "Skill template intelligence artifact",
      "status": "implemented",
      "surfaces": [
        "skills/skill-maintenance/scripts/generate_template_intelligence.py",
        "skills/skill-maintenance/graph/skill-template-intelligence.json",
        "skills/skill-maintenance/templates/archive",
        "docs/skills/templates/SKILL_TEMPLATE.md"
      ]
    },
    {
      "evidence_refs": [
        "bin/validators/test_sync_skill_registry.py",
        "skills/skill-maintenance/scripts/test_generate_template_intelligence.py"
      ],
      "id": "FEAT-0059",
      "known_limits": "Template-level feature metadata is authoritative for structural template features; skill rows declare only local eval, QA checklist, and skill UI surfaces. Existing skills are not automatically marked current for a new template version unless their structure is verified.",
      "last_verified": "2026-06-15",
      "metrics": [
        "skill_surface_metadata_coverage",
        "template_feature_inference_pass"
      ],
      "name": "Template-owned skill feature metadata",
      "status": "implemented",
      "surfaces": [
        "docs/skills/templates/SKILL_TEMPLATE.md",
        "skills/skill-maintenance/scripts/migrate_skill_surfaces.py",
        "bin/validators/sync_skill_registry.py",
        "skills/skill-maintenance/scripts/generate_template_intelligence.py",
        "docs/skills/system.md",
        "docs/skills/README.md"
      ]
    },
    {
      "evidence_refs": [
        "skills/refactoring/SKILL.md",
        "skills/hardening/SKILL.md",
        "skills/refactoring/eval_task.json",
        "skills/hardening/eval_task.json",
        "tickets/TASK-0224/progress.md"
      ],
      "id": "FEAT-0062",
      "known_limits": "Reference-driven workflows and eval rows only; no analyzer aggregation script or automatic project tool installation exists yet. Stack-specific tooling remains optional and must be adopted by each project through PROJECT_RULES or a setup ticket.",
      "last_verified": "2026-06-25",
      "metrics": [
        "skill_registry_validation_pass",
        "skill_eval_query_lint_pass",
        "quality_tooling_slots_present"
      ],
      "name": "Budget-aware refactoring and hardening workflows",
      "status": "implemented",
      "surfaces": [
        "skills/refactoring",
        "skills/hardening",
        "skills/init-advisor/references/PROJECT_RULES_TEMPLATE.md",
        "docs/skills/registry.jsonl"
      ]
    },
    {
      "evidence_refs": [
        "skills/metric-advisor/SKILL.md",
        "skills/metric-advisor/eval_task.json",
        "tickets/TASK-0228/ticket.md"
      ],
      "id": "FEAT-0063",
      "known_limits": "Advisory metric-card contract only; callers still own execution, proof, review, and writeback. It must preserve qualitative `none mechanical` cases instead of forcing fake scores.",
      "last_verified": "2026-06-26",
      "metrics": [
        "metric_card_traceability_pass",
        "skill_eval_query_lint_pass"
      ],
      "name": "Metric advisor cards",
      "status": "implemented",
      "surfaces": [
        "skills/metric-advisor",
        "docs/skills/README.md",
        "docs/specs/self-improvement-contracts.md",
        "docs/specs/review-gates.md"
      ]
    },
    {
      "evidence_refs": [
        "skills/taste-loop/SKILL.md",
        "skills/taste-loop/templates/heartbeat-prompt.md",
        "skills/taste-loop/eval_task.json"
      ],
      "id": "FEAT-0064",
      "known_limits": "Official ranking contract only; the current implementation is prompt-consumed by Taste Loop and generated graph data. No standalone scorer, UI renderer, hidden scheduler, or automatic skill mutation is shipped.",
      "last_verified": "2026-06-26",
      "metrics": [
        "skill_compounding_score_traceability_pass",
        "taste_loop_score_breakdown_pass",
        "skill_registry_validation_pass"
      ],
      "name": "Skill compounding score",
      "status": "implemented",
      "surfaces": [
        "docs/specs/skill-compounding-score.md",
        "docs/skills/system.md",
        "skills/taste-loop",
        "farplane/automations.md",
        "docs/skills/registry.jsonl"
      ]
    }
  ],
  "generated_at": "2026-06-26T12:46:23+00:00",
  "rollout": [
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/deliberative-advice/SKILL.md",
      "qa_checklist": "",
      "skill_id": "deliberative-advice",
      "skill_ui": "",
      "source": "local",
      "status": "current",
      "template_version": "0.3.2",
      "tier": 2
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/feed-scout/SKILL.md",
      "qa_checklist": "",
      "skill_id": "feed-scout",
      "skill_ui": "",
      "source": "local",
      "status": "current",
      "template_version": "0.3.2",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/hardening/SKILL.md",
      "qa_checklist": "",
      "skill_id": "hardening",
      "skill_ui": "",
      "source": "local",
      "status": "current",
      "template_version": "0.3.2",
      "tier": 2
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/metric-advisor/SKILL.md",
      "qa_checklist": "",
      "skill_id": "metric-advisor",
      "skill_ui": "",
      "source": "local",
      "status": "current",
      "template_version": "0.3.2",
      "tier": 1
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/refactoring/SKILL.md",
      "qa_checklist": "",
      "skill_id": "refactoring",
      "skill_ui": "",
      "source": "local",
      "status": "current",
      "template_version": "0.3.2",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/runtime-debugging/SKILL.md",
      "qa_checklist": "",
      "skill_id": "runtime-debugging",
      "skill_ui": "",
      "source": "local",
      "status": "current",
      "template_version": "0.3.2",
      "tier": 2
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/skill-creator/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "skill-creator",
      "skill_ui": "",
      "source": "local",
      "status": "current",
      "template_version": "0.3.2",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": false,
      "path": "skills/agent-browser/SKILL.md",
      "qa_checklist": "",
      "skill_id": "agent-browser",
      "skill_ui": "",
      "source": "external",
      "status": "external",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": false,
      "path": "skills/convex/SKILL.md",
      "qa_checklist": "",
      "skill_id": "convex",
      "skill_ui": "",
      "source": "external",
      "status": "external",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": false,
      "path": "skills/vercel-react-best-practices/SKILL.md",
      "qa_checklist": "",
      "skill_id": "vercel-react-best-practices",
      "skill_ui": "",
      "source": "external",
      "status": "external",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/agent-behavior-test/SKILL.md",
      "qa_checklist": "",
      "skill_id": "agent-behavior-test",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/agent-qa-test/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "agent-qa-test",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/agent-testability-plan/SKILL.md",
      "qa_checklist": "",
      "skill_id": "agent-testability-plan",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/apify/SKILL.md",
      "qa_checklist": "",
      "skill_id": "apify",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/bash-efficiency/SKILL.md",
      "qa_checklist": "",
      "skill_id": "bash-efficiency",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/best-of-worlds/SKILL.md",
      "qa_checklist": "",
      "skill_id": "best-of-worlds",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/brainstorm/SKILL.md",
      "qa_checklist": "",
      "skill_id": "brainstorm",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/close-ticket/SKILL.md",
      "qa_checklist": "",
      "skill_id": "close-ticket",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/codebase-analysis/SKILL.md",
      "qa_checklist": "",
      "skill_id": "codebase-analysis",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/coderabbit-review/SKILL.md",
      "qa_checklist": "",
      "skill_id": "coderabbit-review",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/commit-message/SKILL.md",
      "qa_checklist": "",
      "skill_id": "commit-message",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/data-viz/SKILL.md",
      "qa_checklist": "",
      "skill_id": "data-viz",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/deep-interview/SKILL.md",
      "qa_checklist": "",
      "skill_id": "deep-interview",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/deep-system-design/SKILL.md",
      "qa_checklist": "",
      "skill_id": "deep-system-design",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/deep-ui-design/SKILL.md",
      "qa_checklist": "",
      "skill_id": "deep-ui-design",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/delegate-cli/SKILL.md",
      "qa_checklist": "",
      "skill_id": "delegate-cli",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/delegate-frontend/SKILL.md",
      "qa_checklist": "",
      "skill_id": "delegate-frontend",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/demo/SKILL.md",
      "qa_checklist": "",
      "skill_id": "demo",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/demo-realism/SKILL.md",
      "qa_checklist": "",
      "skill_id": "demo-realism",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/desloppify/SKILL.md",
      "qa_checklist": "",
      "skill_id": "desloppify",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/diagramming/SKILL.md",
      "qa_checklist": "",
      "skill_id": "diagramming",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/execute/SKILL.md",
      "qa_checklist": "",
      "skill_id": "execute",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/external-patterns/SKILL.md",
      "qa_checklist": "",
      "skill_id": "external-patterns",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/farplane-invocation/SKILL.md",
      "qa_checklist": "",
      "skill_id": "farplane-invocation",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/find-skills/SKILL.md",
      "qa_checklist": "",
      "skill_id": "find-skills",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/frontend-design/SKILL.md",
      "qa_checklist": "",
      "skill_id": "frontend-design",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/functional-ui/SKILL.md",
      "qa_checklist": "",
      "skill_id": "functional-ui",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/harness-scout/SKILL.md",
      "qa_checklist": "",
      "skill_id": "harness-scout",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/image-generation/SKILL.md",
      "qa_checklist": "",
      "skill_id": "image-generation",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/init-advisor/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "init-advisor",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/landing-page/SKILL.md",
      "qa_checklist": "",
      "skill_id": "landing-page",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/media-ingest/SKILL.md",
      "qa_checklist": "",
      "skill_id": "media-ingest",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/notion-task-field-fill/SKILL.md",
      "qa_checklist": "",
      "skill_id": "notion-task-field-fill",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/pr-review-watch/SKILL.md",
      "qa_checklist": "",
      "skill_id": "pr-review-watch",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/pr-runtime/SKILL.md",
      "qa_checklist": "",
      "skill_id": "pr-runtime",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/pr-splitting/SKILL.md",
      "qa_checklist": "",
      "skill_id": "pr-splitting",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/prd/SKILL.md",
      "qa_checklist": "",
      "skill_id": "prd",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/product-photography/SKILL.md",
      "qa_checklist": "",
      "skill_id": "product-photography",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/qa/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "qa",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/react-flow/SKILL.md",
      "qa_checklist": "",
      "skill_id": "react-flow",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/reel-collage/SKILL.md",
      "qa_checklist": "",
      "skill_id": "reel-collage",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/remotion/SKILL.md",
      "qa_checklist": "",
      "skill_id": "remotion",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/remotion-render/SKILL.md",
      "qa_checklist": "",
      "skill_id": "remotion-render",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/research/SKILL.md",
      "qa_checklist": "",
      "skill_id": "research",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/skill-registry-ui/SKILL.md",
      "qa_checklist": "",
      "skill_id": "skill-registry-ui",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/social-content/SKILL.md",
      "qa_checklist": "",
      "skill_id": "social-content",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/spec-to-ticket/SKILL.md",
      "qa_checklist": "",
      "skill_id": "spec-to-ticket",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/summarize/SKILL.md",
      "qa_checklist": "",
      "skill_id": "summarize",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/telegram-message/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "telegram-message",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 1
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/testing/SKILL.md",
      "qa_checklist": "",
      "skill_id": "testing",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/video-generation/SKILL.md",
      "qa_checklist": "",
      "skill_id": "video-generation",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/video-production/SKILL.md",
      "qa_checklist": "",
      "skill_id": "video-production",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/video-understanding/SKILL.md",
      "qa_checklist": "",
      "skill_id": "video-understanding",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/visual-design/SKILL.md",
      "qa_checklist": "",
      "skill_id": "visual-design",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/visual-qa/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "visual-qa",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/web-design-guidelines/SKILL.md",
      "qa_checklist": "",
      "skill_id": "web-design-guidelines",
      "skill_ui": "",
      "source": "local",
      "status": "missing",
      "template_version": "missing",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/advise/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "advise",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.1.0",
      "tier": 1
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/automation-advisor/SKILL.md",
      "qa_checklist": "",
      "skill_id": "automation-advisor",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/budget-advisor/SKILL.md",
      "qa_checklist": "",
      "skill_id": "budget-advisor",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.3.0",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/code-review/SKILL.md",
      "qa_checklist": "",
      "skill_id": "code-review",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/documentation/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "documentation",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.3.0",
      "tier": 2
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/eval/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "eval",
      "skill_ui": "skills/eval/templates/viewer-react",
      "source": "local",
      "status": "stale",
      "template_version": "0.3.0",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/frontend-craft/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "frontend-craft",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/gap-analysis/SKILL.md",
      "qa_checklist": "",
      "skill_id": "gap-analysis",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 2
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/goal-advisor/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "goal-advisor",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/harness-advisor/SKILL.md",
      "qa_checklist": "",
      "skill_id": "harness-advisor",
      "skill_ui": "skills/harness-advisor",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/harness-creator/SKILL.md",
      "qa_checklist": "",
      "skill_id": "harness-creator",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/horizon-advisor/SKILL.md",
      "qa_checklist": "",
      "skill_id": "horizon-advisor",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.3.0",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/impl-plan/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "impl-plan",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.3.0",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/ingest-content/SKILL.md",
      "qa_checklist": "",
      "skill_id": "ingest-content",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/interval-update/SKILL.md",
      "qa_checklist": "",
      "skill_id": "interval-update",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/knowledge-tidier/SKILL.md",
      "qa_checklist": "",
      "skill_id": "knowledge-tidier",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.3.0",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/leverage-advisor/SKILL.md",
      "qa_checklist": "",
      "skill_id": "leverage-advisor",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/leverage-rollout/SKILL.md",
      "qa_checklist": "",
      "skill_id": "leverage-rollout",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/optimize-harness/SKILL.md",
      "qa_checklist": "",
      "skill_id": "optimize-harness",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/optimize-with-human/SKILL.md",
      "qa_checklist": "",
      "skill_id": "optimize-with-human",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 2
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/plan/SKILL.md",
      "qa_checklist": "",
      "skill_id": "plan",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 2
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/proof-advisor/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "proof-advisor",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.3.0",
      "tier": 2
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/prototyping/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "prototyping",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.1.0",
      "tier": 1
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/pulse-update/SKILL.md",
      "qa_checklist": "",
      "skill_id": "pulse-update",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/reference-grounding/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "reference-grounding",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.1.0",
      "tier": 1
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/review/SKILL.md",
      "qa_checklist": "",
      "skill_id": "review",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 2
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/self-improve/SKILL.md",
      "qa_checklist": "",
      "skill_id": "self-improve",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/skill-maintenance/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "skill_id": "skill-maintenance",
      "skill_ui": "skills/skill-maintenance/graph/index.html",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    },
    {
      "eval": "eval_task.json",
      "has_checklist": true,
      "path": "skills/taste-loop/SKILL.md",
      "qa_checklist": "",
      "skill_id": "taste-loop",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/update-memory/SKILL.md",
      "qa_checklist": "",
      "skill_id": "update-memory",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    },
    {
      "eval": "",
      "has_checklist": true,
      "path": "skills/update-strategy/SKILL.md",
      "qa_checklist": "",
      "skill_id": "update-strategy",
      "skill_ui": "",
      "source": "local",
      "status": "stale",
      "template_version": "0.2.0",
      "tier": 3
    }
  ],
  "rollout_summary": {
    "by_source": {
      "external": 3,
      "local": 94
    },
    "by_status": {
      "current": 7,
      "external": 3,
      "missing": 56,
      "stale": 31
    },
    "by_template_version": {
      "0.1.0": 3,
      "0.2.0": 21,
      "0.3.0": 7,
      "0.3.2": 7,
      "missing": 59
    },
    "total_skills": 97
  },
  "schema_version": "1.0.0",
  "source": {
    "feature_registry_path": "docs/features/registry.jsonl",
    "repo": "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane",
    "skill_registry_path": "docs/skills/registry.jsonl",
    "template_path": "docs/skills/templates/SKILL_TEMPLATE.md"
  },
  "template_consumers": [
    {
      "consumer_id": "advise",
      "consumer_scope": "skill",
      "path": "skills/advise/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": true,
        "skill": true
      },
      "template_uses": {
        "skill-qa-checklist": "0.1.0",
        "skill-template": "0.1.0"
      }
    },
    {
      "consumer_id": "agent-behavior-test",
      "consumer_scope": "skill",
      "path": "skills/agent-behavior-test/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "agent-qa-test",
      "consumer_scope": "skill",
      "path": "skills/agent-qa-test/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": true,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "agent-testability-plan",
      "consumer_scope": "skill",
      "path": "skills/agent-testability-plan/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "apify",
      "consumer_scope": "skill",
      "path": "skills/apify/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "automation-advisor",
      "consumer_scope": "skill",
      "path": "skills/automation-advisor/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "bash-efficiency",
      "consumer_scope": "skill",
      "path": "skills/bash-efficiency/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "best-of-worlds",
      "consumer_scope": "skill",
      "path": "skills/best-of-worlds/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "brainstorm",
      "consumer_scope": "skill",
      "path": "skills/brainstorm/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "budget-advisor",
      "consumer_scope": "skill",
      "path": "skills/budget-advisor/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-template": "0.3.0"
      }
    },
    {
      "consumer_id": "close-ticket",
      "consumer_scope": "skill",
      "path": "skills/close-ticket/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "code-review",
      "consumer_scope": "skill",
      "path": "skills/code-review/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "codebase-analysis",
      "consumer_scope": "skill",
      "path": "skills/codebase-analysis/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "coderabbit-review",
      "consumer_scope": "skill",
      "path": "skills/coderabbit-review/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "commit-message",
      "consumer_scope": "skill",
      "path": "skills/commit-message/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "data-viz",
      "consumer_scope": "skill",
      "path": "skills/data-viz/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "deep-interview",
      "consumer_scope": "skill",
      "path": "skills/deep-interview/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "deep-system-design",
      "consumer_scope": "skill",
      "path": "skills/deep-system-design/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "deep-ui-design",
      "consumer_scope": "skill",
      "path": "skills/deep-ui-design/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "delegate-cli",
      "consumer_scope": "skill",
      "path": "skills/delegate-cli/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "delegate-frontend",
      "consumer_scope": "skill",
      "path": "skills/delegate-frontend/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "deliberative-advice",
      "consumer_scope": "skill",
      "path": "skills/deliberative-advice/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-template": "0.3.2"
      }
    },
    {
      "consumer_id": "demo",
      "consumer_scope": "skill",
      "path": "skills/demo/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "demo-realism",
      "consumer_scope": "skill",
      "path": "skills/demo-realism/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "desloppify",
      "consumer_scope": "skill",
      "path": "skills/desloppify/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "diagramming",
      "consumer_scope": "skill",
      "path": "skills/diagramming/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "documentation",
      "consumer_scope": "skill",
      "path": "skills/documentation/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": true,
        "skill": true
      },
      "template_uses": {
        "skill-qa-checklist": "0.1.0",
        "skill-template": "0.3.0"
      }
    },
    {
      "consumer_id": "eval",
      "consumer_scope": "skill",
      "path": "skills/eval/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": true,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-qa-checklist": "0.1.0",
        "skill-template": "0.3.0"
      }
    },
    {
      "consumer_id": "execute",
      "consumer_scope": "skill",
      "path": "skills/execute/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "external-patterns",
      "consumer_scope": "skill",
      "path": "skills/external-patterns/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "farplane-invocation",
      "consumer_scope": "skill",
      "path": "skills/farplane-invocation/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "feed-scout",
      "consumer_scope": "skill",
      "path": "skills/feed-scout/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.3.2"
      }
    },
    {
      "consumer_id": "find-skills",
      "consumer_scope": "skill",
      "path": "skills/find-skills/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "frontend-craft",
      "consumer_scope": "skill",
      "path": "skills/frontend-craft/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": true,
        "skill": true
      },
      "template_uses": {
        "skill-qa-checklist": "0.1.0",
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "frontend-design",
      "consumer_scope": "skill",
      "path": "skills/frontend-design/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "functional-ui",
      "consumer_scope": "skill",
      "path": "skills/functional-ui/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "gap-analysis",
      "consumer_scope": "skill",
      "path": "skills/gap-analysis/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "goal-advisor",
      "consumer_scope": "skill",
      "path": "skills/goal-advisor/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": true,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-qa-checklist": "0.1.0",
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "hardening",
      "consumer_scope": "skill",
      "path": "skills/hardening/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.3.2"
      }
    },
    {
      "consumer_id": "harness-advisor",
      "consumer_scope": "skill",
      "path": "skills/harness-advisor/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "harness-creator",
      "consumer_scope": "skill",
      "path": "skills/harness-creator/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "harness-scout",
      "consumer_scope": "skill",
      "path": "skills/harness-scout/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "horizon-advisor",
      "consumer_scope": "skill",
      "path": "skills/horizon-advisor/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.3.0"
      }
    },
    {
      "consumer_id": "image-generation",
      "consumer_scope": "skill",
      "path": "skills/image-generation/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "impl-plan",
      "consumer_scope": "skill",
      "path": "skills/impl-plan/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": true,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-qa-checklist": "0.1.0",
        "skill-template": "0.3.0"
      }
    },
    {
      "consumer_id": "ingest-content",
      "consumer_scope": "skill",
      "path": "skills/ingest-content/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "init-advisor",
      "consumer_scope": "skill",
      "path": "skills/init-advisor/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": true,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "interval-update",
      "consumer_scope": "skill",
      "path": "skills/interval-update/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "knowledge-tidier",
      "consumer_scope": "skill",
      "path": "skills/knowledge-tidier/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-template": "0.3.0"
      }
    },
    {
      "consumer_id": "landing-page",
      "consumer_scope": "skill",
      "path": "skills/landing-page/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "leverage-advisor",
      "consumer_scope": "skill",
      "path": "skills/leverage-advisor/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "leverage-rollout",
      "consumer_scope": "skill",
      "path": "skills/leverage-rollout/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "media-ingest",
      "consumer_scope": "skill",
      "path": "skills/media-ingest/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "metric-advisor",
      "consumer_scope": "skill",
      "path": "skills/metric-advisor/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.3.2"
      }
    },
    {
      "consumer_id": "notion-task-field-fill",
      "consumer_scope": "skill",
      "path": "skills/notion-task-field-fill/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "optimize-harness",
      "consumer_scope": "skill",
      "path": "skills/optimize-harness/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "optimize-with-human",
      "consumer_scope": "skill",
      "path": "skills/optimize-with-human/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "plan",
      "consumer_scope": "skill",
      "path": "skills/plan/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "pr-review-watch",
      "consumer_scope": "skill",
      "path": "skills/pr-review-watch/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "pr-runtime",
      "consumer_scope": "skill",
      "path": "skills/pr-runtime/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "pr-splitting",
      "consumer_scope": "skill",
      "path": "skills/pr-splitting/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "prd",
      "consumer_scope": "skill",
      "path": "skills/prd/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "product-photography",
      "consumer_scope": "skill",
      "path": "skills/product-photography/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "proof-advisor",
      "consumer_scope": "skill",
      "path": "skills/proof-advisor/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": true,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-qa-checklist": "0.1.0",
        "skill-template": "0.3.0"
      }
    },
    {
      "consumer_id": "prototyping",
      "consumer_scope": "skill",
      "path": "skills/prototyping/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": true,
        "skill": true
      },
      "template_uses": {
        "skill-qa-checklist": "0.1.0",
        "skill-template": "0.1.0"
      }
    },
    {
      "consumer_id": "pulse-update",
      "consumer_scope": "skill",
      "path": "skills/pulse-update/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "qa",
      "consumer_scope": "skill",
      "path": "skills/qa/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": true,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "react-flow",
      "consumer_scope": "skill",
      "path": "skills/react-flow/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "reel-collage",
      "consumer_scope": "skill",
      "path": "skills/reel-collage/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "refactoring",
      "consumer_scope": "skill",
      "path": "skills/refactoring/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.3.2"
      }
    },
    {
      "consumer_id": "reference-grounding",
      "consumer_scope": "skill",
      "path": "skills/reference-grounding/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": true,
        "skill": true
      },
      "template_uses": {
        "skill-qa-checklist": "0.1.0",
        "skill-template": "0.1.0"
      }
    },
    {
      "consumer_id": "remotion",
      "consumer_scope": "skill",
      "path": "skills/remotion/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "remotion-render",
      "consumer_scope": "skill",
      "path": "skills/remotion-render/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "research",
      "consumer_scope": "skill",
      "path": "skills/research/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "review",
      "consumer_scope": "skill",
      "path": "skills/review/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "runtime-debugging",
      "consumer_scope": "skill",
      "path": "skills/runtime-debugging/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.3.2"
      }
    },
    {
      "consumer_id": "self-improve",
      "consumer_scope": "skill",
      "path": "skills/self-improve/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "skill-creator",
      "consumer_scope": "skill",
      "path": "skills/skill-creator/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": true,
        "skill": true
      },
      "template_uses": {
        "skill-qa-checklist": "0.1.0",
        "skill-template": "0.3.2"
      }
    },
    {
      "consumer_id": "skill-maintenance",
      "consumer_scope": "skill",
      "path": "skills/skill-maintenance/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": true,
        "skill": true
      },
      "template_uses": {
        "skill-eval-task": "0.1.0",
        "skill-qa-checklist": "0.1.0",
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "skill-registry-ui",
      "consumer_scope": "skill",
      "path": "skills/skill-registry-ui/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "social-content",
      "consumer_scope": "skill",
      "path": "skills/social-content/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "spec-to-ticket",
      "consumer_scope": "skill",
      "path": "skills/spec-to-ticket/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "summarize",
      "consumer_scope": "skill",
      "path": "skills/summarize/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "taste-loop",
      "consumer_scope": "skill",
      "path": "skills/taste-loop/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "telegram-message",
      "consumer_scope": "skill",
      "path": "skills/telegram-message/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": true,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "testing",
      "consumer_scope": "skill",
      "path": "skills/testing/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "update-memory",
      "consumer_scope": "skill",
      "path": "skills/update-memory/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "update-strategy",
      "consumer_scope": "skill",
      "path": "skills/update-strategy/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": true
      },
      "template_uses": {
        "skill-template": "0.2.0"
      }
    },
    {
      "consumer_id": "video-generation",
      "consumer_scope": "skill",
      "path": "skills/video-generation/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "video-production",
      "consumer_scope": "skill",
      "path": "skills/video-production/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "video-understanding",
      "consumer_scope": "skill",
      "path": "skills/video-understanding/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "visual-design",
      "consumer_scope": "skill",
      "path": "skills/visual-design/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "visual-qa",
      "consumer_scope": "skill",
      "path": "skills/visual-qa/SKILL.md",
      "surfaces": {
        "eval": true,
        "qa_checklist": true,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "web-design-guidelines",
      "consumer_scope": "skill",
      "path": "skills/web-design-guidelines/SKILL.md",
      "surfaces": {
        "eval": false,
        "qa_checklist": false,
        "skill": false
      },
      "template_uses": {}
    },
    {
      "consumer_id": "Farplane",
      "consumer_scope": "project",
      "path": "farplane/manifest.json",
      "surfaces": {
        "project": true
      },
      "template_uses": {
        "farplane-framework": "1.6.1"
      }
    },
    {
      "consumer_id": "Farplane-UI",
      "consumer_scope": "project",
      "path": "../Farplane-UI/farplane/manifest.json",
      "surfaces": {
        "project": true
      },
      "template_uses": {
        "farplane-framework": "1.6.1"
      }
    }
  ],
  "template_rollout": [
    {
      "consumer_id": "Farplane",
      "consumer_scope": "project",
      "current_version": "1.6.2",
      "feature_refs": [
        "FEAT-0060"
      ],
      "path": "farplane/manifest.json",
      "status": "stale",
      "target_basis": "projects with a farplane/manifest.json surface",
      "template_id": "farplane-framework",
      "used_version": "1.6.1"
    },
    {
      "consumer_id": "Farplane-UI",
      "consumer_scope": "project",
      "current_version": "1.6.2",
      "feature_refs": [
        "FEAT-0060"
      ],
      "path": "../Farplane-UI/farplane/manifest.json",
      "status": "stale",
      "target_basis": "projects with a farplane/manifest.json surface",
      "template_id": "farplane-framework",
      "used_version": "1.6.1"
    },
    {
      "consumer_id": "budget-advisor",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/budget-advisor/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "deliberative-advice",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/deliberative-advice/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "eval",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/eval/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "gap-analysis",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/gap-analysis/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "goal-advisor",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/goal-advisor/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "harness-advisor",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/harness-advisor/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "impl-plan",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/impl-plan/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "interval-update",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/interval-update/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "knowledge-tidier",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/knowledge-tidier/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "optimize-harness",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/optimize-harness/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "optimize-with-human",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/optimize-with-human/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "plan",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/plan/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "proof-advisor",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/proof-advisor/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "pulse-update",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/pulse-update/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "self-improve",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/self-improve/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "skill-maintenance",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/skill-maintenance/SKILL.md",
      "status": "current",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "agent-qa-test",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/agent-qa-test/SKILL.md",
      "status": "missing",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": ""
    },
    {
      "consumer_id": "farplane-invocation",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/farplane-invocation/SKILL.md",
      "status": "missing",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": ""
    },
    {
      "consumer_id": "feed-scout",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/feed-scout/SKILL.md",
      "status": "missing",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": ""
    },
    {
      "consumer_id": "hardening",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/hardening/SKILL.md",
      "status": "missing",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": ""
    },
    {
      "consumer_id": "init-advisor",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/init-advisor/SKILL.md",
      "status": "missing",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": ""
    },
    {
      "consumer_id": "metric-advisor",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/metric-advisor/SKILL.md",
      "status": "missing",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": ""
    },
    {
      "consumer_id": "qa",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/qa/SKILL.md",
      "status": "missing",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": ""
    },
    {
      "consumer_id": "refactoring",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/refactoring/SKILL.md",
      "status": "missing",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": ""
    },
    {
      "consumer_id": "skill-creator",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/skill-creator/SKILL.md",
      "status": "missing",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": ""
    },
    {
      "consumer_id": "taste-loop",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/taste-loop/SKILL.md",
      "status": "missing",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": ""
    },
    {
      "consumer_id": "visual-qa",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "path": "skills/visual-qa/SKILL.md",
      "status": "missing",
      "target_basis": "skills with an eval_task.json surface",
      "template_id": "skill-eval-task",
      "used_version": ""
    },
    {
      "consumer_id": "advise",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/advise/SKILL.md",
      "status": "current",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "documentation",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/documentation/SKILL.md",
      "status": "current",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "eval",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/eval/SKILL.md",
      "status": "current",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "frontend-craft",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/frontend-craft/SKILL.md",
      "status": "current",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "goal-advisor",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/goal-advisor/SKILL.md",
      "status": "current",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "impl-plan",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/impl-plan/SKILL.md",
      "status": "current",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "proof-advisor",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/proof-advisor/SKILL.md",
      "status": "current",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "prototyping",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/prototyping/SKILL.md",
      "status": "current",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "reference-grounding",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/reference-grounding/SKILL.md",
      "status": "current",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "skill-creator",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/skill-creator/SKILL.md",
      "status": "current",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "skill-maintenance",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/skill-maintenance/SKILL.md",
      "status": "current",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "agent-qa-test",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/agent-qa-test/SKILL.md",
      "status": "missing",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": ""
    },
    {
      "consumer_id": "init-advisor",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/init-advisor/SKILL.md",
      "status": "missing",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": ""
    },
    {
      "consumer_id": "qa",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/qa/SKILL.md",
      "status": "missing",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": ""
    },
    {
      "consumer_id": "telegram-message",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/telegram-message/SKILL.md",
      "status": "missing",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": ""
    },
    {
      "consumer_id": "visual-qa",
      "consumer_scope": "skill",
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "path": "skills/visual-qa/SKILL.md",
      "status": "missing",
      "target_basis": "skills with a qa_checklist.md surface",
      "template_id": "skill-qa-checklist",
      "used_version": ""
    },
    {
      "consumer_id": "advise",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/advise/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "automation-advisor",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/automation-advisor/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "budget-advisor",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/budget-advisor/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.0"
    },
    {
      "consumer_id": "code-review",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/code-review/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "deliberative-advice",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/deliberative-advice/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.2"
    },
    {
      "consumer_id": "documentation",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/documentation/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.0"
    },
    {
      "consumer_id": "eval",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/eval/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.0"
    },
    {
      "consumer_id": "feed-scout",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/feed-scout/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.2"
    },
    {
      "consumer_id": "frontend-craft",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/frontend-craft/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "gap-analysis",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/gap-analysis/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "goal-advisor",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/goal-advisor/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "hardening",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/hardening/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.2"
    },
    {
      "consumer_id": "harness-advisor",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/harness-advisor/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "harness-creator",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/harness-creator/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "horizon-advisor",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/horizon-advisor/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.0"
    },
    {
      "consumer_id": "impl-plan",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/impl-plan/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.0"
    },
    {
      "consumer_id": "ingest-content",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/ingest-content/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "interval-update",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/interval-update/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "knowledge-tidier",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/knowledge-tidier/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.0"
    },
    {
      "consumer_id": "leverage-advisor",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/leverage-advisor/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "leverage-rollout",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/leverage-rollout/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "metric-advisor",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/metric-advisor/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.2"
    },
    {
      "consumer_id": "optimize-harness",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/optimize-harness/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "optimize-with-human",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/optimize-with-human/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "plan",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/plan/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "proof-advisor",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/proof-advisor/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.0"
    },
    {
      "consumer_id": "prototyping",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/prototyping/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "pulse-update",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/pulse-update/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "refactoring",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/refactoring/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.2"
    },
    {
      "consumer_id": "reference-grounding",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/reference-grounding/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.1.0"
    },
    {
      "consumer_id": "review",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/review/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "runtime-debugging",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/runtime-debugging/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.2"
    },
    {
      "consumer_id": "self-improve",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/self-improve/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "skill-creator",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/skill-creator/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.3.2"
    },
    {
      "consumer_id": "skill-maintenance",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/skill-maintenance/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "taste-loop",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/taste-loop/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "update-memory",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/update-memory/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    },
    {
      "consumer_id": "update-strategy",
      "consumer_scope": "skill",
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "path": "skills/update-strategy/SKILL.md",
      "status": "stale",
      "target_basis": "local skills that declare skill-template usage",
      "template_id": "skill-template",
      "used_version": "0.2.0"
    }
  ],
  "template_rollout_summary": {
    "farplane-framework": {
      "by_scope": {
        "project": 2
      },
      "by_status": {
        "stale": 2
      },
      "current_version": "1.6.2",
      "feature_refs": [
        "FEAT-0060"
      ],
      "target_basis": "projects with a farplane/manifest.json surface",
      "total_consumers": 2
    },
    "skill-eval-task": {
      "by_scope": {
        "skill": 27
      },
      "by_status": {
        "current": 16,
        "missing": 11
      },
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0054"
      ],
      "target_basis": "skills with an eval_task.json surface",
      "total_consumers": 27
    },
    "skill-qa-checklist": {
      "by_scope": {
        "skill": 16
      },
      "by_status": {
        "current": 11,
        "missing": 5
      },
      "current_version": "0.1.0",
      "feature_refs": [
        "FEAT-0057"
      ],
      "target_basis": "skills with a qa_checklist.md surface",
      "total_consumers": 16
    },
    "skill-template": {
      "by_scope": {
        "skill": 38
      },
      "by_status": {
        "stale": 38
      },
      "current_version": "0.3.3",
      "feature_refs": [
        "FEAT-0048",
        "FEAT-0054",
        "FEAT-0057",
        "FEAT-0058",
        "FEAT-0059"
      ],
      "target_basis": "local skills that declare skill-template usage",
      "total_consumers": 38
    }
  },
  "template_versions": [
    {
      "introduced_at": "2026-06-24",
      "latest_at": "2026-06-24",
      "latest_commit": "a55523040aca",
      "latest_summary": "chore(skills): upgrade skill creator workflows",
      "release_count": 1,
      "sections": [
        "Context",
        "Skill Signature",
        "Phase Contract",
        "Phase Boundary",
        "Todo List",
        "Templates",
        "Gotchas",
        "Reference Map",
        "Output"
      ],
      "snapshot_path": "skills/skill-maintenance/templates/archive/skill-template-0.3.2-a55523040aca.md",
      "snapshots": [
        {
          "introduced_at": "2026-06-24",
          "snapshot_path": "skills/skill-maintenance/templates/archive/skill-template-0.3.2-a55523040aca.md",
          "source_commit": "a55523040aca",
          "summary": "chore(skills): upgrade skill creator workflows"
        }
      ],
      "source_commit": "a55523040aca",
      "summary": "chore(skills): upgrade skill creator workflows",
      "template_metadata": {
        "feature_refs": [
          "FEAT-0048",
          "FEAT-0054",
          "FEAT-0057",
          "FEAT-0058",
          "FEAT-0059"
        ],
        "surface_fields": {
          "eval": "supported",
          "qa_checklist": "supported",
          "skill_ui": "supported"
        },
        "template_id": "skill-template",
        "template_version": "0.3.2"
      },
      "version": "0.3.2"
    },
    {
      "introduced_at": "2026-06-24",
      "latest_at": "2026-06-26",
      "latest_commit": "d8abb67693a6",
      "latest_summary": "working tree current template",
      "release_count": 2,
      "sections": [
        "Context",
        "Skill Signature",
        "Phase Contract",
        "Phase Boundary",
        "Todo List",
        "Templates",
        "Gotchas",
        "Reference Map",
        "Output"
      ],
      "snapshot_path": "skills/skill-maintenance/templates/archive/skill-template-0.3.3-d8abb67693a6.md",
      "snapshots": [
        {
          "introduced_at": "2026-06-24",
          "snapshot_path": "skills/skill-maintenance/templates/archive/skill-template-0.3.3-b8f67d0311ce.md",
          "source_commit": "b8f67d0311ce",
          "summary": "Introduce proof advisor workflow inference"
        },
        {
          "introduced_at": "2026-06-26",
          "snapshot_path": "skills/skill-maintenance/templates/archive/skill-template-0.3.3-d8abb67693a6.md",
          "source_commit": "d8abb67693a6",
          "summary": "working tree current template"
        }
      ],
      "source_commit": "b8f67d0311ce",
      "summary": "Introduce proof advisor workflow inference",
      "template_metadata": {
        "feature_refs": [
          "FEAT-0048",
          "FEAT-0054",
          "FEAT-0057",
          "FEAT-0058",
          "FEAT-0059"
        ],
        "surface_fields": {
          "eval": "supported",
          "qa_checklist": "supported",
          "skill_ui": "supported",
          "workflow": "optional"
        },
        "template_id": "skill-template",
        "template_version": "0.3.3"
      },
      "version": "0.3.3"
    }
  ]
};
