window.FARPLANE_FRAMEWORK_CORE_GRAPH = {
  "counts": {
    "edge_types": {
      "defines-workflow": 7,
      "lifecycle-workflow": 6,
      "literal-path": 59,
      "markdown-link": 1,
      "mentions-skill": 30,
      "routes_to": 8,
      "triggers": 1,
      "updates": 1,
      "workflow-next": 21,
      "workflow-skill": 27,
      "workflow-stage": 6,
      "writes": 5
    },
    "edges": 172,
    "framework_roles": {
      "linked": 43,
      "source": 7,
      "workflow": 7
    },
    "isolated_nodes": 0,
    "linked_nodes": 50,
    "node_kinds": {
      "doc": 7,
      "file": 8,
      "skill": 30,
      "spec": 5,
      "workflow": 7
    },
    "nodes": 57,
    "other_nodes": 0,
    "source_nodes": 7,
    "workflow_nodes": 7
  },
  "edges": [
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/graph-contract.md",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:docs/farplane-framework/graph-contract.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/harness-maintenance.md",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:docs/farplane-framework/harness-maintenance.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/hooks-and-runtime.md",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:docs/farplane-framework/hooks-and-runtime.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/lifecycle.md",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:docs/farplane-framework/lifecycle.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/specs/program-notation.md",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:docs/specs/program-notation.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/specs/steer-pulse-automation.md",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:docs/specs/steer-pulse-automation.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "../specs/steer-pulse-automation.md",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:docs/specs/steer-pulse-automation.md",
      "type": "markdown-link"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/README.md",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:farplane/README.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/automations.md",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:farplane/automations.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/bindings.md",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:farplane/bindings.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/evals.md",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:farplane/evals.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/goals.md",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:farplane/goals.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/harness.md",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:farplane/harness.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/manifest.json",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:farplane/manifest.json",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/pm.json",
      "source": "file:docs/farplane-framework/README.md",
      "target": "file:farplane/pm.json",
      "type": "literal-path"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "automation-advisor",
      "source": "file:docs/farplane-framework/README.md",
      "target": "skill:automation-advisor",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "deep-init-project",
      "source": "file:docs/farplane-framework/README.md",
      "target": "skill:deep-init-project",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "eval",
      "source": "file:docs/farplane-framework/README.md",
      "target": "skill:eval",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "harness-creator",
      "source": "file:docs/farplane-framework/README.md",
      "target": "skill:harness-creator",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "interval-update",
      "source": "file:docs/farplane-framework/README.md",
      "target": "skill:interval-update",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "pulse-update",
      "source": "file:docs/farplane-framework/README.md",
      "target": "skill:pulse-update",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/README.md",
      "projection": "farplane-framework-core",
      "raw_ref": "qa",
      "source": "file:docs/farplane-framework/README.md",
      "target": "skill:qa",
      "type": "mentions-skill"
    },
    {
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/README.md",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "file:docs/farplane-framework/README.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/project-files.md",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "file:docs/farplane-framework/project-files.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/specs/README.md",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "file:docs/specs/README.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/specs/steer-pulse-automation.md",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "file:docs/specs/steer-pulse-automation.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/README.md",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "file:farplane/README.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/automations.md",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "file:farplane/automations.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/bindings.md",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "file:farplane/bindings.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/evals.md",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "file:farplane/evals.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/goals.md",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "file:farplane/goals.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/harness.md",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "file:farplane/harness.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/manifest.json",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "file:farplane/manifest.json",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/pm.json",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "file:farplane/pm.json",
      "type": "literal-path"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "brainstorm",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "skill:brainstorm",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "deep-interview",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "skill:deep-interview",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "execute",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "skill:execute",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "goal-advisor",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "skill:goal-advisor",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "horizon-advisor",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "skill:horizon-advisor",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "impl-plan",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "skill:impl-plan",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "prd",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "skill:prd",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "research",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "skill:research",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "review",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "skill:review",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "skill-maintenance",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "skill:skill-maintenance",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "projection": "farplane-framework-core",
      "raw_ref": "spec-to-ticket",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "skill:spec-to-ticket",
      "type": "mentions-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "label": "Bootstrap",
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:bootstrap",
      "source": "file:docs/farplane-framework/deep-init-critical-path.md",
      "target": "workflow:bootstrap",
      "type": "defines-workflow"
    },
    {
      "from_file": "docs/farplane-framework/graph-contract.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/hooks-and-runtime.md",
      "source": "file:docs/farplane-framework/graph-contract.md",
      "target": "file:docs/farplane-framework/hooks-and-runtime.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/graph-contract.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/lifecycle.md",
      "source": "file:docs/farplane-framework/graph-contract.md",
      "target": "file:docs/farplane-framework/lifecycle.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/graph-contract.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/specs/goal-loop-contract.md",
      "source": "file:docs/farplane-framework/graph-contract.md",
      "target": "file:docs/specs/goal-loop-contract.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/graph-contract.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/specs/steer-pulse-automation.md",
      "source": "file:docs/farplane-framework/graph-contract.md",
      "target": "file:docs/specs/steer-pulse-automation.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/graph-contract.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/goals.md",
      "source": "file:docs/farplane-framework/graph-contract.md",
      "target": "file:farplane/goals.md",
      "type": "literal-path"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/graph-contract.md",
      "projection": "farplane-framework-core",
      "raw_ref": "demo",
      "source": "file:docs/farplane-framework/graph-contract.md",
      "target": "skill:demo",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/graph-contract.md",
      "projection": "farplane-framework-core",
      "raw_ref": "learning-drain",
      "source": "file:docs/farplane-framework/graph-contract.md",
      "target": "skill:learning-drain",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/graph-contract.md",
      "projection": "farplane-framework-core",
      "raw_ref": "plan",
      "source": "file:docs/farplane-framework/graph-contract.md",
      "target": "skill:plan",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/graph-contract.md",
      "projection": "farplane-framework-core",
      "raw_ref": "update-memory",
      "source": "file:docs/farplane-framework/graph-contract.md",
      "target": "skill:update-memory",
      "type": "mentions-skill"
    },
    {
      "from_file": "docs/farplane-framework/harness-maintenance.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/graph-contract.md",
      "source": "file:docs/farplane-framework/harness-maintenance.md",
      "target": "file:docs/farplane-framework/graph-contract.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/harness-maintenance.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/lifecycle.md",
      "source": "file:docs/farplane-framework/harness-maintenance.md",
      "target": "file:docs/farplane-framework/lifecycle.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/harness-maintenance.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/manifest.json",
      "source": "file:docs/farplane-framework/harness-maintenance.md",
      "target": "file:farplane/manifest.json",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/lifecycle.md",
      "source": "file:docs/farplane-framework/hooks-and-runtime.md",
      "target": "file:docs/farplane-framework/lifecycle.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/project-files.md",
      "source": "file:docs/farplane-framework/hooks-and-runtime.md",
      "target": "file:docs/farplane-framework/project-files.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/specs/filesystem-lifecycle.md",
      "source": "file:docs/farplane-framework/hooks-and-runtime.md",
      "target": "file:docs/specs/filesystem-lifecycle.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/specs/steer-pulse-automation.md",
      "source": "file:docs/farplane-framework/hooks-and-runtime.md",
      "target": "file:docs/specs/steer-pulse-automation.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/automations.md",
      "source": "file:docs/farplane-framework/hooks-and-runtime.md",
      "target": "file:farplane/automations.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/pm.json",
      "source": "file:docs/farplane-framework/hooks-and-runtime.md",
      "target": "file:farplane/pm.json",
      "type": "literal-path"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "projection": "farplane-framework-core",
      "raw_ref": "documentation",
      "source": "file:docs/farplane-framework/hooks-and-runtime.md",
      "target": "skill:documentation",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "projection": "farplane-framework-core",
      "raw_ref": "knowledge-tidier",
      "source": "file:docs/farplane-framework/hooks-and-runtime.md",
      "target": "skill:knowledge-tidier",
      "type": "mentions-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "label": "Autonomy loops",
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:autonomy-loops",
      "source": "file:docs/farplane-framework/hooks-and-runtime.md",
      "target": "workflow:autonomy-loops",
      "type": "defines-workflow"
    },
    {
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/README.md",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "file:docs/farplane-framework/README.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/deep-init-critical-path.md",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "file:docs/farplane-framework/deep-init-critical-path.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/graph-contract.md",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "file:docs/farplane-framework/graph-contract.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/hooks-and-runtime.md",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "file:docs/farplane-framework/hooks-and-runtime.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/project-files.md",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "file:docs/farplane-framework/project-files.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/specs/filesystem-lifecycle.md",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "file:docs/specs/filesystem-lifecycle.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/specs/goal-loop-contract.md",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "file:docs/specs/goal-loop-contract.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/specs/steer-pulse-automation.md",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "file:docs/specs/steer-pulse-automation.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/README.md",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "file:farplane/README.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/goals.md",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "file:farplane/goals.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/harness.md",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "file:farplane/harness.md",
      "type": "literal-path"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "hardening",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "skill:hardening",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "harness-advisor",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "skill:harness-advisor",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "leverage-advisor",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "skill:leverage-advisor",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "optimize-harness",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "skill:optimize-harness",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "proof-advisor",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "skill:proof-advisor",
      "type": "mentions-skill"
    },
    {
      "confidence": "parsed",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "projection": "farplane-framework-core",
      "raw_ref": "skill-creator",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "skill:skill-creator",
      "type": "mentions-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "Autonomy loops",
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:autonomy-loops",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "workflow:autonomy-loops",
      "type": "lifecycle-workflow"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "Bootstrap",
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:bootstrap",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "workflow:bootstrap",
      "type": "lifecycle-workflow"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "Goal execution",
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:goal-execution",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "workflow:goal-execution",
      "type": "defines-workflow"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "Goal execution",
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:goal-execution",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "workflow:goal-execution",
      "type": "lifecycle-workflow"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "Improvement",
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:improvement",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "workflow:improvement",
      "type": "defines-workflow"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "Improvement",
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:improvement",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "workflow:improvement",
      "type": "lifecycle-workflow"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "Farplane lifecycle",
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:lifecycle",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "workflow:lifecycle",
      "type": "defines-workflow"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "Proof",
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:proof",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "workflow:proof",
      "type": "defines-workflow"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "Proof",
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:proof",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "workflow:proof",
      "type": "lifecycle-workflow"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "Strategy",
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:strategy",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "workflow:strategy",
      "type": "defines-workflow"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "Strategy",
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:strategy",
      "source": "file:docs/farplane-framework/lifecycle.md",
      "target": "workflow:strategy",
      "type": "lifecycle-workflow"
    },
    {
      "from_file": "docs/farplane-framework/project-files.md",
      "projection": "farplane-framework-core",
      "raw_ref": "docs/farplane-framework/README.md",
      "source": "file:docs/farplane-framework/project-files.md",
      "target": "file:docs/farplane-framework/README.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/project-files.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/automations.md",
      "source": "file:docs/farplane-framework/project-files.md",
      "target": "file:farplane/automations.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/project-files.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/bindings.md",
      "source": "file:docs/farplane-framework/project-files.md",
      "target": "file:farplane/bindings.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/project-files.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/evals.md",
      "source": "file:docs/farplane-framework/project-files.md",
      "target": "file:farplane/evals.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/project-files.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/goals.md",
      "source": "file:docs/farplane-framework/project-files.md",
      "target": "file:farplane/goals.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/project-files.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/harness.md",
      "source": "file:docs/farplane-framework/project-files.md",
      "target": "file:farplane/harness.md",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/project-files.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/manifest.json",
      "source": "file:docs/farplane-framework/project-files.md",
      "target": "file:farplane/manifest.json",
      "type": "literal-path"
    },
    {
      "from_file": "docs/farplane-framework/project-files.md",
      "projection": "farplane-framework-core",
      "raw_ref": "farplane/pm.json",
      "source": "file:docs/farplane-framework/project-files.md",
      "target": "file:farplane/pm.json",
      "type": "literal-path"
    },
    {
      "confidence": "curated",
      "from_file": "docs/specs/goal-loop-contract.md",
      "label": "triggers",
      "projection": "farplane-framework-core",
      "raw_ref": "skill:goal-advisor",
      "source": "file:farplane/goals.md",
      "target": "skill:goal-advisor",
      "type": "triggers"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "label": "next.1",
      "order": 1,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:autonomy-loops",
      "source": "skill:automation-advisor",
      "target": "skill:pulse-update",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/project-files.md",
      "label": "writes",
      "projection": "farplane-framework-core",
      "raw_ref": "file:farplane/automations.md",
      "source": "skill:deep-init-project",
      "target": "file:farplane/automations.md",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/project-files.md",
      "label": "writes",
      "projection": "farplane-framework-core",
      "raw_ref": "file:farplane/goals.md",
      "source": "skill:deep-init-project",
      "target": "file:farplane/goals.md",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/project-files.md",
      "label": "writes",
      "projection": "farplane-framework-core",
      "raw_ref": "file:farplane/harness.md",
      "source": "skill:deep-init-project",
      "target": "file:farplane/harness.md",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/project-files.md",
      "label": "writes",
      "projection": "farplane-framework-core",
      "raw_ref": "file:farplane/manifest.json",
      "source": "skill:deep-init-project",
      "target": "file:farplane/manifest.json",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/project-files.md",
      "label": "writes",
      "projection": "farplane-framework-core",
      "raw_ref": "file:farplane/pm.json",
      "source": "skill:deep-init-project",
      "target": "file:farplane/pm.json",
      "type": "writes"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "label": "next.1",
      "order": 1,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:bootstrap",
      "source": "skill:deep-init-project",
      "target": "skill:harness-creator",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "label": "next.3",
      "order": 3,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:bootstrap",
      "source": "skill:deep-interview",
      "target": "skill:prd",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.4",
      "order": 4,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:goal-execution",
      "source": "skill:demo",
      "target": "skill:review",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.2",
      "order": 2,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:proof",
      "source": "skill:eval",
      "target": "skill:qa",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.1",
      "order": 1,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:goal-execution",
      "source": "skill:goal-advisor",
      "target": "skill:impl-plan",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "routes_to",
      "projection": "farplane-framework-core",
      "raw_ref": "skill:goal-advisor",
      "source": "skill:harness-advisor",
      "target": "skill:goal-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.3",
      "order": 3,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:strategy",
      "source": "skill:harness-advisor",
      "target": "skill:goal-advisor",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "routes_to",
      "projection": "farplane-framework-core",
      "raw_ref": "skill:proof-advisor",
      "source": "skill:harness-advisor",
      "target": "skill:proof-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "label": "next.2",
      "order": 2,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:bootstrap",
      "source": "skill:harness-creator",
      "target": "skill:deep-interview",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "updates",
      "projection": "farplane-framework-core",
      "raw_ref": "file:farplane/goals.md",
      "source": "skill:horizon-advisor",
      "target": "file:farplane/goals.md",
      "type": "updates"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.1",
      "order": 1,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:strategy",
      "source": "skill:horizon-advisor",
      "target": "skill:leverage-advisor",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.2",
      "order": 2,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:goal-execution",
      "source": "skill:impl-plan",
      "target": "skill:qa",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "skills/learning-drain/SKILL.md",
      "label": "routes_to",
      "projection": "farplane-framework-core",
      "raw_ref": "skill:skill-maintenance",
      "source": "skill:learning-drain",
      "target": "skill:skill-maintenance",
      "type": "routes_to"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.2",
      "order": 2,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:improvement",
      "source": "skill:learning-drain",
      "target": "skill:skill-maintenance",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "routes_to",
      "projection": "farplane-framework-core",
      "raw_ref": "skill:harness-advisor",
      "source": "skill:leverage-advisor",
      "target": "skill:harness-advisor",
      "type": "routes_to"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.2",
      "order": 2,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:strategy",
      "source": "skill:leverage-advisor",
      "target": "skill:harness-advisor",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.5",
      "order": 5,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:improvement",
      "source": "skill:optimize-harness",
      "target": "skill:eval",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "label": "next.4",
      "order": 4,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:bootstrap",
      "source": "skill:prd",
      "target": "skill:spec-to-ticket",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "skills/proof-advisor/SKILL.md",
      "label": "routes_to",
      "projection": "farplane-framework-core",
      "raw_ref": "skill:eval",
      "source": "skill:proof-advisor",
      "target": "skill:eval",
      "type": "routes_to"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.1",
      "order": 1,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:proof",
      "source": "skill:proof-advisor",
      "target": "skill:eval",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "skills/proof-advisor/SKILL.md",
      "label": "routes_to",
      "projection": "farplane-framework-core",
      "raw_ref": "skill:qa",
      "source": "skill:proof-advisor",
      "target": "skill:qa",
      "type": "routes_to"
    },
    {
      "confidence": "curated",
      "from_file": "skills/proof-advisor/SKILL.md",
      "label": "routes_to",
      "projection": "farplane-framework-core",
      "raw_ref": "skill:review",
      "source": "skill:proof-advisor",
      "target": "skill:review",
      "type": "routes_to"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "label": "next.2",
      "order": 2,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:autonomy-loops",
      "source": "skill:pulse-update",
      "target": "skill:interval-update",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.3",
      "order": 3,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:goal-execution",
      "source": "skill:qa",
      "target": "skill:demo",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.3",
      "order": 3,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:proof",
      "source": "skill:qa",
      "target": "skill:review",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.4",
      "order": 4,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:improvement",
      "source": "skill:skill-creator",
      "target": "skill:optimize-harness",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "skills/skill-maintenance/SKILL.md",
      "label": "routes_to",
      "projection": "farplane-framework-core",
      "raw_ref": "skill:eval",
      "source": "skill:skill-maintenance",
      "target": "skill:eval",
      "type": "routes_to"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.3",
      "order": 3,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:improvement",
      "source": "skill:skill-maintenance",
      "target": "skill:skill-creator",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "next.1",
      "order": 1,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:improvement",
      "source": "skill:update-memory",
      "target": "skill:learning-drain",
      "type": "workflow-next"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "label": "1. automation-advisor",
      "order": 1,
      "projection": "farplane-framework-core",
      "raw_ref": "automation-advisor",
      "source": "workflow:autonomy-loops",
      "target": "skill:automation-advisor",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "label": "3. interval-update",
      "order": 3,
      "projection": "farplane-framework-core",
      "raw_ref": "interval-update",
      "source": "workflow:autonomy-loops",
      "target": "skill:interval-update",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/hooks-and-runtime.md",
      "label": "2. pulse-update",
      "order": 2,
      "projection": "farplane-framework-core",
      "raw_ref": "pulse-update",
      "source": "workflow:autonomy-loops",
      "target": "skill:pulse-update",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "label": "1. deep-init-project",
      "order": 1,
      "projection": "farplane-framework-core",
      "raw_ref": "deep-init-project",
      "source": "workflow:bootstrap",
      "target": "skill:deep-init-project",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "label": "3. deep-interview",
      "order": 3,
      "projection": "farplane-framework-core",
      "raw_ref": "deep-interview",
      "source": "workflow:bootstrap",
      "target": "skill:deep-interview",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "label": "2. harness-creator",
      "order": 2,
      "projection": "farplane-framework-core",
      "raw_ref": "harness-creator",
      "source": "workflow:bootstrap",
      "target": "skill:harness-creator",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "label": "4. prd",
      "order": 4,
      "projection": "farplane-framework-core",
      "raw_ref": "prd",
      "source": "workflow:bootstrap",
      "target": "skill:prd",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/deep-init-critical-path.md",
      "label": "5. spec-to-ticket",
      "order": 5,
      "projection": "farplane-framework-core",
      "raw_ref": "spec-to-ticket",
      "source": "workflow:bootstrap",
      "target": "skill:spec-to-ticket",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "4. demo",
      "order": 4,
      "projection": "farplane-framework-core",
      "raw_ref": "demo",
      "source": "workflow:goal-execution",
      "target": "skill:demo",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "1. goal-advisor",
      "order": 1,
      "projection": "farplane-framework-core",
      "raw_ref": "goal-advisor",
      "source": "workflow:goal-execution",
      "target": "skill:goal-advisor",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "2. impl-plan",
      "order": 2,
      "projection": "farplane-framework-core",
      "raw_ref": "impl-plan",
      "source": "workflow:goal-execution",
      "target": "skill:impl-plan",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "3. qa",
      "order": 3,
      "projection": "farplane-framework-core",
      "raw_ref": "qa",
      "source": "workflow:goal-execution",
      "target": "skill:qa",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "5. review",
      "order": 5,
      "projection": "farplane-framework-core",
      "raw_ref": "review",
      "source": "workflow:goal-execution",
      "target": "skill:review",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "6. eval",
      "order": 6,
      "projection": "farplane-framework-core",
      "raw_ref": "eval",
      "source": "workflow:improvement",
      "target": "skill:eval",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "2. learning-drain",
      "order": 2,
      "projection": "farplane-framework-core",
      "raw_ref": "learning-drain",
      "source": "workflow:improvement",
      "target": "skill:learning-drain",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "5. optimize-harness",
      "order": 5,
      "projection": "farplane-framework-core",
      "raw_ref": "optimize-harness",
      "source": "workflow:improvement",
      "target": "skill:optimize-harness",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "4. skill-creator",
      "order": 4,
      "projection": "farplane-framework-core",
      "raw_ref": "skill-creator",
      "source": "workflow:improvement",
      "target": "skill:skill-creator",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "3. skill-maintenance",
      "order": 3,
      "projection": "farplane-framework-core",
      "raw_ref": "skill-maintenance",
      "source": "workflow:improvement",
      "target": "skill:skill-maintenance",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "1. update-memory",
      "order": 1,
      "projection": "farplane-framework-core",
      "raw_ref": "update-memory",
      "source": "workflow:improvement",
      "target": "skill:update-memory",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "stage.4",
      "order": 4,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:autonomy-loops",
      "source": "workflow:lifecycle",
      "target": "workflow:autonomy-loops",
      "type": "workflow-stage"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "stage.1",
      "order": 1,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:bootstrap",
      "source": "workflow:lifecycle",
      "target": "workflow:bootstrap",
      "type": "workflow-stage"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "stage.3",
      "order": 3,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:goal-execution",
      "source": "workflow:lifecycle",
      "target": "workflow:goal-execution",
      "type": "workflow-stage"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "stage.6",
      "order": 6,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:improvement",
      "source": "workflow:lifecycle",
      "target": "workflow:improvement",
      "type": "workflow-stage"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "stage.5",
      "order": 5,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:proof",
      "source": "workflow:lifecycle",
      "target": "workflow:proof",
      "type": "workflow-stage"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "stage.2",
      "order": 2,
      "projection": "farplane-framework-core",
      "raw_ref": "workflow:strategy",
      "source": "workflow:lifecycle",
      "target": "workflow:strategy",
      "type": "workflow-stage"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "2. eval",
      "order": 2,
      "projection": "farplane-framework-core",
      "raw_ref": "eval",
      "source": "workflow:proof",
      "target": "skill:eval",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "1. proof-advisor",
      "order": 1,
      "projection": "farplane-framework-core",
      "raw_ref": "proof-advisor",
      "source": "workflow:proof",
      "target": "skill:proof-advisor",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "3. qa",
      "order": 3,
      "projection": "farplane-framework-core",
      "raw_ref": "qa",
      "source": "workflow:proof",
      "target": "skill:qa",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "4. review",
      "order": 4,
      "projection": "farplane-framework-core",
      "raw_ref": "review",
      "source": "workflow:proof",
      "target": "skill:review",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "4. goal-advisor",
      "order": 4,
      "projection": "farplane-framework-core",
      "raw_ref": "goal-advisor",
      "source": "workflow:strategy",
      "target": "skill:goal-advisor",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "3. harness-advisor",
      "order": 3,
      "projection": "farplane-framework-core",
      "raw_ref": "harness-advisor",
      "source": "workflow:strategy",
      "target": "skill:harness-advisor",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "1. horizon-advisor",
      "order": 1,
      "projection": "farplane-framework-core",
      "raw_ref": "horizon-advisor",
      "source": "workflow:strategy",
      "target": "skill:horizon-advisor",
      "type": "workflow-skill"
    },
    {
      "confidence": "curated",
      "from_file": "docs/farplane-framework/lifecycle.md",
      "label": "2. leverage-advisor",
      "order": 2,
      "projection": "farplane-framework-core",
      "raw_ref": "leverage-advisor",
      "source": "workflow:strategy",
      "target": "skill:leverage-advisor",
      "type": "workflow-skill"
    }
  ],
  "generated_at": "2026-06-25T07:10:30+00:00",
  "nodes": [
    {
      "framework_role": "linked",
      "id": "file:farplane/README.md",
      "kind": "file",
      "label": "farplane/README.md",
      "path": "farplane/README.md",
      "source_match": false,
      "source_path": "farplane/README.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "id": "file:farplane/automations.md",
      "kind": "file",
      "label": "farplane/automations.md",
      "path": "farplane/automations.md",
      "source_match": false,
      "source_path": "farplane/automations.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "id": "file:farplane/bindings.md",
      "kind": "file",
      "label": "farplane/bindings.md",
      "path": "farplane/bindings.md",
      "source_match": false,
      "source_path": "farplane/bindings.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "id": "file:farplane/evals.md",
      "kind": "file",
      "label": "farplane/evals.md",
      "path": "farplane/evals.md",
      "source_match": false,
      "source_path": "farplane/evals.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "id": "file:farplane/goals.md",
      "kind": "file",
      "label": "farplane/goals.md",
      "path": "farplane/goals.md",
      "source_match": false,
      "source_path": "farplane/goals.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "id": "file:farplane/harness.md",
      "kind": "file",
      "label": "farplane/harness.md",
      "path": "farplane/harness.md",
      "source_match": false,
      "source_path": "farplane/harness.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "id": "file:farplane/manifest.json",
      "kind": "file",
      "label": "farplane/manifest.json",
      "path": "farplane/manifest.json",
      "source_match": false,
      "source_path": "farplane/manifest.json",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "id": "file:farplane/pm.json",
      "kind": "file",
      "label": "farplane/pm.json",
      "path": "farplane/pm.json",
      "source_match": false,
      "source_path": "farplane/pm.json",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:automation-advisor",
      "kind": "skill",
      "label": "automation-advisor",
      "path": "skills/automation-advisor/SKILL.md",
      "source_match": false,
      "source_path": "skills/automation-advisor/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 7,
        "distinct_threads_window": 7,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 14,
        "invocation_count_30d": 7,
        "invocation_count_7d": 0,
        "invocation_count_all": 7,
        "invocation_count_recent": 0,
        "invocation_count_window": 7,
        "last_invoked_at": "2026-06-06T14:11:49.058419Z",
        "observed_event_count_all": 14,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:brainstorm",
      "kind": "skill",
      "label": "brainstorm",
      "path": "skills/brainstorm/SKILL.md",
      "source_match": false,
      "source_path": "skills/brainstorm/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:deep-init-project",
      "kind": "skill",
      "label": "deep-init-project",
      "path": "skills/deep-init-project/SKILL.md",
      "source_match": false,
      "source_path": "skills/deep-init-project/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:deep-interview",
      "kind": "skill",
      "label": "deep-interview",
      "path": "skills/deep-interview/SKILL.md",
      "source_match": false,
      "source_path": "skills/deep-interview/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:demo",
      "kind": "skill",
      "label": "demo",
      "path": "skills/demo/SKILL.md",
      "source_match": false,
      "source_path": "skills/demo/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:documentation",
      "kind": "skill",
      "label": "documentation",
      "path": "skills/documentation/SKILL.md",
      "source_match": false,
      "source_path": "skills/documentation/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:eval",
      "kind": "skill",
      "label": "eval",
      "path": "skills/eval/SKILL.md",
      "source_match": false,
      "source_path": "skills/eval/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:execute",
      "kind": "skill",
      "label": "execute",
      "path": "skills/execute/SKILL.md",
      "source_match": false,
      "source_path": "skills/execute/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:goal-advisor",
      "kind": "skill",
      "label": "goal-advisor",
      "path": "skills/goal-advisor/SKILL.md",
      "source_match": false,
      "source_path": "skills/goal-advisor/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:hardening",
      "kind": "skill",
      "label": "hardening",
      "path": "skills/hardening/SKILL.md",
      "source_match": false,
      "source_path": "skills/hardening/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:harness-advisor",
      "kind": "skill",
      "label": "harness-advisor",
      "path": "skills/harness-advisor/SKILL.md",
      "source_match": false,
      "source_path": "skills/harness-advisor/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:harness-creator",
      "kind": "skill",
      "label": "harness-creator",
      "path": "skills/harness-creator/SKILL.md",
      "source_match": false,
      "source_path": "skills/harness-creator/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:horizon-advisor",
      "kind": "skill",
      "label": "horizon-advisor",
      "path": "skills/horizon-advisor/SKILL.md",
      "source_match": false,
      "source_path": "skills/horizon-advisor/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 7,
        "distinct_threads_window": 7,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 14,
        "invocation_count_30d": 7,
        "invocation_count_7d": 0,
        "invocation_count_all": 7,
        "invocation_count_recent": 0,
        "invocation_count_window": 7,
        "last_invoked_at": "2026-06-06T14:11:49.058337Z",
        "observed_event_count_all": 14,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:impl-plan",
      "kind": "skill",
      "label": "impl-plan",
      "path": "skills/impl-plan/SKILL.md",
      "source_match": false,
      "source_path": "skills/impl-plan/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:interval-update",
      "kind": "skill",
      "label": "interval-update",
      "path": "skills/interval-update/SKILL.md",
      "source_match": false,
      "source_path": "skills/interval-update/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:knowledge-tidier",
      "kind": "skill",
      "label": "knowledge-tidier",
      "path": "skills/knowledge-tidier/SKILL.md",
      "source_match": false,
      "source_path": "skills/knowledge-tidier/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:learning-drain",
      "kind": "skill",
      "label": "learning-drain",
      "path": "skills/learning-drain/SKILL.md",
      "source_match": false,
      "source_path": "skills/learning-drain/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:leverage-advisor",
      "kind": "skill",
      "label": "leverage-advisor",
      "path": "skills/leverage-advisor/SKILL.md",
      "source_match": false,
      "source_path": "skills/leverage-advisor/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:optimize-harness",
      "kind": "skill",
      "label": "optimize-harness",
      "path": "skills/optimize-harness/SKILL.md",
      "source_match": false,
      "source_path": "skills/optimize-harness/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:plan",
      "kind": "skill",
      "label": "plan",
      "path": "skills/plan/SKILL.md",
      "source_match": false,
      "source_path": "skills/plan/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:prd",
      "kind": "skill",
      "label": "prd",
      "path": "skills/prd/SKILL.md",
      "source_match": false,
      "source_path": "skills/prd/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:proof-advisor",
      "kind": "skill",
      "label": "proof-advisor",
      "path": "skills/proof-advisor/SKILL.md",
      "source_match": false,
      "source_path": "skills/proof-advisor/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:pulse-update",
      "kind": "skill",
      "label": "pulse-update",
      "path": "skills/pulse-update/SKILL.md",
      "source_match": false,
      "source_path": "skills/pulse-update/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:qa",
      "kind": "skill",
      "label": "qa",
      "path": "skills/qa/SKILL.md",
      "source_match": false,
      "source_path": "skills/qa/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:research",
      "kind": "skill",
      "label": "research",
      "path": "skills/research/SKILL.md",
      "source_match": false,
      "source_path": "skills/research/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:review",
      "kind": "skill",
      "label": "review",
      "path": "skills/review/SKILL.md",
      "source_match": false,
      "source_path": "skills/review/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:skill-creator",
      "kind": "skill",
      "label": "skill-creator",
      "path": "skills/skill-creator/SKILL.md",
      "source_match": false,
      "source_path": "skills/skill-creator/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:skill-maintenance",
      "kind": "skill",
      "label": "skill-maintenance",
      "path": "skills/skill-maintenance/SKILL.md",
      "source_match": false,
      "source_path": "skills/skill-maintenance/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:spec-to-ticket",
      "kind": "skill",
      "label": "spec-to-ticket",
      "path": "skills/spec-to-ticket/SKILL.md",
      "source_match": false,
      "source_path": "skills/spec-to-ticket/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "heat": {
        "distinct_threads_30d": 0,
        "distinct_threads_window": 0,
        "distinct_tickets_30d": 0,
        "distinct_tickets_window": 0,
        "heat_score": 0,
        "invocation_count_30d": 0,
        "invocation_count_7d": 0,
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "last_invoked_at": "",
        "observed_event_count_all": 0,
        "recent_days": 7,
        "window_days": 30
      },
      "id": "skill:update-memory",
      "kind": "skill",
      "label": "update-memory",
      "path": "skills/update-memory/SKILL.md",
      "source_match": false,
      "source_path": "skills/update-memory/SKILL.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "id": "file:docs/specs/README.md",
      "kind": "spec",
      "label": "docs/specs/README.md",
      "path": "docs/specs/README.md",
      "source_match": false,
      "source_path": "docs/specs/README.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "id": "file:docs/specs/filesystem-lifecycle.md",
      "kind": "spec",
      "label": "docs/specs/filesystem-lifecycle.md",
      "path": "docs/specs/filesystem-lifecycle.md",
      "source_match": false,
      "source_path": "docs/specs/filesystem-lifecycle.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "id": "file:docs/specs/goal-loop-contract.md",
      "kind": "spec",
      "label": "docs/specs/goal-loop-contract.md",
      "path": "docs/specs/goal-loop-contract.md",
      "source_match": false,
      "source_path": "docs/specs/goal-loop-contract.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "id": "file:docs/specs/program-notation.md",
      "kind": "spec",
      "label": "docs/specs/program-notation.md",
      "path": "docs/specs/program-notation.md",
      "source_match": false,
      "source_path": "docs/specs/program-notation.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "linked",
      "id": "file:docs/specs/steer-pulse-automation.md",
      "kind": "spec",
      "label": "docs/specs/steer-pulse-automation.md",
      "path": "docs/specs/steer-pulse-automation.md",
      "source_match": false,
      "source_path": "docs/specs/steer-pulse-automation.md",
      "tags": [
        "framework-core",
        "framework-role:linked"
      ]
    },
    {
      "framework_role": "source",
      "id": "file:docs/farplane-framework/README.md",
      "kind": "doc",
      "label": "docs/farplane-framework/README.md",
      "matched_patterns": [
        "docs/farplane-framework/README.md"
      ],
      "path": "docs/farplane-framework/README.md",
      "source_match": true,
      "source_path": "docs/farplane-framework/README.md",
      "tags": [
        "framework-core",
        "framework-role:source"
      ]
    },
    {
      "framework_role": "source",
      "id": "file:docs/farplane-framework/deep-init-critical-path.md",
      "kind": "doc",
      "label": "docs/farplane-framework/deep-init-critical-path.md",
      "matched_patterns": [
        "docs/farplane-framework/deep-init-critical-path.md"
      ],
      "path": "docs/farplane-framework/deep-init-critical-path.md",
      "source_match": true,
      "source_path": "docs/farplane-framework/deep-init-critical-path.md",
      "tags": [
        "framework-core",
        "framework-role:source"
      ]
    },
    {
      "framework_role": "source",
      "id": "file:docs/farplane-framework/graph-contract.md",
      "kind": "doc",
      "label": "docs/farplane-framework/graph-contract.md",
      "matched_patterns": [
        "docs/farplane-framework/graph-contract.md"
      ],
      "path": "docs/farplane-framework/graph-contract.md",
      "source_match": true,
      "source_path": "docs/farplane-framework/graph-contract.md",
      "tags": [
        "framework-core",
        "framework-role:source"
      ]
    },
    {
      "framework_role": "source",
      "id": "file:docs/farplane-framework/harness-maintenance.md",
      "kind": "doc",
      "label": "docs/farplane-framework/harness-maintenance.md",
      "matched_patterns": [
        "docs/farplane-framework/harness-maintenance.md"
      ],
      "path": "docs/farplane-framework/harness-maintenance.md",
      "source_match": true,
      "source_path": "docs/farplane-framework/harness-maintenance.md",
      "tags": [
        "framework-core",
        "framework-role:source"
      ]
    },
    {
      "framework_role": "source",
      "id": "file:docs/farplane-framework/hooks-and-runtime.md",
      "kind": "doc",
      "label": "docs/farplane-framework/hooks-and-runtime.md",
      "matched_patterns": [
        "docs/farplane-framework/hooks-and-runtime.md"
      ],
      "path": "docs/farplane-framework/hooks-and-runtime.md",
      "source_match": true,
      "source_path": "docs/farplane-framework/hooks-and-runtime.md",
      "tags": [
        "framework-core",
        "framework-role:source"
      ]
    },
    {
      "framework_role": "source",
      "id": "file:docs/farplane-framework/lifecycle.md",
      "kind": "doc",
      "label": "docs/farplane-framework/lifecycle.md",
      "matched_patterns": [
        "docs/farplane-framework/lifecycle.md"
      ],
      "path": "docs/farplane-framework/lifecycle.md",
      "source_match": true,
      "source_path": "docs/farplane-framework/lifecycle.md",
      "tags": [
        "framework-core",
        "framework-role:source"
      ]
    },
    {
      "framework_role": "source",
      "id": "file:docs/farplane-framework/project-files.md",
      "kind": "doc",
      "label": "docs/farplane-framework/project-files.md",
      "matched_patterns": [
        "docs/farplane-framework/project-files.md"
      ],
      "path": "docs/farplane-framework/project-files.md",
      "source_match": true,
      "source_path": "docs/farplane-framework/project-files.md",
      "tags": [
        "framework-core",
        "framework-role:source"
      ]
    },
    {
      "description": "Run Pulse and interval loops for bounded action and planning cadence.",
      "framework_role": "workflow",
      "id": "workflow:autonomy-loops",
      "kind": "workflow",
      "label": "Autonomy loops",
      "path": "docs/farplane-framework/hooks-and-runtime.md",
      "source_match": false,
      "source_path": "docs/farplane-framework/hooks-and-runtime.md",
      "tags": [
        "framework-core",
        "framework-role:workflow",
        "workflow"
      ],
      "workflow_order": 4,
      "workflow_skills": [
        "automation-advisor",
        "pulse-update",
        "interval-update"
      ]
    },
    {
      "description": "Create the project substrate and first usable harness state.",
      "framework_role": "workflow",
      "id": "workflow:bootstrap",
      "kind": "workflow",
      "label": "Bootstrap",
      "path": "docs/farplane-framework/deep-init-critical-path.md",
      "source_match": false,
      "source_path": "docs/farplane-framework/deep-init-critical-path.md",
      "tags": [
        "framework-core",
        "framework-role:workflow",
        "workflow"
      ],
      "workflow_order": 1,
      "workflow_skills": [
        "deep-init-project",
        "harness-creator",
        "deep-interview",
        "prd",
        "spec-to-ticket"
      ]
    },
    {
      "description": "Top-level lifecycle spine from init through goals, proof, autonomy loops, and improvement.",
      "framework_role": "workflow",
      "id": "workflow:lifecycle",
      "kind": "workflow",
      "label": "Farplane lifecycle",
      "path": "docs/farplane-framework/lifecycle.md",
      "source_match": false,
      "source_path": "docs/farplane-framework/lifecycle.md",
      "tags": [
        "framework-core",
        "framework-role:workflow",
        "workflow"
      ],
      "workflow_order": 0,
      "workflow_skills": []
    },
    {
      "description": "Compile a goal into a ticket-backed program, execute it, and produce proof.",
      "framework_role": "workflow",
      "id": "workflow:goal-execution",
      "kind": "workflow",
      "label": "Goal execution",
      "path": "docs/farplane-framework/lifecycle.md",
      "source_match": false,
      "source_path": "docs/farplane-framework/lifecycle.md",
      "tags": [
        "framework-core",
        "framework-role:workflow",
        "workflow"
      ],
      "workflow_order": 3,
      "workflow_skills": [
        "goal-advisor",
        "impl-plan",
        "qa",
        "demo",
        "review"
      ]
    },
    {
      "description": "Drain outcomes into memory, lessons, skill maintenance, and future evals.",
      "framework_role": "workflow",
      "id": "workflow:improvement",
      "kind": "workflow",
      "label": "Improvement",
      "path": "docs/farplane-framework/lifecycle.md",
      "source_match": false,
      "source_path": "docs/farplane-framework/lifecycle.md",
      "tags": [
        "framework-core",
        "framework-role:workflow",
        "workflow"
      ],
      "workflow_order": 6,
      "workflow_skills": [
        "update-memory",
        "learning-drain",
        "skill-maintenance",
        "skill-creator",
        "optimize-harness",
        "eval"
      ]
    },
    {
      "description": "Select and run proof paths for claims, tickets, skills, and workflows.",
      "framework_role": "workflow",
      "id": "workflow:proof",
      "kind": "workflow",
      "label": "Proof",
      "path": "docs/farplane-framework/lifecycle.md",
      "source_match": false,
      "source_path": "docs/farplane-framework/lifecycle.md",
      "tags": [
        "framework-core",
        "framework-role:workflow",
        "workflow"
      ],
      "workflow_order": 5,
      "workflow_skills": [
        "proof-advisor",
        "eval",
        "qa",
        "review"
      ]
    },
    {
      "description": "Shape goals, horizons, leverage bets, and executable frontier choices.",
      "framework_role": "workflow",
      "id": "workflow:strategy",
      "kind": "workflow",
      "label": "Strategy",
      "path": "docs/farplane-framework/lifecycle.md",
      "source_match": false,
      "source_path": "docs/farplane-framework/lifecycle.md",
      "tags": [
        "framework-core",
        "framework-role:workflow",
        "workflow"
      ],
      "workflow_order": 2,
      "workflow_skills": [
        "horizon-advisor",
        "leverage-advisor",
        "harness-advisor",
        "goal-advisor"
      ]
    }
  ],
  "projection": "farplane-framework-core",
  "schema_version": "1.0.0",
  "source": {
    "exclude": [
      "farplane/products.md",
      "tickets/archive/**",
      ".farplane/reports/**",
      ".farplane/logs/**",
      "experiments/**"
    ],
    "expansion": "framework-doc-direct-refs",
    "include": [
      "docs/farplane-framework/README.md",
      "docs/farplane-framework/lifecycle.md",
      "docs/farplane-framework/deep-init-critical-path.md",
      "docs/farplane-framework/project-files.md",
      "docs/farplane-framework/graph-contract.md",
      "docs/farplane-framework/hooks-and-runtime.md",
      "docs/farplane-framework/harness-maintenance.md"
    ],
    "manifest": "farplane/manifest.json"
  }
};
