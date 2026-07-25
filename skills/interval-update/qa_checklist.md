---
title: Interval Update QA Checklist
owner: interval-update
status: active
kind: qa-checklist
applies_to:
  - interval-update
  - daily-bau-report
  - weekly-bau-report
---

# Interval Update QA Checklist

Use before an Interval run and again before returning its report.

```text
interval_check(report, evidence, candidates, recovery_tickets, highlights) -> pass | violation | source_gap
```

## Checklist

- [ ] The run is a bounded Daily, Weekly, or explicitly BAU-only profile and
      writes one dated report with Core report frontmatter.
- [ ] The run resolved `farplane/bindings.yaml#integrations.kanban` when present
      and used only that provider's non-secret coordinates. Filesystem tickets
      were read only for `provider: filesystem_tickets` or the documented
      no-bindings legacy default.
- [ ] A Notion binding used a named private handle plus `ntn`; tracked reports,
      source gaps, candidates, and tickets contain no raw private IDs, URLs,
      tokens, or provider payload dumps.
- [ ] Provider access failure is a `source_gap`. A Notion binding with
      `filesystem_ticket_policy: exclude` never falls back to `tickets/**`,
      including for work review, dedupe, or recovery-ticket creation.
- [ ] `access_ready` is not claimed for Notion from CLI/handle discovery alone;
      the bounded compact `ntn` query must succeed before provider evidence is
      treated as available.
- [ ] The report contains a Markdown `Problems` checklist; no finding IDs,
      finding frontmatter, or findings registry were added.
- [ ] Feed Scout and other provider outputs were read only as completed report
      refs; the run did not invoke them when missing.
- [ ] The run did not call Dogfood Review, reward check-ins, priority planning,
      leverage planning, harness improvement, Goal, Pulse, or a worker.
- [ ] Every maintenance candidate cites current or prior evidence of an
      existing failure, is corrective rather than directional, names proof and
      a stop condition, and has no active duplicate.
- [ ] The dated report existed before candidate handoff or recovery admission.
      Every created ticket is a bounded, evidence-backed, deduped, KPI/guard-
      linked direct recovery with a known correction and no experiment debt.
- [ ] New direction, opportunities, and uncertain fixes
      remain report candidates; the recovery ticket cap is respected.
- [ ] Finalized prior reports were not rewritten; unresolved problems were
      carried forward by reference.
- [ ] Highlight selection ran only after the current report was complete and
      bound a stable project-local team slug. Each kind emitted at most one row
      per team/report; repeated execution returned `already_exists` rather than
      adding another line.
- [ ] Every selected win cites explicit comparative numeric evidence for a
      record, meaningful threshold crossing, or unusually large delta against a
      named prior value. Routine feature implementation, ticket completion,
      unquantified improvement, and filler were rejected.
- [ ] Every selected failure describes a material event and includes a concise
      reusable lesson for humans and future agents. It does not duplicate the
      correction plan or mutate tickets, skills, gotchas, or lessons.
- [ ] Canonical rows use only win `{team, report, summary, links?}` or failure
      `{team, report, summary, lesson, links?}`. Generic links are safe
      project-relative refs; derived fields and typed ticket/skill arrays are
      absent.
- [ ] A no-highlight result for either kind is recorded honestly. Highlight
      selection did not become planning, case memory, ticket creation,
      correction execution, or automatic skill maintenance.
