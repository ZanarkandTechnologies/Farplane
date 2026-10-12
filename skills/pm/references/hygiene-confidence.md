# Confidence And Escalation

## Labels

`high`: enough evidence to write the field in live-high-confidence mode.

Required qualities:

- direct project relation, exact project alias, or unambiguous Plan Week/project
  context
- no conflicting field evidence
- target value exists in the Notion schema or private mapping
- source refs are specific enough to audit

`medium`: good suggestion, not safe to write automatically.

Typical causes:

- one plausible project, but no direct relation or Plan Week tie
- fuzzy date language
- project has multiple possible areas
- tag is likely but not essential

`low`: Kenji should fill or choose.

Typical causes:

- generic task title
- multiple plausible projects or areas
- missing active project/area map
- task requires personal judgment not visible in Notion context
- source context is stale, contradictory, or connector-approximated

`none`: no proposal.

Use when the field is already set, not in scope, or the connector could not
return enough task data to reason.

## Status Mapping

```text
high   -> proposed      -> eligible for typed live write
medium -> suggested     -> report only
low    -> needs_kenji   -> Telegram review request
none   -> abstain/already_set
```

## Telegram Trigger

Send or queue a Telegram request when any of these is true:

- a missing target field is `low`
- a field abstains because of conflicting project/area evidence
- live mode skipped a task because its required private handle was missing
- connector approximation could cause an unsafe project or area write

Do not send a Telegram request for every medium suggestion by default. Medium
suggestions belong in the proposal report unless the user asks for aggressive
human review.

## Escalation Message Shape

The message should answer:

1. Which task needs Kenji.
2. Which field is missing or conflicted.
3. Why automation could not fill it safely.
4. The 2-3 most likely options, when available.
5. The local proposal artifact path.

Keep it short enough to read on a phone.

## Write Eligibility

A field may be written only when:

- proposal status is `proposed`
- confidence is `high`
- value is schema-valid
- source refs do not include unresolved private IDs
- the run mode is `live-high-confidence`
- the typed Notion action path is available
- readback can verify the field after write

If any condition fails, keep the field in the local proposal and do not mutate
Notion.
