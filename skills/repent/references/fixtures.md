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

## 6. Post-Fix Lesson Capture

- `User:` `repent lesson, the fix was that you should have updated the ticket before claiming done`
- `Expected behavior:`
  - verify the fix status and evidence path
  - create a compact seed packet
  - append a `docs/LESSONS.md` row
  - create a Notion proposal only if private Notion context and tools are available
  - do not update `docs/MEMORY.md` from a single raw lesson

## 7. Hardcase Capture

- `User:` `repent hardcase, this is a good training sample now that it is fixed`
- `Expected behavior:`
  - verify the fixed outcome first
  - create a sanitized `experiments/hardcases/YYYYMMDD-HHMM-*/case.md`
    artifact
  - include failure class, correction, correct behavior, evidence refs, future
    eval idea, and privacy level
  - do not include raw private transcript bulk or secrets

## 8. High-Priority Eval Capture

- `User:` `repent eval, this should never happen again`
- `Expected behavior:`
  - verify the corrected miss and fixed outcome first
  - create or update the narrowest regression eval that would have caught the
    miss
  - use the owning eval surface, such as `.codex/evals/tasks/*.json` for
    project-level Codex behavior
  - keep `query` as a realistic user prompt and put proactive expectations in
    `reference_points`
  - run structural eval validation and, when available and worth the cost, an
    `agent-behavior-test` or `agent-qa-test` proof pass
  - report the eval task path, task ID, run result or skipped-run reason, and
    any hardcase artifact
