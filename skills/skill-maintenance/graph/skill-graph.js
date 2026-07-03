window.SKILL_GRAPH = {
  "counts": {
    "edge_types": {
      "common-chain": 21,
      "markdown-ref": 321,
      "todo-chain": 332
    },
    "edges": 674,
    "nodes": 101,
    "skill_heat_config": {
      "default_top_n": 25,
      "event_types": [
        "control_surface_detected",
        "hook_result",
        "learning_review_launched",
        "skill_requested"
      ],
      "recent_days": 7,
      "window_days": 30
    },
    "skill_heat_event_types": [
      "control_surface_detected",
      "hook_result",
      "learning_review_launched",
      "skill_requested"
    ],
    "sources": {
      "external": 3,
      "local": 98
    },
    "tiers": {
      "1": 6,
      "2": 38,
      "3": 57
    }
  },
  "edges": [
    {
      "label": "markdown-ref",
      "source": "advise",
      "target": "best-of-worlds",
      "target_ref": "best-of-worlds",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "advise",
      "target": "deliberative-advice",
      "target_ref": "deliberative-advice",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "advise",
      "target": "deliberative-advice",
      "target_ref": "deliberative-advice",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "advise",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "agent-behavior-test",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "agent-behavior-test",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "agent-behavior-test",
      "target": "agent-qa-test",
      "target_ref": "agent-qa-test",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "agent-behavior-test",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "agent-behavior-test",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "agent-behavior-test",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "agent-behavior-test",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "agent-qa-test",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "agent-qa-test",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "agent-qa-test",
      "target": "agent-behavior-test",
      "target_ref": "agent-behavior-test",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "agent-qa-test",
      "target": "qa",
      "target_ref": "qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "agent-qa-test",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "agent-qa-test",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "agent-qa-test",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "agent-qa-test",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "agent-qa-test",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "agent-testability-plan",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "agent-testability-plan",
      "target": "spec-to-ticket",
      "target_ref": "spec-to-ticket",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "apify",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "apify",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "apify",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "apify",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "apify",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "apify",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "automation-advisor",
      "target": "interval-update",
      "target_ref": "interval-update",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "automation-advisor",
      "target": "pulse-update",
      "target_ref": "pulse-update",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "bash-efficiency",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "bash-efficiency",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "bash-efficiency",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "bash-efficiency",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "bash-efficiency",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "bash-efficiency",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "best-of-worlds",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "best-of-worlds",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "best-of-worlds",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "best-of-worlds",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "research#researchgap",
      "source": "best-of-worlds",
      "target": "research",
      "target_ref": "research#researchgap",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchparity",
      "source": "best-of-worlds",
      "target": "research",
      "target_ref": "research#researchparity",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchsource-synthesis",
      "source": "best-of-worlds",
      "target": "research",
      "target_ref": "research#researchsource-synthesis",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "best-of-worlds",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "best-of-worlds",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "brainstorm",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "brainstorm",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "brainstorm",
      "target": "deep-interview",
      "target_ref": "deep-interview",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "brainstorm",
      "target": "prd",
      "target_ref": "prd",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "brainstorm",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "brainstorm",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "brainstorm",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "brainstorm",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "brainstorm",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "close-ticket",
      "target": "commit-message",
      "target_ref": "commit-message",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "close-ticket",
      "target": "commit-message",
      "target_ref": "commit-message",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "close-ticket",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "close-ticket",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "code-review",
      "target": "consolidate",
      "target_ref": "consolidate",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "code-review",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "code-review",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "codebase-analysis",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "codebase-analysis",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "codebase-analysis",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "codebase-analysis",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "codebase-analysis",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "codebase-analysis",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "commit-message",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "commit-message",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "commit-message",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "commit-message",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "commit-message",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "commit-message",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "data-viz",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "data-viz",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "data-viz",
      "target": "frontend-design",
      "target_ref": "frontend-design",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "data-viz",
      "target": "frontend-design",
      "target_ref": "frontend-design",
      "type": "todo-chain"
    },
    {
      "label": "research#researchofficial-docs",
      "source": "data-viz",
      "target": "research",
      "target_ref": "research#researchofficial-docs",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchparity",
      "source": "data-viz",
      "target": "research",
      "target_ref": "research#researchparity",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "data-viz",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "data-viz",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "data-viz",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deep-interview",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "deep-interview",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deep-interview",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "deep-interview",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deep-interview",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "deep-interview",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deep-system-design",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "deep-system-design",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "deep-system-design",
      "target": "agent-testability-plan",
      "target_ref": "agent-testability-plan",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "deep-system-design",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deep-system-design",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "deep-system-design",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deep-system-design",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "deep-system-design",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "deep-system-design",
      "target": "spec-to-ticket",
      "target_ref": "spec-to-ticket",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deep-ui-design",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "deep-ui-design",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deep-ui-design",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "deep-ui-design",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deep-ui-design",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "deep-ui-design",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "delegate-cli",
      "target": "demo",
      "target_ref": "demo",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "delegate-cli",
      "target": "demo",
      "target_ref": "demo",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "delegate-cli",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "delegate-cli",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "delegate-cli",
      "target": "qa",
      "target_ref": "qa",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "delegate-cli",
      "target": "qa",
      "target_ref": "qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "delegate-frontend",
      "target": "delegate-cli",
      "target_ref": "delegate-cli",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "delegate-frontend",
      "target": "delegate-cli",
      "target_ref": "delegate-cli",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "delegate-frontend",
      "target": "demo",
      "target_ref": "demo",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.7",
      "order": 7,
      "source": "delegate-frontend",
      "target": "demo",
      "target_ref": "demo",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "delegate-frontend",
      "target": "functional-ui",
      "target_ref": "functional-ui",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "delegate-frontend",
      "target": "functional-ui",
      "target_ref": "functional-ui",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "delegate-frontend",
      "target": "qa",
      "target_ref": "qa",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "delegate-frontend",
      "target": "qa",
      "target_ref": "qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "delegate-frontend",
      "target": "vercel-react-best-practices",
      "target_ref": "vercel-react-best-practices",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "delegate-frontend",
      "target": "vercel-react-best-practices",
      "target_ref": "vercel-react-best-practices",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "delegate-frontend",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "delegate-frontend",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "delegate-frontend",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "delegate-frontend",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deliberative-advice",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "deliberative-advice",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deliberative-advice",
      "target": "budget-advisor",
      "target_ref": "budget-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "deliberative-advice",
      "target": "budget-advisor",
      "target_ref": "budget-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deliberative-advice",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "deliberative-advice",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deliberative-advice",
      "target": "research",
      "target_ref": "research",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "deliberative-advice",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "deliberative-advice",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "demo",
      "target": "agent-browser",
      "target_ref": "agent-browser",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "demo",
      "target": "agent-browser",
      "target_ref": "agent-browser",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "demo",
      "target": "close-ticket",
      "target_ref": "close-ticket",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "demo",
      "target": "qa",
      "target_ref": "qa",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "demo",
      "target": "qa",
      "target_ref": "qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "demo-realism",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "demo-realism",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "demo-realism",
      "target": "functional-ui",
      "target_ref": "functional-ui",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "demo-realism",
      "target": "functional-ui",
      "target_ref": "functional-ui",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "demo-realism",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "demo-realism",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "todo-chain"
    },
    {
      "label": "research#researchcompetitor",
      "source": "demo-realism",
      "target": "research",
      "target_ref": "research#researchcompetitor",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchparity",
      "source": "demo-realism",
      "target": "research",
      "target_ref": "research#researchparity",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchuser-grounding",
      "source": "demo-realism",
      "target": "research",
      "target_ref": "research#researchuser-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "demo-realism",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "demo-realism",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "demo-realism",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "doc-advisor",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "doc-advisor",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "doc-advisor",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "doc-advisor",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "doc-advisor",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "eval",
      "target": "consolidate",
      "target_ref": "consolidate",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "eval",
      "target": "deliberative-advice",
      "target_ref": "deliberative-advice",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "eval",
      "target": "skill-maintenance",
      "target_ref": "skill-maintenance",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "execute",
      "target": "prototyping",
      "target_ref": "prototyping",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "execute",
      "target": "prototyping",
      "target_ref": "prototyping",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "execute",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "execute",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "execute",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "execute",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "external-patterns",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "external-patterns",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "external-patterns",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "external-patterns",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "external-patterns",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "external-patterns",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "feed-scout",
      "target": "best-of-worlds",
      "target_ref": "best-of-worlds",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "feed-scout",
      "target": "best-of-worlds",
      "target_ref": "best-of-worlds",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "feed-scout",
      "target": "harness-scout",
      "target_ref": "harness-scout",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "feed-scout",
      "target": "harness-scout",
      "target_ref": "harness-scout",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "feed-scout",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "feed-scout",
      "target": "skill-creator",
      "target_ref": "skill-creator",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "feed-scout",
      "target": "skill-creator",
      "target_ref": "skill-creator",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "feed-scout",
      "target": "summarize",
      "target_ref": "summarize",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "feed-scout",
      "target": "summarize",
      "target_ref": "summarize",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "find-skills",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "find-skills",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "find-skills",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "find-skills",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "find-skills",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "find-skills",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-craft",
      "target": "agent-browser",
      "target_ref": "agent-browser",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.13",
      "order": 13,
      "source": "frontend-craft",
      "target": "agent-browser",
      "target_ref": "agent-browser",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-craft",
      "target": "best-of-worlds",
      "target_ref": "best-of-worlds",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "frontend-craft",
      "target": "best-of-worlds",
      "target_ref": "best-of-worlds",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-craft",
      "target": "frontend-design",
      "target_ref": "frontend-design",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "frontend-craft",
      "target": "frontend-design",
      "target_ref": "frontend-design",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-craft",
      "target": "functional-ui",
      "target_ref": "functional-ui",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "frontend-craft",
      "target": "functional-ui",
      "target_ref": "functional-ui",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-craft",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.7",
      "order": 7,
      "source": "frontend-craft",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-craft",
      "target": "landing-page",
      "target_ref": "landing-page",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "frontend-craft",
      "target": "landing-page",
      "target_ref": "landing-page",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-craft",
      "target": "remotion",
      "target_ref": "remotion",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.9",
      "order": 9,
      "source": "frontend-craft",
      "target": "remotion",
      "target_ref": "remotion",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-craft",
      "target": "remotion-render",
      "target_ref": "remotion-render",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.10",
      "order": 10,
      "source": "frontend-craft",
      "target": "remotion-render",
      "target_ref": "remotion-render",
      "type": "todo-chain"
    },
    {
      "label": "research#researchuser-grounding",
      "source": "frontend-craft",
      "target": "research",
      "target_ref": "research#researchuser-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "frontend-craft",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-craft",
      "target": "video-generation",
      "target_ref": "video-generation",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.8",
      "order": 8,
      "source": "frontend-craft",
      "target": "video-generation",
      "target_ref": "video-generation",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-craft",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "frontend-craft",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "frontend-craft",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-craft",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.12",
      "order": 12,
      "source": "frontend-craft",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-craft",
      "target": "web-design-guidelines",
      "target_ref": "web-design-guidelines",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.11",
      "order": 11,
      "source": "frontend-craft",
      "target": "web-design-guidelines",
      "target_ref": "web-design-guidelines",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-design",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "frontend-design",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-design",
      "target": "functional-ui",
      "target_ref": "functional-ui",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "frontend-design",
      "target": "functional-ui",
      "target_ref": "functional-ui",
      "type": "todo-chain"
    },
    {
      "label": "research#researchcode-patterns",
      "source": "frontend-design",
      "target": "research",
      "target_ref": "research#researchcode-patterns",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchofficial-docs",
      "source": "frontend-design",
      "target": "research",
      "target_ref": "research#researchofficial-docs",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "frontend-design",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "frontend-design",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "frontend-design",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "functional-ui",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "functional-ui",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "label": "research#researchcompetitor",
      "source": "functional-ui",
      "target": "research",
      "target_ref": "research#researchcompetitor",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchparity",
      "source": "functional-ui",
      "target": "research",
      "target_ref": "research#researchparity",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchuser-grounding",
      "source": "functional-ui",
      "target": "research",
      "target_ref": "research#researchuser-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "functional-ui",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "functional-ui",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "functional-ui",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "functional-ui",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "gap-analysis",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "gap-analysis",
      "target": "eval",
      "target_ref": "eval",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "gap-analysis",
      "target": "harness-advisor",
      "target_ref": "harness-advisor",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "gap-analysis",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "gap-analysis",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "goal-advisor",
      "target": "demo",
      "target_ref": "demo",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "goal-advisor",
      "target": "horizon-advisor",
      "target_ref": "horizon-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "goal-advisor",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "goal-advisor",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "goal-advisor",
      "target": "optimize-with-human",
      "target_ref": "optimize-with-human",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "goal-advisor",
      "target": "optimize-with-human",
      "target_ref": "optimize-with-human",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "goal-advisor",
      "target": "qa",
      "target_ref": "qa",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "goal-advisor",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "hardening",
      "target": "budget-advisor",
      "target_ref": "budget-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "hardening",
      "target": "budget-advisor",
      "target_ref": "budget-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "hardening",
      "target": "proof-advisor",
      "target_ref": "proof-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "hardening",
      "target": "proof-advisor",
      "target_ref": "proof-advisor",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "hardening",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "hardening",
      "target": "testing",
      "target_ref": "testing",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "harness-advisor",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "harness-advisor",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "harness-advisor",
      "target": "eval",
      "target_ref": "eval",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "harness-advisor",
      "target": "gap-analysis",
      "target_ref": "gap-analysis",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "harness-advisor",
      "target": "optimize-harness",
      "target_ref": "optimize-harness",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-advisor",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "harness-advisor",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-advisor",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "harness-advisor",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-creator",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "harness-creator",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-creator",
      "target": "harness-advisor",
      "target_ref": "harness-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.9",
      "order": 9,
      "source": "harness-creator",
      "target": "harness-advisor",
      "target_ref": "harness-advisor",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "harness-creator",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-creator",
      "target": "init-advisor",
      "target_ref": "init-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "harness-creator",
      "target": "init-advisor",
      "target_ref": "init-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-creator",
      "target": "interval-update",
      "target_ref": "interval-update",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "harness-creator",
      "target": "interval-update",
      "target_ref": "interval-update",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-creator",
      "target": "optimize-with-human",
      "target_ref": "optimize-with-human",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.11",
      "order": 11,
      "source": "harness-creator",
      "target": "optimize-with-human",
      "target_ref": "optimize-with-human",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "harness-creator",
      "target": "pulse-update",
      "target_ref": "pulse-update",
      "type": "todo-chain"
    },
    {
      "label": "research#researchcompetitor",
      "source": "harness-creator",
      "target": "research",
      "target_ref": "research#researchcompetitor",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchgap",
      "source": "harness-creator",
      "target": "research",
      "target_ref": "research#researchgap",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchparity",
      "source": "harness-creator",
      "target": "research",
      "target_ref": "research#researchparity",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchuser-grounding",
      "source": "harness-creator",
      "target": "research",
      "target_ref": "research#researchuser-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "harness-creator",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-creator",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.12",
      "order": 12,
      "source": "harness-creator",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-creator",
      "target": "skill-creator",
      "target_ref": "skill-creator",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.10",
      "order": 10,
      "source": "harness-creator",
      "target": "skill-creator",
      "target_ref": "skill-creator",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-creator",
      "target": "update-memory",
      "target_ref": "update-memory",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.8",
      "order": 8,
      "source": "harness-creator",
      "target": "update-memory",
      "target_ref": "update-memory",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-creator",
      "target": "update-strategy",
      "target_ref": "update-strategy",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.7",
      "order": 7,
      "source": "harness-creator",
      "target": "update-strategy",
      "target_ref": "update-strategy",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "best-of-worlds",
      "target_ref": "best-of-worlds",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "harness-scout",
      "target": "best-of-worlds",
      "target_ref": "best-of-worlds",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "brainstorm",
      "target_ref": "brainstorm",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "codebase-analysis",
      "target_ref": "codebase-analysis",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "doc-advisor",
      "target_ref": "doc-advisor",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "external-patterns",
      "target_ref": "external-patterns",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "harness-advisor",
      "target_ref": "harness-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "harness-scout",
      "target": "harness-advisor",
      "target_ref": "harness-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "harness-scout",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "media-ingest",
      "target_ref": "media-ingest",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchgap",
      "source": "harness-scout",
      "target": "research",
      "target_ref": "research#researchgap",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchparity",
      "source": "harness-scout",
      "target": "research",
      "target_ref": "research#researchparity",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchsource-synthesis",
      "source": "harness-scout",
      "target": "research",
      "target_ref": "research#researchsource-synthesis",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "harness-scout",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "self-improve",
      "target_ref": "self-improve",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "summarize",
      "target_ref": "summarize",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "harness-scout",
      "target": "summarize",
      "target_ref": "summarize",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "harness-scout",
      "target": "video-understanding",
      "target_ref": "video-understanding",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "horizon-advisor",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "horizon-advisor",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "horizon-advisor",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "image-generation",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "image-generation",
      "target": "product-photography",
      "target_ref": "product-photography",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "image-generation",
      "target": "social-content",
      "target_ref": "social-content",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.8",
      "order": 8,
      "source": "impl-plan",
      "target": "agent-qa-test",
      "target_ref": "agent-qa-test",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.9",
      "order": 9,
      "source": "impl-plan",
      "target": "close-ticket",
      "target_ref": "close-ticket",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "impl-plan",
      "target": "deep-system-design",
      "target_ref": "deep-system-design",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "impl-plan",
      "target": "deep-system-design",
      "target_ref": "deep-system-design",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "impl-plan",
      "target": "doc-advisor",
      "target_ref": "doc-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "impl-plan",
      "target": "doc-advisor",
      "target_ref": "doc-advisor",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "impl-plan",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "common-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "impl-plan",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "impl-plan",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "impl-plan",
      "target": "qa",
      "target_ref": "qa",
      "type": "todo-chain"
    },
    {
      "label": "research#researchgap",
      "source": "impl-plan",
      "target": "research",
      "target_ref": "research#researchgap",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchparity",
      "source": "impl-plan",
      "target": "research",
      "target_ref": "research#researchparity",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "impl-plan",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "impl-plan",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.7",
      "order": 7,
      "source": "impl-plan",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "infographic",
      "target": "data-viz",
      "target_ref": "data-viz",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "infographic",
      "target": "data-viz",
      "target_ref": "data-viz",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "infographic",
      "target": "diagramming",
      "target_ref": "diagramming",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "infographic",
      "target": "diagramming",
      "target_ref": "diagramming",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "infographic",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "infographic",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "infographic",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "infographic",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "infographic",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "infographic",
      "target": "social-content",
      "target_ref": "social-content",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "infographic",
      "target": "social-content",
      "target_ref": "social-content",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "infographic",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "markdown-ref"
    },
    {
      "label": "common_chains.after",
      "source": "infographic",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "infographic",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "infographic",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "ingest-content",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "markdown-ref"
    },
    {
      "label": "common_chains.after",
      "source": "ingest-content",
      "target": "media-ingest",
      "target_ref": "media-ingest",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "ingest-content",
      "target": "media-ingest",
      "target_ref": "media-ingest",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "ingest-content",
      "target": "media-ingest",
      "target_ref": "media-ingest",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "ingest-content",
      "target": "summarize",
      "target_ref": "summarize",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "ingest-content",
      "target": "summarize",
      "target_ref": "summarize",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "ingest-content",
      "target": "summarize",
      "target_ref": "summarize",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "ingest-content",
      "target": "video-generation",
      "target_ref": "video-generation",
      "type": "markdown-ref"
    },
    {
      "label": "common_chains.after",
      "source": "ingest-content",
      "target": "video-understanding",
      "target_ref": "video-understanding",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "ingest-content",
      "target": "video-understanding",
      "target_ref": "video-understanding",
      "type": "markdown-ref"
    },
    {
      "label": "common_chains.after",
      "source": "ingest-content",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "ingest-content",
      "target": "visual-design",
      "target_ref": "visual-design",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "init-advisor",
      "target": "automation-advisor",
      "target_ref": "automation-advisor",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "init-advisor",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "init-advisor",
      "target": "harness-advisor",
      "target_ref": "harness-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "init-advisor",
      "target": "harness-creator",
      "target_ref": "harness-creator",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "init-advisor",
      "target": "harness-creator",
      "target_ref": "harness-creator",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "init-advisor",
      "target": "horizon-advisor",
      "target_ref": "horizon-advisor",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "init-advisor",
      "target": "skill-creator",
      "target_ref": "skill-creator",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "instagram-account",
      "target": "apify",
      "target_ref": "apify",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "instagram-account",
      "target": "feed-scout",
      "target_ref": "feed-scout",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "interval-update",
      "target": "doc-advisor",
      "target_ref": "doc-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "interval-update",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "interval-update",
      "target": "update-memory",
      "target_ref": "update-memory",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "knowledge-tidier",
      "target": "consolidate",
      "target_ref": "consolidate",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "knowledge-tidier",
      "target": "consolidate",
      "target_ref": "consolidate",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "knowledge-tidier",
      "target": "doc-advisor",
      "target_ref": "doc-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "knowledge-tidier",
      "target": "doc-advisor",
      "target_ref": "doc-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "knowledge-tidier",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "knowledge-tidier",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "knowledge-tidier",
      "target": "skill-maintenance",
      "target_ref": "skill-maintenance",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "knowledge-tidier",
      "target": "skill-maintenance",
      "target_ref": "skill-maintenance",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "knowledge-tidier",
      "target": "update-memory",
      "target_ref": "update-memory",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "knowledge-tidier",
      "target": "update-memory",
      "target_ref": "update-memory",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "landing-page",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "landing-page",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "leverage-advisor",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "leverage-advisor",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "leverage-advisor",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "leverage-advisor",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.7",
      "order": 7,
      "source": "leverage-advisor",
      "target": "harness-advisor",
      "target_ref": "harness-advisor",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "leverage-advisor",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "leverage-advisor",
      "target": "leverage-rollout",
      "target_ref": "leverage-rollout",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.8",
      "order": 8,
      "source": "leverage-advisor",
      "target": "leverage-rollout",
      "target_ref": "leverage-rollout",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "leverage-advisor",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "leverage-advisor",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "leverage-advisor",
      "target": "prototyping",
      "target_ref": "prototyping",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "leverage-advisor",
      "target": "prototyping",
      "target_ref": "prototyping",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "leverage-advisor",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "leverage-advisor",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "leverage-rollout",
      "target": "eval",
      "target_ref": "eval",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "leverage-rollout",
      "target": "eval",
      "target_ref": "eval",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "leverage-rollout",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "leverage-rollout",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "leverage-rollout",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "leverage-rollout",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "leverage-rollout",
      "target": "leverage-advisor",
      "target_ref": "leverage-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "leverage-rollout",
      "target": "leverage-advisor",
      "target_ref": "leverage-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "leverage-rollout",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "leverage-rollout",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "leverage-rollout",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "media-ingest",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "media-ingest",
      "target": "summarize",
      "target_ref": "summarize",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "media-ingest",
      "target": "summarize",
      "target_ref": "summarize",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "media-ingest",
      "target": "video-understanding",
      "target_ref": "video-understanding",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "metric-advisor",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "metric-advisor",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "metric-advisor",
      "target": "optimize-harness",
      "target_ref": "optimize-harness",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "metric-advisor",
      "target": "proof-advisor",
      "target_ref": "proof-advisor",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "metric-advisor",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "metric-advisor",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "metric-advisor",
      "target": "self-improve",
      "target_ref": "self-improve",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "metric-advisor",
      "target": "self-improve",
      "target_ref": "self-improve",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "notion-task-field-fill",
      "target": "interval-update",
      "target_ref": "interval-update",
      "type": "common-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "optimize-harness",
      "target": "agent-browser",
      "target_ref": "agent-browser",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-harness",
      "target": "eval",
      "target_ref": "eval",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-harness",
      "target": "gap-analysis",
      "target_ref": "gap-analysis",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "optimize-harness",
      "target": "gap-analysis",
      "target_ref": "gap-analysis",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-harness",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.11",
      "order": 11,
      "source": "optimize-harness",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-harness",
      "target": "harness-advisor",
      "target_ref": "harness-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "optimize-harness",
      "target": "harness-advisor",
      "target_ref": "harness-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-harness",
      "target": "horizon-advisor",
      "target_ref": "horizon-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "optimize-harness",
      "target": "horizon-advisor",
      "target_ref": "horizon-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-harness",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.10",
      "order": 10,
      "source": "optimize-harness",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-harness",
      "target": "leverage-advisor",
      "target_ref": "leverage-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "optimize-harness",
      "target": "leverage-advisor",
      "target_ref": "leverage-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-harness",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-harness",
      "target": "proof-advisor",
      "target_ref": "proof-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "optimize-harness",
      "target": "proof-advisor",
      "target_ref": "proof-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-harness",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-harness",
      "target": "self-improve",
      "target_ref": "self-improve",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.7",
      "order": 7,
      "source": "optimize-harness",
      "target": "self-improve",
      "target_ref": "self-improve",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-harness",
      "target": "skill-creator",
      "target_ref": "skill-creator",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.9",
      "order": 9,
      "source": "optimize-harness",
      "target": "skill-creator",
      "target_ref": "skill-creator",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-harness",
      "target": "skill-maintenance",
      "target_ref": "skill-maintenance",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.8",
      "order": 8,
      "source": "optimize-harness",
      "target": "skill-maintenance",
      "target_ref": "skill-maintenance",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-with-human",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "optimize-with-human",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "optimize-with-human",
      "target": "telegram-message",
      "target_ref": "telegram-message",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "optimize-with-human",
      "target": "telegram-message",
      "target_ref": "telegram-message",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "plan",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "plan",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "plan",
      "target": "deliberative-advice",
      "target_ref": "deliberative-advice",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "plan",
      "target": "prototyping",
      "target_ref": "prototyping",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "plan",
      "target": "prototyping",
      "target_ref": "prototyping",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "plan",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "plan",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "plan",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "plan",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "plan",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "pr-review-watch",
      "target": "pr-runtime",
      "target_ref": "pr-runtime",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "pr-review-watch",
      "target": "pr-runtime",
      "target_ref": "pr-runtime",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "pr-review-watch",
      "target": "pr-runtime",
      "target_ref": "pr-runtime",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "pr-review-watch",
      "target": "review",
      "target_ref": "review",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "pr-review-watch",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "pr-review-watch",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "pr-review-watch",
      "target": "telegram-message",
      "target_ref": "telegram-message",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "pr-runtime",
      "target": "qa",
      "target_ref": "qa",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "pr-runtime",
      "target": "qa",
      "target_ref": "qa",
      "type": "todo-chain"
    },
    {
      "label": "research#researchcompetitor",
      "source": "prd",
      "target": "research",
      "target_ref": "research#researchcompetitor",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchparity",
      "source": "prd",
      "target": "research",
      "target_ref": "research#researchparity",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchuser-grounding",
      "source": "prd",
      "target": "research",
      "target_ref": "research#researchuser-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "prd",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "prd",
      "target": "spec-to-ticket",
      "target_ref": "spec-to-ticket",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "prd",
      "target": "spec-to-ticket",
      "target_ref": "spec-to-ticket",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "prd",
      "target": "spec-to-ticket",
      "target_ref": "spec-to-ticket",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "product-photography",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "product-photography",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "product-photography",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "product-photography",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "todo-chain"
    },
    {
      "label": "research#researchcompetitor",
      "source": "product-photography",
      "target": "research",
      "target_ref": "research#researchcompetitor",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchparity",
      "source": "product-photography",
      "target": "research",
      "target_ref": "research#researchparity",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "product-photography",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "proof-advisor",
      "target": "agent-behavior-test",
      "target_ref": "agent-behavior-test",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "proof-advisor",
      "target": "agent-qa-test",
      "target_ref": "agent-qa-test",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "proof-advisor",
      "target": "eval",
      "target_ref": "eval",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "proof-advisor",
      "target": "eval",
      "target_ref": "eval",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "proof-advisor",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "proof-advisor",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "proof-advisor",
      "target": "qa",
      "target_ref": "qa",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.8",
      "order": 8,
      "source": "proof-advisor",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "proof-advisor",
      "target": "testing",
      "target_ref": "testing",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "proof-advisor",
      "target": "testing",
      "target_ref": "testing",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.7",
      "order": 7,
      "source": "proof-advisor",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "prototyping",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "qa",
      "target": "agent-browser",
      "target_ref": "agent-browser",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "qa",
      "target": "agent-browser",
      "target_ref": "agent-browser",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "qa",
      "target": "close-ticket",
      "target_ref": "close-ticket",
      "type": "common-chain"
    },
    {
      "label": "common_chains.after",
      "source": "qa",
      "target": "demo",
      "target_ref": "demo",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "qa",
      "target": "pr-runtime",
      "target_ref": "pr-runtime",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "qa",
      "target": "pr-runtime",
      "target_ref": "pr-runtime",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "qa",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "qa",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "react-flow",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "react-flow",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "react-flow",
      "target": "frontend-design",
      "target_ref": "frontend-design",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "react-flow",
      "target": "frontend-design",
      "target_ref": "frontend-design",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "react-flow",
      "target": "functional-ui",
      "target_ref": "functional-ui",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "react-flow",
      "target": "functional-ui",
      "target_ref": "functional-ui",
      "type": "todo-chain"
    },
    {
      "label": "research#researchofficial-docs",
      "source": "react-flow",
      "target": "research",
      "target_ref": "research#researchofficial-docs",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchparity",
      "source": "react-flow",
      "target": "research",
      "target_ref": "research#researchparity",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "react-flow",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "react-flow",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "react-flow",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "refactoring",
      "target": "budget-advisor",
      "target_ref": "budget-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "refactoring",
      "target": "budget-advisor",
      "target_ref": "budget-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "refactoring",
      "target": "code-review",
      "target_ref": "code-review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "refactoring",
      "target": "proof-advisor",
      "target_ref": "proof-advisor",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "refactoring",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "refactoring",
      "target": "testing",
      "target_ref": "testing",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "refactoring",
      "target": "testing",
      "target_ref": "testing",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "reference-grounding",
      "target": "research",
      "target_ref": "research",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "reference-grounding",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "remotion",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "remotion",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "remotion",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "remotion",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "remotion",
      "target": "remotion-render",
      "target_ref": "remotion-render",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "remotion",
      "target": "remotion-render",
      "target_ref": "remotion-render",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "remotion",
      "target": "remotion-render",
      "target_ref": "remotion-render",
      "type": "todo-chain"
    },
    {
      "label": "research#researchcode-patterns",
      "source": "remotion",
      "target": "research",
      "target_ref": "research#researchcode-patterns",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchofficial-docs",
      "source": "remotion",
      "target": "research",
      "target_ref": "research#researchofficial-docs",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "remotion",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "remotion",
      "target": "video-generation",
      "target_ref": "video-generation",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "remotion",
      "target": "video-generation",
      "target_ref": "video-generation",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "remotion",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "remotion",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "remotion-render",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "remotion-render",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "remotion-render",
      "target": "remotion",
      "target_ref": "remotion",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "remotion-render",
      "target": "remotion",
      "target_ref": "remotion",
      "type": "todo-chain"
    },
    {
      "label": "research#researchcode-patterns",
      "source": "remotion-render",
      "target": "research",
      "target_ref": "research#researchcode-patterns",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchofficial-docs",
      "source": "remotion-render",
      "target": "research",
      "target_ref": "research#researchofficial-docs",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "remotion-render",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "remotion-render",
      "target": "video-generation",
      "target_ref": "video-generation",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "remotion-render",
      "target": "video-generation",
      "target_ref": "video-generation",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "remotion-render",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "remotion-render",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "research",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "research",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "research",
      "target": "best-of-worlds",
      "target_ref": "best-of-worlds",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "research",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "research",
      "target": "prototyping",
      "target_ref": "prototyping",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "research",
      "target": "prototyping",
      "target_ref": "prototyping",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "research",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "research",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "research",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "research",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "review",
      "target": "plan",
      "target_ref": "plan",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "runtime-debugging",
      "target": "bash-efficiency",
      "target_ref": "bash-efficiency",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "runtime-debugging",
      "target": "budget-advisor",
      "target_ref": "budget-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "runtime-debugging",
      "target": "budget-advisor",
      "target_ref": "budget-advisor",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "runtime-debugging",
      "target": "testing",
      "target_ref": "testing",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "runtime-debugging",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "self-improve",
      "target": "eval",
      "target_ref": "eval",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "self-improve",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchsource-synthesis",
      "source": "self-improve",
      "target": "research",
      "target_ref": "research#researchsource-synthesis",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "self-improve",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "self-improve",
      "target": "skill-maintenance",
      "target_ref": "skill-maintenance",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "self-improve",
      "target": "skill-maintenance",
      "target_ref": "skill-maintenance",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "skill-creator",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "skill-creator",
      "target": "agent-behavior-test",
      "target_ref": "agent-behavior-test",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "skill-creator",
      "target": "deliberative-advice",
      "target_ref": "deliberative-advice",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "skill-creator",
      "target": "eval",
      "target_ref": "eval",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "skill-creator",
      "target": "harness-advisor",
      "target_ref": "harness-advisor",
      "type": "todo-chain"
    },
    {
      "label": "research#researchparity",
      "source": "skill-creator",
      "target": "research",
      "target_ref": "research#researchparity",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchsource-synthesis",
      "source": "skill-creator",
      "target": "research",
      "target_ref": "research#researchsource-synthesis",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "skill-creator",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "skill-maintenance",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "skill-maintenance",
      "target": "consolidate",
      "target_ref": "consolidate",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "skill-maintenance",
      "target": "eval",
      "target_ref": "eval",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "skill-maintenance",
      "target": "eval",
      "target_ref": "eval",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "skill-maintenance",
      "target": "gap-analysis",
      "target_ref": "gap-analysis",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "skill-maintenance",
      "target": "harness-advisor",
      "target_ref": "harness-advisor",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "skill-maintenance",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "skill-maintenance",
      "target": "self-improve",
      "target_ref": "self-improve",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "skill-maintenance",
      "target": "self-improve",
      "target_ref": "self-improve",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "skill-registry-ui",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "skill-registry-ui",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "social-content",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "social-content",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "social-content",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "social-content",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "social-content",
      "target": "remotion",
      "target_ref": "remotion",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "social-content",
      "target": "remotion",
      "target_ref": "remotion",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "social-content",
      "target": "remotion-render",
      "target_ref": "remotion-render",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "social-content",
      "target": "remotion-render",
      "target_ref": "remotion-render",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "social-content",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "social-content",
      "target": "video-generation",
      "target_ref": "video-generation",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "social-content",
      "target": "video-generation",
      "target_ref": "video-generation",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "spec-to-ticket",
      "target": "impl-plan",
      "target_ref": "impl-plan",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "spec-to-ticket",
      "target": "research",
      "target_ref": "research",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "spec-to-ticket",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "summarize",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "summarize",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "summarize",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "summarize",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "summarize",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "summarize",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "taste-loop",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "taste-loop",
      "target": "functional-ui",
      "target_ref": "functional-ui",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "taste-loop",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "taste-loop",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "taste-loop",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.8",
      "order": 8,
      "source": "taste-loop",
      "target": "metric-advisor",
      "target_ref": "metric-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "taste-loop",
      "target": "optimize-with-human",
      "target_ref": "optimize-with-human",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.9",
      "order": 9,
      "source": "taste-loop",
      "target": "optimize-with-human",
      "target_ref": "optimize-with-human",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "taste-loop",
      "target": "remotion",
      "target_ref": "remotion",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "taste-loop",
      "target": "remotion-render",
      "target_ref": "remotion-render",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "taste-loop",
      "target": "self-improve",
      "target_ref": "self-improve",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "taste-loop",
      "target": "self-improve",
      "target_ref": "self-improve",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.7",
      "order": 7,
      "source": "taste-loop",
      "target": "skill-maintenance",
      "target_ref": "skill-maintenance",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "testing",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "testing",
      "target": "advise",
      "target_ref": "advise",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "testing",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "testing",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "testing",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "testing",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "update-memory",
      "target": "consolidate",
      "target_ref": "consolidate",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "update-memory",
      "target": "doc-advisor",
      "target_ref": "doc-advisor",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "update-memory",
      "target": "doc-advisor",
      "target_ref": "doc-advisor",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "update-memory",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "update-memory",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "update-memory",
      "target": "skill-maintenance",
      "target_ref": "skill-maintenance",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "update-strategy",
      "target": "goal-advisor",
      "target_ref": "goal-advisor",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "update-strategy",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "update-strategy",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "video-generation",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "video-generation",
      "target": "remotion",
      "target_ref": "remotion",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "video-generation",
      "target": "remotion-render",
      "target_ref": "remotion-render",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "video-generation",
      "target": "video-production",
      "target_ref": "video-production",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "video-generation",
      "target": "visual-qa",
      "target_ref": "visual-qa",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "video-production",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.6",
      "order": 6,
      "source": "video-production",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "video-production",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "video-production",
      "target": "image-generation",
      "target_ref": "image-generation",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "video-production",
      "target": "remotion",
      "target_ref": "remotion",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "video-production",
      "target": "remotion",
      "target_ref": "remotion",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "video-production",
      "target": "remotion",
      "target_ref": "remotion",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "video-production",
      "target": "remotion-render",
      "target_ref": "remotion-render",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "video-production",
      "target": "remotion-render",
      "target_ref": "remotion-render",
      "type": "todo-chain"
    },
    {
      "label": "research#researchcompetitor",
      "source": "video-production",
      "target": "research",
      "target_ref": "research#researchcompetitor",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchparity",
      "source": "video-production",
      "target": "research",
      "target_ref": "research#researchparity",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "video-production",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "video-production",
      "target": "video-generation",
      "target_ref": "video-generation",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "video-production",
      "target": "video-generation",
      "target_ref": "video-generation",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "video-production",
      "target": "video-generation",
      "target_ref": "video-generation",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "video-understanding",
      "target": "advise",
      "target_ref": "advise",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "video-understanding",
      "target": "harness-advisor",
      "target_ref": "harness-advisor",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "video-understanding",
      "target": "harness-scout",
      "target_ref": "harness-scout",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "video-understanding",
      "target": "media-ingest",
      "target_ref": "media-ingest",
      "type": "markdown-ref"
    },
    {
      "label": "markdown-ref",
      "source": "visual-design",
      "target": "best-of-worlds",
      "target_ref": "best-of-worlds",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.3",
      "order": 3,
      "source": "visual-design",
      "target": "best-of-worlds",
      "target_ref": "best-of-worlds",
      "type": "todo-chain"
    },
    {
      "label": "common_chains.after",
      "source": "visual-design",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "common-chain"
    },
    {
      "label": "markdown-ref",
      "source": "visual-design",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.5",
      "order": 5,
      "source": "visual-design",
      "target": "frontend-craft",
      "target_ref": "frontend-craft",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "visual-design",
      "target": "frontend-design",
      "target_ref": "frontend-design",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.4",
      "order": 4,
      "source": "visual-design",
      "target": "frontend-design",
      "target_ref": "frontend-design",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "visual-design",
      "target": "functional-ui",
      "target_ref": "functional-ui",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "visual-design",
      "target": "functional-ui",
      "target_ref": "functional-ui",
      "type": "todo-chain"
    },
    {
      "label": "research#researchcompetitor",
      "source": "visual-design",
      "target": "research",
      "target_ref": "research#researchcompetitor",
      "type": "markdown-ref"
    },
    {
      "label": "research#researchparity",
      "source": "visual-design",
      "target": "research",
      "target_ref": "research#researchparity",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "visual-design",
      "target": "research",
      "target_ref": "research",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "visual-qa",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "visual-qa",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "web-design-guidelines",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "web-design-guidelines",
      "target": "reference-grounding",
      "target_ref": "reference-grounding",
      "type": "todo-chain"
    },
    {
      "label": "markdown-ref",
      "source": "web-design-guidelines",
      "target": "review",
      "target_ref": "review",
      "type": "markdown-ref"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "web-design-guidelines",
      "target": "review",
      "target_ref": "review",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.1",
      "order": 1,
      "source": "x-account",
      "target": "apify",
      "target_ref": "apify",
      "type": "todo-chain"
    },
    {
      "chain_source": "todo_list",
      "label": "todo.2",
      "order": 2,
      "source": "x-account",
      "target": "feed-scout",
      "target_ref": "feed-scout",
      "type": "todo-chain"
    }
  ],
  "generated_at": "2026-07-02T19:53:31+00:00",
  "nodes": [
    {
      "description": "Turn an under-specified decision into three options, tradeoffs, and one recommendation when the user asks for advice.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "advise",
      "label": "advise",
      "methods": [],
      "path": "skills/advise/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 1,
          "incoming_ref_count": 28,
          "last_referenced_at": "2026-06-06T14:11:49.058419Z",
          "top_referrers": [
            {
              "invocation_count_window": 7,
              "last_invoked_at": "2026-06-06T14:11:49.058419Z",
              "skill": "brainstorm"
            }
          ],
          "window_referrer_invocations": 7
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": true,
          "status": "moderate",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "harden",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 28,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 1
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 1,
      "todo_skill_refs": [
        "deliberative-advice"
      ]
    },
    {
      "description": "Compress artifacts into their minimal owner-correct form when material value must be preserved while duplication, fluff, or sprawl is removed.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "consolidate",
      "label": "consolidate",
      "methods": [],
      "path": "skills/consolidate/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 5,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.3.5"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 5,
          "method_count": 0,
          "outgoing_ref_count": 0,
          "source": "local",
          "tier": 1
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 1,
      "todo_skill_refs": []
    },
    {
      "description": "Turn objectives and evidence into honest metric cards, guard metrics, anti-metrics, and route hints.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "metric-advisor",
      "label": "metric-advisor",
      "methods": [],
      "path": "skills/metric-advisor/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 1,
          "incoming_ref_count": 12,
          "last_referenced_at": "2026-06-30T22:27:59.195216Z",
          "top_referrers": [
            {
              "invocation_count_window": 8,
              "last_invoked_at": "2026-06-30T22:27:59.195216Z",
              "skill": "impl-plan"
            }
          ],
          "window_referrer_invocations": 8
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.3.2"
        },
        "maintenance_recommendation": "harden",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 12,
          "method_count": 0,
          "outgoing_ref_count": 5,
          "source": "local",
          "tier": 1
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 1,
      "todo_skill_refs": [
        "review",
        "self-improve",
        "goal-advisor"
      ]
    },
    {
      "description": "Turn an unproven pattern into the smallest representative proof before expanding scope, automation, volume, or implementation depth.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "prototyping",
      "label": "prototyping",
      "methods": [],
      "path": "skills/prototyping/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 4,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": true,
          "status": "moderate",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 4,
          "method_count": 0,
          "outgoing_ref_count": 1,
          "source": "local",
          "tier": 1
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 1,
      "todo_skill_refs": []
    },
    {
      "description": "Turn claims, plans, or implementation choices into compact evidence notes with the right local, current-web, official, peer, or provided sources.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "reference-grounding",
      "label": "reference-grounding",
      "methods": [],
      "path": "skills/reference-grounding/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 1,
          "incoming_ref_count": 26,
          "last_referenced_at": "2026-06-06T14:11:49.058419Z",
          "top_referrers": [
            {
              "invocation_count_window": 7,
              "last_invoked_at": "2026-06-06T14:11:49.058419Z",
              "skill": "brainstorm"
            }
          ],
          "window_referrer_invocations": 7
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": true,
          "status": "moderate",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "harden",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 26,
          "method_count": 0,
          "outgoing_ref_count": 1,
          "source": "local",
          "tier": 1
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 1,
      "todo_skill_refs": [
        "research"
      ]
    },
    {
      "description": "Turn short feedback, automation, blocker, or artifact-review updates into Telegram notifications that Kenji can understand and answer from Telegram.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "telegram-message",
      "label": "telegram-message",
      "methods": [],
      "path": "skills/telegram-message/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 2,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": "0.3.6"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 2,
          "method_count": 0,
          "outgoing_ref_count": 0,
          "source": "local",
          "tier": 1
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 1,
      "todo_skill_refs": []
    },
    {
      "description": "Capture one isolated agent or Codex exec run into logs, artifacts, and a scored behavior report when behavior needs proof.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "agent-behavior-test",
      "label": "agent-behavior-test",
      "methods": [],
      "path": "skills/agent-behavior-test/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 3,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 3,
          "method_count": 0,
          "outgoing_ref_count": 4,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "agent-qa-test",
        "advise",
        "review"
      ]
    },
    {
      "description": "Automate browser or web-app tasks into clicks, form fills, screenshots, scraped data, or QA evidence when a page must be operated.",
      "eval": "",
      "group": "",
      "has_checklist": false,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "agent-browser",
      "label": "agent-browser",
      "methods": [],
      "path": "skills/agent-browser/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 4,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": false,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "low",
          "template_version": ""
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 4,
          "method_count": 0,
          "outgoing_ref_count": 0,
          "source": "external",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "external",
      "tier": 2,
      "todo_skill_refs": []
    },
    {
      "description": "Turn an app, skill, prompt, or workflow claim into adversarial QA cases, tester evidence, critique, and rerun guidance.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "agent-qa-test",
      "label": "agent-qa-test",
      "methods": [
        "agent-qa-test:prompt",
        "agent-qa-test:app",
        "agent-qa-test:skill",
        "agent-qa-test:regression"
      ],
      "path": "skills/agent-qa-test/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 1,
          "incoming_ref_count": 3,
          "last_referenced_at": "2026-06-30T22:27:59.195216Z",
          "top_referrers": [
            {
              "invocation_count_window": 8,
              "last_invoked_at": "2026-06-30T22:27:59.195216Z",
              "skill": "impl-plan"
            }
          ],
          "window_referrer_invocations": 8
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": ""
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 3,
          "method_count": 4,
          "outgoing_ref_count": 6,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "qa",
        "visual-qa",
        "reference-grounding",
        "agent-behavior-test",
        "review",
        "advise"
      ]
    },
    {
      "description": "Turn social, video, profile, or place targets into normalized external data through Apify MCP actors when scraping is required.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "apify",
      "label": "apify",
      "methods": [],
      "path": "skills/apify/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 2,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "1.0.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 2,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "advise",
        "review"
      ]
    },
    {
      "description": "Turn shell-heavy filesystem, build, or debug work into safe command sequences and verification when terminal execution is central.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "bash-efficiency",
      "label": "bash-efficiency",
      "methods": [],
      "path": "skills/bash-efficiency/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "1.0.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "advise",
        "review"
      ]
    },
    {
      "description": "Turn multiple projects, repos, tools, or sources into scored feature takeaways and an adapted workflow or implementation plan.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "best-of-worlds",
      "label": "best-of-worlds",
      "methods": [],
      "path": "skills/best-of-worlds/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 6,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 6,
          "method_count": 0,
          "outgoing_ref_count": 4,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "advise",
        "review"
      ]
    },
    {
      "description": "Turn early ambiguous intent into option space, useful questions, and candidate directions before requirements are committed.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 7,
        "distinct_tickets_window": 0,
        "invocation_count_all": 7,
        "invocation_count_recent": 0,
        "invocation_count_window": 7,
        "last_invoked_at": "2026-06-06T14:11:49.058419Z",
        "observed_event_count_all": 14,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "brainstorm",
      "label": "brainstorm",
      "methods": [],
      "path": "skills/brainstorm/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 7,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 7,
          "last_invoked_at": "2026-06-06T14:11:49.058419Z"
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "refine",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 6,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "research",
        "advise",
        "deep-interview",
        "prd",
        "review"
      ]
    },
    {
      "description": "Resolve a budget-aware skill call into a base reviewed path plus optional persona-council lanes when effort changes workflow shape.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "budget-advisor",
      "label": "budget-advisor",
      "methods": [],
      "path": "skills/budget-advisor/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 4,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.3.0"
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 4,
          "method_count": 0,
          "outgoing_ref_count": 0,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": []
    },
    {
      "description": "Turn local diffs and branch context into maintainability, modularity, and code-smell findings before pushing agent-written code.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "code-review",
      "label": "code-review",
      "methods": [],
      "path": "skills/code-review/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 2,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "review"
      ]
    },
    {
      "description": "Turn local codebase questions into file maps, implementation explanations, and reusable pattern findings.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "codebase-analysis",
      "label": "codebase-analysis",
      "methods": [],
      "path": "skills/codebase-analysis/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "advise",
        "review"
      ]
    },
    {
      "description": "Turn local changes or a PR branch into a heavyweight CodeRabbit CLI review result when external review is useful before push.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "coderabbit-review",
      "label": "coderabbit-review",
      "methods": [],
      "path": "skills/coderabbit-review/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "retire_review",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 0,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": []
    },
    {
      "description": "Turn staged or recent git diffs into a compact repo-style commit subject when a commit message is needed.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "commit-message",
      "label": "commit-message",
      "methods": [],
      "path": "skills/commit-message/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "advise",
        "review"
      ]
    },
    {
      "description": "Turn ambiguous user intent into clarified goals, constraints, and decision points through a Socratic interview before execution.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "deep-interview",
      "label": "deep-interview",
      "methods": [],
      "path": "skills/deep-interview/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 1,
          "incoming_ref_count": 1,
          "last_referenced_at": "2026-06-06T14:11:49.058419Z",
          "top_referrers": [
            {
              "invocation_count_window": 7,
              "last_invoked_at": "2026-06-06T14:11:49.058419Z",
              "skill": "brainstorm"
            }
          ],
          "window_referrer_invocations": 7
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "refine",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "advise",
        "review"
      ]
    },
    {
      "description": "Turn underspecified architecture intent into entities, APIs, storage, execution boundaries, retries, and design choices.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "deep-system-design",
      "label": "deep-system-design",
      "methods": [],
      "path": "skills/deep-system-design/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 1,
          "incoming_ref_count": 1,
          "last_referenced_at": "2026-06-30T22:27:59.195216Z",
          "top_referrers": [
            {
              "invocation_count_window": 8,
              "last_invoked_at": "2026-06-30T22:27:59.195216Z",
              "skill": "impl-plan"
            }
          ],
          "window_referrer_invocations": 8
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "refine",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 6,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "advise",
        "review",
        "impl-plan",
        "agent-testability-plan",
        "spec-to-ticket"
      ]
    },
    {
      "description": "Turn unclear UI taste or aesthetic direction into grounded visual preferences and boundaries before design implementation.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "deep-ui-design",
      "label": "deep-ui-design",
      "methods": [],
      "path": "skills/deep-ui-design/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "advise",
        "review"
      ]
    },
    {
      "description": "Turn a high-stakes decision into a budgeted advise council preset with independent perspectives, dissent, and one recommended path.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "deliberative-advice",
      "label": "deliberative-advice",
      "methods": [
        "advise:complex",
        "advise:council"
      ],
      "path": "skills/deliberative-advice/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 4,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.3.2"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 4,
          "method_count": 2,
          "outgoing_ref_count": 5,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "advise",
        "reference-grounding",
        "research",
        "budget-advisor"
      ]
    },
    {
      "description": "Turn plans, specs, tickets, architecture notes, or code explanations into compact Mermaid diagrams and flow traces.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "diagramming",
      "label": "diagramming",
      "methods": [],
      "path": "skills/diagramming/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 0,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": []
    },
    {
      "description": "Turn ticket, plan, or durable doc changes into a docs strategy or grounded doc update with doc-quality checks.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "doc-advisor",
      "label": "doc-advisor",
      "methods": [
        "doc-advisor:strategy",
        "doc-advisor:doc-architecture",
        "doc-advisor:metadata",
        "doc-advisor:feature-system-spec",
        "doc-advisor:finish-gate"
      ],
      "path": "skills/doc-advisor/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 1,
          "incoming_ref_count": 5,
          "last_referenced_at": "2026-06-30T22:27:59.195216Z",
          "top_referrers": [
            {
              "invocation_count_window": 8,
              "last_invoked_at": "2026-06-30T22:27:59.195216Z",
              "skill": "impl-plan"
            }
          ],
          "window_referrer_invocations": 8
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": "0.3.6"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 5,
          "method_count": 5,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "review"
      ]
    },
    {
      "description": "Deprecated compatibility wrapper for native execution phase guidance when no domain execution skill owns the artifact.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "execute",
      "label": "execute",
      "methods": [],
      "path": "skills/execute/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "prototyping",
        "review"
      ]
    },
    {
      "description": "Turn API or implementation uncertainty into GitHub code examples and repository pattern findings.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "external-patterns",
      "label": "external-patterns",
      "methods": [],
      "path": "skills/external-patterns/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "advise",
        "review"
      ]
    },
    {
      "description": "Turn a capability-seeking request into matching installable skills and installation guidance.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "find-skills",
      "label": "find-skills",
      "methods": [],
      "path": "skills/find-skills/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "advise",
        "review"
      ]
    },
    {
      "description": "Turn current-vs-expected behavior evidence into a grounded GapReport with missing pieces, owner surface, and proof path.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "gap-analysis",
      "label": "gap-analysis",
      "methods": [
        "gap-analysis:skill",
        "gap-analysis:harness",
        "gap-analysis:ui",
        "gap-analysis:feature"
      ],
      "path": "skills/gap-analysis/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 3,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 3,
          "method_count": 4,
          "outgoing_ref_count": 4,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding"
      ]
    },
    {
      "description": "Turn working software into lower-risk software with threat, failure, abuse, and resilience proof.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "hardening",
      "label": "hardening",
      "methods": [],
      "path": "skills/hardening/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.3.2"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 4,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "budget-advisor",
        "proof-advisor",
        "review"
      ]
    },
    {
      "description": "Turn a Farplane improvement idea into a recommended owner surface across policy, templates, skills, agents, hooks, tickets, docs, or validators.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "harness-advisor",
      "label": "harness-advisor",
      "methods": [],
      "path": "skills/harness-advisor/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 9,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": true,
          "incoming_ref_count": 9,
          "method_count": 0,
          "outgoing_ref_count": 6,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "skills/harness-advisor",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "gap-analysis",
        "reference-grounding",
        "eval",
        "advise",
        "optimize-harness",
        "review"
      ]
    },
    {
      "description": "Turn an existing feature or capability into ranked leverage plays, a rollout roadmap, and the next executable proof step.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "leverage-advisor",
      "label": "leverage-advisor",
      "methods": [],
      "path": "skills/leverage-advisor/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 2,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 2,
          "method_count": 0,
          "outgoing_ref_count": 8,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "advise",
        "prototyping",
        "metric-advisor",
        "impl-plan",
        "goal-advisor",
        "harness-advisor",
        "leverage-rollout"
      ]
    },
    {
      "description": "Turn URLs or local audio, video, or social media into metadata, transcript status, representative frames, retention notes, and handoff paths.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "media-ingest",
      "label": "media-ingest",
      "methods": [],
      "path": "skills/media-ingest/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 3,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 3,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "summarize"
      ]
    },
    {
      "description": "Route an optimization goal through Goal Advisor with human feedback as the metric and Telegram-first review requests.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "optimize-with-human",
      "label": "optimize-with-human",
      "methods": [],
      "path": "skills/optimize-with-human/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 3,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 3,
          "method_count": 0,
          "outgoing_ref_count": 2,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "goal-advisor",
        "telegram-message"
      ]
    },
    {
      "description": "Turn a goal, context, invoked skills, and budget into composed todos, proof targets, and handoff when planning can reduce wasted work.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "plan",
      "label": "plan",
      "methods": [],
      "path": "skills/plan/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 6,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "research",
        "advise",
        "deliberative-advice",
        "prototyping",
        "review"
      ]
    },
    {
      "description": "Turn behavior claims into proof plans, high-quality cases, proof-surface choices, and execution handoffs.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "proof-advisor",
      "label": "proof-advisor",
      "methods": [],
      "path": "skills/proof-advisor/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 4,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": "0.3.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 4,
          "method_count": 0,
          "outgoing_ref_count": 8,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "metric-advisor",
        "testing",
        "eval",
        "agent-qa-test",
        "agent-behavior-test",
        "qa",
        "visual-qa",
        "review"
      ]
    },
    {
      "description": "Turn working code into simpler behavior-preserving structure with smell metrics, tests, and reviewable proof.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "refactoring",
      "label": "refactoring",
      "methods": [],
      "path": "skills/refactoring/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.3.2"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 5,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "budget-advisor",
        "testing",
        "proof-advisor",
        "review"
      ]
    },
    {
      "description": "Turn current external evidence needs into method-addressed research briefs for parity, gaps, competitors, official docs, code patterns, users, or sources.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "research",
      "label": "research",
      "methods": [
        "research:parity",
        "research:gap",
        "research:competitor",
        "research:official-docs",
        "research:code-patterns",
        "research:user-grounding",
        "research:source-synthesis"
      ],
      "path": "skills/research/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 2,
          "incoming_ref_count": 24,
          "last_referenced_at": "2026-06-30T22:27:59.195216Z",
          "top_referrers": [
            {
              "invocation_count_window": 8,
              "last_invoked_at": "2026-06-30T22:27:59.195216Z",
              "skill": "impl-plan"
            },
            {
              "invocation_count_window": 7,
              "last_invoked_at": "2026-06-06T14:11:49.058419Z",
              "skill": "brainstorm"
            }
          ],
          "window_referrer_invocations": 15
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "refine",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 24,
          "method_count": 7,
          "outgoing_ref_count": 7,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "prototyping",
        "advise",
        "best-of-worlds",
        "impl-plan",
        "review"
      ]
    },
    {
      "description": "Turn task context, artifacts, and evidence into a TAS review verdict: pass-ready, needs revision, blocked, or invalid.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "review",
      "label": "review",
      "methods": [],
      "path": "skills/review/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 2,
          "incoming_ref_count": 41,
          "last_referenced_at": "2026-06-30T22:27:59.195216Z",
          "top_referrers": [
            {
              "invocation_count_window": 8,
              "last_invoked_at": "2026-06-30T22:27:59.195216Z",
              "skill": "impl-plan"
            },
            {
              "invocation_count_window": 7,
              "last_invoked_at": "2026-06-06T14:11:49.058419Z",
              "skill": "brainstorm"
            }
          ],
          "window_referrer_invocations": 15
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "refine",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 41,
          "method_count": 0,
          "outgoing_ref_count": 1,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "plan"
      ]
    },
    {
      "description": "Turn reproducible runtime failures into instrumentation, evidence, root cause, fixes, and proof.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "runtime-debugging",
      "label": "runtime-debugging",
      "methods": [],
      "path": "skills/runtime-debugging/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.3.2"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 4,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "budget-advisor",
        "visual-qa",
        "testing",
        "bash-efficiency"
      ]
    },
    {
      "description": "Turn URLs, podcasts, transcripts, or local files into concise summaries or extracted text.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "summarize",
      "label": "summarize",
      "methods": [],
      "path": "skills/summarize/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 4,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 4,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "advise",
        "review"
      ]
    },
    {
      "description": "Turn a testing need into the right Farplane testing guidance, backpressure, and domain-specific verification path.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "testing",
      "label": "testing",
      "methods": [],
      "path": "skills/testing/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 4,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "1.1.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 4,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "advise",
        "review"
      ]
    },
    {
      "description": "Turn transcripts and representative media frames into storyboard evidence, workflow reconstruction, extracted todos, and proof requirements.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "video-understanding",
      "label": "video-understanding",
      "methods": [],
      "path": "skills/video-understanding/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 3,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 3,
          "method_count": 0,
          "outgoing_ref_count": 4,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": []
    },
    {
      "description": "Turn expected UI specs and screenshots into observed reports, layout assertions, diffs, fix plans, and evidence artifacts.",
      "eval": "eval_task.json",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "visual-qa",
      "label": "visual-qa",
      "methods": [],
      "path": "skills/visual-qa/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 1,
          "incoming_ref_count": 14,
          "last_referenced_at": "2026-06-30T22:27:59.195216Z",
          "top_referrers": [
            {
              "invocation_count_window": 8,
              "last_invoked_at": "2026-06-30T22:27:59.195216Z",
              "skill": "impl-plan"
            }
          ],
          "window_referrer_invocations": 8
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 14,
          "method_count": 0,
          "outgoing_ref_count": 1,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "review"
      ]
    },
    {
      "description": "Turn UI code or site review requests into Web Interface Guidelines findings for accessibility, UX, and best-practice compliance.",
      "eval": "",
      "group": "",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "web-design-guidelines",
      "label": "web-design-guidelines",
      "methods": [],
      "path": "skills/web-design-guidelines/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "1.0.0"
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 2,
          "source": "local",
          "tier": 2
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 2,
      "todo_skill_refs": [
        "reference-grounding",
        "review"
      ]
    },
    {
      "description": "Turn a System Design Brief into an Agent Testability Brief with controls, state probes, coordination views, tooling, and proof surfaces.",
      "eval": "",
      "group": "coding",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "agent-testability-plan",
      "label": "agent-testability-plan",
      "methods": [],
      "path": "skills/agent-testability-plan/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "coding",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 2,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "spec-to-ticket",
        "impl-plan"
      ]
    },
    {
      "description": "Design or revise Farplane Codex automations using full project-owned automations.toml configs and generic Pulse/Interval skill calls.",
      "eval": "",
      "group": "harness",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "automation-advisor",
      "label": "automation-advisor",
      "methods": [],
      "path": "skills/automation-advisor/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "harness",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 2,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "pulse-update",
        "interval-update"
      ]
    },
    {
      "description": "Turn a completed ticket into durable closeout, docs writeback, final checks, commit prep, and optional publish steps.",
      "eval": "",
      "group": "coding",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "close-ticket",
      "label": "close-ticket",
      "methods": [],
      "path": "skills/close-ticket/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 1,
          "incoming_ref_count": 3,
          "last_referenced_at": "2026-06-30T22:27:59.195216Z",
          "top_referrers": [
            {
              "invocation_count_window": 8,
              "last_invoked_at": "2026-06-30T22:27:59.195216Z",
              "skill": "impl-plan"
            }
          ],
          "window_referrer_invocations": 8
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "refine",
        "uniqueness": {
          "group": "coding",
          "has_skill_ui": false,
          "incoming_ref_count": 3,
          "method_count": 0,
          "outgoing_ref_count": 2,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "commit-message",
        "review"
      ]
    },
    {
      "description": "Route Convex project questions to official Convex AI instructions when a repo uses Convex backend files or deployment tooling.",
      "eval": "",
      "group": "backend",
      "has_checklist": false,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "convex",
      "label": "convex",
      "methods": [],
      "path": "skills/convex/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": false,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "low",
          "template_version": "4.0.0"
        },
        "maintenance_recommendation": "retire_review",
        "uniqueness": {
          "group": "backend",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 0,
          "source": "external",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "external",
      "tier": 3,
      "todo_skill_refs": []
    },
    {
      "description": "Turn chart, dashboard, or graph UI needs into D3 or Recharts implementation guidance when data visualization is the core task.",
      "eval": "",
      "group": "frontend-data",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "data-viz",
      "label": "data-viz",
      "methods": [],
      "path": "skills/data-viz/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "frontend-data",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 4,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research",
        "frontend-craft",
        "frontend-design",
        "visual-qa"
      ]
    },
    {
      "description": "Turn bounded Farplane work into an external coding-agent CLI handoff while preserving ticket, log, QA, review, and integration control.",
      "eval": "",
      "group": "harness",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "delegate-cli",
      "label": "delegate-cli",
      "methods": [],
      "path": "skills/delegate-cli/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "harness",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "goal-advisor",
        "qa",
        "demo"
      ]
    },
    {
      "description": "Turn frontend build or polish work into an external CLI handoff while Farplane keeps ticket, QA, visual review, and integration control.",
      "eval": "",
      "group": "frontend",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "delegate-frontend",
      "label": "delegate-frontend",
      "methods": [],
      "path": "skills/delegate-frontend/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "frontend",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 7,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "functional-ui",
        "visual-design",
        "delegate-cli",
        "vercel-react-best-practices",
        "visual-qa",
        "qa",
        "demo"
      ]
    },
    {
      "description": "Turn passing QA artifacts for one ticket into demo-ready outputs and a structured demo result for ticket completion review.",
      "eval": "",
      "group": "coding",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "demo",
      "label": "demo",
      "methods": [],
      "path": "skills/demo/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 4,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "coding",
          "has_skill_ui": false,
          "incoming_ref_count": 4,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "qa",
        "agent-browser"
      ]
    },
    {
      "description": "Turn a fake-feeling MVP or prototype into realistic workflows, demo data, and a presentation-readiness rubric.",
      "eval": "",
      "group": "coding",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "demo-realism",
      "label": "demo-realism",
      "methods": [],
      "path": "skills/demo-realism/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "coding",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 5,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research",
        "functional-ui",
        "visual-design",
        "frontend-craft",
        "impl-plan"
      ]
    },
    {
      "description": "Turn repo cleanup requests into desloppify scan, next, and resolve loops while keeping nested runner ownership explicit.",
      "eval": "",
      "group": "repo-health",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "desloppify",
      "label": "desloppify",
      "methods": [],
      "path": "skills/desloppify/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "retire_review",
        "uniqueness": {
          "group": "repo-health",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 0,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": []
    },
    {
      "description": "Turn agent, prompt, or skill behavior into local eval tasks, boolean or tier judges, run artifacts, and verdicts.",
      "eval": "eval_task.json",
      "group": "harness",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "eval",
      "label": "eval",
      "methods": [
        "eval:onboarding",
        "eval:consolidate"
      ],
      "path": "skills/eval/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 8,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": "0.3.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "harness",
          "has_skill_ui": true,
          "incoming_ref_count": 8,
          "method_count": 2,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "skills/eval/templates/viewer-react",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "deliberative-advice",
        "skill-maintenance"
      ]
    },
    {
      "description": "Turn a FarplaneRunEnvelope into policy validation, compute selection, skill routing, and a filesystem ProofPacket.",
      "eval": "eval_task.json",
      "group": "harness",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "farplane-invocation",
      "label": "farplane-invocation",
      "methods": [],
      "path": "skills/farplane-invocation/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": ""
        },
        "maintenance_recommendation": "retire_review",
        "uniqueness": {
          "group": "harness",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 0,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": []
    },
    {
      "description": "Turn curated feeds into deduped source items, harness-scout runs, pattern synthesis, and proposal tickets or inbox entries.",
      "eval": "eval_task.json",
      "group": "harness",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "feed-scout",
      "label": "feed-scout",
      "methods": [],
      "path": "skills/feed-scout/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 2,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.3.2"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "harness",
          "has_skill_ui": false,
          "incoming_ref_count": 2,
          "method_count": 0,
          "outgoing_ref_count": 5,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "summarize",
        "skill-creator",
        "harness-scout",
        "best-of-worlds",
        "review"
      ]
    },
    {
      "description": "Route frontend build or improvement work through UX, visual design, implementation, assets, standards review, and QA.",
      "eval": "",
      "group": "frontend",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "frontend-craft",
      "label": "frontend-craft",
      "methods": [
        "frontend-craft:composed-scroll-animation"
      ],
      "path": "skills/frontend-craft/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 16,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": true,
          "status": "moderate",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "frontend",
          "has_skill_ui": false,
          "incoming_ref_count": 16,
          "method_count": 1,
          "outgoing_ref_count": 13,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research",
        "functional-ui",
        "landing-page",
        "visual-design",
        "best-of-worlds",
        "frontend-design",
        "image-generation",
        "video-generation",
        "remotion",
        "remotion-render",
        "web-design-guidelines",
        "visual-qa",
        "agent-browser"
      ]
    },
    {
      "description": "Turn settled app UX and visual direction into shadcn, AI Elements, theming, registry, and component implementation guidance.",
      "eval": "",
      "group": "frontend",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "frontend-design",
      "label": "frontend-design",
      "methods": [],
      "path": "skills/frontend-design/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 4,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "1.1.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "frontend",
          "has_skill_ui": false,
          "incoming_ref_count": 4,
          "method_count": 0,
          "outgoing_ref_count": 4,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "frontend-craft",
        "functional-ui",
        "visual-design",
        "research"
      ]
    },
    {
      "description": "Turn broken or unclear product workflows into user stories, UI-state diagnosis, comparable examples, and implementation handoff.",
      "eval": "",
      "group": "frontend",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "functional-ui",
      "label": "functional-ui",
      "methods": [],
      "path": "skills/functional-ui/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 7,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": true,
          "status": "moderate",
          "template_version": "1.1.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "frontend",
          "has_skill_ui": false,
          "incoming_ref_count": 7,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research",
        "visual-design",
        "frontend-craft"
      ]
    },
    {
      "description": "Turn an ambitious request into Goal architecture, ticket-backed loop state, and a native Codex /goal prompt when warranted.",
      "eval": "eval_task.json",
      "group": "harness",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "goal-advisor",
      "label": "goal-advisor",
      "methods": [],
      "path": "skills/goal-advisor/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 1,
          "incoming_ref_count": 12,
          "last_referenced_at": "2026-06-30T22:27:59.195216Z",
          "top_referrers": [
            {
              "invocation_count_window": 8,
              "last_invoked_at": "2026-06-30T22:27:59.195216Z",
              "skill": "impl-plan"
            }
          ],
          "window_referrer_invocations": 8
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "harness",
          "has_skill_ui": false,
          "incoming_ref_count": 12,
          "method_count": 0,
          "outgoing_ref_count": 7,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "optimize-with-human",
        "review",
        "qa",
        "demo",
        "impl-plan"
      ]
    },
    {
      "description": "Turn a high-level project or business idea into split Farplane project files, advisor handoffs, missing-system tickets, and a current milestone.",
      "eval": "",
      "group": "harness",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "harness-creator",
      "label": "harness-creator",
      "methods": [],
      "path": "skills/harness-creator/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "harness",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 12,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research",
        "init-advisor",
        "pulse-update",
        "interval-update",
        "impl-plan",
        "goal-advisor",
        "update-strategy",
        "update-memory",
        "harness-advisor",
        "skill-creator",
        "optimize-with-human",
        "review"
      ]
    },
    {
      "description": "Turn an external source into deduped Farplane feature candidates, adopt/adapt/reject/defer scorecards, and ticket handoffs.",
      "eval": "",
      "group": "harness",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "harness-scout",
      "label": "harness-scout",
      "methods": [],
      "path": "skills/harness-scout/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 2,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "harness",
          "has_skill_ui": false,
          "incoming_ref_count": 2,
          "method_count": 0,
          "outgoing_ref_count": 16,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "summarize",
        "research",
        "harness-advisor",
        "best-of-worlds",
        "impl-plan"
      ]
    },
    {
      "description": "Turn ambiguous long-horizon intent into goals.yaml, KPI trees, feedback-sized projects, and Goal Advisor handoffs.",
      "eval": "",
      "group": "harness",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "horizon-advisor",
      "label": "horizon-advisor",
      "methods": [],
      "path": "skills/horizon-advisor/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 3,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.3.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "harness",
          "has_skill_ui": false,
          "incoming_ref_count": 3,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "review"
      ]
    },
    {
      "description": "Turn image generation or editing requests into inference.sh belt image pipeline outputs when Codex-native imagegen is not enough.",
      "eval": "",
      "group": "content-image",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "image-generation",
      "label": "image-generation",
      "methods": [],
      "path": "skills/image-generation/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 7,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "1.0.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "content-image",
          "has_skill_ui": false,
          "incoming_ref_count": 7,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "product-photography",
        "social-content",
        "frontend-craft"
      ]
    },
    {
      "description": "Turn one selected coding ticket or material implementation request into an approval-ready ticket plan, test strategy, and proof contract.",
      "eval": "eval_task.json",
      "group": "coding",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 8,
        "distinct_tickets_window": 0,
        "invocation_count_all": 8,
        "invocation_count_recent": 1,
        "invocation_count_window": 8,
        "last_invoked_at": "2026-06-30T22:27:59.195216Z",
        "observed_event_count_all": 16,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "impl-plan",
      "label": "impl-plan",
      "methods": [],
      "path": "skills/impl-plan/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 11,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 8,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 1,
          "invocation_count_window": 8,
          "last_invoked_at": "2026-06-30T22:27:59.195216Z"
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": "0.3.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "coding",
          "has_skill_ui": false,
          "incoming_ref_count": 11,
          "method_count": 0,
          "outgoing_ref_count": 10,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research",
        "deep-system-design",
        "doc-advisor",
        "goal-advisor",
        "review",
        "qa",
        "visual-qa",
        "agent-qa-test",
        "close-ticket"
      ]
    },
    {
      "description": "Turn an explanation, dataset, product flow, or argument into a clear infographic brief, layout spec, and production-ready visual asset plan.",
      "eval": "eval_task.json",
      "group": "content-visual",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "infographic",
      "label": "infographic",
      "methods": [
        "infographic:handdrawn-saas-wireframe"
      ],
      "path": "skills/infographic/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": "0.3.6"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "content-visual",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 1,
          "outgoing_ref_count": 7,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "social-content",
        "frontend-craft",
        "data-viz",
        "diagramming",
        "image-generation",
        "visual-qa"
      ]
    },
    {
      "description": "Route liked links, images, videos, files, or notes into analyzed, searchable Resource Bank records with audience-aware Tasty Pack retrieval fields.",
      "eval": "",
      "group": "content-social",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "ingest-content",
      "label": "ingest-content",
      "methods": [],
      "path": "skills/ingest-content/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "content-social",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 6,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "summarize",
        "media-ingest"
      ]
    },
    {
      "description": "Turn a new-project intake into a Farplane substrate, readiness audit, optional code scaffold, and harness-creator handoff.",
      "eval": "eval_task.json",
      "group": "coding",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "init-advisor",
      "label": "init-advisor",
      "methods": [],
      "path": "skills/init-advisor/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": "3.0.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "coding",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 6,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "harness-creator",
        "horizon-advisor",
        "harness-advisor",
        "skill-creator",
        "goal-advisor",
        "automation-advisor"
      ]
    },
    {
      "description": "Turn Instagram account posting or insights requests into validated artifacts, normalized KPI snapshots, or gated API actions.",
      "eval": "",
      "group": "content-social",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "instagram-account",
      "label": "instagram-account",
      "methods": [],
      "path": "skills/instagram-account/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": true,
          "status": "moderate",
          "template_version": "0.3.7"
        },
        "maintenance_recommendation": "retire_review",
        "uniqueness": {
          "group": "content-social",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 2,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "apify",
        "feed-scout"
      ]
    },
    {
      "description": "Run one Farplane interval automation: review the past window, write a dated report, plan the next window, and emit Pulse or Goal Advisor guidance.",
      "eval": "eval_task.json",
      "group": "harness",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "interval-update",
      "label": "interval-update",
      "methods": [],
      "path": "skills/interval-update/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 3,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "harness",
          "has_skill_ui": false,
          "incoming_ref_count": 3,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "update-memory",
        "doc-advisor"
      ]
    },
    {
      "description": "Turn bloated knowledge artifacts into ranked keep/cut/reroute decisions when docs, memory, or context surfaces need pruning.",
      "eval": "eval_task.json",
      "group": "project-ops",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "knowledge-tidier",
      "label": "knowledge-tidier",
      "methods": [],
      "path": "skills/knowledge-tidier/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.3.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "project-ops",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 5,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "consolidate",
        "doc-advisor",
        "skill-maintenance",
        "update-memory",
        "review"
      ]
    },
    {
      "description": "Turn a one-page marketing or launch surface into offer, story arc, sections, assets, motion, and proof before frontend implementation.",
      "eval": "",
      "group": "frontend-content",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "landing-page",
      "label": "landing-page",
      "methods": [],
      "path": "skills/landing-page/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": true,
          "status": "moderate",
          "template_version": "1.0.0"
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "frontend-content",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 1,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "frontend-craft"
      ]
    },
    {
      "description": "Turn a selected leverage play into exemplar proof, extracted rollout pattern, and optional Goal-backed staged rollout.",
      "eval": "",
      "group": "harness",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "leverage-rollout",
      "label": "leverage-rollout",
      "methods": [],
      "path": "skills/leverage-rollout/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "harness",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 6,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "leverage-advisor",
        "impl-plan",
        "goal-advisor",
        "review",
        "eval"
      ]
    },
    {
      "description": "Turn incomplete Notion Tasks into field proposals, safe high-confidence patches, and Telegram review requests.",
      "eval": "",
      "group": "personal-ops",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "notion-task-field-fill",
      "label": "notion-task-field-fill",
      "methods": [],
      "path": "skills/notion-task-field-fill/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.3.7"
        },
        "maintenance_recommendation": "retire_review",
        "uniqueness": {
          "group": "personal-ops",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 1,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": []
    },
    {
      "description": "Turn observed Farplane behavior gaps into placement decisions, proof or eval, accepted changes, and review.",
      "eval": "eval_task.json",
      "group": "harness",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "optimize-harness",
      "label": "optimize-harness",
      "methods": [],
      "path": "skills/optimize-harness/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 2,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "harness",
          "has_skill_ui": false,
          "incoming_ref_count": 2,
          "method_count": 0,
          "outgoing_ref_count": 14,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "gap-analysis",
        "horizon-advisor",
        "leverage-advisor",
        "harness-advisor",
        "proof-advisor",
        "agent-browser",
        "self-improve",
        "skill-maintenance",
        "skill-creator",
        "impl-plan",
        "goal-advisor"
      ]
    },
    {
      "description": "Turn an explicit GitHub PR into bounded polling, review-memory checks, fix loops, and notification-ready status until checks pass.",
      "eval": "",
      "group": "coding",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "pr-review-watch",
      "label": "pr-review-watch",
      "methods": [],
      "path": "skills/pr-review-watch/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "coding",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "pr-runtime",
        "review",
        "telegram-message"
      ]
    },
    {
      "description": "Turn PR follow-up or separate-writer work into an isolated checkout and ticket runtime record.",
      "eval": "",
      "group": "coding",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "pr-runtime",
      "label": "pr-runtime",
      "methods": [],
      "path": "skills/pr-runtime/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 2,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.1.0"
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "coding",
          "has_skill_ui": false,
          "incoming_ref_count": 2,
          "method_count": 0,
          "outgoing_ref_count": 1,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "qa"
      ]
    },
    {
      "description": "Turn a finished branch into smaller non-stacked pull requests when feature seams or layers can be separated.",
      "eval": "",
      "group": "coding",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "pr-splitting",
      "label": "pr-splitting",
      "methods": [],
      "path": "skills/pr-splitting/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "retire_review",
        "uniqueness": {
          "group": "coding",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 0,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": []
    },
    {
      "description": "Turn product intent into a Phase-1 Farplane PRD with requirements, scope, and handoff shape.",
      "eval": "",
      "group": "coding",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "prd",
      "label": "prd",
      "methods": [],
      "path": "skills/prd/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 1,
          "incoming_ref_count": 1,
          "last_referenced_at": "2026-06-06T14:11:49.058419Z",
          "top_referrers": [
            {
              "invocation_count_window": 7,
              "last_invoked_at": "2026-06-06T14:11:49.058419Z",
              "skill": "brainstorm"
            }
          ],
          "window_referrer_invocations": 7
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "1.0.0"
        },
        "maintenance_recommendation": "refine",
        "uniqueness": {
          "group": "coding",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 2,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research",
        "spec-to-ticket"
      ]
    },
    {
      "description": "Turn product-image needs into packshots, lifestyle photos, detail shots, marketplace assets, cutouts, mockups, or product-page visuals.",
      "eval": "",
      "group": "content-image",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "product-photography",
      "label": "product-photography",
      "methods": [
        "product-photography:hero",
        "product-photography:packshot",
        "product-photography:lifestyle",
        "product-photography:detail",
        "product-photography:marketplace",
        "product-photography:cutout-upscale"
      ],
      "path": "skills/product-photography/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "1.0.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "content-image",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 6,
          "outgoing_ref_count": 3,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research",
        "image-generation",
        "frontend-craft"
      ]
    },
    {
      "description": "Run the Farplane fast executor loop: reconcile outcomes, execute ready tickets up to policy cap, request planning when blocked, and update ledgers.",
      "eval": "eval_task.json",
      "group": "harness",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "pulse-update",
      "label": "pulse-update",
      "methods": [],
      "path": "skills/pulse-update/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 2,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "harness",
          "has_skill_ui": false,
          "incoming_ref_count": 2,
          "method_count": 0,
          "outgoing_ref_count": 0,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": []
    },
    {
      "description": "Turn one selected ticket into proof artifacts, reconciled Done and QA Strategy obligations, and a structured QA result for Goal/ticket completion.",
      "eval": "eval_task.json",
      "group": "coding",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "qa",
      "label": "qa",
      "methods": [],
      "path": "skills/qa/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 1,
          "incoming_ref_count": 8,
          "last_referenced_at": "2026-06-30T22:27:59.195216Z",
          "top_referrers": [
            {
              "invocation_count_window": 8,
              "last_invoked_at": "2026-06-30T22:27:59.195216Z",
              "skill": "impl-plan"
            }
          ],
          "window_referrer_invocations": 8
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": ""
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "coding",
          "has_skill_ui": false,
          "incoming_ref_count": 8,
          "method_count": 0,
          "outgoing_ref_count": 5,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "agent-browser",
        "pr-runtime",
        "visual-qa"
      ]
    },
    {
      "description": "Turn graph-app or node-editor needs into React Flow implementation guidance and best-practice patterns.",
      "eval": "",
      "group": "frontend-data",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "react-flow",
      "label": "react-flow",
      "methods": [],
      "path": "skills/react-flow/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "frontend-data",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 5,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research",
        "functional-ui",
        "frontend-craft",
        "frontend-design",
        "visual-qa"
      ]
    },
    {
      "description": "Turn image URLs or local files into 9:16 reel collage backgrounds for shorts, explainers, and green-screen videos.",
      "eval": "",
      "group": "content-social",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "reel-collage",
      "label": "reel-collage",
      "methods": [],
      "path": "skills/reel-collage/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "retire_review",
        "uniqueness": {
          "group": "content-social",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 0,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": []
    },
    {
      "description": "Turn deterministic video requirements into Remotion/React compositions with timing, media, captions, audio, transitions, and render checks.",
      "eval": "",
      "group": "content-video",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "remotion",
      "label": "remotion",
      "methods": [],
      "path": "skills/remotion/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 6,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "content-video",
          "has_skill_ui": false,
          "incoming_ref_count": 6,
          "method_count": 0,
          "outgoing_ref_count": 6,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research",
        "image-generation",
        "video-generation",
        "remotion-render",
        "frontend-craft",
        "visual-qa"
      ]
    },
    {
      "description": "Turn existing React/Remotion video code into rendered MP4 output through inference.sh belt when code-to-video export is needed.",
      "eval": "",
      "group": "content-video",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "remotion-render",
      "label": "remotion-render",
      "methods": [],
      "path": "skills/remotion-render/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 6,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "1.0.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "content-video",
          "has_skill_ui": false,
          "incoming_ref_count": 6,
          "method_count": 0,
          "outgoing_ref_count": 5,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "remotion",
        "research",
        "frontend-craft",
        "visual-qa",
        "video-generation"
      ]
    },
    {
      "description": "Turn an existing skill improvement goal into evals, variant comparison, prompt context, memory, or Goal-backed improvement artifacts.",
      "eval": "eval_task.json",
      "group": "self-improvement",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "self-improve",
      "label": "self-improve",
      "methods": [],
      "path": "skills/self-improve/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 5,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "self-improvement",
          "has_skill_ui": false,
          "incoming_ref_count": 5,
          "method_count": 0,
          "outgoing_ref_count": 4,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research",
        "skill-maintenance"
      ]
    },
    {
      "description": "Turn a reusable workflow or capability idea into a Farplane skill package with frontmatter, todo path, references, and proof surfaces.",
      "eval": "eval_task.json",
      "group": "skills",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill-creator",
      "label": "skill-creator",
      "methods": [],
      "path": "skills/skill-creator/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 4,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": "0.3.2"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "skills",
          "has_skill_ui": false,
          "incoming_ref_count": 4,
          "method_count": 0,
          "outgoing_ref_count": 6,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "harness-advisor",
        "research",
        "eval",
        "agent-behavior-test",
        "advise",
        "deliberative-advice"
      ]
    },
    {
      "description": "Turn skill behavior deltas, lesson hardening, or skill compaction into owner-local skill edits, eval/gotcha updates, registry sync, audit proof, and review.",
      "eval": "eval_task.json",
      "group": "skills",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill-maintenance",
      "label": "skill-maintenance",
      "methods": [],
      "path": "skills/skill-maintenance/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 6,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "skills",
          "has_skill_ui": true,
          "incoming_ref_count": 6,
          "method_count": 0,
          "outgoing_ref_count": 7,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "skills/skill-maintenance/graph/index.html",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "gap-analysis",
        "harness-advisor",
        "advise",
        "eval",
        "self-improve",
        "metric-advisor"
      ]
    },
    {
      "description": "Turn the Farplane skill registry into a refreshed graph UI with rendered skill docs, frontmatter, tier colors, and chain edges.",
      "eval": "",
      "group": "skills",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill-registry-ui",
      "label": "skill-registry-ui",
      "methods": [],
      "path": "skills/skill-registry-ui/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": ""
        },
        "maintenance_recommendation": "retire_review",
        "uniqueness": {
          "group": "skills",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 1,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "visual-qa"
      ]
    },
    {
      "description": "Turn social campaign goals into posts, carousels, threads, calendars, hooks, captions, thumbnails, or cross-platform bundles.",
      "eval": "eval_task.json",
      "group": "content-social",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "social-content",
      "label": "social-content",
      "methods": [
        "social-content:cross-platform",
        "social-content:carousel",
        "social-content:linkedin",
        "social-content:twitter-thread"
      ],
      "path": "skills/social-content/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 2,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": true,
          "status": "low",
          "template_version": "0.3.6"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "content-social",
          "has_skill_ui": false,
          "incoming_ref_count": 2,
          "method_count": 4,
          "outgoing_ref_count": 6,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research",
        "image-generation",
        "video-generation",
        "remotion",
        "remotion-render",
        "frontend-craft"
      ]
    },
    {
      "description": "Turn one SLC spec slice into filesystem tickets with compact summaries, agent contracts, and evidence requirements.",
      "eval": "",
      "group": "coding",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "spec-to-ticket",
      "label": "spec-to-ticket",
      "methods": [],
      "path": "skills/spec-to-ticket/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 3,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "1.5.0"
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "coding",
          "has_skill_ui": false,
          "incoming_ref_count": 3,
          "method_count": 0,
          "outgoing_ref_count": 2,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research"
      ]
    },
    {
      "description": "Run a Codex-native active-hours heartbeat prompt that turns human taste into Goal-backed concept and execution feedback loops.",
      "eval": "eval_task.json",
      "group": "self-improvement",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "taste-loop",
      "label": "taste-loop",
      "methods": [],
      "path": "skills/taste-loop/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": true,
          "has_qa_checklist": false,
          "status": "moderate",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "self-improvement",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 9,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "frontend-craft",
        "functional-ui",
        "remotion",
        "remotion-render",
        "goal-advisor",
        "self-improve",
        "skill-maintenance",
        "metric-advisor",
        "optimize-with-human"
      ]
    },
    {
      "description": "Turn project history, memory, README, docs, lessons, troubles, and recent progress into consolidated project context and doc deltas.",
      "eval": "",
      "group": "project-ops",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "update-memory",
      "label": "update-memory",
      "methods": [],
      "path": "skills/update-memory/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 3,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "project-ops",
          "has_skill_ui": false,
          "incoming_ref_count": 3,
          "method_count": 0,
          "outgoing_ref_count": 4,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "doc-advisor",
        "review"
      ]
    },
    {
      "description": "Turn project goals, tickets, progress, and feedback into strategy deltas, system gaps, experiments, and ticket updates.",
      "eval": "",
      "group": "project-ops",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "update-strategy",
      "label": "update-strategy",
      "methods": [],
      "path": "skills/update-strategy/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "0.2.0"
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "project-ops",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 2,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "review"
      ]
    },
    {
      "description": "Turn React or Next.js code work into Vercel performance-guideline checks for components, pages, and data fetching.",
      "eval": "",
      "group": "frontend",
      "has_checklist": false,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "vercel-react-best-practices",
      "label": "vercel-react-best-practices",
      "methods": [],
      "path": "skills/vercel-react-best-practices/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [],
          "has_checklist": false,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "low",
          "template_version": ""
        },
        "maintenance_recommendation": "watch",
        "uniqueness": {
          "group": "frontend",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 0,
          "outgoing_ref_count": 0,
          "source": "external",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "external",
      "tier": 3,
      "todo_skill_refs": []
    },
    {
      "description": "Turn AI video generation or editing requests into inference.sh belt video outputs such as text-to-video, image-to-video, avatars, edits, or upscales.",
      "eval": "",
      "group": "content-video",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "video-generation",
      "label": "video-generation",
      "methods": [],
      "path": "skills/video-generation/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 6,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "1.0.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "content-video",
          "has_skill_ui": false,
          "incoming_ref_count": 6,
          "method_count": 0,
          "outgoing_ref_count": 5,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "remotion",
        "remotion-render",
        "video-production",
        "frontend-craft",
        "visual-qa"
      ]
    },
    {
      "description": "Turn video deliverable goals into marketing clips, explainers, storyboards, talking-head pieces, demos, or platform ad specs.",
      "eval": "",
      "group": "content-video",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "video-production",
      "label": "video-production",
      "methods": [
        "video-production:marketing",
        "video-production:explainer",
        "video-production:storyboard",
        "video-production:talking-head",
        "video-production:ad-spec"
      ],
      "path": "skills/video-production/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 1,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "1.0.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "content-video",
          "has_skill_ui": false,
          "incoming_ref_count": 1,
          "method_count": 5,
          "outgoing_ref_count": 6,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "research",
        "video-generation",
        "image-generation",
        "remotion",
        "remotion-render",
        "frontend-craft"
      ]
    },
    {
      "description": "Turn a known frontend workflow into typography, color, layout, hierarchy, motion, and anti-generic visual direction.",
      "eval": "",
      "group": "frontend",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "visual-design",
      "label": "visual-design",
      "methods": [],
      "path": "skills/visual-design/SKILL.md",
      "qa_checklist": "",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 7,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval",
            "missing_qa_checklist"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": false,
          "status": "high",
          "template_version": "1.0.0"
        },
        "maintenance_recommendation": "keep",
        "uniqueness": {
          "group": "frontend",
          "has_skill_ui": false,
          "incoming_ref_count": 7,
          "method_count": 0,
          "outgoing_ref_count": 5,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "functional-ui",
        "research",
        "best-of-worlds",
        "frontend-design",
        "frontend-craft"
      ]
    },
    {
      "description": "Turn X account posting or metrics requests into validated drafts, normalized KPI snapshots, or gated API actions.",
      "eval": "",
      "group": "content-social",
      "has_checklist": true,
      "heat": {
        "distinct_threads_window": 0,
        "distinct_tickets_window": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "x-account",
      "label": "x-account",
      "methods": [],
      "path": "skills/x-account/SKILL.md",
      "qa_checklist": "qa_checklist.md",
      "signals": {
        "composition_heat": {
          "hot_referrer_count": 0,
          "incoming_ref_count": 0,
          "last_referenced_at": "",
          "top_referrers": [],
          "window_referrer_invocations": 0
        },
        "direct_heat": {
          "distinct_threads_window": 0,
          "distinct_tickets_window": 0,
          "invocation_count_recent": 0,
          "invocation_count_window": 0,
          "last_invoked_at": ""
        },
        "maintenance_burden": {
          "findings": [
            "missing_eval"
          ],
          "has_checklist": true,
          "has_eval": false,
          "has_qa_checklist": true,
          "status": "moderate",
          "template_version": "0.3.7"
        },
        "maintenance_recommendation": "retire_review",
        "uniqueness": {
          "group": "content-social",
          "has_skill_ui": false,
          "incoming_ref_count": 0,
          "method_count": 0,
          "outgoing_ref_count": 2,
          "source": "local",
          "tier": 3
        }
      },
      "skill_ui": "",
      "source": "local",
      "tier": 3,
      "todo_skill_refs": [
        "apify",
        "feed-scout"
      ]
    }
  ],
  "schema_version": "1.0.0"
};
