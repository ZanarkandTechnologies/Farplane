---
kind: council-decision-note
status: draft
created_at: 2026-06-15
decision: deep-init-project-vs-harness-creator
owner: harness
---

# Deep Init Project Vs Harness Creator

## Decision

Should `deep-init-project` and `harness-creator` remain separate skills, merge
into one project-init skill, or become one orchestrator with two internal
phases?

## Stakes

This decision affects how every future repo becomes a Farplane project, whether
Farplane feels like a universal AI office framework, and whether project setup
becomes too heavy for simple code repos.

## Grounding

- `docs/farplane-framework/README.md` defines every project as files, tickets,
  skills, goals, bindings, automations, and runtime reports.
- `deep-init-project` currently owns substrate setup: AGENTS, PROJECT_RULES,
  ARCHITECTURE, docs, tickets, QA, automation and binding templates.
- `harness-creator` currently owns operating-program setup: mission, values,
  goals, KPIs, feedback loops, missing systems, unblock tickets, and recurring
  cadence.
- Farplane's dogfood files now include `farplane/harness.md`,
  `farplane/goals.md`, `farplane/automations.md`, `farplane/bindings.md`, and
  `farplane/evals.md`.

## Options

1. Keep both skills fully separate.
2. Merge them into one large `deep-init-project`.
3. Make `deep-init-project` the public orchestrator and keep
   `harness-creator` as the internal program phase.

## Perspectives

### Operator Value

Every project should become a Farplane project by default.
The operator should not have to remember two skills or decide whether a repo
needs a harness.
The public experience should be: initialize the project, and Farplane sets up
the code/repo substrate plus the PM harness.

### Engineering Risk

Fully merging the skills would make one large skill own too many concerns:
stack setup, QA, project docs, ticket state, strategy, business goals,
feedback loops, skills, automations, and bindings.
That increases blast radius and makes it harder to test or update each phase.

### Evidence Skeptic

The framework is still draft.
We should dogfood the new shape before deleting the old boundary.
The evidence supports making Farplane harness setup the default, but not
collapsing all internals into one giant skill yet.

### Systems Fit

The clean abstraction is:

```text
deep_init_project(harness_depth=standard)
  -> scaffold substrate
  -> call project_harness_creator(...)
  -> compile automation preview
  -> create first tickets / Goal Advisor handoff
```

`deep-init-project` is the entrypoint.
`harness-creator` remains a callable phase.
This matches compiler architecture: one frontend command, modular passes.

## Recommendation

Use option 3.

Farplane should encourage every project to be a Farplane project by default,
but keep `harness-creator` as an internal phase rather than merging it away.

## Dissent

The strongest dissent is product simplicity: if users see two skills, the
system feels under-integrated.
If the public interface still requires users to manually run both, the split
will feel like accidental complexity.

## Tradeoff Accepted

Accept an internal two-phase architecture to preserve modularity, while hiding
that complexity behind one normal setup command.

## Next Owner

`deep-init-project` should become the public orchestrator for project setup.
Farplane is the default framework, not a mode:

```text
deep_init_project(project_idea?, repo_shape?, harness_depth?)
```

It should call or route to `harness-creator` when `harness_depth != none`.

## Proof

The next proof is a framework edit:

- update `deep-init-project` signature and docs
- remove the redundant `mode=farplane` parameter
- make `harness-creator` an internal phase in the lifecycle docs
- keep a `harness_depth` escape hatch for tiny repos or migration-only work
