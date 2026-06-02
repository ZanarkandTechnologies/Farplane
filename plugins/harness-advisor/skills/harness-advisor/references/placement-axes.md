# Harness Placement Axes

Use this reference when deciding where a Farplane improvement belongs. The goal
is to optimize harness performance by minimizing always-loaded context,
maximizing progressive disclosure, preserving durable state in files, and using
programmatic checks only where they are deterministic.

## Algebra

```text
Harness :=
  AlwaysLoadedPolicy
+ ProgressiveSkills
+ IsolatedSubagents
+ DurableArtifacts
+ ToolSurfaces
+ LifecycleHooks
+ Registries
+ ReviewLoop

PlacementDecision :=
  FailureMode
+ ContextBudget
+ ReuseFrequency
+ OwnershipBoundary
+ Determinism
+ EvidenceSurface
+ DuplicationRisk
+ Discoverability
+ MaintenanceCost
```

## OOP Sketch

```java
interface HarnessSurface {
  boolean shouldOwn(ChangeRequest request);
  ContextCost contextCost();
  Ownership ownership();
  Proof proofMode();
}

final class AgentPrompt implements HarnessSurface {
  // Always loaded. Best for durable invariants and routing.
}

final class Skill implements HarnessSurface {
  // Progressively loaded. Best for repeated procedures and domain methods.
}

final class Subagent implements HarnessSurface {
  // Separate thread/context. Best for independent ownership and context isolation.
}

final class DurableDoc implements HarnessSurface {
  // Filesystem memory. Best for shared state, specs, references, and handoff.
}

final class ToolOrMcp implements HarnessSurface {
  // Capability adapter. Best when agents need external ground truth or APIs.
}

final class HookOrValidator implements HarnessSurface {
  // Programmatic boundary. Best for deterministic checks and lifecycle routing.
}
```

## Surface Matrix

| Surface | Optimizes for | Use when | Avoid when |
| --- | --- | --- | --- |
| Root `AGENTS.md` | always-on routing, durable repo invariants | every loop needs the rule | procedure, examples, or bulky doctrine |
| `templates/global/AGENTS.md` | shipped cross-repo defaults | all installed repos need the default | the rule is Farplane-local |
| Generated project `AGENTS_TEMPLATE.md` | project-local always-loaded workflow | new repos should inherit the operating rule | the detail belongs to this Farplane repo only |
| `PROJECT_RULES_TEMPLATE.md` | project technical standards | stack, commands, runtime, QA paths, conventions | agent workflow or lifecycle doctrine |
| Skill | progressive procedure | repeated workflow, called multiple times, domain method | one-off docs or role isolation problem |
| Skill reference | progressive detail | reusable model, algebra, examples, templates, long guidance | agents need the rule every turn |
| Subagent | isolated context and owner output | self-review risk, context rot, independent lane | same role just needs better steps |
| Subagent + skill | isolated role plus consistent procedure | specialist lane repeats a workflow | no clear independent output |
| Durable docs/files | shared state and memory | project truth, specs, decisions, artifacts | ephemeral thinking or always-needed rule |
| MCP/tool | external capability or ground truth | APIs, search, browser, databases, model jobs | policy or judgment can solve it |
| Hook/script/validator | deterministic lifecycle control | objective checks, routing, metadata, stale-state detection | taste, nuance, or exploratory planning |
| Registry | dedupe and discoverability | feature/skill already exists or needs provenance | primary instructions or long docs |
| Ticket contract | work package and proof target | size, scope, acceptance, evidence, handoff | global policy or reusable procedure |

## Advisor Questions

Ask these before recommending a surface:

- Is this rule needed every turn, or only when a skill is invoked?
- Will the workflow be called multiple times across tickets or projects?
- Is the current problem context rot, duplication, weak procedure, weak proof,
  missing capability, or unclear ownership?
- Would adding this to `AGENTS.md` bloat always-loaded context?
- Does an existing skill, feature, hook, subagent, registry row, or doc already
  own the behavior?
- Would a new skill duplicate an existing implementation?
- Should this be project configuration, agent capability, durable reference, or
  runtime enforcement?
- Can a deterministic hook or validator prove it, or is it judgment-heavy?
- Would a subagent improve throughput by isolating context and output
  ownership?
- Should a subagent prompt call an existing skill instead of copying its
  procedure?

## Output Scoring

For material placement decisions, score the candidate surfaces compactly:

```text
SurfaceScore :=
  context_cost: low | medium | high
  reuse_frequency: once | occasional | repeated | universal
  determinism: judgment | mixed | deterministic
  ownership_fit: weak | acceptable | strong
  duplication_risk: low | medium | high
  recommended: yes | no
```

Prefer the surface with the strongest ownership fit and lowest context cost
that still preserves discoverability and proof.
