# Bootstrap Brief

Use this brief to capture the project-shaping answers before generating or
finalizing the scaffold.

## Summary
- Project:
- Goal:
- Audience:

## Intent
- Why now:
- What good looks like:
- What this scaffold should optimize for first:

## Recommended Shape
- Project profile:
- Lifecycle route:
- App type:
- Topology recommendation:
- Why this topology:
- Non-goals for v1:

## Profile Components
- Component matrix:
- Advice axes to explore:
- Material choices that need `advise`:
- Defaults that do not need exploration:

## Prototype Gates
- Highest-risk assumption:
- Smallest PoC artifact:
- Pass signal:
- Prototype ticket before full build:

## Pipeline Handoff
- Recommended downstream skill:
- Required handoff inputs:
- Expected output packet:
- Proof surfaces:

## Stack Decisions
- Frontend:
- Backend:
- Database:
- Runtime / package manager:
- Deployment target:

## Frontend UI Baseline
- UI applies to this repo:
- Component system: [default `shadcn/ui` for app UI]
- shadcn/tweakcn status:
- Default theme command:
  `pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/darkmatter.json`
- Theme applied:
- Skip reason if not applied: [explicit user opt-out / no UI / existing design system / static throwaway artifact only]
- Plain HTML exception accepted by user:
- Tooltip-over-explainer rule accepted:
- Initial visual QA evidence path:

## Runtime / QA Commands
- Preferred app-only run path:
- Preferred QA / evidence-capture run path:
- Required local services:
- Process vs compose expectation:
- Expected targets or base URLs:
- Port / env assumptions agents must honor:
- Evidence-capture notes:

## Validation and Hooks
- Required local checks:
- Optional heavy local checks:
- Hook policy:
- Hook activation choice:
- Preferred hook stages:
- CodeRabbit policy:
- Desloppify policy:
- Separate CI / deployment gate:
- TypeScript typecheck policy:

## Agent Experience / Testability
- Important states the agent must reach quickly:
- Fast-entry surfaces to create or preserve:
- Reset / seed / fixture strategy:
- Hidden state that needs probes, HUDs, or DOM mirrors:
- Preferred browser proof stack:
- Initial QA cookbook workflows to document:

## Autonomy Readiness
- Human inputs/assets needed before unattended work:
- Credentials / external-service access needed:
- Compute needs such as GPU, queues, workers, or long-running jobs:
- Tooling gaps the agent should surface before implementation:
- Hard-to-QA or hard-to-inspect surfaces:
- Required human gates:
  - Plan review:
  - QA review:
  - Deploy/publish:
  - Spend/billing:
  - Destructive or migration actions:
- Decisions the agent may make autonomously:
- Decisions that must stop and ask:

## File-Size Policy
- Warn threshold:
- Block threshold:
- Measurement:
- Source-file scope / exclusions:

## Shared Utility Policy
- Preferred shared utility location:
- When to extract vs keep local:
- Helper naming / placement constraints:

## Decision Boundaries
- What the scaffold may decide automatically:
- What still requires confirmation:

## Defaults Chosen
- Recommended defaults accepted:
- Explicit overrides:
