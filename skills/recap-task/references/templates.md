# Recap Task Templates

Load this after the task packet has been reconciled. Choose one template and
remove empty or irrelevant lines. Template labels are scaffolding; replace them
with task facts.

## Selector

Every template opens with this block, filled from N2:

```md
### Problem & goal
- **Problem:** <who hurts, and how, in the user's terms> [confirmed / inferred / open]
- **Goal:** <the change in their experience or the outcome reached> [confirmed / inferred / open]
- **Drift:** <only when the work has moved away from the original problem>
```

| Template | Use when | Required shape |
| --- | --- | --- |
| `idea` | Shaping stage, or the operator asks to see the idea played back | Problem & goal, one proposed visual, correction questions |
| `quick` | The work packet is coherent and the operator needs orientation | Problem & goal, Now, Delta, Risks & action |
| `full` | Requested, or a conflict, failed attempt, or evidence gap changes the safe response | Quick card plus sourced history and ledger |
| `source-gap` | No reliable task boundary or durable source can be read | Known limit, missing source, safe request |

## `idea`

```md
## <task> — proposed model (shaping)

<Problem & goal block>

**Confirm:** <the one thing the operator is being asked to verify>

<one filled template from idea-templates.md, rendered inline>

**Assumptions and open choices:** <inferences and contradictions the visual must not resolve>

**Questions:**
1. <riskiest mismatch>
```

Ask one to three questions. Do not add a status card, plan, or second view.

## `quick`

```md
## <task> — <state / confidence>

<Problem & goal block>

### Now
- **Reply now:** <safe posture>
- **Need now:** <what the operator must answer or decide next>
- **Since you left:** <most decision-relevant update>

### Delta
- **Before:** <prior state> [source]
- **After:** <current state> [source]
  - **Example:** <representative input -> outcome> [source]

### Risks & action
- **Problems:** <material symptom, attempt, and disposition> [source]
- **Open:** <smallest unresolved loop or conflict> [source]
  - **Need from you:** <decision, source, or None>
  - **Evidence limit:** <freshness or coverage limit>
```

## `full`

Begin with the complete `quick` card, then append:

```md
### Details

**Latest user context:** <latest question or decision need> [source]

**Timeline and decisions**
- <YYYY-MM-DD HH:MM> — <one material event> [source]

**Problems and attempts**
- <symptom> -> <attempt> -> <observed result> -> <disposition> -> <remaining impact> [source]

**Evidence and conflicts**
- <what is proven, contradicted, stale, or still unverified> [source]

**Source ledger and gaps**
- `<literal supplied or task-relative path>` — <support and freshness>

Safe next: <one reply posture, decision, or source request>
```

Use one dated bullet per material event. Do not shorten later events to
time-only entries or group source paths with commas, braces, or shorthand.

## `source-gap`

```md
## <task label if known> — source gap

<Problem & goal block, marked open where unknown>

### Now
- **Reply now:** I cannot reconstruct this task reliably from the available context.
- **Need now:** <what the operator is trying to answer or decide>

### Delta
- **Before:** Unknown — no authoritative task record is available.
- **After:** Unknown — no safe comparison can be made.

### Risks & action
- **Problems:** Reconstructing from topic memory would invent task history.
- **Open:** Provide `<smallest useful ticket, artifact, thread reference, or pasted source>`.
  - **Need from you:** <exact source request>
  - **Evidence limit:** <what was available and why it was insufficient>
```
