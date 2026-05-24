---
name: {skill_name}
version: {version}
description: [TODO: Provide a clear description. Include triggering scenarios (e.g., "Use when building X...") and specific tasks it enables. This description is the primary triggering mechanism.]
allowed-tools: {tools}
---

# {skill_title} Skill

## Purpose

[TODO: One sentence description. What specific integration problem does this solve? Based on the Sequential Thinking reasoning.]

## First-Load Checklist

Ensure an agent can execute the core path after only reading this file.

- Trigger conditions
- 5-8 step workflow
- Core decision branches
- Top 3 gotchas
- Judgement questions that should route to `advise`
- Outcome contract (files/outputs that must exist or be updated)

## Documentation Index (Source of Truth)

- **[Feature 1]**: [Title](link-to-docs)
- **[Feature 2]**: [Title](link-to-docs)

## Integration Workflow

1. **Identify Use Case**: Find the relevant link in the Documentation Index.
2. **Fetch Source of Truth**: Delegate to `documentation-searcher` with the specific URL to get latest API specs.
3. **Choose Branch**:
   - **Simple/default path** -> execute steps inline in this SKILL.md.
   - **Complex/variant-heavy path** -> load specific reference files.
4. **Implementation**: Main Agent synthesizes findings to implement.

## Decision Branches

- **Branch A (default)**: [TODO: shortest successful path]
- **Branch B (alternative)**: [TODO: when and why to use]

## Judgement Questions

Use `advise` when these cannot be answered mechanically:

- [TODO: Material decision question 1]
- [TODO: Metric, guard, scope, or quality question 2]
- [TODO: Rejection/defer question 3]

## Architectural Decisions

- [TODO: Key decision 1]
- [TODO: Key decision 2]
- [Optional deep dive] [architecture.md](references/architecture.md)

## Common Gotchas

- [TODO: Pitfall 1]
- [TODO: Pitfall 2]
- [TODO: Pitfall 3]
- [Optional long-tail list] [gotchas.md](references/gotchas.md)

## Outcome Contract

After this skill runs, these artifacts should exist or be updated:

- [TODO: path/to/output-1]
- [TODO: path/to/output-2]

## Prompt Templates

Include copy/paste prompts when the workflow repeats across sessions.

- [prompts/plan.md](prompts/plan.md) - [TODO: when to use]
- [prompts/build.md](prompts/build.md) - [TODO: when to use]

## Bundled Resources

- **scripts/**: [TODO: Describe utility scripts here.]
- **references/**: [TODO: Include only non-core or verbose details (do not hide the baseline workflow here).]
- **prompts/**: [TODO: Add copy/paste planning/build/review prompts when useful.]
- **assets/**: [TODO: List static assets (templates, icons, boilerplates).]

## References

- [references/workflows.md](references/workflows.md) - Optional: variant-heavy branches only.
- [references/architecture.md](references/architecture.md) - Optional: deep tradeoff history.
- [references/gotchas.md](references/gotchas.md) - Optional: long-tail edge cases.
- [references/judgement-questions.md](references/judgement-questions.md) - Optional: reusable advise-style decisions.
