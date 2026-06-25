window.FARPLANE_LIFECYCLE_GRAPH = {
  "counts": {
    "edge_confidence": {
      "curated": 43,
      "explicit": 6,
      "parsed": 418
    },
    "edge_types": {
      "consumes": 4,
      "contains": 2,
      "guards": 120,
      "reads": 131,
      "routes_to": 116,
      "triggers": 15,
      "updates": 4,
      "writes": 75
    },
    "edges": 467,
    "fsa_projections": 5,
    "node_kinds": {
      "automation": 3,
      "command": 3,
      "doc": 11,
      "file": 19,
      "fsa_state": 40,
      "gate": 116,
      "hook": 2,
      "report": 2,
      "route": 4,
      "runtime": 1,
      "skill": 40,
      "state": 118,
      "ticket": 6
    },
    "nodes": 365,
    "parsed_skills": 18
  },
  "edges": [
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/steer-pulse-automation.md",
      "source": "automation:daily-interval",
      "target": "skill:interval-update",
      "type": "triggers"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/steer-pulse-automation.md",
      "source": "automation:pulse",
      "target": "skill:pulse-update",
      "type": "triggers"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/steer-pulse-automation.md",
      "source": "automation:weekly-interval",
      "target": "skill:interval-update",
      "type": "triggers"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/minimal-autonomy-loop.md",
      "source": "doc:docs/LESSONS.md",
      "target": "skill:skill-maintenance",
      "type": "triggers"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/minimal-autonomy-loop.md",
      "source": "doc:docs/TROUBLES.md",
      "target": "skill:skill-maintenance",
      "type": "triggers"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/steer-pulse-automation.md",
      "source": "file:farplane/automations.md",
      "target": "automation:daily-interval",
      "type": "triggers"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/steer-pulse-automation.md",
      "source": "file:farplane/automations.md",
      "target": "automation:pulse",
      "type": "triggers"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/steer-pulse-automation.md",
      "source": "file:farplane/automations.md",
      "target": "automation:weekly-interval",
      "type": "triggers"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/goal-loop-contract.md",
      "source": "file:farplane/goals.md",
      "target": "skill:goal-advisor",
      "type": "triggers"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/minimal-autonomy-loop.md",
      "source": "file:farplane/products.md",
      "target": "skill:interval-update",
      "type": "consumes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/minimal-autonomy-loop.md",
      "source": "file:farplane/products.md",
      "target": "skill:pulse-update",
      "type": "consumes"
    },
    {
      "confidence": "explicit",
      "evidence_ref": "hooks.json",
      "source": "file:hooks.json",
      "target": "hook:Stop",
      "type": "contains"
    },
    {
      "confidence": "explicit",
      "evidence_ref": "hooks.json",
      "source": "file:hooks.json",
      "target": "hook:UserPromptSubmit",
      "type": "contains"
    },
    {
      "confidence": "explicit",
      "evidence_ref": "hooks.json",
      "label": "Evaluating Ralph stop hook",
      "source": "hook:Stop",
      "target": "command:python3-home/.codex/bin/stop_hook.py",
      "type": "triggers"
    },
    {
      "confidence": "explicit",
      "evidence_ref": "hooks.json",
      "label": "Sending Farplane Console stop heartbeat",
      "source": "hook:Stop",
      "target": "command:python3-home/.codex/hooks/farplane_console_ping.py",
      "type": "triggers"
    },
    {
      "confidence": "explicit",
      "evidence_ref": "hooks.json",
      "label": "Capturing current-turn user intent",
      "source": "hook:UserPromptSubmit",
      "target": "command:python3-home/.codex/bin/capture_user_turn.py",
      "type": "triggers"
    },
    {
      "confidence": "explicit",
      "evidence_ref": "hooks.json",
      "label": "Sending Farplane Console start heartbeat",
      "source": "hook:UserPromptSubmit",
      "target": "command:python3-home/.codex/hooks/farplane_console_ping.py",
      "type": "triggers"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/steer-pulse-automation.md",
      "source": "report:.farplane/reports/interval/<interval_id>/<timestamp>.md",
      "target": "skill:horizon-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/lifecycle.md",
      "source": "report:.farplane/reports/interval/<interval_id>/<timestamp>.md",
      "target": "skill:leverage-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/steer-pulse-automation.md",
      "source": "report:.farplane/reports/interval/<interval_id>/<timestamp>.md",
      "target": "skill:pulse-update",
      "type": "consumes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/steer-pulse-automation.md",
      "source": "report:.farplane/reports/pulse/<timestamp>.md",
      "target": "skill:interval-update",
      "type": "consumes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/goal-loop-contract.md",
      "source": "runtime:native-codex-goal",
      "target": "ticket:tickets/TASK-*/artifacts/",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/goal-loop-contract.md",
      "source": "runtime:native-codex-goal",
      "target": "ticket:tickets/TASK-*/progress.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "docs/specs/steer-pulse-automation.md",
      "source": "skill:automation-advisor",
      "target": "doc:docs/specs/steer-pulse-automation.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "farplane/automations.md?",
      "source": "skill:automation-advisor",
      "target": "file:farplane/automations.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "farplane/automations.md prompt updates",
      "source": "skill:automation-advisor",
      "target": "file:farplane/automations.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "farplane/pm.json?",
      "source": "skill:automation-advisor",
      "target": "file:farplane/pm.json",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "farplane/pm.json thread grouping when live activation succeeds",
      "source": "skill:automation-advisor",
      "target": "file:farplane/pm.json",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "skills/automation-advisor/qa_checklist.md?",
      "source": "skill:automation-advisor",
      "target": "file:skills/automation-advisor/qa_checklist.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "skills/automation-advisor/templates/*",
      "source": "skill:automation-advisor",
      "target": "file:skills/automation-advisor/templates/*",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "skills/interval-update/SKILL.md",
      "source": "skill:automation-advisor",
      "target": "file:skills/interval-update/SKILL.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "skills/pulse-update/SKILL.md",
      "source": "skill:automation-advisor",
      "target": "file:skills/pulse-update/SKILL.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "cadence_named",
      "source": "skill:automation-advisor",
      "target": "gate:cadence_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "dated_report_path_used",
      "source": "skill:automation-advisor",
      "target": "gate:dated_report_path_used",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "loop_choice_made",
      "source": "skill:automation-advisor",
      "target": "gate:loop_choice_made",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "no_hidden_scheduler_config",
      "source": "skill:automation-advisor",
      "target": "gate:no_hidden_scheduler_config",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "no_lane_manifest_required",
      "source": "skill:automation-advisor",
      "target": "gate:no_lane_manifest_required",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "prompt_calls_skill_plainly",
      "source": "skill:automation-advisor",
      "target": "gate:prompt_calls_skill_plainly",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "side_effect_gates_named",
      "source": "skill:automation-advisor",
      "target": "gate:side_effect_gates_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "goal-advisor",
      "source": "skill:automation-advisor",
      "target": "skill:goal-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "interval-update",
      "source": "skill:automation-advisor",
      "target": "skill:interval-update",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "pulse-update",
      "source": "skill:automation-advisor",
      "target": "skill:pulse-update",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/automation-advisor/SKILL.md",
      "label": "review",
      "source": "skill:automation-advisor",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "baseline_before_mutation",
      "source": "skill:eval",
      "target": "gate:baseline_before_mutation",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "evidence_inspected_before_claim",
      "source": "skill:eval",
      "target": "gate:evidence_inspected_before_claim",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "expected_behavior:testable",
      "source": "skill:eval",
      "target": "gate:expected_behavior-testable",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "hardcase:sanitized_and_reusable",
      "source": "skill:eval",
      "target": "gate:hardcase-sanitized_and_reusable",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "query_not_spoiled",
      "source": "skill:eval",
      "target": "gate:query_not_spoiled",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "agent-behavior-test",
      "source": "skill:eval",
      "target": "skill:agent-behavior-test",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "agent-qa-test",
      "source": "skill:eval",
      "target": "skill:agent-qa-test",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "deliberative-advice",
      "source": "skill:eval",
      "target": "skill:deliberative-advice",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "optimize-harness",
      "source": "skill:eval",
      "target": "skill:optimize-harness",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "review",
      "source": "skill:eval",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "self-improve",
      "source": "skill:eval",
      "target": "skill:self-improve",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "skill-maintenance",
      "source": "skill:eval",
      "target": "skill:skill-maintenance",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "consolidation reports",
      "source": "skill:eval",
      "target": "state:consolidation-reports",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "eval-drain processed state",
      "source": "skill:eval",
      "target": "state:eval-drain-processed-state",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "eval tasks",
      "source": "skill:eval",
      "target": "state:eval-tasks",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "existing evals",
      "source": "skill:eval",
      "target": "state:existing-evals",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "expected behavior",
      "source": "skill:eval",
      "target": "state:expected-behavior",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "fixtures",
      "source": "skill:eval",
      "target": "state:fixtures",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "hardcase metadata",
      "source": "skill:eval",
      "target": "state:hardcase-metadata",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "processed state",
      "source": "skill:eval",
      "target": "state:processed-state",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "qa_checklist?",
      "source": "skill:eval",
      "target": "state:qa_checklist",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "run artifacts",
      "source": "skill:eval",
      "target": "state:run-artifacts",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "skill eval_task.json files",
      "source": "skill:eval",
      "target": "state:skill-eval_task.json-files",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/eval/SKILL.md",
      "label": "task context",
      "source": "skill:eval",
      "target": "state:task-context",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "farplane/goals.md?",
      "source": "skill:goal-advisor",
      "target": "file:farplane/goals.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "approval_before_goal_run_when_material",
      "source": "skill:goal-advisor",
      "target": "gate:approval_before_goal_run_when_material",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "budget_named",
      "source": "skill:goal-advisor",
      "target": "gate:budget_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "drift_policy_named",
      "source": "skill:goal-advisor",
      "target": "gate:drift_policy_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "final_evidence_policy_named",
      "source": "skill:goal-advisor",
      "target": "gate:final_evidence_policy_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "logging_policy_named",
      "source": "skill:goal-advisor",
      "target": "gate:logging_policy_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "loop_owner_single",
      "source": "skill:goal-advisor",
      "target": "gate:loop_owner_single",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "material_goal_has_files",
      "source": "skill:goal-advisor",
      "target": "gate:material_goal_has_files",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "metric_provider_named",
      "source": "skill:goal-advisor",
      "target": "gate:metric_provider_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "missing_execution_inputs_resolved_or_asked",
      "source": "skill:goal-advisor",
      "target": "gate:missing_execution_inputs_resolved_or_asked",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "progress_surface_named",
      "source": "skill:goal-advisor",
      "target": "gate:progress_surface_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "proof_route_named",
      "source": "skill:goal-advisor",
      "target": "gate:proof_route_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "direct-answer",
      "source": "skill:goal-advisor",
      "target": "route:direct-answer",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "agent-qa-test",
      "source": "skill:goal-advisor",
      "target": "skill:agent-qa-test",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "impl-plan",
      "source": "skill:goal-advisor",
      "target": "skill:impl-plan",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "optimize-with-human",
      "source": "skill:goal-advisor",
      "target": "skill:optimize-with-human",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "qa",
      "source": "skill:goal-advisor",
      "target": "skill:qa",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "review",
      "source": "skill:goal-advisor",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "visual-qa",
      "source": "skill:goal-advisor",
      "target": "skill:visual-qa",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "board files?",
      "source": "skill:goal-advisor",
      "target": "state:board-files",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "goal-loop contract",
      "source": "skill:goal-advisor",
      "target": "state:goal-loop-contract",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "listed files",
      "source": "skill:goal-advisor",
      "target": "state:listed-files",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "operator intent",
      "source": "skill:goal-advisor",
      "target": "state:operator-intent",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "program.md?",
      "source": "skill:goal-advisor",
      "target": "state:program.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "progress.md?",
      "source": "skill:goal-advisor",
      "target": "state:progress.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "relevant skills/docs",
      "source": "skill:goal-advisor",
      "target": "state:relevant-skills/docs",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "ticket/program/progress? generated goal prompt? or recommendation",
      "source": "skill:goal-advisor",
      "target": "state:ticket/program/progress-generated-goal-prompt-or-recommendation",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/goal-loop-contract.md",
      "source": "skill:goal-advisor",
      "target": "ticket:tickets/TASK-*/program.md",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/goal-loop-contract.md",
      "source": "skill:goal-advisor",
      "target": "ticket:tickets/TASK-*/progress.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "tickets",
      "source": "skill:goal-advisor",
      "target": "ticket:tickets/TASK-*/ticket.md",
      "type": "reads"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/goal-loop-contract.md",
      "source": "skill:goal-advisor",
      "target": "ticket:tickets/TASK-*/ticket.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "failure_named",
      "source": "skill:harness-advisor",
      "target": "gate:failure_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "owner_surface:named",
      "source": "skill:harness-advisor",
      "target": "gate:owner_surface-named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "proof_path:named",
      "source": "skill:harness-advisor",
      "target": "gate:proof_path-named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "rejected_surfaces:named",
      "source": "skill:harness-advisor",
      "target": "gate:rejected_surfaces-named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "direct-answer",
      "source": "skill:harness-advisor",
      "target": "route:direct-answer",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "eval",
      "source": "skill:harness-advisor",
      "target": "skill:eval",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "gap-analysis",
      "source": "skill:harness-advisor",
      "target": "skill:gap-analysis",
      "type": "routes_to"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/lifecycle.md",
      "source": "skill:harness-advisor",
      "target": "skill:goal-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "impl-plan",
      "source": "skill:harness-advisor",
      "target": "skill:impl-plan",
      "type": "routes_to"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/lifecycle.md",
      "source": "skill:harness-advisor",
      "target": "skill:proof-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "self-improve",
      "source": "skill:harness-advisor",
      "target": "skill:self-improve",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "skill-maintenance",
      "source": "skill:harness-advisor",
      "target": "skill:skill-maintenance",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "spec-to-ticket",
      "source": "skill:harness-advisor",
      "target": "skill:spec-to-ticket",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "feature registry",
      "source": "skill:harness-advisor",
      "target": "state:feature-registry",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "harness doctrine",
      "source": "skill:harness-advisor",
      "target": "state:harness-doctrine",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "relevant surfaces",
      "source": "skill:harness-advisor",
      "target": "state:relevant-surfaces",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "skill registry",
      "source": "skill:harness-advisor",
      "target": "state:skill-registry",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/harness-advisor/SKILL.md",
      "label": "ticket? handoff?",
      "source": "skill:harness-advisor",
      "target": "state:ticket-handoff",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/project-files.md",
      "source": "skill:harness-creator",
      "target": "file:.agents/skills/README.md",
      "type": "updates"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "farplane/automations.md?",
      "source": "skill:horizon-advisor",
      "target": "file:farplane/automations.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "farplane/goals.md",
      "source": "skill:horizon-advisor",
      "target": "file:farplane/goals.md",
      "type": "reads"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/lifecycle.md",
      "source": "skill:horizon-advisor",
      "target": "file:farplane/goals.md",
      "type": "updates"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "farplane/goals.md delta or strategy artifact when explicitly in scope",
      "source": "skill:horizon-advisor",
      "target": "file:farplane/goals.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "farplane/harness.md",
      "source": "skill:horizon-advisor",
      "target": "file:farplane/harness.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "anti_metrics_named",
      "source": "skill:horizon-advisor",
      "target": "gate:anti_metrics_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "current_frontier_expanded_only",
      "source": "skill:horizon-advisor",
      "target": "gate:current_frontier_expanded_only",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "execution_handoff_goes_to_goal_advisor",
      "source": "skill:horizon-advisor",
      "target": "gate:execution_handoff_goes_to_goal_advisor",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "metrics_have_proof_surfaces",
      "source": "skill:horizon-advisor",
      "target": "gate:metrics_have_proof_surfaces",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "north_star_named",
      "source": "skill:horizon-advisor",
      "target": "gate:north_star_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "value_function_named",
      "source": "skill:horizon-advisor",
      "target": "gate:value_function_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "deep-interview",
      "source": "skill:horizon-advisor",
      "target": "skill:deep-interview",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "goal-advisor",
      "source": "skill:horizon-advisor",
      "target": "skill:goal-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "review",
      "source": "skill:horizon-advisor",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "update-strategy",
      "source": "skill:horizon-advisor",
      "target": "skill:update-strategy",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "memory",
      "source": "skill:horizon-advisor",
      "target": "state:memory",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "metrics",
      "source": "skill:horizon-advisor",
      "target": "state:metrics",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "progress",
      "source": "skill:horizon-advisor",
      "target": "state:progress",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "relevant strategy docs",
      "source": "skill:horizon-advisor",
      "target": "state:relevant-strategy-docs",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/horizon-advisor/SKILL.md",
      "label": "tickets",
      "source": "skill:horizon-advisor",
      "target": "ticket:tickets/TASK-*/ticket.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "docs/LESSONS.md?",
      "source": "skill:impl-plan",
      "target": "doc:docs/LESSONS.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "docs/MEMORY.md?",
      "source": "skill:impl-plan",
      "target": "doc:docs/MEMORY.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "docs/TROUBLES.md?",
      "source": "skill:impl-plan",
      "target": "doc:docs/TROUBLES.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "approval_before_goal_run",
      "source": "skill:impl-plan",
      "target": "gate:approval_before_goal_run",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "code_context_read",
      "source": "skill:impl-plan",
      "target": "gate:code_context_read",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "done_proof_concrete",
      "source": "skill:impl-plan",
      "target": "gate:done_proof_concrete",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "goal_packet_preview_compiled",
      "source": "skill:impl-plan",
      "target": "gate:goal_packet_preview_compiled",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "minimal_plan_challenge_passed",
      "source": "skill:impl-plan",
      "target": "gate:minimal_plan_challenge_passed",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "missing_inputs_resolved_or_asked",
      "source": "skill:impl-plan",
      "target": "gate:missing_inputs_resolved_or_asked",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "proof_route_named",
      "source": "skill:impl-plan",
      "target": "gate:proof_route_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "ticket_surface_exists",
      "source": "skill:impl-plan",
      "target": "gate:ticket_surface_exists",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "agent-qa-test",
      "source": "skill:impl-plan",
      "target": "skill:agent-qa-test",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "deep-system-design",
      "source": "skill:impl-plan",
      "target": "skill:deep-system-design",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "goal-advisor",
      "source": "skill:impl-plan",
      "target": "skill:goal-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "qa",
      "source": "skill:impl-plan",
      "target": "skill:qa",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "research:gap",
      "source": "skill:impl-plan",
      "target": "skill:research",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "review",
      "source": "skill:impl-plan",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "visual-qa",
      "source": "skill:impl-plan",
      "target": "skill:visual-qa",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "active ticket",
      "source": "skill:impl-plan",
      "target": "state:active-ticket",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "approval handoff",
      "source": "skill:impl-plan",
      "target": "state:approval-handoff",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "linked PRD/specs/docs",
      "source": "skill:impl-plan",
      "target": "state:linked-prd/specs/docs",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "optional design.md or Agent Testability Brief",
      "source": "skill:impl-plan",
      "target": "state:optional-design.md-or-agent-testability-brief",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "optional design.md recommendation",
      "source": "skill:impl-plan",
      "target": "state:optional-design.md-recommendation",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "proof route",
      "source": "skill:impl-plan",
      "target": "state:proof-route",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "relevant code",
      "source": "skill:impl-plan",
      "target": "state:relevant-code",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/impl-plan/SKILL.md",
      "label": "ticket.md updates",
      "source": "skill:impl-plan",
      "target": "state:ticket.md-updates",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/project-files.md",
      "source": "skill:init-advisor",
      "target": "file:.agents/skills/README.md",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/init-advisor-critical-path.md",
      "source": "skill:init-advisor",
      "target": "file:AGENTS.md",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/init-advisor-critical-path.md",
      "source": "skill:init-advisor",
      "target": "file:ARCHITECTURE.md",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/init-advisor-critical-path.md",
      "source": "skill:init-advisor",
      "target": "file:PROJECT_RULES.md",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/project-files.md",
      "source": "skill:init-advisor",
      "target": "file:farplane/automations.md",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/project-files.md",
      "source": "skill:init-advisor",
      "target": "file:farplane/goals.md",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/project-files.md",
      "source": "skill:init-advisor",
      "target": "file:farplane/harness.md",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/project-files.md",
      "source": "skill:init-advisor",
      "target": "file:farplane/hooks.json",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/project-files.md",
      "source": "skill:init-advisor",
      "target": "file:farplane/manifest.json",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/project-files.md",
      "source": "skill:init-advisor",
      "target": "file:farplane/pm.json",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/project-files.md",
      "source": "skill:init-advisor",
      "target": "file:farplane/products.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "existing_files_preserved",
      "source": "skill:init-advisor",
      "target": "gate:existing_files_preserved",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "human_gates_named",
      "source": "skill:init-advisor",
      "target": "gate:human_gates_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "interactive_stack_steps_stop_for_human",
      "source": "skill:init-advisor",
      "target": "gate:interactive_stack_steps_stop_for_human",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "no_hidden_automation",
      "source": "skill:init-advisor",
      "target": "gate:no_hidden_automation",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "secrets_not_written",
      "source": "skill:init-advisor",
      "target": "gate:secrets_not_written",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "spec_version_recorded",
      "source": "skill:init-advisor",
      "target": "gate:spec_version_recorded",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "automation-advisor",
      "source": "skill:init-advisor",
      "target": "skill:automation-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "deep-interview",
      "source": "skill:init-advisor",
      "target": "skill:deep-interview",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "harness-creator",
      "source": "skill:init-advisor",
      "target": "skill:harness-creator",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "prd",
      "source": "skill:init-advisor",
      "target": "skill:prd",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "research:official-docs",
      "source": "skill:init-advisor",
      "target": "skill:research",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "spec-to-ticket",
      "source": "skill:init-advisor",
      "target": "skill:spec-to-ticket",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "AGENTS/PROJECT_RULES/ARCHITECTURE/docs/tickets/qa/farplane scaffolds",
      "source": "skill:init-advisor",
      "target": "state:agents/project_rules/architecture/docs/tickets/qa/farplane-scaffolds",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "and starter PRD ticket",
      "source": "skill:init-advisor",
      "target": "state:and-starter-prd-ticket",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "bootstrap brief",
      "source": "skill:init-advisor",
      "target": "state:bootstrap-brief",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "existing repo files",
      "source": "skill:init-advisor",
      "target": "state:existing-repo-files",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "operator context",
      "source": "skill:init-advisor",
      "target": "state:operator-context",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "optional stack scaffold",
      "source": "skill:init-advisor",
      "target": "state:optional-stack-scaffold",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "project profile",
      "source": "skill:init-advisor",
      "target": "state:project-profile",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/init-advisor/SKILL.md",
      "label": "README/AGENTS/docs/tickets when present",
      "source": "skill:init-advisor",
      "target": "state:readme/agents/docs/tickets",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "docs/HISTORY.md?",
      "source": "skill:interval-update",
      "target": "doc:docs/HISTORY.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "docs/LESSONS.md?",
      "source": "skill:interval-update",
      "target": "doc:docs/LESSONS.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "docs/MEMORY.md?",
      "source": "skill:interval-update",
      "target": "doc:docs/MEMORY.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "docs/TROUBLES.md?",
      "source": "skill:interval-update",
      "target": "doc:docs/TROUBLES.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "farplane/goals.md?",
      "source": "skill:interval-update",
      "target": "file:farplane/goals.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "farplane/goals.md only through explicit goals-delta policy",
      "source": "skill:interval-update",
      "target": "file:farplane/goals.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "farplane/harness.md?",
      "source": "skill:interval-update",
      "target": "file:farplane/harness.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "farplane/pm.json?",
      "source": "skill:interval-update",
      "target": "file:farplane/pm.json",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "farplane/products.md?",
      "source": "skill:interval-update",
      "target": "file:farplane/products.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "configured_refs_merged",
      "source": "skill:interval-update",
      "target": "gate:configured_refs_merged",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "configured_report_workflows_run",
      "source": "skill:interval-update",
      "target": "gate:configured_report_workflows_run",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "context_bundle_written_or_summarized",
      "source": "skill:interval-update",
      "target": "gate:context_bundle_written_or_summarized",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "cross_interval_refs_resolved_or_gap_labeled",
      "source": "skill:interval-update",
      "target": "gate:cross_interval_refs_resolved_or_gap_labeled",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "date_stamped_report_used",
      "source": "skill:interval-update",
      "target": "gate:date_stamped_report_used",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "default_refs_resolved",
      "source": "skill:interval-update",
      "target": "gate:default_refs_resolved",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "drift_checked",
      "source": "skill:interval-update",
      "target": "gate:drift_checked",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "next_window_plan_written",
      "source": "skill:interval-update",
      "target": "gate:next_window_plan_written",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "report_written_before_plan_or_goals_mutation",
      "source": "skill:interval-update",
      "target": "gate:report_written_before_plan_or_goals_mutation",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "review_window_bound",
      "source": "skill:interval-update",
      "target": "gate:review_window_bound",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "side_effect_gates_respected",
      "source": "skill:interval-update",
      "target": "gate:side_effect_gates_respected",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": ".farplane/reports/interval/?",
      "source": "skill:interval-update",
      "target": "report:.farplane/reports/interval/<interval_id>/<timestamp>.md",
      "type": "reads"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/steer-pulse-automation.md",
      "source": "skill:interval-update",
      "target": "report:.farplane/reports/interval/<interval_id>/<timestamp>.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": ".farplane/reports/interval/<interval_id>/<YYYY-MM-DDTHHMMSSZ>.md",
      "source": "skill:interval-update",
      "target": "report:.farplane/reports/interval/<interval_id>/<timestamp>.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": ".farplane/reports/pulse/?",
      "source": "skill:interval-update",
      "target": "report:.farplane/reports/pulse/<timestamp>.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "feed-scout",
      "source": "skill:interval-update",
      "target": "skill:feed-scout",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "goal-advisor",
      "source": "skill:interval-update",
      "target": "skill:goal-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "pulse-update",
      "source": "skill:interval-update",
      "target": "skill:pulse-update",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "review",
      "source": "skill:interval-update",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "skill-maintenance",
      "source": "skill:interval-update",
      "target": "skill:skill-maintenance",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "update-memory",
      "source": "skill:interval-update",
      "target": "skill:update-memory",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "update-strategy",
      "source": "skill:interval-update",
      "target": "skill:update-strategy",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": ".agents/skills/**/SKILL.md?",
      "source": "skill:interval-update",
      "target": "state:.agents/skills/*/skill.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "optional .farplane/reports/interval/<interval_id>/context/<YYYY-MM-DDTHHMMSSZ>.md",
      "source": "skill:interval-update",
      "target": "state:optional-.farplane/reports/interval/<interval_id>/context/<yyyy-mm-ddthhmmssz>.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "worker thread refs when available",
      "source": "skill:interval-update",
      "target": "state:worker-thread-refs",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/interval-update/SKILL.md",
      "label": "tickets/",
      "source": "skill:interval-update",
      "target": "ticket:tickets/TASK-*/ticket.md",
      "type": "reads"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/hooks-and-runtime.md",
      "source": "skill:knowledge-tidier",
      "target": "doc:docs/MEMORY.md",
      "type": "updates"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "AGENTS.md",
      "source": "skill:knowledge-tidier",
      "target": "file:AGENTS.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "no_data_loss",
      "source": "skill:knowledge-tidier",
      "target": "gate:no_data_loss",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "owner_checked",
      "source": "skill:knowledge-tidier",
      "target": "gate:owner_checked",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "scoring_applied",
      "source": "skill:knowledge-tidier",
      "target": "gate:scoring_applied",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "source_preserved",
      "source": "skill:knowledge-tidier",
      "target": "gate:source_preserved",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "stale_facts_flagged",
      "source": "skill:knowledge-tidier",
      "target": "gate:stale_facts_flagged",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "validators_or_review_run",
      "source": "skill:knowledge-tidier",
      "target": "gate:validators_or_review_run",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "documentation",
      "source": "skill:knowledge-tidier",
      "target": "skill:documentation",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "review",
      "source": "skill:knowledge-tidier",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "skill-maintenance",
      "source": "skill:knowledge-tidier",
      "target": "skill:skill-maintenance",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "update-memory",
      "source": "skill:knowledge-tidier",
      "target": "skill:update-memory",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "archive only when preserving exact source rows",
      "source": "skill:knowledge-tidier",
      "target": "state:archive-only",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "archive_ref",
      "source": "skill:knowledge-tidier",
      "target": "state:archive_ref",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "relevant specs/skills/docs",
      "source": "skill:knowledge-tidier",
      "target": "state:relevant-specs/skills/docs",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "target_file",
      "source": "skill:knowledge-tidier",
      "target": "state:target_file",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/knowledge-tidier/SKILL.md",
      "label": "target_file",
      "source": "skill:knowledge-tidier",
      "target": "state:target_file",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "feature_grounded",
      "source": "skill:leverage-advisor",
      "target": "gate:feature_grounded",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "next_action_executable",
      "source": "skill:leverage-advisor",
      "target": "gate:next_action_executable",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "opportunities_ranked",
      "source": "skill:leverage-advisor",
      "target": "gate:opportunities_ranked",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "proof_path_named",
      "source": "skill:leverage-advisor",
      "target": "gate:proof_path_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "recommendation_named",
      "source": "skill:leverage-advisor",
      "target": "gate:recommendation_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "advise",
      "source": "skill:leverage-advisor",
      "target": "skill:advise",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "autoresearch-plan",
      "source": "skill:leverage-advisor",
      "target": "skill:autoresearch-plan",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "goal-advisor",
      "source": "skill:leverage-advisor",
      "target": "skill:goal-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/farplane-framework/lifecycle.md",
      "source": "skill:leverage-advisor",
      "target": "skill:harness-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "harness-advisor",
      "source": "skill:leverage-advisor",
      "target": "skill:harness-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "impl-plan",
      "source": "skill:leverage-advisor",
      "target": "skill:impl-plan",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "leverage-rollout",
      "source": "skill:leverage-advisor",
      "target": "skill:leverage-rollout",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "prototyping",
      "source": "skill:leverage-advisor",
      "target": "skill:prototyping",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "reference-grounding",
      "source": "skill:leverage-advisor",
      "target": "skill:reference-grounding",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "current repo state",
      "source": "skill:leverage-advisor",
      "target": "state:current-repo-state",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "feature docs",
      "source": "skill:leverage-advisor",
      "target": "state:feature-docs",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "feature registry",
      "source": "skill:leverage-advisor",
      "target": "state:feature-registry",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "leverage_plan.md? ticket_seed? autoresearch_seed? goal_recommendation?",
      "source": "skill:leverage-advisor",
      "target": "state:leverage_plan.md-ticket_seed-autoresearch_seed-goal_recommendation",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "prior proof",
      "source": "skill:leverage-advisor",
      "target": "state:prior-proof",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "related skills",
      "source": "skill:leverage-advisor",
      "target": "state:related-skills",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "specs",
      "source": "skill:leverage-advisor",
      "target": "state:specs",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "tickets",
      "source": "skill:leverage-advisor",
      "target": "ticket:tickets/TASK-*/ticket.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "farplane/goals.md?",
      "source": "skill:optimize-harness",
      "target": "file:farplane/goals.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "accept_hold_or_rollback_named",
      "source": "skill:optimize-harness",
      "target": "gate:accept_hold_or_rollback_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "gap_named",
      "source": "skill:optimize-harness",
      "target": "gate:gap_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "loss_term_named",
      "source": "skill:optimize-harness",
      "target": "gate:loss_term_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "metric_or_reward_signal_named",
      "source": "skill:optimize-harness",
      "target": "gate:metric_or_reward_signal_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "owner_surface_named",
      "source": "skill:optimize-harness",
      "target": "gate:owner_surface_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "proof_route_named",
      "source": "skill:optimize-harness",
      "target": "gate:proof_route_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "review_passes_or_blocked",
      "source": "skill:optimize-harness",
      "target": "gate:review_passes_or_blocked",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "eval",
      "source": "skill:optimize-harness",
      "target": "skill:eval",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "gap-analysis",
      "source": "skill:optimize-harness",
      "target": "skill:gap-analysis",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "goal-advisor",
      "source": "skill:optimize-harness",
      "target": "skill:goal-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "harness-advisor",
      "source": "skill:optimize-harness",
      "target": "skill:harness-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "horizon-advisor",
      "source": "skill:optimize-harness",
      "target": "skill:horizon-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "impl-plan",
      "source": "skill:optimize-harness",
      "target": "skill:impl-plan",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "leverage-advisor",
      "source": "skill:optimize-harness",
      "target": "skill:leverage-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "proof-advisor",
      "source": "skill:optimize-harness",
      "target": "skill:proof-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "review",
      "source": "skill:optimize-harness",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "self-improve",
      "source": "skill:optimize-harness",
      "target": "skill:self-improve",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "skill-creator",
      "source": "skill:optimize-harness",
      "target": "skill:skill-creator",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "skill-maintenance",
      "source": "skill:optimize-harness",
      "target": "skill:skill-maintenance",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "applied_change?",
      "source": "skill:optimize-harness",
      "target": "state:applied_change",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "eval_case?",
      "source": "skill:optimize-harness",
      "target": "state:eval_case",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "evals",
      "source": "skill:optimize-harness",
      "target": "state:evals",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "experiment_artifact?",
      "source": "skill:optimize-harness",
      "target": "state:experiment_artifact",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "feature registry",
      "source": "skill:optimize-harness",
      "target": "state:feature-registry",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "gap reports",
      "source": "skill:optimize-harness",
      "target": "state:gap-reports",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "goals_delta_candidate?",
      "source": "skill:optimize-harness",
      "target": "state:goals_delta_candidate",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "harness algebra",
      "source": "skill:optimize-harness",
      "target": "state:harness-algebra",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "harness doctrine",
      "source": "skill:optimize-harness",
      "target": "state:harness-doctrine",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "interval reports?",
      "source": "skill:optimize-harness",
      "target": "state:interval-reports",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "review_receipt?",
      "source": "skill:optimize-harness",
      "target": "state:review_receipt",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "skill registry",
      "source": "skill:optimize-harness",
      "target": "state:skill-registry",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "target surfaces",
      "source": "skill:optimize-harness",
      "target": "state:target-surfaces",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "ticket?",
      "source": "skill:optimize-harness",
      "target": "state:ticket",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/optimize-harness/SKILL.md",
      "label": "tickets",
      "source": "skill:optimize-harness",
      "target": "ticket:tickets/TASK-*/ticket.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "anti-cheat_reviewed",
      "source": "skill:proof-advisor",
      "target": "gate:anti-cheat_reviewed",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "cases_distinct_and_judgeable",
      "source": "skill:proof-advisor",
      "target": "gate:cases_distinct_and_judgeable",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "oracle_defined",
      "source": "skill:proof-advisor",
      "target": "gate:oracle_defined",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "proof_surface_fit",
      "source": "skill:proof-advisor",
      "target": "gate:proof_surface_fit",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "source_material_classified",
      "source": "skill:proof-advisor",
      "target": "gate:source_material_classified",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "target_behavior_named",
      "source": "skill:proof-advisor",
      "target": "gate:target_behavior_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "agent-behavior-test",
      "source": "skill:proof-advisor",
      "target": "skill:agent-behavior-test",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "agent-qa-test",
      "source": "skill:proof-advisor",
      "target": "skill:agent-qa-test",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "eval",
      "source": "skill:proof-advisor",
      "target": "skill:eval",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "qa",
      "source": "skill:proof-advisor",
      "target": "skill:qa",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "review",
      "source": "skill:proof-advisor",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "skill-maintenance",
      "source": "skill:proof-advisor",
      "target": "skill:skill-maintenance",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "testing",
      "source": "skill:proof-advisor",
      "target": "skill:testing",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "visual-qa",
      "source": "skill:proof-advisor",
      "target": "skill:visual-qa",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "case matrix",
      "source": "skill:proof-advisor",
      "target": "state:case-matrix",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "eval rows",
      "source": "skill:proof-advisor",
      "target": "state:eval-rows",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "eval_task.json files",
      "source": "skill:proof-advisor",
      "target": "state:eval_task.json-files",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "existing tests",
      "source": "skill:proof-advisor",
      "target": "state:existing-tests",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "external source notes when needed",
      "source": "skill:proof-advisor",
      "target": "state:external-source-notes",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "local contracts",
      "source": "skill:proof-advisor",
      "target": "state:local-contracts",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "logs/traces/failures",
      "source": "skill:proof-advisor",
      "target": "state:logs/traces/failures",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "or handoff notes",
      "source": "skill:proof-advisor",
      "target": "state:or-handoff-notes",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "proof plan",
      "source": "skill:proof-advisor",
      "target": "state:proof-plan",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "QA checklists",
      "source": "skill:proof-advisor",
      "target": "state:qa-checklists",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "QA findings",
      "source": "skill:proof-advisor",
      "target": "state:qa-findings",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "test-case drafts",
      "source": "skill:proof-advisor",
      "target": "state:test-case-drafts",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/proof-advisor/SKILL.md",
      "label": "tickets/specs",
      "source": "skill:proof-advisor",
      "target": "ticket:tickets/specs",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "farplane/goals.md?",
      "source": "skill:pulse-update",
      "target": "file:farplane/goals.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "farplane/harness.md?",
      "source": "skill:pulse-update",
      "target": "file:farplane/harness.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "farplane/pm.json?",
      "source": "skill:pulse-update",
      "target": "file:farplane/pm.json",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "farplane/pm.json when persistent PM-owned worker threads are spawned",
      "source": "skill:pulse-update",
      "target": "file:farplane/pm.json",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "farplane/products.md?",
      "source": "skill:pulse-update",
      "target": "file:farplane/products.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "board_loaded",
      "source": "skill:pulse-update",
      "target": "gate:board_loaded",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "decision_recorded",
      "source": "skill:pulse-update",
      "target": "gate:decision_recorded",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "default_refs_resolved",
      "source": "skill:pulse-update",
      "target": "gate:default_refs_resolved",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "execution_cap_respected",
      "source": "skill:pulse-update",
      "target": "gate:execution_cap_respected",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "extensions_merged",
      "source": "skill:pulse-update",
      "target": "gate:extensions_merged",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "pm_thread_grouping_updated_when_persistent",
      "source": "skill:pulse-update",
      "target": "gate:pm_thread_grouping_updated_when_persistent",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "proceedable_ticket_admission_checked",
      "source": "skill:pulse-update",
      "target": "gate:proceedable_ticket_admission_checked",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "rewards_reconciled",
      "source": "skill:pulse-update",
      "target": "gate:rewards_reconciled",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "side_effect_gates_respected",
      "source": "skill:pulse-update",
      "target": "gate:side_effect_gates_respected",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": ".farplane/reports/interval/**?",
      "source": "skill:pulse-update",
      "target": "report:.farplane/reports/interval/<interval_id>/<timestamp>.md",
      "type": "reads"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/steer-pulse-automation.md",
      "source": "skill:pulse-update",
      "target": "report:.farplane/reports/pulse/<timestamp>.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": ".farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md",
      "source": "skill:pulse-update",
      "target": "report:.farplane/reports/pulse/<timestamp>.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "eval",
      "source": "skill:pulse-update",
      "target": "skill:eval",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "feed-scout",
      "source": "skill:pulse-update",
      "target": "skill:feed-scout",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "goal-advisor",
      "source": "skill:pulse-update",
      "target": "skill:goal-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "impl-plan",
      "source": "skill:pulse-update",
      "target": "skill:impl-plan",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "qa",
      "source": "skill:pulse-update",
      "target": "skill:qa",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "review",
      "source": "skill:pulse-update",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "skill-maintenance",
      "source": "skill:pulse-update",
      "target": "skill:skill-maintenance",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": ".agents/skills/**/SKILL.md?",
      "source": "skill:pulse-update",
      "target": "state:.agents/skills/*/skill.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": ".farplane/automation/action-outcomes.jsonl",
      "source": "skill:pulse-update",
      "target": "state:.farplane/automation/action-outcomes.jsonl",
      "type": "reads"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/steer-pulse-automation.md",
      "source": "skill:pulse-update",
      "target": "state:.farplane/automation/decisions.jsonl",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": ".farplane/automation/decisions.jsonl",
      "source": "skill:pulse-update",
      "target": "state:.farplane/automation/decisions.jsonl",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": ".farplane/automation/heartbeat-policy.json",
      "source": "skill:pulse-update",
      "target": "state:.farplane/automation/heartbeat-policy.json",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": ".farplane/automation/rewards.jsonl",
      "source": "skill:pulse-update",
      "target": "state:.farplane/automation/rewards.jsonl",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": ".farplane/automation/spawned-threads.jsonl",
      "source": "skill:pulse-update",
      "target": "state:.farplane/automation/spawned-threads.jsonl",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": ".farplane/automation/spawned-threads.jsonl",
      "source": "skill:pulse-update",
      "target": "state:.farplane/automation/spawned-threads.jsonl",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/pulse-update/SKILL.md",
      "label": "tickets/TASK-*/ticket.md",
      "source": "skill:pulse-update",
      "target": "ticket:tickets/TASK-*/ticket.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "artifacts_captured",
      "source": "skill:qa",
      "target": "gate:artifacts_captured",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "proof_policy_read",
      "source": "skill:qa",
      "target": "gate:proof_policy_read",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "ticket_selected",
      "source": "skill:qa",
      "target": "gate:ticket_selected",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "ui_work_has_screenshots_or_blocker",
      "source": "skill:qa",
      "target": "gate:ui_work_has_screenshots_or_blocker",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "weak_proof_blocks",
      "source": "skill:qa",
      "target": "gate:weak_proof_blocks",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "qa-tester",
      "source": "skill:qa",
      "target": "route:qa-tester",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "agent-qa-test",
      "source": "skill:qa",
      "target": "skill:agent-qa-test",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "review",
      "source": "skill:qa",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "visual-qa",
      "source": "skill:qa",
      "target": "skill:visual-qa",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "captured artifacts",
      "source": "skill:qa",
      "target": "state:captured-artifacts",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "linked specs/docs",
      "source": "skill:qa",
      "target": "state:linked-specs/docs",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "optional design.md",
      "source": "skill:qa",
      "target": "state:optional-design.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "result.json",
      "source": "skill:qa",
      "target": "state:result.json",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "runtime handoff",
      "source": "skill:qa",
      "target": "state:runtime-handoff",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "ticket State/Links",
      "source": "skill:qa",
      "target": "state:ticket-state/links",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "ticket.md",
      "source": "skill:qa",
      "target": "state:ticket.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/qa/SKILL.md",
      "label": "tickets/TASK-XXXX/artifacts/qa/<run>/report.md",
      "source": "skill:qa",
      "target": "ticket:tickets/TASK-*/artifacts/",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/review/SKILL.md",
      "label": "docs/review/rubrics selected rubrics",
      "source": "skill:review",
      "target": "doc:docs/review/rubrics selected rubrics",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/review/SKILL.md",
      "label": "evidence_inspected",
      "source": "skill:review",
      "target": "gate:evidence_inspected",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/review/SKILL.md",
      "label": "next_action_named",
      "source": "skill:review",
      "target": "gate:next_action_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/review/SKILL.md",
      "label": "rubric_family_named",
      "source": "skill:review",
      "target": "gate:rubric_family_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/review/SKILL.md",
      "label": "TAS_supported",
      "source": "skill:review",
      "target": "gate:tas_supported",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/review/SKILL.md",
      "label": "caller-owned",
      "source": "skill:review",
      "target": "route:caller-owned",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/review/SKILL.md",
      "label": "changed artifacts",
      "source": "skill:review",
      "target": "state:changed-artifacts",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/review/SKILL.md",
      "label": "evidence",
      "source": "skill:review",
      "target": "state:evidence",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/review/SKILL.md",
      "label": "review artifact?",
      "source": "skill:review",
      "target": "state:review-artifact",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/review/SKILL.md",
      "label": "task context",
      "source": "skill:review",
      "target": "state:task-context",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "proof_or_blocker_named",
      "source": "skill:skill-creator",
      "target": "gate:proof_or_blocker_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "review_ready",
      "source": "skill:skill-creator",
      "target": "gate:review_ready",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "template_structure_valid",
      "source": "skill:skill-creator",
      "target": "gate:template_structure_valid",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "trigger_stable",
      "source": "skill:skill-creator",
      "target": "gate:trigger_stable",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "advise",
      "source": "skill:skill-creator",
      "target": "skill:advise",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "deliberative-advice",
      "source": "skill:skill-creator",
      "target": "skill:deliberative-advice",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "gap-analysis",
      "source": "skill:skill-creator",
      "target": "skill:gap-analysis",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "research:source-synthesis",
      "source": "skill:skill-creator",
      "target": "skill:research",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "review",
      "source": "skill:skill-creator",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "skill-maintenance",
      "source": "skill:skill-creator",
      "target": "skill:skill-maintenance",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "references?",
      "source": "skill:skill-creator",
      "target": "state:references",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "registry",
      "source": "skill:skill-creator",
      "target": "state:registry",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "registry?",
      "source": "skill:skill-creator",
      "target": "state:registry",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "scripts?",
      "source": "skill:skill-creator",
      "target": "state:scripts",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "skill-system docs",
      "source": "skill:skill-creator",
      "target": "state:skill-system-docs",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "SKILL.md",
      "source": "skill:skill-creator",
      "target": "state:skill.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "target skill",
      "source": "skill:skill-creator",
      "target": "state:target-skill",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-creator/SKILL.md",
      "label": "template",
      "source": "skill:skill-creator",
      "target": "state:template",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "docs/LESSONS.md?",
      "source": "skill:skill-maintenance",
      "target": "doc:docs/LESSONS.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "docs/TROUBLES.md?",
      "source": "skill:skill-maintenance",
      "target": "doc:docs/TROUBLES.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "docs/skills/registry.jsonl",
      "source": "skill:skill-maintenance",
      "target": "doc:docs/skills/registry.jsonl",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "docs/skills/registry.jsonl",
      "source": "skill:skill-maintenance",
      "target": "doc:docs/skills/registry.jsonl",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "audit_or_skip_recorded",
      "source": "skill:skill-maintenance",
      "target": "gate:audit_or_skip_recorded",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "behavior_delta_named",
      "source": "skill:skill-maintenance",
      "target": "gate:behavior_delta_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "check_skills_passed",
      "source": "skill:skill-maintenance",
      "target": "gate:check_skills_passed",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "eval_guardrails_synced_or_skipped",
      "source": "skill:skill-maintenance",
      "target": "gate:eval_guardrails_synced_or_skipped",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "first_load_executable",
      "source": "skill:skill-maintenance",
      "target": "gate:first_load_executable",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "owner_surface_clear",
      "source": "skill:skill-maintenance",
      "target": "gate:owner_surface_clear",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "registry_synced",
      "source": "skill:skill-maintenance",
      "target": "gate:registry_synced",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "reviewer_routed_when_material",
      "source": "skill:skill-maintenance",
      "target": "gate:reviewer_routed_when_material",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "source_owner_preserved",
      "source": "skill:skill-maintenance",
      "target": "gate:source_owner_preserved",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "template_version_truthful",
      "source": "skill:skill-maintenance",
      "target": "gate:template_version_truthful",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "advise",
      "source": "skill:skill-maintenance",
      "target": "skill:advise",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "deliberative-advice",
      "source": "skill:skill-maintenance",
      "target": "skill:deliberative-advice",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "eval",
      "source": "skill:skill-maintenance",
      "target": "skill:eval",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "gap-analysis",
      "source": "skill:skill-maintenance",
      "target": "skill:gap-analysis",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "harness-advisor",
      "source": "skill:skill-maintenance",
      "target": "skill:harness-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "review",
      "source": "skill:skill-maintenance",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "self-improve",
      "source": "skill:skill-maintenance",
      "target": "skill:self-improve",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "skill-creator",
      "source": "skill:skill-maintenance",
      "target": "skill:skill-creator",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "edited_skill.eval_task?",
      "source": "skill:skill-maintenance",
      "target": "state:edited_skill.eval_task",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "edited_skill.eval_task?",
      "source": "skill:skill-maintenance",
      "target": "state:edited_skill.eval_task",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "edited_skill.qa_checklist?",
      "source": "skill:skill-maintenance",
      "target": "state:edited_skill.qa_checklist",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "edited_skill.qa_checklist?",
      "source": "skill:skill-maintenance",
      "target": "state:edited_skill.qa_checklist",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "edited_skill.references?",
      "source": "skill:skill-maintenance",
      "target": "state:edited_skill.references",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "edited_skill.references?",
      "source": "skill:skill-maintenance",
      "target": "state:edited_skill.references",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "edited_skill.SKILL.md",
      "source": "skill:skill-maintenance",
      "target": "state:edited_skill.skill.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "edited_skill.SKILL.md?",
      "source": "skill:skill-maintenance",
      "target": "state:edited_skill.skill.md",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "interval_reports?",
      "source": "skill:skill-maintenance",
      "target": "state:interval_reports",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "optional .farplane/state/skill-maintenance/processed-learning.jsonl",
      "source": "skill:skill-maintenance",
      "target": "state:optional-.farplane/state/skill-maintenance/processed-learning.jsonl",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "prior_audits?",
      "source": "skill:skill-maintenance",
      "target": "state:prior_audits",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "pulse_reports?",
      "source": "skill:skill-maintenance",
      "target": "state:pulse_reports",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "reviewer_receipts?",
      "source": "skill:skill-maintenance",
      "target": "state:reviewer_receipts",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "run_artifacts?",
      "source": "skill:skill-maintenance",
      "target": "state:run_artifacts",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "skill-local audit?",
      "source": "skill:skill-maintenance",
      "target": "state:skill-local-audit",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/skill-maintenance/SKILL.md",
      "label": "tickets/**/progress.md?",
      "source": "skill:skill-maintenance",
      "target": "ticket:tickets/**/progress.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "docs/**/*.md",
      "source": "skill:update-memory",
      "target": "doc:docs/**/*.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "docs/HISTORY.md",
      "source": "skill:update-memory",
      "target": "doc:docs/HISTORY.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "docs/LESSONS.md",
      "source": "skill:update-memory",
      "target": "doc:docs/LESSONS.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "docs/MEMORY.md",
      "source": "skill:update-memory",
      "target": "doc:docs/MEMORY.md",
      "type": "reads"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/filesystem-lifecycle.md",
      "source": "skill:update-memory",
      "target": "doc:docs/MEMORY.md",
      "type": "updates"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "docs/TROUBLES.md",
      "source": "skill:update-memory",
      "target": "doc:docs/TROUBLES.md",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "docs_owner_identified",
      "source": "skill:update-memory",
      "target": "gate:docs_owner_identified",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "no_raw_transcripts",
      "source": "skill:update-memory",
      "target": "gate:no_raw_transcripts",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "promotion_threshold_named",
      "source": "skill:update-memory",
      "target": "gate:promotion_threshold_named",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "skill_hardening_routed_out",
      "source": "skill:update-memory",
      "target": "gate:skill_hardening_routed_out",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "source_files_read",
      "source": "skill:update-memory",
      "target": "gate:source_files_read",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "stale_context_labeled",
      "source": "skill:update-memory",
      "target": "gate:stale_context_labeled",
      "type": "guards"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "ticket/spec owner",
      "source": "skill:update-memory",
      "target": "route:ticket/spec-owner",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "documentation",
      "source": "skill:update-memory",
      "target": "skill:documentation",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "review",
      "source": "skill:update-memory",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "skill-maintenance:harden_skill",
      "source": "skill:update-memory",
      "target": "skill:skill-maintenance",
      "type": "routes_to"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "docs only when an owning project path and approval are explicit",
      "source": "skill:update-memory",
      "target": "state:docs-only",
      "type": "writes"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "README",
      "source": "skill:update-memory",
      "target": "state:readme",
      "type": "reads"
    },
    {
      "confidence": "parsed",
      "evidence_ref": "skills/update-memory/SKILL.md",
      "label": "tickets/progress/PM reports",
      "source": "skill:update-memory",
      "target": "state:tickets/progress/pm-reports",
      "type": "reads"
    },
    {
      "confidence": "curated",
      "evidence_ref": "docs/specs/goal-loop-contract.md",
      "source": "ticket:tickets/TASK-*/program.md",
      "target": "runtime:native-codex-goal",
      "type": "triggers"
    },
    {
      "confidence": "curated",
      "evidence_ref": "tickets/TASK-0213/ticket.md",
      "source": "ticket:tickets/TASK-*/ticket.md",
      "target": "skill:impl-plan",
      "type": "triggers"
    }
  ],
  "fsa_projections": [
    {
      "id": "project_initialization",
      "label": "Project initialization",
      "start": "fsa:project_initialization:operator-intent",
      "states": [
        "fsa:project_initialization:operator-intent",
        "fsa:project_initialization:init-advisor-target-bound",
        "fsa:project_initialization:project-substrate-written",
        "fsa:project_initialization:framework-config-written",
        "fsa:project_initialization:readiness-audited",
        "fsa:project_initialization:horizon-goals-shaped",
        "fsa:project_initialization:goal-advisor-handoff-ready"
      ],
      "terminal": [
        "fsa:project_initialization:goal-advisor-handoff-ready"
      ],
      "transitions": [
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "operator intent -> init advisor target bound",
          "source": "fsa:project_initialization:operator-intent",
          "target": "fsa:project_initialization:init-advisor-target-bound",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "init advisor target bound -> project substrate written",
          "source": "fsa:project_initialization:init-advisor-target-bound",
          "target": "fsa:project_initialization:project-substrate-written",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "project substrate written -> framework config written",
          "source": "fsa:project_initialization:project-substrate-written",
          "target": "fsa:project_initialization:framework-config-written",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "framework config written -> readiness audited",
          "source": "fsa:project_initialization:framework-config-written",
          "target": "fsa:project_initialization:readiness-audited",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "readiness audited -> horizon goals shaped",
          "source": "fsa:project_initialization:readiness-audited",
          "target": "fsa:project_initialization:horizon-goals-shaped",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "horizon goals shaped -> goal advisor handoff ready",
          "source": "fsa:project_initialization:horizon-goals-shaped",
          "target": "fsa:project_initialization:goal-advisor-handoff-ready",
          "type": "transition"
        }
      ]
    },
    {
      "id": "automation_activation",
      "label": "Automation activation",
      "start": "fsa:automation_activation:automation-prompts-reviewed",
      "states": [
        "fsa:automation_activation:automation-prompts-reviewed",
        "fsa:automation_activation:pulse-thread-created",
        "fsa:automation_activation:pulse-heartbeat-attached",
        "fsa:automation_activation:daily-interval-cron-created",
        "fsa:automation_activation:weekly-interval-cron-created",
        "fsa:automation_activation:pm-json-grouped"
      ],
      "terminal": [
        "fsa:automation_activation:pm-json-grouped"
      ],
      "transitions": [
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "automation prompts reviewed -> pulse thread created",
          "source": "fsa:automation_activation:automation-prompts-reviewed",
          "target": "fsa:automation_activation:pulse-thread-created",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "pulse thread created -> pulse heartbeat attached",
          "source": "fsa:automation_activation:pulse-thread-created",
          "target": "fsa:automation_activation:pulse-heartbeat-attached",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "pulse heartbeat attached -> daily interval cron created",
          "source": "fsa:automation_activation:pulse-heartbeat-attached",
          "target": "fsa:automation_activation:daily-interval-cron-created",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "daily interval cron created -> weekly interval cron created",
          "source": "fsa:automation_activation:daily-interval-cron-created",
          "target": "fsa:automation_activation:weekly-interval-cron-created",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "weekly interval cron created -> pm json grouped",
          "source": "fsa:automation_activation:weekly-interval-cron-created",
          "target": "fsa:automation_activation:pm-json-grouped",
          "type": "transition"
        }
      ]
    },
    {
      "id": "ticket_goal_execution",
      "label": "Ticket to native Goal execution",
      "start": "fsa:ticket_goal_execution:ticket-selected",
      "states": [
        "fsa:ticket_goal_execution:ticket-selected",
        "fsa:ticket_goal_execution:implementation-plan-prepared",
        "fsa:ticket_goal_execution:goal-packet-written",
        "fsa:ticket_goal_execution:native-goal-started",
        "fsa:ticket_goal_execution:build-executed",
        "fsa:ticket_goal_execution:qa-proof-captured",
        "fsa:ticket_goal_execution:demo-proof-captured",
        "fsa:ticket_goal_execution:review-passed",
        "fsa:ticket_goal_execution:ticket-closed-out"
      ],
      "terminal": [
        "fsa:ticket_goal_execution:ticket-closed-out"
      ],
      "transitions": [
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "ticket selected -> implementation plan prepared",
          "source": "fsa:ticket_goal_execution:ticket-selected",
          "target": "fsa:ticket_goal_execution:implementation-plan-prepared",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "implementation plan prepared -> goal packet written",
          "source": "fsa:ticket_goal_execution:implementation-plan-prepared",
          "target": "fsa:ticket_goal_execution:goal-packet-written",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "goal packet written -> native goal started",
          "source": "fsa:ticket_goal_execution:goal-packet-written",
          "target": "fsa:ticket_goal_execution:native-goal-started",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "native goal started -> build executed",
          "source": "fsa:ticket_goal_execution:native-goal-started",
          "target": "fsa:ticket_goal_execution:build-executed",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "build executed -> qa proof captured",
          "source": "fsa:ticket_goal_execution:build-executed",
          "target": "fsa:ticket_goal_execution:qa-proof-captured",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "qa proof captured -> demo proof captured when required",
          "source": "fsa:ticket_goal_execution:qa-proof-captured",
          "target": "fsa:ticket_goal_execution:demo-proof-captured",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "demo proof captured when required -> review passed",
          "source": "fsa:ticket_goal_execution:demo-proof-captured",
          "target": "fsa:ticket_goal_execution:review-passed",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "review passed -> ticket closed out",
          "source": "fsa:ticket_goal_execution:review-passed",
          "target": "fsa:ticket_goal_execution:ticket-closed-out",
          "type": "transition"
        }
      ]
    },
    {
      "id": "memory_drain_upkeep",
      "label": "Memory and drain upkeep",
      "start": "fsa:memory_drain_upkeep:raw-signals-accumulated",
      "states": [
        "fsa:memory_drain_upkeep:raw-signals-accumulated",
        "fsa:memory_drain_upkeep:drain-window-selected",
        "fsa:memory_drain_upkeep:rows-deduped-and-scored",
        "fsa:memory_drain_upkeep:owner-surfaces-chosen",
        "fsa:memory_drain_upkeep:memory-or-docs-updated",
        "fsa:memory_drain_upkeep:skill-hardening-routed",
        "fsa:memory_drain_upkeep:eval-or-review-evidence-recorded",
        "fsa:memory_drain_upkeep:processed-state-written"
      ],
      "terminal": [
        "fsa:memory_drain_upkeep:processed-state-written"
      ],
      "transitions": [
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "raw signals accumulated -> drain window selected",
          "source": "fsa:memory_drain_upkeep:raw-signals-accumulated",
          "target": "fsa:memory_drain_upkeep:drain-window-selected",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "drain window selected -> rows deduped and scored",
          "source": "fsa:memory_drain_upkeep:drain-window-selected",
          "target": "fsa:memory_drain_upkeep:rows-deduped-and-scored",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "rows deduped and scored -> owner surfaces chosen",
          "source": "fsa:memory_drain_upkeep:rows-deduped-and-scored",
          "target": "fsa:memory_drain_upkeep:owner-surfaces-chosen",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "owner surfaces chosen -> memory or docs updated",
          "source": "fsa:memory_drain_upkeep:owner-surfaces-chosen",
          "target": "fsa:memory_drain_upkeep:memory-or-docs-updated",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "memory or docs updated -> skill hardening routed",
          "source": "fsa:memory_drain_upkeep:memory-or-docs-updated",
          "target": "fsa:memory_drain_upkeep:skill-hardening-routed",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "skill hardening routed -> eval or review evidence recorded",
          "source": "fsa:memory_drain_upkeep:skill-hardening-routed",
          "target": "fsa:memory_drain_upkeep:eval-or-review-evidence-recorded",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "eval or review evidence recorded -> processed state written",
          "source": "fsa:memory_drain_upkeep:eval-or-review-evidence-recorded",
          "target": "fsa:memory_drain_upkeep:processed-state-written",
          "type": "transition"
        }
      ]
    },
    {
      "id": "self_update_loop",
      "label": "Weekly self-update loop",
      "start": "fsa:self_update_loop:weekly-report-written",
      "states": [
        "fsa:self_update_loop:weekly-report-written",
        "fsa:self_update_loop:goals-delta-classified",
        "fsa:self_update_loop:leverage-bets-scored",
        "fsa:self_update_loop:proof-route-selected",
        "fsa:self_update_loop:operator-approval-or-source-gap-recorded",
        "fsa:self_update_loop:horizon-delta-applied",
        "fsa:self_update_loop:goal-advisor-handoff-compiled",
        "fsa:self_update_loop:pulse-executes-bounded-work",
        "fsa:self_update_loop:reward-signal-recorded",
        "fsa:self_update_loop:next-weekly-review-reads-outcomes"
      ],
      "terminal": [
        "fsa:self_update_loop:next-weekly-review-reads-outcomes"
      ],
      "transitions": [
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "weekly report written -> goals delta classified",
          "source": "fsa:self_update_loop:weekly-report-written",
          "target": "fsa:self_update_loop:goals-delta-classified",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "goals delta classified -> leverage bets scored",
          "source": "fsa:self_update_loop:goals-delta-classified",
          "target": "fsa:self_update_loop:leverage-bets-scored",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "leverage bets scored -> proof route selected",
          "source": "fsa:self_update_loop:leverage-bets-scored",
          "target": "fsa:self_update_loop:proof-route-selected",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "proof route selected -> operator approval or source gap recorded",
          "source": "fsa:self_update_loop:proof-route-selected",
          "target": "fsa:self_update_loop:operator-approval-or-source-gap-recorded",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "operator approval or source gap recorded -> horizon delta applied when approved",
          "source": "fsa:self_update_loop:operator-approval-or-source-gap-recorded",
          "target": "fsa:self_update_loop:horizon-delta-applied",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "horizon delta applied when approved -> goal advisor handoff compiled",
          "source": "fsa:self_update_loop:horizon-delta-applied",
          "target": "fsa:self_update_loop:goal-advisor-handoff-compiled",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "goal advisor handoff compiled -> pulse executes bounded work",
          "source": "fsa:self_update_loop:goal-advisor-handoff-compiled",
          "target": "fsa:self_update_loop:pulse-executes-bounded-work",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "pulse executes bounded work -> reward signal recorded",
          "source": "fsa:self_update_loop:pulse-executes-bounded-work",
          "target": "fsa:self_update_loop:reward-signal-recorded",
          "type": "transition"
        },
        {
          "confidence": "curated",
          "evidence_ref": "docs/farplane-framework/graph-contract.md",
          "label": "reward signal recorded -> next weekly review reads outcomes",
          "source": "fsa:self_update_loop:reward-signal-recorded",
          "target": "fsa:self_update_loop:next-weekly-review-reads-outcomes",
          "type": "transition"
        }
      ]
    }
  ],
  "generated_at": "2026-06-25T18:00:50+00:00",
  "nodes": [
    {
      "id": "automation:daily-interval",
      "kind": "automation",
      "label": "daily-interval",
      "tags": [
        "automation"
      ]
    },
    {
      "id": "automation:pulse",
      "kind": "automation",
      "label": "pulse",
      "tags": [
        "automation"
      ]
    },
    {
      "id": "automation:weekly-interval",
      "kind": "automation",
      "label": "weekly-interval",
      "tags": [
        "automation"
      ]
    },
    {
      "id": "command:python3-home/.codex/bin/capture_user_turn.py",
      "kind": "command",
      "label": "python3 \"$HOME/.codex/bin/capture_user_turn.py\"",
      "metadata": {
        "statusMessage": "Capturing current-turn user intent",
        "timeout": 30
      },
      "path": "hooks.json",
      "tags": [
        "command",
        "hook"
      ]
    },
    {
      "id": "command:python3-home/.codex/bin/stop_hook.py",
      "kind": "command",
      "label": "python3 \"$HOME/.codex/bin/stop_hook.py\"",
      "metadata": {
        "statusMessage": "Evaluating Ralph stop hook",
        "timeout": 90
      },
      "path": "hooks.json",
      "tags": [
        "command",
        "hook"
      ]
    },
    {
      "id": "command:python3-home/.codex/hooks/farplane_console_ping.py",
      "kind": "command",
      "label": "python3 \"$HOME/.codex/hooks/farplane_console_ping.py\"",
      "metadata": {
        "statusMessage": "Sending Farplane Console start heartbeat",
        "timeout": 5
      },
      "path": "hooks.json",
      "tags": [
        "command",
        "hook"
      ]
    },
    {
      "id": "doc:docs/**/*.md",
      "kind": "doc",
      "label": "docs/**/*.md",
      "path": "docs/**/*.md",
      "tags": [
        "parsed"
      ]
    },
    {
      "id": "doc:docs/HISTORY.md",
      "kind": "doc",
      "label": "Project history",
      "path": "docs/HISTORY.md",
      "tags": [
        "docs",
        "memory"
      ]
    },
    {
      "id": "doc:docs/LESSONS.md",
      "kind": "doc",
      "label": "Distilled lessons",
      "path": "docs/LESSONS.md",
      "tags": [
        "docs",
        "memory"
      ]
    },
    {
      "id": "doc:docs/MEMORY.md",
      "kind": "doc",
      "label": "Durable memory",
      "path": "docs/MEMORY.md",
      "tags": [
        "docs",
        "memory"
      ]
    },
    {
      "id": "doc:docs/TROUBLES.md",
      "kind": "doc",
      "label": "Raw trouble log",
      "path": "docs/TROUBLES.md",
      "tags": [
        "docs",
        "memory"
      ]
    },
    {
      "id": "doc:docs/farplane-framework/graph-contract.md",
      "kind": "doc",
      "label": "Lifecycle graph contract",
      "path": "docs/farplane-framework/graph-contract.md",
      "tags": [
        "docs",
        "framework",
        "graph"
      ]
    },
    {
      "id": "doc:docs/farplane-framework/hooks-and-runtime.md",
      "kind": "doc",
      "label": "Hooks and runtime",
      "path": "docs/farplane-framework/hooks-and-runtime.md",
      "tags": [
        "docs",
        "framework",
        "hooks"
      ]
    },
    {
      "id": "doc:docs/farplane-framework/lifecycle.md",
      "kind": "doc",
      "label": "Lifecycle hub",
      "path": "docs/farplane-framework/lifecycle.md",
      "tags": [
        "docs",
        "framework"
      ]
    },
    {
      "id": "doc:docs/review/rubrics selected rubrics",
      "kind": "doc",
      "label": "docs/review/rubrics selected rubrics",
      "path": "docs/review/rubrics selected rubrics",
      "tags": [
        "parsed"
      ]
    },
    {
      "id": "doc:docs/skills/registry.jsonl",
      "kind": "doc",
      "label": "docs/skills/registry.jsonl",
      "path": "docs/skills/registry.jsonl",
      "tags": [
        "parsed"
      ]
    },
    {
      "id": "doc:docs/specs/steer-pulse-automation.md",
      "kind": "doc",
      "label": "docs/specs/steer-pulse-automation.md",
      "path": "docs/specs/steer-pulse-automation.md",
      "tags": [
        "parsed"
      ]
    },
    {
      "id": "file:.agents/skills/README.md",
      "kind": "file",
      "label": "Local product skill home",
      "path": ".agents/skills/README.md",
      "tags": [
        "agents",
        "skills",
        "tracked-config"
      ]
    },
    {
      "id": "file:AGENTS.md",
      "kind": "file",
      "label": "Project operating policy",
      "path": "AGENTS.md",
      "tags": [
        "policy",
        "project"
      ]
    },
    {
      "id": "file:ARCHITECTURE.md",
      "kind": "file",
      "label": "Project architecture",
      "path": "ARCHITECTURE.md",
      "tags": [
        "docs",
        "project"
      ]
    },
    {
      "id": "file:PROJECT_RULES.md",
      "kind": "file",
      "label": "Project rules",
      "path": "PROJECT_RULES.md",
      "tags": [
        "policy",
        "project"
      ]
    },
    {
      "id": "file:README.md",
      "kind": "file",
      "label": "Project README",
      "path": "README.md",
      "tags": [
        "docs",
        "project"
      ]
    },
    {
      "id": "file:farplane/README.md",
      "kind": "file",
      "label": "Framework local README",
      "path": "farplane/README.md",
      "tags": [
        "farplane",
        "tracked-config"
      ]
    },
    {
      "id": "file:farplane/automations.md",
      "kind": "file",
      "label": "Reviewed automation prompts",
      "path": "farplane/automations.md",
      "tags": [
        "automation",
        "farplane"
      ]
    },
    {
      "id": "file:farplane/bindings.md",
      "kind": "file",
      "label": "Project bindings",
      "path": "farplane/bindings.md",
      "tags": [
        "farplane",
        "tracked-config"
      ]
    },
    {
      "id": "file:farplane/goals.md",
      "kind": "file",
      "label": "Project goals",
      "path": "farplane/goals.md",
      "tags": [
        "farplane",
        "goals",
        "tracked-config"
      ]
    },
    {
      "id": "file:farplane/harness.md",
      "kind": "file",
      "label": "Project harness",
      "path": "farplane/harness.md",
      "tags": [
        "farplane",
        "tracked-config"
      ]
    },
    {
      "id": "file:farplane/hooks.json",
      "kind": "file",
      "label": "Project hook config",
      "path": "farplane/hooks.json",
      "tags": [
        "farplane",
        "hooks",
        "tracked-config"
      ]
    },
    {
      "id": "file:farplane/manifest.json",
      "kind": "file",
      "label": "Framework manifest",
      "path": "farplane/manifest.json",
      "tags": [
        "farplane",
        "tracked-config"
      ]
    },
    {
      "id": "file:farplane/pm.json",
      "kind": "file",
      "label": "PM UI thread grouping",
      "path": "farplane/pm.json",
      "tags": [
        "farplane",
        "pm-ui"
      ]
    },
    {
      "id": "file:farplane/products.md",
      "kind": "file",
      "label": "Project products and work lanes",
      "path": "farplane/products.md",
      "tags": [
        "farplane",
        "products",
        "tracked-config"
      ]
    },
    {
      "id": "file:hooks.json",
      "kind": "file",
      "label": "Codex hook config",
      "path": "hooks.json",
      "tags": [
        "hooks",
        "runtime"
      ]
    },
    {
      "id": "file:skills/automation-advisor/qa_checklist.md",
      "kind": "file",
      "label": "skills/automation-advisor/qa_checklist.md",
      "path": "skills/automation-advisor/qa_checklist.md",
      "tags": [
        "parsed"
      ]
    },
    {
      "id": "file:skills/automation-advisor/templates/*",
      "kind": "file",
      "label": "skills/automation-advisor/templates/*",
      "path": "skills/automation-advisor/templates/*",
      "tags": [
        "parsed"
      ]
    },
    {
      "id": "file:skills/interval-update/SKILL.md",
      "kind": "file",
      "label": "skills/interval-update/SKILL.md",
      "path": "skills/interval-update/SKILL.md",
      "tags": [
        "parsed"
      ]
    },
    {
      "id": "file:skills/pulse-update/SKILL.md",
      "kind": "file",
      "label": "skills/pulse-update/SKILL.md",
      "path": "skills/pulse-update/SKILL.md",
      "tags": [
        "parsed"
      ]
    },
    {
      "id": "fsa:automation_activation:automation-prompts-reviewed",
      "kind": "fsa_state",
      "label": "automation prompts reviewed",
      "tags": [
        "automation_activation",
        "fsa"
      ]
    },
    {
      "id": "fsa:automation_activation:daily-interval-cron-created",
      "kind": "fsa_state",
      "label": "daily interval cron created",
      "tags": [
        "automation_activation",
        "fsa"
      ]
    },
    {
      "id": "fsa:automation_activation:pm-json-grouped",
      "kind": "fsa_state",
      "label": "pm json grouped",
      "tags": [
        "automation_activation",
        "fsa"
      ]
    },
    {
      "id": "fsa:automation_activation:pulse-heartbeat-attached",
      "kind": "fsa_state",
      "label": "pulse heartbeat attached",
      "tags": [
        "automation_activation",
        "fsa"
      ]
    },
    {
      "id": "fsa:automation_activation:pulse-thread-created",
      "kind": "fsa_state",
      "label": "pulse thread created",
      "tags": [
        "automation_activation",
        "fsa"
      ]
    },
    {
      "id": "fsa:automation_activation:weekly-interval-cron-created",
      "kind": "fsa_state",
      "label": "weekly interval cron created",
      "tags": [
        "automation_activation",
        "fsa"
      ]
    },
    {
      "id": "fsa:memory_drain_upkeep:drain-window-selected",
      "kind": "fsa_state",
      "label": "drain window selected",
      "tags": [
        "fsa",
        "memory_drain_upkeep"
      ]
    },
    {
      "id": "fsa:memory_drain_upkeep:eval-or-review-evidence-recorded",
      "kind": "fsa_state",
      "label": "eval or review evidence recorded",
      "tags": [
        "fsa",
        "memory_drain_upkeep"
      ]
    },
    {
      "id": "fsa:memory_drain_upkeep:memory-or-docs-updated",
      "kind": "fsa_state",
      "label": "memory or docs updated",
      "tags": [
        "fsa",
        "memory_drain_upkeep"
      ]
    },
    {
      "id": "fsa:memory_drain_upkeep:owner-surfaces-chosen",
      "kind": "fsa_state",
      "label": "owner surfaces chosen",
      "tags": [
        "fsa",
        "memory_drain_upkeep"
      ]
    },
    {
      "id": "fsa:memory_drain_upkeep:processed-state-written",
      "kind": "fsa_state",
      "label": "processed state written",
      "tags": [
        "fsa",
        "memory_drain_upkeep"
      ]
    },
    {
      "id": "fsa:memory_drain_upkeep:raw-signals-accumulated",
      "kind": "fsa_state",
      "label": "raw signals accumulated",
      "tags": [
        "fsa",
        "memory_drain_upkeep"
      ]
    },
    {
      "id": "fsa:memory_drain_upkeep:rows-deduped-and-scored",
      "kind": "fsa_state",
      "label": "rows deduped and scored",
      "tags": [
        "fsa",
        "memory_drain_upkeep"
      ]
    },
    {
      "id": "fsa:memory_drain_upkeep:skill-hardening-routed",
      "kind": "fsa_state",
      "label": "skill hardening routed",
      "tags": [
        "fsa",
        "memory_drain_upkeep"
      ]
    },
    {
      "id": "fsa:project_initialization:framework-config-written",
      "kind": "fsa_state",
      "label": "framework config written",
      "tags": [
        "fsa",
        "project_initialization"
      ]
    },
    {
      "id": "fsa:project_initialization:goal-advisor-handoff-ready",
      "kind": "fsa_state",
      "label": "goal advisor handoff ready",
      "tags": [
        "fsa",
        "project_initialization"
      ]
    },
    {
      "id": "fsa:project_initialization:horizon-goals-shaped",
      "kind": "fsa_state",
      "label": "horizon goals shaped",
      "tags": [
        "fsa",
        "project_initialization"
      ]
    },
    {
      "id": "fsa:project_initialization:init-advisor-target-bound",
      "kind": "fsa_state",
      "label": "init advisor target bound",
      "tags": [
        "fsa",
        "project_initialization"
      ]
    },
    {
      "id": "fsa:project_initialization:operator-intent",
      "kind": "fsa_state",
      "label": "operator intent",
      "tags": [
        "fsa",
        "project_initialization"
      ]
    },
    {
      "id": "fsa:project_initialization:project-substrate-written",
      "kind": "fsa_state",
      "label": "project substrate written",
      "tags": [
        "fsa",
        "project_initialization"
      ]
    },
    {
      "id": "fsa:project_initialization:readiness-audited",
      "kind": "fsa_state",
      "label": "readiness audited",
      "tags": [
        "fsa",
        "project_initialization"
      ]
    },
    {
      "id": "fsa:self_update_loop:goal-advisor-handoff-compiled",
      "kind": "fsa_state",
      "label": "goal advisor handoff compiled",
      "tags": [
        "fsa",
        "self_update_loop"
      ]
    },
    {
      "id": "fsa:self_update_loop:goals-delta-classified",
      "kind": "fsa_state",
      "label": "goals delta classified",
      "tags": [
        "fsa",
        "self_update_loop"
      ]
    },
    {
      "id": "fsa:self_update_loop:horizon-delta-applied",
      "kind": "fsa_state",
      "label": "horizon delta applied",
      "tags": [
        "fsa",
        "self_update_loop"
      ]
    },
    {
      "id": "fsa:self_update_loop:leverage-bets-scored",
      "kind": "fsa_state",
      "label": "leverage bets scored",
      "tags": [
        "fsa",
        "self_update_loop"
      ]
    },
    {
      "id": "fsa:self_update_loop:next-weekly-review-reads-outcomes",
      "kind": "fsa_state",
      "label": "next weekly review reads outcomes",
      "tags": [
        "fsa",
        "self_update_loop"
      ]
    },
    {
      "id": "fsa:self_update_loop:operator-approval-or-source-gap-recorded",
      "kind": "fsa_state",
      "label": "operator approval or source gap recorded",
      "tags": [
        "fsa",
        "self_update_loop"
      ]
    },
    {
      "id": "fsa:self_update_loop:proof-route-selected",
      "kind": "fsa_state",
      "label": "proof route selected",
      "tags": [
        "fsa",
        "self_update_loop"
      ]
    },
    {
      "id": "fsa:self_update_loop:pulse-executes-bounded-work",
      "kind": "fsa_state",
      "label": "pulse executes bounded work",
      "tags": [
        "fsa",
        "self_update_loop"
      ]
    },
    {
      "id": "fsa:self_update_loop:reward-signal-recorded",
      "kind": "fsa_state",
      "label": "reward signal recorded",
      "tags": [
        "fsa",
        "self_update_loop"
      ]
    },
    {
      "id": "fsa:self_update_loop:weekly-report-written",
      "kind": "fsa_state",
      "label": "weekly report written",
      "tags": [
        "fsa",
        "self_update_loop"
      ]
    },
    {
      "id": "fsa:ticket_goal_execution:build-executed",
      "kind": "fsa_state",
      "label": "build executed",
      "tags": [
        "fsa",
        "ticket_goal_execution"
      ]
    },
    {
      "id": "fsa:ticket_goal_execution:demo-proof-captured",
      "kind": "fsa_state",
      "label": "demo proof captured",
      "tags": [
        "fsa",
        "ticket_goal_execution"
      ]
    },
    {
      "id": "fsa:ticket_goal_execution:goal-packet-written",
      "kind": "fsa_state",
      "label": "goal packet written",
      "tags": [
        "fsa",
        "ticket_goal_execution"
      ]
    },
    {
      "id": "fsa:ticket_goal_execution:implementation-plan-prepared",
      "kind": "fsa_state",
      "label": "implementation plan prepared",
      "tags": [
        "fsa",
        "ticket_goal_execution"
      ]
    },
    {
      "id": "fsa:ticket_goal_execution:native-goal-started",
      "kind": "fsa_state",
      "label": "native goal started",
      "tags": [
        "fsa",
        "ticket_goal_execution"
      ]
    },
    {
      "id": "fsa:ticket_goal_execution:qa-proof-captured",
      "kind": "fsa_state",
      "label": "qa proof captured",
      "tags": [
        "fsa",
        "ticket_goal_execution"
      ]
    },
    {
      "id": "fsa:ticket_goal_execution:review-passed",
      "kind": "fsa_state",
      "label": "review passed",
      "tags": [
        "fsa",
        "ticket_goal_execution"
      ]
    },
    {
      "id": "fsa:ticket_goal_execution:ticket-closed-out",
      "kind": "fsa_state",
      "label": "ticket closed out",
      "tags": [
        "fsa",
        "ticket_goal_execution"
      ]
    },
    {
      "id": "fsa:ticket_goal_execution:ticket-selected",
      "kind": "fsa_state",
      "label": "ticket selected",
      "tags": [
        "fsa",
        "ticket_goal_execution"
      ]
    },
    {
      "id": "gate:accept_hold_or_rollback_named",
      "kind": "gate",
      "label": "accept_hold_or_rollback_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:anti-cheat_reviewed",
      "kind": "gate",
      "label": "anti-cheat_reviewed",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:anti_metrics_named",
      "kind": "gate",
      "label": "anti_metrics_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:approval_before_goal_run",
      "kind": "gate",
      "label": "approval_before_goal_run",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:approval_before_goal_run_when_material",
      "kind": "gate",
      "label": "approval_before_goal_run_when_material",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:artifacts_captured",
      "kind": "gate",
      "label": "artifacts_captured",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:audit_or_skip_recorded",
      "kind": "gate",
      "label": "audit_or_skip_recorded",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:baseline_before_mutation",
      "kind": "gate",
      "label": "baseline_before_mutation",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:behavior_delta_named",
      "kind": "gate",
      "label": "behavior_delta_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:board_loaded",
      "kind": "gate",
      "label": "board_loaded",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:budget_named",
      "kind": "gate",
      "label": "budget_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:cadence_named",
      "kind": "gate",
      "label": "cadence_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:cases_distinct_and_judgeable",
      "kind": "gate",
      "label": "cases_distinct_and_judgeable",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:check_skills_passed",
      "kind": "gate",
      "label": "check_skills_passed",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:code_context_read",
      "kind": "gate",
      "label": "code_context_read",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:configured_refs_merged",
      "kind": "gate",
      "label": "configured_refs_merged",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:configured_report_workflows_run",
      "kind": "gate",
      "label": "configured_report_workflows_run",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:context_bundle_written_or_summarized",
      "kind": "gate",
      "label": "context_bundle_written_or_summarized",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:cross_interval_refs_resolved_or_gap_labeled",
      "kind": "gate",
      "label": "cross_interval_refs_resolved_or_gap_labeled",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:current_frontier_expanded_only",
      "kind": "gate",
      "label": "current_frontier_expanded_only",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:date_stamped_report_used",
      "kind": "gate",
      "label": "date_stamped_report_used",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:dated_report_path_used",
      "kind": "gate",
      "label": "dated_report_path_used",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:decision_recorded",
      "kind": "gate",
      "label": "decision_recorded",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:default_refs_resolved",
      "kind": "gate",
      "label": "default_refs_resolved",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:docs_owner_identified",
      "kind": "gate",
      "label": "docs_owner_identified",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:done_proof_concrete",
      "kind": "gate",
      "label": "done_proof_concrete",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:drift_checked",
      "kind": "gate",
      "label": "drift_checked",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:drift_policy_named",
      "kind": "gate",
      "label": "drift_policy_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:eval_guardrails_synced_or_skipped",
      "kind": "gate",
      "label": "eval_guardrails_synced_or_skipped",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:evidence_inspected",
      "kind": "gate",
      "label": "evidence_inspected",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:evidence_inspected_before_claim",
      "kind": "gate",
      "label": "evidence_inspected_before_claim",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:execution_cap_respected",
      "kind": "gate",
      "label": "execution_cap_respected",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:execution_handoff_goes_to_goal_advisor",
      "kind": "gate",
      "label": "execution_handoff_goes_to_goal_advisor",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:existing_files_preserved",
      "kind": "gate",
      "label": "existing_files_preserved",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:expected_behavior-testable",
      "kind": "gate",
      "label": "expected_behavior:testable",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:extensions_merged",
      "kind": "gate",
      "label": "extensions_merged",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:failure_named",
      "kind": "gate",
      "label": "failure_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:feature_grounded",
      "kind": "gate",
      "label": "feature_grounded",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:final_evidence_policy_named",
      "kind": "gate",
      "label": "final_evidence_policy_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:first_load_executable",
      "kind": "gate",
      "label": "first_load_executable",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:gap_named",
      "kind": "gate",
      "label": "gap_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:goal_packet_preview_compiled",
      "kind": "gate",
      "label": "goal_packet_preview_compiled",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:hardcase-sanitized_and_reusable",
      "kind": "gate",
      "label": "hardcase:sanitized_and_reusable",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:human_gates_named",
      "kind": "gate",
      "label": "human_gates_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:interactive_stack_steps_stop_for_human",
      "kind": "gate",
      "label": "interactive_stack_steps_stop_for_human",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:logging_policy_named",
      "kind": "gate",
      "label": "logging_policy_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:loop_choice_made",
      "kind": "gate",
      "label": "loop_choice_made",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:loop_owner_single",
      "kind": "gate",
      "label": "loop_owner_single",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:loss_term_named",
      "kind": "gate",
      "label": "loss_term_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:material_goal_has_files",
      "kind": "gate",
      "label": "material_goal_has_files",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:metric_or_reward_signal_named",
      "kind": "gate",
      "label": "metric_or_reward_signal_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:metric_provider_named",
      "kind": "gate",
      "label": "metric_provider_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:metrics_have_proof_surfaces",
      "kind": "gate",
      "label": "metrics_have_proof_surfaces",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:minimal_plan_challenge_passed",
      "kind": "gate",
      "label": "minimal_plan_challenge_passed",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:missing_execution_inputs_resolved_or_asked",
      "kind": "gate",
      "label": "missing_execution_inputs_resolved_or_asked",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:missing_inputs_resolved_or_asked",
      "kind": "gate",
      "label": "missing_inputs_resolved_or_asked",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:next_action_executable",
      "kind": "gate",
      "label": "next_action_executable",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:next_action_named",
      "kind": "gate",
      "label": "next_action_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:next_window_plan_written",
      "kind": "gate",
      "label": "next_window_plan_written",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:no_data_loss",
      "kind": "gate",
      "label": "no_data_loss",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:no_hidden_automation",
      "kind": "gate",
      "label": "no_hidden_automation",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:no_hidden_scheduler_config",
      "kind": "gate",
      "label": "no_hidden_scheduler_config",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:no_lane_manifest_required",
      "kind": "gate",
      "label": "no_lane_manifest_required",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:no_raw_transcripts",
      "kind": "gate",
      "label": "no_raw_transcripts",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:north_star_named",
      "kind": "gate",
      "label": "north_star_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:opportunities_ranked",
      "kind": "gate",
      "label": "opportunities_ranked",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:oracle_defined",
      "kind": "gate",
      "label": "oracle_defined",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:owner_checked",
      "kind": "gate",
      "label": "owner_checked",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:owner_surface-named",
      "kind": "gate",
      "label": "owner_surface:named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:owner_surface_clear",
      "kind": "gate",
      "label": "owner_surface_clear",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:owner_surface_named",
      "kind": "gate",
      "label": "owner_surface_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:pm_thread_grouping_updated_when_persistent",
      "kind": "gate",
      "label": "pm_thread_grouping_updated_when_persistent",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:proceedable_ticket_admission_checked",
      "kind": "gate",
      "label": "proceedable_ticket_admission_checked",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:progress_surface_named",
      "kind": "gate",
      "label": "progress_surface_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:promotion_threshold_named",
      "kind": "gate",
      "label": "promotion_threshold_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:prompt_calls_skill_plainly",
      "kind": "gate",
      "label": "prompt_calls_skill_plainly",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:proof_or_blocker_named",
      "kind": "gate",
      "label": "proof_or_blocker_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:proof_path-named",
      "kind": "gate",
      "label": "proof_path:named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:proof_path_named",
      "kind": "gate",
      "label": "proof_path_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:proof_policy_read",
      "kind": "gate",
      "label": "proof_policy_read",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:proof_route_named",
      "kind": "gate",
      "label": "proof_route_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:proof_surface_fit",
      "kind": "gate",
      "label": "proof_surface_fit",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:query_not_spoiled",
      "kind": "gate",
      "label": "query_not_spoiled",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:recommendation_named",
      "kind": "gate",
      "label": "recommendation_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:registry_synced",
      "kind": "gate",
      "label": "registry_synced",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:rejected_surfaces-named",
      "kind": "gate",
      "label": "rejected_surfaces:named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:report_written_before_plan_or_goals_mutation",
      "kind": "gate",
      "label": "report_written_before_plan_or_goals_mutation",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:review_passes_or_blocked",
      "kind": "gate",
      "label": "review_passes_or_blocked",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:review_ready",
      "kind": "gate",
      "label": "review_ready",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:review_window_bound",
      "kind": "gate",
      "label": "review_window_bound",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:reviewer_routed_when_material",
      "kind": "gate",
      "label": "reviewer_routed_when_material",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:rewards_reconciled",
      "kind": "gate",
      "label": "rewards_reconciled",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:rubric_family_named",
      "kind": "gate",
      "label": "rubric_family_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:scoring_applied",
      "kind": "gate",
      "label": "scoring_applied",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:secrets_not_written",
      "kind": "gate",
      "label": "secrets_not_written",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:side_effect_gates_named",
      "kind": "gate",
      "label": "side_effect_gates_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:side_effect_gates_respected",
      "kind": "gate",
      "label": "side_effect_gates_respected",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:skill_hardening_routed_out",
      "kind": "gate",
      "label": "skill_hardening_routed_out",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:source_files_read",
      "kind": "gate",
      "label": "source_files_read",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:source_material_classified",
      "kind": "gate",
      "label": "source_material_classified",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:source_owner_preserved",
      "kind": "gate",
      "label": "source_owner_preserved",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:source_preserved",
      "kind": "gate",
      "label": "source_preserved",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:spec_version_recorded",
      "kind": "gate",
      "label": "spec_version_recorded",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:stale_context_labeled",
      "kind": "gate",
      "label": "stale_context_labeled",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:stale_facts_flagged",
      "kind": "gate",
      "label": "stale_facts_flagged",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:target_behavior_named",
      "kind": "gate",
      "label": "target_behavior_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:tas_supported",
      "kind": "gate",
      "label": "TAS_supported",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:template_structure_valid",
      "kind": "gate",
      "label": "template_structure_valid",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:template_version_truthful",
      "kind": "gate",
      "label": "template_version_truthful",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:ticket_selected",
      "kind": "gate",
      "label": "ticket_selected",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:ticket_surface_exists",
      "kind": "gate",
      "label": "ticket_surface_exists",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:trigger_stable",
      "kind": "gate",
      "label": "trigger_stable",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:ui_work_has_screenshots_or_blocker",
      "kind": "gate",
      "label": "ui_work_has_screenshots_or_blocker",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:validators_or_review_run",
      "kind": "gate",
      "label": "validators_or_review_run",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:value_function_named",
      "kind": "gate",
      "label": "value_function_named",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "gate:weak_proof_blocks",
      "kind": "gate",
      "label": "weak_proof_blocks",
      "tags": [
        "gate"
      ]
    },
    {
      "id": "hook:Stop",
      "kind": "hook",
      "label": "Stop",
      "path": "hooks.json",
      "tags": [
        "hook"
      ]
    },
    {
      "id": "hook:UserPromptSubmit",
      "kind": "hook",
      "label": "UserPromptSubmit",
      "path": "hooks.json",
      "tags": [
        "hook"
      ]
    },
    {
      "id": "report:.farplane/reports/interval/<interval_id>/<timestamp>.md",
      "kind": "report",
      "label": "Interval reports",
      "path": ".farplane/reports/interval/<interval_id>/<timestamp>.md",
      "tags": [
        "interval",
        "runtime"
      ]
    },
    {
      "id": "report:.farplane/reports/pulse/<timestamp>.md",
      "kind": "report",
      "label": "Pulse reports",
      "path": ".farplane/reports/pulse/<timestamp>.md",
      "tags": [
        "pulse",
        "runtime"
      ]
    },
    {
      "id": "route:caller-owned",
      "kind": "route",
      "label": "caller-owned",
      "tags": [
        "abstract-route",
        "route"
      ]
    },
    {
      "id": "route:direct-answer",
      "kind": "route",
      "label": "direct-answer",
      "tags": [
        "abstract-route",
        "route"
      ]
    },
    {
      "id": "route:qa-tester",
      "kind": "route",
      "label": "qa-tester",
      "tags": [
        "abstract-route",
        "route"
      ]
    },
    {
      "id": "route:ticket/spec-owner",
      "kind": "route",
      "label": "ticket/spec owner",
      "tags": [
        "abstract-route",
        "route"
      ]
    },
    {
      "id": "runtime:native-codex-goal",
      "kind": "runtime",
      "label": "native-codex-goal",
      "tags": [
        "goal",
        "runtime"
      ]
    },
    {
      "id": "skill:advise",
      "kind": "skill",
      "label": "advise",
      "path": "skills/advise/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:agent-behavior-test",
      "kind": "skill",
      "label": "agent-behavior-test",
      "path": "skills/agent-behavior-test/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:agent-qa-test",
      "kind": "skill",
      "label": "agent-qa-test",
      "path": "skills/agent-qa-test/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:automation-advisor",
      "kind": "skill",
      "label": "automation-advisor",
      "metadata": {
        "description": "Design or revise Farplane Codex automations using reviewable automations.md prompts and generic Pulse/Interval skill calls.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/automation-advisor/SKILL.md",
      "tags": [
        "harness",
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:autoresearch-plan",
      "kind": "skill",
      "label": "autoresearch-plan",
      "path": "skills/autoresearch-plan/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:deep-interview",
      "kind": "skill",
      "label": "deep-interview",
      "path": "skills/deep-interview/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:deep-system-design",
      "kind": "skill",
      "label": "deep-system-design",
      "path": "skills/deep-system-design/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:deliberative-advice",
      "kind": "skill",
      "label": "deliberative-advice",
      "path": "skills/deliberative-advice/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:documentation",
      "kind": "skill",
      "label": "documentation",
      "path": "skills/documentation/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:eval",
      "kind": "skill",
      "label": "eval",
      "metadata": {
        "description": "Turn agent, prompt, or skill behavior into local eval tasks, boolean or tier judges, run artifacts, and verdicts.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/eval/SKILL.md",
      "tags": [
        "harness",
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:feed-scout",
      "kind": "skill",
      "label": "feed-scout",
      "path": "skills/feed-scout/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:gap-analysis",
      "kind": "skill",
      "label": "gap-analysis",
      "path": "skills/gap-analysis/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:goal-advisor",
      "kind": "skill",
      "label": "goal-advisor",
      "metadata": {
        "description": "Turn an ambitious request into Goal architecture, ticket-backed loop state, and a native Codex /goal prompt when warranted.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/goal-advisor/SKILL.md",
      "tags": [
        "harness",
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:harness-advisor",
      "kind": "skill",
      "label": "harness-advisor",
      "metadata": {
        "description": "Turn a Farplane improvement idea into a recommended owner surface across policy, templates, skills, agents, hooks, tickets, docs, or validators.",
        "source": "local",
        "tier": 2
      },
      "path": "skills/harness-advisor/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:harness-creator",
      "kind": "skill",
      "label": "harness-creator",
      "path": "skills/harness-creator/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:horizon-advisor",
      "kind": "skill",
      "label": "horizon-advisor",
      "metadata": {
        "description": "Turn ambiguous long-horizon intent into goals.md, KPI trees, feedback-sized projects, and Goal Advisor handoffs.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/horizon-advisor/SKILL.md",
      "tags": [
        "harness",
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:impl-plan",
      "kind": "skill",
      "label": "impl-plan",
      "metadata": {
        "description": "Turn one selected coding ticket or material implementation request into an approval-ready ticket plan, test strategy, and proof contract.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/impl-plan/SKILL.md",
      "tags": [
        "coding",
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:init-advisor",
      "kind": "skill",
      "label": "init-advisor",
      "metadata": {
        "description": "Turn a new-project intake into a Farplane substrate, readiness audit, optional code scaffold, and harness-creator handoff.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/init-advisor/SKILL.md",
      "tags": [
        "coding",
        "skill"
      ]
    },
    {
      "id": "skill:interval-update",
      "kind": "skill",
      "label": "interval-update",
      "metadata": {
        "description": "Run one Farplane interval automation: review the past window, write a dated report, plan the next window, and emit Pulse or Goal Advisor guidance.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/interval-update/SKILL.md",
      "tags": [
        "harness",
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:knowledge-tidier",
      "kind": "skill",
      "label": "knowledge-tidier",
      "metadata": {
        "description": "Turn bloated knowledge artifacts into ranked keep/cut/reroute decisions when docs, memory, or context surfaces need pruning.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/knowledge-tidier/SKILL.md",
      "tags": [
        "project-ops",
        "skill"
      ]
    },
    {
      "id": "skill:leverage-advisor",
      "kind": "skill",
      "label": "leverage-advisor",
      "metadata": {
        "description": "Turn an existing feature or capability into ranked leverage plays, a rollout roadmap, and the next executable proof step.",
        "source": "local",
        "tier": 2
      },
      "path": "skills/leverage-advisor/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:leverage-rollout",
      "kind": "skill",
      "label": "leverage-rollout",
      "path": "skills/leverage-rollout/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:optimize-harness",
      "kind": "skill",
      "label": "optimize-harness",
      "metadata": {
        "description": "Turn observed Farplane behavior gaps into placement decisions, proof or eval, accepted changes, and review.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/optimize-harness/SKILL.md",
      "tags": [
        "harness",
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:optimize-with-human",
      "kind": "skill",
      "label": "optimize-with-human",
      "path": "skills/optimize-with-human/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:prd",
      "kind": "skill",
      "label": "prd",
      "path": "skills/prd/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:proof-advisor",
      "kind": "skill",
      "label": "proof-advisor",
      "metadata": {
        "description": "Turn behavior claims into proof plans, high-quality cases, proof-surface choices, and execution handoffs.",
        "source": "local",
        "tier": 2
      },
      "path": "skills/proof-advisor/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:prototyping",
      "kind": "skill",
      "label": "prototyping",
      "path": "skills/prototyping/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:pulse-update",
      "kind": "skill",
      "label": "pulse-update",
      "metadata": {
        "description": "Run the Farplane fast executor loop: reconcile outcomes, execute ready tickets up to policy cap, request planning when blocked, and update ledgers.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/pulse-update/SKILL.md",
      "tags": [
        "harness",
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:qa",
      "kind": "skill",
      "label": "qa",
      "metadata": {
        "description": "Turn one selected ticket into proof artifacts, reconciled Done / Proof obligations, and a structured QA result for Stop-hook gating.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/qa/SKILL.md",
      "tags": [
        "coding",
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:reference-grounding",
      "kind": "skill",
      "label": "reference-grounding",
      "path": "skills/reference-grounding/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:research",
      "kind": "skill",
      "label": "research",
      "path": "skills/research/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:review",
      "kind": "skill",
      "label": "review",
      "metadata": {
        "description": "Turn task context, artifacts, and evidence into a TAS review verdict: pass-ready, needs revision, blocked, or invalid.",
        "source": "local",
        "tier": 2
      },
      "path": "skills/review/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:self-improve",
      "kind": "skill",
      "label": "self-improve",
      "path": "skills/self-improve/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:skill-creator",
      "kind": "skill",
      "label": "skill-creator",
      "metadata": {
        "description": "Turn a reusable workflow or capability idea into a Farplane skill package with frontmatter, todo path, references, and proof surfaces.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/skill-creator/SKILL.md",
      "tags": [
        "route-target",
        "skill",
        "skills"
      ]
    },
    {
      "id": "skill:skill-maintenance",
      "kind": "skill",
      "label": "skill-maintenance",
      "metadata": {
        "description": "Turn skill behavior deltas, lesson hardening, or skill compaction into owner-local skill edits, eval/gotcha updates, registry sync, audit proof, and review.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/skill-maintenance/SKILL.md",
      "tags": [
        "route-target",
        "skill",
        "skills"
      ]
    },
    {
      "id": "skill:spec-to-ticket",
      "kind": "skill",
      "label": "spec-to-ticket",
      "path": "skills/spec-to-ticket/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:testing",
      "kind": "skill",
      "label": "testing",
      "path": "skills/testing/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:update-memory",
      "kind": "skill",
      "label": "update-memory",
      "metadata": {
        "description": "Turn project history, memory, README, docs, lessons, troubles, and recent progress into consolidated project context and doc deltas.",
        "source": "local",
        "tier": 3
      },
      "path": "skills/update-memory/SKILL.md",
      "tags": [
        "project-ops",
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:update-strategy",
      "kind": "skill",
      "label": "update-strategy",
      "path": "skills/update-strategy/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "skill:visual-qa",
      "kind": "skill",
      "label": "visual-qa",
      "path": "skills/visual-qa/SKILL.md",
      "tags": [
        "route-target",
        "skill"
      ]
    },
    {
      "id": "state:.agents/skills/*/skill.md",
      "kind": "state",
      "label": ".agents/skills/**/SKILL.md",
      "path": ".agents/skills/*/skill.md",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:.farplane/automation/action-outcomes.jsonl",
      "kind": "state",
      "label": "Pulse action outcomes",
      "path": ".farplane/automation/action-outcomes.jsonl",
      "tags": [
        "pulse",
        "runtime"
      ]
    },
    {
      "id": "state:.farplane/automation/decisions.jsonl",
      "kind": "state",
      "label": "Pulse decisions",
      "path": ".farplane/automation/decisions.jsonl",
      "tags": [
        "pulse",
        "runtime"
      ]
    },
    {
      "id": "state:.farplane/automation/heartbeat-policy.json",
      "kind": "state",
      "label": ".farplane/automation/heartbeat-policy.json",
      "path": ".farplane/automation/heartbeat-policy.json",
      "tags": [
        "parsed"
      ]
    },
    {
      "id": "state:.farplane/automation/rewards.jsonl",
      "kind": "state",
      "label": "Pulse rewards",
      "path": ".farplane/automation/rewards.jsonl",
      "tags": [
        "pulse",
        "runtime"
      ]
    },
    {
      "id": "state:.farplane/automation/spawned-threads.jsonl",
      "kind": "state",
      "label": "Spawned thread ledger",
      "path": ".farplane/automation/spawned-threads.jsonl",
      "tags": [
        "pulse",
        "runtime"
      ]
    },
    {
      "id": "state:.farplane/state/run-ledger.json",
      "kind": "state",
      "label": "Run ledger",
      "path": ".farplane/state/run-ledger.json",
      "tags": [
        "runtime"
      ]
    },
    {
      "id": "state:active-ticket",
      "kind": "state",
      "label": "active ticket",
      "path": "active-ticket",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:agents/project_rules/architecture/docs/tickets/qa/farplane-scaffolds",
      "kind": "state",
      "label": "AGENTS/PROJECT_RULES/ARCHITECTURE/docs/tickets/qa/farplane scaffolds",
      "path": "agents/project_rules/architecture/docs/tickets/qa/farplane-scaffolds",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:and-starter-prd-ticket",
      "kind": "state",
      "label": "and starter PRD ticket",
      "path": "and-starter-prd-ticket",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:applied_change",
      "kind": "state",
      "label": "applied_change",
      "path": "applied_change",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:approval-handoff",
      "kind": "state",
      "label": "approval handoff",
      "path": "approval-handoff",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:archive-only",
      "kind": "state",
      "label": "archive only when preserving exact source rows",
      "path": "archive-only",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:archive_ref",
      "kind": "state",
      "label": "archive_ref",
      "path": "archive_ref",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:board-files",
      "kind": "state",
      "label": "board files",
      "path": "board-files",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:bootstrap-brief",
      "kind": "state",
      "label": "bootstrap brief",
      "path": "bootstrap-brief",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:captured-artifacts",
      "kind": "state",
      "label": "captured artifacts",
      "path": "captured-artifacts",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:case-matrix",
      "kind": "state",
      "label": "case matrix",
      "path": "case-matrix",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:changed-artifacts",
      "kind": "state",
      "label": "changed artifacts",
      "path": "changed-artifacts",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:consolidation-reports",
      "kind": "state",
      "label": "consolidation reports",
      "path": "consolidation-reports",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:current-repo-state",
      "kind": "state",
      "label": "current repo state",
      "path": "current-repo-state",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:docs-only",
      "kind": "state",
      "label": "docs only when an owning project path and approval are explicit",
      "path": "docs-only",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:edited_skill.eval_task",
      "kind": "state",
      "label": "edited_skill.eval_task",
      "path": "edited_skill.eval_task",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:edited_skill.qa_checklist",
      "kind": "state",
      "label": "edited_skill.qa_checklist",
      "path": "edited_skill.qa_checklist",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:edited_skill.references",
      "kind": "state",
      "label": "edited_skill.references",
      "path": "edited_skill.references",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:edited_skill.skill.md",
      "kind": "state",
      "label": "edited_skill.SKILL.md",
      "path": "edited_skill.skill.md",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:eval-drain-processed-state",
      "kind": "state",
      "label": "eval-drain processed state",
      "path": "eval-drain-processed-state",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:eval-rows",
      "kind": "state",
      "label": "eval rows",
      "path": "eval-rows",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:eval-tasks",
      "kind": "state",
      "label": "eval tasks",
      "path": "eval-tasks",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:eval_case",
      "kind": "state",
      "label": "eval_case",
      "path": "eval_case",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:eval_task.json-files",
      "kind": "state",
      "label": "eval_task.json files",
      "path": "eval_task.json-files",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:evals",
      "kind": "state",
      "label": "evals",
      "path": "evals",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:evidence",
      "kind": "state",
      "label": "evidence",
      "path": "evidence",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:existing-evals",
      "kind": "state",
      "label": "existing evals",
      "path": "existing-evals",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:existing-repo-files",
      "kind": "state",
      "label": "existing repo files",
      "path": "existing-repo-files",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:existing-tests",
      "kind": "state",
      "label": "existing tests",
      "path": "existing-tests",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:expected-behavior",
      "kind": "state",
      "label": "expected behavior",
      "path": "expected-behavior",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:experiment_artifact",
      "kind": "state",
      "label": "experiment_artifact",
      "path": "experiment_artifact",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:external-source-notes",
      "kind": "state",
      "label": "external source notes when needed",
      "path": "external-source-notes",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:feature-docs",
      "kind": "state",
      "label": "feature docs",
      "path": "feature-docs",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:feature-registry",
      "kind": "state",
      "label": "feature registry",
      "path": "feature-registry",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:fixtures",
      "kind": "state",
      "label": "fixtures",
      "path": "fixtures",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:gap-reports",
      "kind": "state",
      "label": "gap reports",
      "path": "gap-reports",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:goal-loop-contract",
      "kind": "state",
      "label": "goal-loop contract",
      "path": "goal-loop-contract",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:goals_delta_candidate",
      "kind": "state",
      "label": "goals_delta_candidate",
      "path": "goals_delta_candidate",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:hardcase-metadata",
      "kind": "state",
      "label": "hardcase metadata",
      "path": "hardcase-metadata",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:harness-algebra",
      "kind": "state",
      "label": "harness algebra",
      "path": "harness-algebra",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:harness-doctrine",
      "kind": "state",
      "label": "harness doctrine",
      "path": "harness-doctrine",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:interval-reports",
      "kind": "state",
      "label": "interval reports",
      "path": "interval-reports",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:interval_reports",
      "kind": "state",
      "label": "interval_reports",
      "path": "interval_reports",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:leverage_plan.md-ticket_seed-autoresearch_seed-goal_recommendation",
      "kind": "state",
      "label": "leverage_plan.md? ticket_seed? autoresearch_seed? goal_recommendation",
      "path": "leverage_plan.md-ticket_seed-autoresearch_seed-goal_recommendation",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:linked-prd/specs/docs",
      "kind": "state",
      "label": "linked PRD/specs/docs",
      "path": "linked-prd/specs/docs",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:linked-specs/docs",
      "kind": "state",
      "label": "linked specs/docs",
      "path": "linked-specs/docs",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:listed-files",
      "kind": "state",
      "label": "listed files",
      "path": "listed-files",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:local-contracts",
      "kind": "state",
      "label": "local contracts",
      "path": "local-contracts",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:logs/traces/failures",
      "kind": "state",
      "label": "logs/traces/failures",
      "path": "logs/traces/failures",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:memory",
      "kind": "state",
      "label": "memory",
      "path": "memory",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:metrics",
      "kind": "state",
      "label": "metrics",
      "path": "metrics",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:operator-context",
      "kind": "state",
      "label": "operator context",
      "path": "operator-context",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:operator-intent",
      "kind": "state",
      "label": "operator intent",
      "path": "operator-intent",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:optional-.farplane/reports/interval/<interval_id>/context/<yyyy-mm-ddthhmmssz>.md",
      "kind": "state",
      "label": "optional .farplane/reports/interval/<interval_id>/context/<YYYY-MM-DDTHHMMSSZ>.md",
      "path": "optional-.farplane/reports/interval/<interval_id>/context/<yyyy-mm-ddthhmmssz>.md",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:optional-.farplane/state/skill-maintenance/processed-learning.jsonl",
      "kind": "state",
      "label": "optional .farplane/state/skill-maintenance/processed-learning.jsonl",
      "path": "optional-.farplane/state/skill-maintenance/processed-learning.jsonl",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:optional-design.md",
      "kind": "state",
      "label": "optional design.md",
      "path": "optional-design.md",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:optional-design.md-or-agent-testability-brief",
      "kind": "state",
      "label": "optional design.md or Agent Testability Brief",
      "path": "optional-design.md-or-agent-testability-brief",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:optional-design.md-recommendation",
      "kind": "state",
      "label": "optional design.md recommendation",
      "path": "optional-design.md-recommendation",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:optional-stack-scaffold",
      "kind": "state",
      "label": "optional stack scaffold",
      "path": "optional-stack-scaffold",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:or-handoff-notes",
      "kind": "state",
      "label": "or handoff notes",
      "path": "or-handoff-notes",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:prior-proof",
      "kind": "state",
      "label": "prior proof",
      "path": "prior-proof",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:prior_audits",
      "kind": "state",
      "label": "prior_audits",
      "path": "prior_audits",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:processed-state",
      "kind": "state",
      "label": "processed state",
      "path": "processed-state",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:program.md",
      "kind": "state",
      "label": "program.md",
      "path": "program.md",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:progress",
      "kind": "state",
      "label": "progress",
      "path": "progress",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:progress.md",
      "kind": "state",
      "label": "progress.md",
      "path": "progress.md",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:project-profile",
      "kind": "state",
      "label": "project profile",
      "path": "project-profile",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:proof-plan",
      "kind": "state",
      "label": "proof plan",
      "path": "proof-plan",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:proof-route",
      "kind": "state",
      "label": "proof route",
      "path": "proof-route",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:pulse_reports",
      "kind": "state",
      "label": "pulse_reports",
      "path": "pulse_reports",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:qa-checklists",
      "kind": "state",
      "label": "QA checklists",
      "path": "qa-checklists",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:qa-findings",
      "kind": "state",
      "label": "QA findings",
      "path": "qa-findings",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:qa_checklist",
      "kind": "state",
      "label": "qa_checklist",
      "path": "qa_checklist",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:readme",
      "kind": "state",
      "label": "README",
      "path": "readme",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:readme/agents/docs/tickets",
      "kind": "state",
      "label": "README/AGENTS/docs/tickets when present",
      "path": "readme/agents/docs/tickets",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:references",
      "kind": "state",
      "label": "references",
      "path": "references",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:registry",
      "kind": "state",
      "label": "registry",
      "path": "registry",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:related-skills",
      "kind": "state",
      "label": "related skills",
      "path": "related-skills",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:relevant-code",
      "kind": "state",
      "label": "relevant code",
      "path": "relevant-code",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:relevant-skills/docs",
      "kind": "state",
      "label": "relevant skills/docs",
      "path": "relevant-skills/docs",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:relevant-specs/skills/docs",
      "kind": "state",
      "label": "relevant specs/skills/docs",
      "path": "relevant-specs/skills/docs",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:relevant-strategy-docs",
      "kind": "state",
      "label": "relevant strategy docs",
      "path": "relevant-strategy-docs",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:relevant-surfaces",
      "kind": "state",
      "label": "relevant surfaces",
      "path": "relevant-surfaces",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:result.json",
      "kind": "state",
      "label": "result.json",
      "path": "result.json",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:review-artifact",
      "kind": "state",
      "label": "review artifact",
      "path": "review-artifact",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:review_receipt",
      "kind": "state",
      "label": "review_receipt",
      "path": "review_receipt",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:reviewer_receipts",
      "kind": "state",
      "label": "reviewer_receipts",
      "path": "reviewer_receipts",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:run-artifacts",
      "kind": "state",
      "label": "run artifacts",
      "path": "run-artifacts",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:run_artifacts",
      "kind": "state",
      "label": "run_artifacts",
      "path": "run_artifacts",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:runtime-handoff",
      "kind": "state",
      "label": "runtime handoff",
      "path": "runtime-handoff",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:scripts",
      "kind": "state",
      "label": "scripts",
      "path": "scripts",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:skill-eval_task.json-files",
      "kind": "state",
      "label": "skill eval_task.json files",
      "path": "skill-eval_task.json-files",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:skill-local-audit",
      "kind": "state",
      "label": "skill-local audit",
      "path": "skill-local-audit",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:skill-registry",
      "kind": "state",
      "label": "skill registry",
      "path": "skill-registry",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:skill-system-docs",
      "kind": "state",
      "label": "skill-system docs",
      "path": "skill-system-docs",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:skill.md",
      "kind": "state",
      "label": "SKILL.md",
      "path": "skill.md",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:specs",
      "kind": "state",
      "label": "specs",
      "path": "specs",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:target-skill",
      "kind": "state",
      "label": "target skill",
      "path": "target-skill",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:target-surfaces",
      "kind": "state",
      "label": "target surfaces",
      "path": "target-surfaces",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:target_file",
      "kind": "state",
      "label": "target_file",
      "path": "target_file",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:task-context",
      "kind": "state",
      "label": "task context",
      "path": "task-context",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:template",
      "kind": "state",
      "label": "template",
      "path": "template",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:test-case-drafts",
      "kind": "state",
      "label": "test-case drafts",
      "path": "test-case-drafts",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:ticket",
      "kind": "state",
      "label": "ticket",
      "path": "ticket",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:ticket-handoff",
      "kind": "state",
      "label": "ticket? handoff",
      "path": "ticket-handoff",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:ticket-state/links",
      "kind": "state",
      "label": "ticket State/Links",
      "path": "ticket-state/links",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:ticket.md",
      "kind": "state",
      "label": "ticket.md",
      "path": "ticket.md",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:ticket.md-updates",
      "kind": "state",
      "label": "ticket.md updates",
      "path": "ticket.md-updates",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:ticket/program/progress-generated-goal-prompt-or-recommendation",
      "kind": "state",
      "label": "ticket/program/progress? generated goal prompt? or recommendation",
      "path": "ticket/program/progress-generated-goal-prompt-or-recommendation",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:tickets/progress/pm-reports",
      "kind": "state",
      "label": "tickets/progress/PM reports",
      "path": "tickets/progress/pm-reports",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "state:worker-thread-refs",
      "kind": "state",
      "label": "worker thread refs when available",
      "path": "worker-thread-refs",
      "tags": [
        "abstract-state"
      ]
    },
    {
      "id": "ticket:tickets/**/progress.md",
      "kind": "ticket",
      "label": "tickets/**/progress.md",
      "path": "tickets/**/progress.md",
      "tags": [
        "parsed"
      ]
    },
    {
      "id": "ticket:tickets/TASK-*/artifacts/",
      "kind": "ticket",
      "label": "Ticket proof artifacts",
      "path": "tickets/TASK-*/artifacts/",
      "tags": [
        "proof",
        "ticket"
      ]
    },
    {
      "id": "ticket:tickets/TASK-*/program.md",
      "kind": "ticket",
      "label": "Goal Packet program",
      "path": "tickets/TASK-*/program.md",
      "tags": [
        "goal-packet",
        "ticket"
      ]
    },
    {
      "id": "ticket:tickets/TASK-*/progress.md",
      "kind": "ticket",
      "label": "Goal Packet progress",
      "path": "tickets/TASK-*/progress.md",
      "tags": [
        "goal-packet",
        "ticket"
      ]
    },
    {
      "id": "ticket:tickets/TASK-*/ticket.md",
      "kind": "ticket",
      "label": "Ticket contract",
      "path": "tickets/TASK-*/ticket.md",
      "tags": [
        "goal-packet",
        "ticket"
      ]
    },
    {
      "id": "ticket:tickets/specs",
      "kind": "ticket",
      "label": "tickets/specs",
      "path": "tickets/specs",
      "tags": [
        "parsed"
      ]
    }
  ],
  "schema_version": "1.0.0",
  "source": {
    "generator": "skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py",
    "included_optional_nodes": {
      "abstract_state": true,
      "fsa_state_nodes": true,
      "gates": true
    },
    "missing_skills": [],
    "mode": "full",
    "target_skills": [
      "init-advisor",
      "horizon-advisor",
      "goal-advisor",
      "harness-advisor",
      "proof-advisor",
      "impl-plan",
      "leverage-advisor",
      "pulse-update",
      "interval-update",
      "automation-advisor",
      "update-memory",
      "optimize-harness",
      "skill-creator",
      "skill-maintenance",
      "knowledge-tidier",
      "eval",
      "qa",
      "review"
    ]
  }
};
