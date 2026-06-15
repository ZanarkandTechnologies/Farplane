---
kind: council-decision
status: draft
created_at: 2026-06-13
decision: harness-creator-design
context_ref: .farplane/context/2026-06-13-harness-creator-council-context.md
---

# Harness Creator Design Decision

## Decision

Create `harness-creator` as an experimental generic Tier 3 meta skill backed by
a portfolio/schema template. It should replace or retire the scratch
`business-harness` abstraction after migration.

`harness-creator` owns the progressive procedure for turning a high-level goal
into a visible harness design. It does not run the goal, publish externally,
create hidden autonomy, or absorb `goal-advisor`.

## Stakes

A good design lets Farplane start from ambitious goals and work backward into
the right operating harness: research, workflow model, skill inventory, missing
primitive plan, state surfaces, feedback loops, and first executable frontier.

A bad design either bloats `goal-advisor`, creates another vague orchestrator,
overproduces skills, hides state, or claims autonomous capability before pilot
evidence exists.

## Grounding

- `docs/fundamentals/harness-engineering-doctrine.md` says repeated procedures
  belong in skills, long-horizon work belongs in portfolios plus child Goal
  Packets, current external truth belongs in tools/search, and root/global
  prompts are last.
- `docs/specs/goal-loop-contract.md` says native Goal is for the selected
  executable leaf; portfolio heartbeat/manual resume owns parent orchestration.
- `skills/goal-advisor/SKILL.md` owns Goal architecture and prompt
  compilation, not domain discovery.
- `skills/harness-advisor/SKILL.md` owns placement decisions for Farplane
  surface changes, not high-level goal harness design.

## Perspectives

### Operator Value

Recommended a generic Tier 3 skill plus compact portfolio template. The first
lovable slice is a one-page visible harness packet with goal understanding,
workflow map, skill inventory, missing primitives, feedback loop, and first
`goal-advisor` handoff.

### Engineering Risk

Recommended a generic Tier 3 skill plus template, with `business-harness`
retired as scratch. The design must avoid auto-creating skills, hidden runtime,
expanded `goal-advisor` scope, and unvalidated registry drift.

### Evidence Skeptic

Recommended not claiming broad reusable power yet. Treat `harness-creator` as
pilot-only or explicitly experimental until at least one reviewed pilot proves
the workflow works.

### Systems Fit

Recommended a generic Tier 3 skill. The skill owns procedure; templates own
schema; tickets and Goal Packets own durable execution state; `goal-advisor`
compiles the selected leaf; `harness-advisor` handles Farplane surface
placement; research/tools provide external truth.

## Critique / Ranking

### Option A: Generic Tier 3 `harness-creator` Skill Plus Templates

Best fit if the repeated value is the procedure: discover domain, choose
levers, inventory skills, identify missing primitives, set feedback loops, and
hand off to `goal-advisor`.

Risk: can become a vague meta-orchestrator unless first-load gates are sharp
and pilot evidence is required.

### Option B: Template-First Portfolio Schema With Thin Wrapper

Best fit if the main value is artifact shape. Lower implementation risk and
faster pilot.

Risk: may under-specify the actual decision workflow, causing each agent to
rediscover research, skill inventory, and missing-primitive rules.

### Option C: Expand `goal-advisor` Or `harness-advisor`

Best fit only if the new behavior is actually Goal compilation or Farplane
surface placement.

Risk: wrong ownership. It would blur domain discovery with Goal execution or
turn `harness-advisor` into a broad orchestrator.

Ranking:

1. Option A, with experimental/pilot gates.
2. Option B, if implementation must be minimized before pilot.
3. Option C, reject for now.

## Recommendation

Implement Option A, but with the skeptic's guardrail:

```text
harness_creator(high_level_goal, context?, constraints?)
  -> harness_packet
   + domain_research_plan
   + operating_loop
   + capability_map
   + missing_primitive_plan
   + portfolio_schema
   + feedback_loop_plan
   + goal_advisor_handoff
```

Mark the first version experimental and pilot-gated. The first pilot should be
the faceless AI/harness engineering channel because it exercises research,
internal content mining, content production, publishing gates, feedback loops,
and Goal Advisor handoff without needing payments or customer operations first.

## Dissent

The strongest dissent is template-first: we might not need a full skill yet.
If a richer `harness-portfolio.md` template alone guides agents to useful
Goal Packets with less ceremony, then `harness-creator` should stay a thin
wrapper or collapse into template guidance.

## Tradeoff Accepted

We accept slightly more structure now to avoid scattering the workflow across
ad hoc prompts. We reduce overreach by making the skill experimental, requiring
visible packets, forbidding hidden runtimes, and requiring pilot evidence before
claiming broad capability.

## Confidence

Medium-high for the ownership decision. Medium for the exact first-load shape
until the pilot proves where agents need more or less guidance.

## Next Owner

`skill-creator` should rework the scratch `skills/business-harness/` into
`skills/harness-creator/` with:

- generic high-level goal trigger;
- business/channel as examples, not the core abstraction;
- `templates/harness-portfolio.md`;
- `templates/capability-map.md`;
- `templates/missing-primitive-plan.md`;
- `templates/goal-advisor-handoff.md`;
- explicit pilot gate and review requirement.

## Proof / Evidence Gap

Proof should be one pilot artifact:

```text
high_level_goal: build a faceless AI and harness engineering channel
output:
  harness packet
  research plan or brief
  capability map
  missing primitive plan
  Goal Advisor handoff for the first pilot video
review:
  Does it reduce handholding?
  Does it avoid premature skill creation?
  Does it produce an actionable first Goal Packet?
  Does it preserve side-effect gates?
```

Only after that pilot should Farplane claim `harness-creator` as a reliable
goal-to-harness primitive.
