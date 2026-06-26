# Framework Validation

## Goal
- Prove the Farplane project substrate still matches the framework file
  contract.

## Fast Entry
- Route or deep link: n/a.
- Shortcut or debug control: n/a.
- Panel or mode to open directly: terminal at repo root.

## Setup
- Auth / fixture / seed: none.
- Reset path: do not reset; inspect git status before broad fixes.
- Commands:
  - `python3 bin/validators/check_farplane_project_files.py`
  - `python3 bin/validators/check_harness_invariants.py`
  - `python3 bin/validators/check_doc_refs.py`

## Stable Selectors
- `data-testid`: n/a.
- Roles / labels: n/a.
- Assertion targets: each command exits zero.

## agent-browser Path
1. Not applicable for framework-only validation.
2. Use terminal proof unless a UI ticket explicitly asks for browser evidence.

## Playwright Path
1. Not applicable unless Farplane UI is the active repo under test.

## Observability
- Validator output.
- Git diff for changed framework files.
- Ticket proof artifacts when a ticket owns the work.

## Known Gaps
- Add a single wrapper command if these checks become too verbose for agents.
