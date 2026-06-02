# Goal Prep Cases

## Ticket-Backed State

Input:

```text
Use goal-crafter for a ticket that already has Summary, Acceptance Criteria,
Proof Contract, Scope Out, Verification, and Blockers.
```

Expected behavior:

- Compile `GoalPrepState` from the ticket.
- Preserve the ticket metric or `Metrics: none mechanical`.
- Put acceptance criteria plus proof/review evidence into `done`.
- Ask no questions when objective, validation, constraints, and blocker policy
  are already present.
- Produce a paste-ready `/goal` that hands execution to `$work` when admission
  is still useful.

## Proxy Evidence Rejected

Input:

```text
The task is done because a Notion page was created.
```

Expected behavior:

- Treat page creation as proxy evidence.
- Require readback, required relation fields, task body content, and review
  evidence when those are part of the actual objective.
- Label incomplete proof as partial or blocked instead of completion.

## Quantified Issue Hunt

Input:

```text
Find 20 meaningful problems in this workflow and make tickets for them.
```

Expected behavior:

- Include count, severity threshold, duplicate handling, reproduction evidence,
  ticket creation proof, and review gate in `GoalPrepState`.
- Stop only when 20 unique qualifying issues are proven or the blocker report
  explains why the remaining count cannot be reached.

## Tiny Direct Ask

Input:

```text
Rename one label in one file.
```

Expected behavior:

- Recommend a normal prompt or direct edit.
- Do not add `GoalPrepState` ceremony.
