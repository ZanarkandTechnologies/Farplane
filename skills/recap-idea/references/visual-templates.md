# Recap Idea Visual Templates

Load this only after `SKILL.md` has classified the product shape. Choose one
template, replace every placeholder with discussion-grounded content, and
remove irrelevant branches. The template is scaffolding, never visible filler.

## Selector

| Template ID | What is being built | Reader checks | Do not substitute |
| --- | --- | --- | --- |
| `journey` | end-to-end product experience | trigger through user value | component inventory |
| `ui-screen-flow` | screen, interaction, or UI design | what the user sees, does, and sees next | backend architecture |
| `lifecycle` | stateful or recoverable behavior | events, failure, retry, terminal state | generic flowchart |
| `system-boundary` | service, ownership, or information flow | who owns and moves what | UI wireflow |
| `before-after-example` | an existing behavior being changed | concrete experiential delta | generic journey |
| `comparison-table` | exact options, fields, or mappings | correspondence and decision rule | decorative arrows |

When two templates seem plausible, use the operator's verification question as
the tie-breaker. A redesign asking “what will users see?” is `ui-screen-flow`;
the same redesign asking “what changed?” is `before-after-example`.

## `journey`

Use for a new product or end-to-end experience.

```mermaid
flowchart LR
  U["Primary user<br/>current context"]
  T["Trigger<br/>why they begin"]
  A["First action<br/>what they provide or choose"]
  P["Product response<br/>what becomes visible"]
  V["User value<br/>what is now easier or possible"]
  Q["? material assumption"]

  U --> T --> A --> P --> V
  P -. uncertainty .-> Q
```

## `ui-screen-flow`

Use for UI or design discussions. Screen nodes contain user-visible information
and controls, not implementation components. Put the concrete example directly
inside those nodes; never append an ASCII wireframe or separate screen mockup.

```mermaid
flowchart LR
  L["SCREEN: List<br/>Visible: priority + reason<br/>Action: select item"]
  D["SCREEN: Detail<br/>Visible: context + evidence<br/>Action: choose next step"]
  W["STATE: Working<br/>Visible: progress + cancel"]
  S["STATE: Success<br/>Visible: result + next item"]
  E["STATE: Error<br/>Visible: reason + retry"]

  L -->|select| D
  D -->|confirm| W
  W -->|complete| S
  W -->|fail| E
  E -->|retry| W
```

## `lifecycle`

Use when state and recovery are the product question.

```mermaid
stateDiagram-v2
  [*] --> Idle
  Idle --> Working: start
  Working --> Complete: success
  Working --> Partial: incomplete result
  Working --> Failed: error
  Failed --> Working: retry
  Partial --> Working: resume
  Complete --> [*]
```

## `system-boundary`

Use when ownership or information movement is what needs confirmation.

```mermaid
flowchart LR
  subgraph UserBoundary[User surface]
    U[User]
    UI[Product UI]
  end

  subgraph ProductBoundary[Product-owned]
    O[Workflow owner]
    DB[(Owned record)]
  end

  subgraph ExternalBoundary[External]
    X[External source]
  end

  U -->|intent| UI
  UI -->|request| O
  O -->|read / write| DB
  O -->|retrieve| X
  O -->|grounded result| UI
```

## `before-after-example`

Use only for a real change to an existing experience. The example trace proves
the delta in a concrete case rather than adding a third abstract diagram.

```mermaid
flowchart LR
  subgraph Before[Before]
    B1["User opens dashboard"] --> B2["Scans broad metrics"]
    B2 --> B3["Opens panels to find work"]
  end

  subgraph After[After]
    A1["User opens dashboard"] --> A2["Sees ranked work + reason"]
    A2 --> A3["Takes the next action"]
  end

  subgraph Example[Example]
    E1["SLA breach in 18 min"] --> E2["Shown first: reply now"]
  end
```

## `comparison-table`

Use when exact correspondence matters more than direction.

| Item | Current meaning | Proposed meaning | Decision or uncertainty |
| --- | --- | --- | --- |
| `[term / field / option]` | `[observed]` | `[intended]` | `[confirmed / ?]` |

## Template Check

- Does the selected template match what is being built and what the operator
  must verify?
- Did every placeholder become a concrete product noun, action, state, or
  uncertainty from the discussion?
- Can the operator spot the likely misunderstanding from the visual alone?
- Is there one primary visual and no duplicate ASCII rendering?
- For UI, is every concrete screen example inside the Mermaid nodes rather than
  repeated in another format?
