# Intake and Readiness

Load in `init`, `migrate` or `charter` mode when human-meaning files are
missing, placeholder, stale or newly introduced.

## Completion states

- `substrate_complete`: Farplane files exist or were preserved; missing intent
  is written as readiness gaps in `docs/bootstrap-brief.md`.
- `project_initialized`: the charter carries real operator intent, measurable
  objectives with honest providers, non-goals and authority. File existence is
  not readiness: placeholder split files mean "operating model still missing".

PRD authoring is downstream of the business foundation, not init completion.

## `human_intake`

- `skip`: scaffold or migrate mechanically; write missing intent as gaps.
- `offer` (default): offer a short intake before filling meaning-heavy files.
- `required`: do not finalize meaning-heavy content until the operator-owned
  params are answered or recorded as blocked.

Use the destination signatures as the question inventory: charter, capability
refs, feedback loops, missing systems and objective shape belong to charter
mode; metric meaning, direction, guards and proof providers belong to the
`goal-advisor` metric card. Ask the first missing param directly; run a focused
clarification only when direct questions would give shallow or contradictory
answers. Never run a second long interview. Record the intake choice and the
missing answers in `docs/bootstrap-brief.md`.

## Split ownership

- `farplane/harness.yaml`: identity, thesis, non-tradeoffs, authority, change
  rule, planning areas, capability refs, selected metric IDs and priorities.
- `farplane/metrics.yaml`: label, unit/type/display, direction, freshness,
  guards and one `refresh` or `refresh_ref` per metric.
- `farplane/bindings.yaml`: non-secret provider coordinates only.
- `farplane/automations/`: one file per approved live routine.
- GitHub issues: temporary commitments, unblock work and the selected milestone.

Use `goal-advisor` only after an issue is concrete enough for a Goal Packet.

```text
setup_operating_model(bootstrap_brief, project_context, existing_harness?,
                      existing_capability_skills?, existing_metrics?, human_intake?)
  -> readiness_status + human_intake_decision + first_missing_question?
   + harness_delta? + capability_skill_delta? + metric_objective_delta?
   + goal_advisor_handoff?
```
