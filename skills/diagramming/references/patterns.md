# Diagramming Patterns

Use these patterns when `SKILL.md` says a diagram is warranted.

## 1. Before Map

Use when:

- the question is "what is confusing, coupled, duplicated, or missing now?"
- the ticket spans multiple components
- the reader needs a fast approval surface

Pattern:

```mermaid
flowchart TD
  classDef keep fill:#f3f4f6,stroke:#6b7280,color:#111827
  classDef problem fill:#fff5f5,stroke:#dc2626,color:#991b1b

  input["input / request"]:::keep
  oldOwner["before: old owner or path"]:::problem
  oldState["before: confusing state"]:::problem
  proof["proof/review infers intent"]:::keep

  input --> oldOwner --> oldState --> proof
```

Legend:

- `gray = kept context`
- `red = problem / removed default / confusing ownership`

## 2. After Map

Use when:

- the question is "what will the workflow look like after this lands?"
- the ticket adds or changes an owner, artifact, or proof path
- the reader needs to compare against the `Before` map

Pattern:

```mermaid
flowchart TD
  classDef keep fill:#f3f4f6,stroke:#6b7280,color:#111827
  classDef changed fill:#fef3c7,stroke:#b45309,color:#111827
  classDef added fill:#dcfce7,stroke:#15803d,color:#111827

  input["input / request"]:::keep
  newOwner["after: new owner or path"]:::changed
  newArtifact["after: new/updated artifact"]:::added
  feedback["operator feedback / proof"]:::keep

  input --> newOwner --> newArtifact --> feedback
```

Legend:

- `gray = kept context`
- `amber = changed owner / behavior`
- `green = added artifact / capability`

## 3. What Changed Delta

Use when:

- the question is "what changed?"
- the operator needs to compare old and new ownership, artifacts, or behavior
- the companion should avoid random supplementary diagrams

Pattern:

```mermaid
flowchart LR
  classDef before fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d,stroke-dasharray: 5 3
  classDef after fill:#dcfce7,stroke:#15803d,color:#111827

  old["before: old path / behavior"]:::before --> new["after: new path / behavior"]:::after
  oldOwner["before owner"]:::before --> newOwner["after owner"]:::after
```

Rules:

- include the words `before` and `after` in the visible node labels
- show replacements, moves, or ownership changes directly
- do not create disconnected context diagrams unless they clarify the delta

## 4. Numbered Data-Flow Trace

Use when:

- the question is "how does data move?"
- ordering matters
- the system map alone is insufficient

Pattern:

```mermaid
flowchart TD
  input["user ask"] -->|1| planner["planner"]
  planner -->|2| ticket[(ticket state)]
  planner -->|3| review["review"]
```

Rules:

- keep only the critical path
- number the edges
- avoid side branches unless the branch is the point

## 5. Zoom-In

Use when:

- one subsystem remains unclear after the top-level map
- one interface cluster needs more detail

Rules:

- inherit the same legend/classes as the top-level map
- keep the zoom-in scoped to one subsystem
- do not redraw the whole system again

## 6. Inline Signatures

Use when:

- the function or interface is the important thing
- a detached list would make the reader scroll

Good:

- `planner / buildPlan(ticket): PlanArtifact`
- `state / claim.ticket_id: string`
- `review / judgePlan(plan): pass|fix`

Bad:

- full type definitions
- three-method classes stuffed into one node
- signatures that wrap across many lines

## 7. Impl-Plan Visual Companion

Use when:

- `impl-plan` has produced a material `ticket.md`
- the operator needs a diagram-first reading surface
- diagrams should stay out of the canonical ticket body

Output path:

```text
tickets/TASK-XXXX/diagrams.md
```

Required metadata:

```yaml
status: companion
source: ticket.md
blocks_approval: false
canonical_contract: ticket.md
generated_by: diagramming
```

Shape:

```text
VisualPlan(
  reading_order,
  before,
  after,
  what_changed?,
  change_unit_maps[]?,
  feedback_guide
)
```

Rules:

- use `ticket.md` as the only source of scope
- keep `ticket.md` free of Mermaid by default
- create one `Before` diagram and one `After` diagram
- use colored Mermaid boxes with `classDef` and node classes
- include a `What Changed` delta when a small old-to-new summary helps
- create one compact map per material `Change Plan` unit only when the ticket
  has multiple units that are hard to compare from the top-level diagrams
- keep each unit map to 2-5 nodes plus short `writes`, `proof`, and `risk`
  notes
- do not make the companion a reviewer gate unless the caller explicitly asks
  for diagram review

## Anti-Patterns

Fail the diagram if:

- it has more diagrams than decisions
- it lacks explicit `Before` and `After` diagrams for an `impl-plan` companion
- it lacks colored Mermaid classes for semantic differences
- the labels are paragraphs
- the legend is missing
- the diagram repeats the prose instead of compressing it
