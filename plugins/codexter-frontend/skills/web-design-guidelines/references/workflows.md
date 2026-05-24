# Workflows

## Direct Audit

1. Fetch the latest upstream guideline command.
2. Read the requested file or pattern.
3. Report findings in the upstream `file:line` format.
4. Skip scoring unless the caller explicitly asks for review integration.

## Frontend Craft Audit

1. `frontend-craft` identifies changed UI source files.
2. This skill audits those files.
3. The implementation handoff records pass/fail findings or the reason the lane
   was skipped.

## Review Metric

1. `review` loads `references/frontend-guidelines.md`.
2. This skill produces raw findings.
3. `review` converts those findings into a `frontend-guidelines` score.
4. The review artifact keeps that score beside `ui-quality`.
