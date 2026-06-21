# Tournament And Hierarchical Aggregation

Use this template when `ensemble.count` is too large for one flat synthesis, or
when the caller explicitly requests tournament-style execution.

For LLM work, tournament should usually mean grouped aggregation, not
winner-take-all elimination. Many candidates contain useful partial ideas even
when they are not the single best candidate.

## Inputs

```text
ensemble.count: number
group_size: number
aggregation: "hierarchical_synthesis" | "score_then_synthesize" | "select"
scoring_rubric?: text
combination_prompt?: text
caller_skill:
output_contract:
```

## Program: Hierarchical Synthesis

```text
lane_outputs = run N lanes
groups = chunk(lane_outputs, group_size)

group_summaries = []
for group in groups:
  group_summaries += synthesize group into:
    - best ideas
    - strongest dissent
    - evidence gaps
    - candidate final answer

final = synthesize group_summaries into caller skill output contract
return final
```

Use this as the default for large advice, planning, strategy, and research
synthesis. It reduces context pressure while preserving diverse ideas.

## Program: Score Then Synthesize

```text
require scoring_rubric
lane_outputs = run N lanes
groups = chunk(lane_outputs, group_size)

for group in groups:
  score each candidate
  keep top candidates and useful fragments
  write group summary

final = synthesize top candidates and useful fragments
return final with score rationale
```

Use this when quality can be judged with explicit criteria, but useful
fragments should still survive.

## Program: Select

```text
require scoring_rubric
lane_outputs = run N lanes
groups = chunk(lane_outputs, group_size)

winner_per_group = select best candidate per group
final = select best candidate from winner_per_group
return final
```

Use pure selection rarely. It fits tasks where one answer must win and the
selection rubric is trustworthy.

## Guardrails

- Do not call a process "tournament" unless the grouping, scoring, and
  aggregation rule are explicit.
- Do not discard dissent or evidence gaps merely because a candidate loses.
- Use `hierarchical_synthesis` when the goal is to combine perspectives.
- Use `select` only with a real scoring function.
- For very large N, consider a Goal Packet, workflow manifest, or batch goal so
  state and proof survive across turns.

## Output Fragment

```text
tournament_program:
  template_ref: skills/budget-advisor/references/tournament-aggregation.md
  count:
  group_size:
  aggregation:
  scoring_rubric:
  combination_prompt:
  final_output_contract:
```
