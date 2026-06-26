window.FARPLANE_LIFECYCLE_GRAPH = {
  "counts": {
    "edge_confidence": {
      "curated": 43,
      "explicit": 6,
      "parsed": 180
    },
    "edge_types": {
      "consumes": 4,
      "contains": 2,
      "reads": 51,
      "routes_to": 122,
      "triggers": 15,
      "updates": 4,
      "writes": 31
    },
    "edges": 229,
    "fsa_projections": 5,
    "node_kinds": {
      "automation": 3,
      "command": 3,
      "doc": 11,
      "file": 19,
      "hook": 2,
      "report": 2,
      "route": 4,
      "runtime": 1,
      "skill": 40,
      "state": 6,
      "ticket": 6
    },
    "nodes": 97,
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
      "evidence_ref": "skills/goal-advisor/SKILL.md",
      "label": "farplane/goals.md?",
      "source": "skill:goal-advisor",
      "target": "file:farplane/goals.md",
      "type": "reads"
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
      "label": "metric-advisor",
      "source": "skill:goal-advisor",
      "target": "skill:metric-advisor",
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
      "label": "metric-advisor",
      "source": "skill:horizon-advisor",
      "target": "skill:metric-advisor",
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
      "label": "metric-advisor",
      "source": "skill:impl-plan",
      "target": "skill:metric-advisor",
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
      "label": "metric-advisor",
      "source": "skill:interval-update",
      "target": "skill:metric-advisor",
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
      "evidence_ref": "skills/leverage-advisor/SKILL.md",
      "label": "advise",
      "source": "skill:leverage-advisor",
      "target": "skill:advise",
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
      "label": "metric-advisor",
      "source": "skill:leverage-advisor",
      "target": "skill:metric-advisor",
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
      "label": "metric-advisor",
      "source": "skill:optimize-harness",
      "target": "skill:metric-advisor",
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
      "label": "tickets",
      "source": "skill:optimize-harness",
      "target": "ticket:tickets/TASK-*/ticket.md",
      "type": "reads"
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
      "label": "metric-advisor",
      "source": "skill:proof-advisor",
      "target": "skill:metric-advisor",
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
      "label": "caller-owned",
      "source": "skill:review",
      "target": "route:caller-owned",
      "type": "routes_to"
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
  "generated_at": "2026-06-26T09:15:15+00:00",
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
      "id": "skill:metric-advisor",
      "kind": "skill",
      "label": "metric-advisor",
      "path": "skills/metric-advisor/SKILL.md",
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
      "abstract_state": false,
      "fsa_state_nodes": false,
      "gates": false
    },
    "missing_skills": [],
    "mode": "core",
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
