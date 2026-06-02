---
name: convex
version: 4.0.0
description: "External Convex routing skill. Prefer the official Convex AI files installed into the current project, with this package kept as a thin upstream pointer."
tier: 3
group: backend
source: external
upstream_url: https://github.com/get-convex/agent-skills/blob/main/skills/convex/SKILL.md
---

# Convex Skill

Use this as a thin pointer to the official Convex agent skill and project-local
Convex AI files. Farplane should not maintain a parallel Convex playbook here.

## Start Here

1. If the current project has Convex AI files installed, read those local files
   first and treat them as the project-specific source of truth.
2. If the project lacks current Convex AI guidance, recommend installing or
   refreshing it with:

```bash
npx convex ai-files install
```

3. If installation is not possible, use the upstream skill at
   <https://github.com/get-convex/agent-skills/blob/main/skills/convex/SKILL.md>
   as the fallback routing reference.

## Boundaries

- Do not copy official Convex rules into this skill body.
- Do not add Farplane wrapper policy here; put local workflow policy in the
  caller skill or project docs.
- If a task needs current Convex API details, use the project's installed
  Convex AI files or official Convex docs through the normal research/docs path.
