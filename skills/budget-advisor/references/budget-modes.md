# Budget Modes

Use this reference when the caller provides a shorthand such as
`budget_mode: deep`, "I have 20 minutes", or "max effort" instead of concrete
fields.

Budget modes are presets. They are not a replacement for explicit fields. When
explicit fields conflict with a preset, the explicit field wins.

## Presets

```text
budget_mode: none
  -> call the base skill directly
```

```text
budget_mode: light
  -> review_depth: 0
   + ensemble: none
   + evidence_depth: light
```

```text
budget_mode: normal
  -> review_depth: 1
   + ensemble: none unless the caller skill says lanes are cheap and useful
   + evidence_depth: light
```

```text
budget_mode: deep
  -> review_depth: 1
   + ensemble.count: 3-5 when the skill benefits from independent lanes
   + ensemble.perspective_mode: different when persona prompts exist
   + aggregation: synthesize
   + evidence_depth: strong for proof-bearing skills
```

```text
budget_mode: max
  -> review_depth: 1-2
   + ensemble.count: choose the largest useful count allowed by time/context
   + aggregation: hierarchical_synthesis for large N
   + evidence_depth: strong
```

## Available Time Mapping

Use time as a constraint, not as a promise to spend all of it.

```text
available_time: "<5m"
  -> none or light
```

```text
available_time: "5-15m"
  -> normal; one review pass or one small ensemble, not both unless cheap
```

```text
available_time: "15-45m"
  -> deep; small ensemble plus one review pass when the skill supports it
```

```text
available_time: ">45m"
  -> max; consider large ensemble, hierarchical aggregation, or a Goal Packet
     if work must continue across turns
```

## Guardrails

- Do not invent persona prompts from vague labels when the caller skill has no
  defaults. Ask for personas or use same-perspective ensemble.
- Do not use `max` to justify unbounded subagent spawning.
- Do not spend extra budget on review loops after repeated reviews produce only
  duplicate or cosmetic findings.
- Escalate to `goal-advisor` when the requested budget implies a time-bounded
  continuation loop, heartbeat, rollout, or batch execution.
