# Budget Modes

Use this reference when the caller provides a shorthand such as "quick pass",
"normal", "deep", "max effort", "I have 20 minutes", or available time/cost
instead of concrete persona-council fields.

Budget modes are presets over the same base reviewed skill path. They do not
decide whether material work gets reviewed; plan review and work review are
already part of the base path.

## Presets

```text
mode: base
  -> caller skill's normal reviewed path
   + persona_count: 1 only when the caller needs a named single perspective
   + evidence_depth: light unless the caller skill requires stronger proof
```

When returning a Budget Program for `base`, say `budget route:
base_reviewed`. Never describe it as an unreviewed route.

```text
mode: plus
  -> persona_count: 3 when complete persona prompts exist
   + perspective_mode: different
   + synthesis: synthesize
   + evidence_depth: light or strong based on the caller skill's proof need
```

```text
mode: max
  -> persona_count: 5 when complete useful persona prompts exist
   + perspective_mode: different
   + synthesis: synthesize
   + evidence_depth: strong for proof-bearing skills
```

If the caller supplies explicit `persona_count`, complete personas, coverage,
or child `delegate_budget`, the explicit field wins as long as it preserves the
caller output contract and avoids hidden fanout.

## Available Time Mapping

Use time as a constraint, not as a promise to spend all of it.

```text
available_time: "<5m"
  -> base
```

```text
available_time: "5-15m"
  -> base or plus with one narrow persona council only when the decision is
     judgment-heavy
```

```text
available_time: "15-45m"
  -> plus; use three diverse personas when the skill benefits from perspective
     coverage
```

```text
available_time: ">45m"
  -> max for bounded five-persona council work, or route to goal-advisor when
     the work needs a time-bounded continuation loop
```

## Child Skill Budget

Parent budget does not copy downward. A child skill runs its own base reviewed
path unless the caller explicitly allocates child budget:

```text
delegate_budget: {
  advise: { mode: "plus", personas: [...] }
}
```

## Guardrails

- Do not invent persona prompts from vague labels when the caller skill has no
  defaults. Return a persona-lane blocker and name the base reviewed path as the
  executable fallback.
- Do not use `max` to justify unbounded subagent spawning or cloned lanes.
- Do not spend extra budget on repeated review loops after the base plan/work
  reviews are already satisfied.
- Do not emit removed public fields in active Budget Programs; use only the
  current base/plus/max council schema.
- Escalate to `goal-advisor` when the requested budget implies a time-bounded
  continuation loop, heartbeat, rollout, or batch execution.
