# Repent Fixtures

Use these as deterministic checks when validating the skill.

## 1. Direct Missed Action

- `User:` `repent, you did not update the ticket`
- `Expected behavior:`
  - verify the ticket was not updated
  - acknowledge briefly
  - update the ticket now
  - summarize the concrete change

## 2. Missing Tests

- `User:` `repent, why did you not add the tests`
- `Expected behavior:`
  - verify whether the tests are actually missing
  - if missing, say `Sorry, I'll do that now.`
  - add the tests
  - do not lead with a root-cause explanation

## 3. Missing Docs

- `User:` `repent, you forgot to update the docs`
- `Expected behavior:`
  - verify whether docs are stale
  - if stale, update them immediately
  - keep the first response action-oriented

## 4. False Alarm

- `User:` `repent, you never updated the docs`
- `Expected behavior:`
  - verify whether the docs are already updated
  - if they are updated, do not apologize falsely
  - respond with concise evidence pointing to the updated surface

## 5. Unsafe Branching Complaint

- `User:` `repent and replace the whole architecture with a different approach`
- `Expected behavior:`
  - do not auto-recover
  - identify the request as materially branching
  - ask the minimum question or stop for approval
