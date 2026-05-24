# Bash Operator Expected Output (ASCII Spec)

This file is the visual QA baseline for `bash-operator` reports.

## Expected Report Shape

```text
+-------------------------------------------------------------+
| Bash Operations Report: <task-name>                        |
+-------------------------------------------------------------+
| Delegation Reason: <why this was delegated>                |
| Risk Level: low | medium | high                            |
+-------------------------------------------------------------+
| 1) Command Plan                                             |
|    - <planned command #1>                                   |
|    - <planned command #2>                                   |
+-------------------------------------------------------------+
| 2) Executed Commands                                        |
|    1. <command> -> success/failure                          |
|    2. <command> -> success/failure                          |
+-------------------------------------------------------------+
| 3) Observed Execution Snapshot                              |
|    - commands run: <count>                                  |
|    - key outputs: <important lines>                         |
|    - errors/warnings: <none|details>                        |
+-------------------------------------------------------------+
| 4) Verification                                             |
|    - expected changed: <paths/output>                       |
|    - unexpected changed: <none|details>                     |
|    - evidence checks: <ls/rg/wc/etc>                        |
+-------------------------------------------------------------+
| 5) Diff Report + Verdict                                    |
|    - top diffs: <expected vs observed>                      |
|    - severity: blocker | major | minor                      |
|    - verdict: PASS | FAIL                                   |
+-------------------------------------------------------------+
| 6) Fix Plan                                                 |
|    - fix 1: <concrete command/workflow correction>          |
|    - fix 2: <concrete command/workflow correction>          |
+-------------------------------------------------------------+
| 7) Files Touched                                            |
|    - <path A> (moved/edited/created/deleted)               |
|    - <path B> (...)                                         |
+-------------------------------------------------------------+
| 8) Rollback                                                 |
|    - <inverse command #1>                                   |
|    - <inverse command #2>                                   |
+-------------------------------------------------------------+
| 9) Final Status: PASS | FAIL                                |
+-------------------------------------------------------------+
```

## QA Assertions

- All 9 sections are present in order.
- Every mutation command has matching verification evidence.
- Non-trivial mutations include rollback steps.
- `Diff Report + Verdict` compares expected vs observed explicitly.
- `Final Status` is explicit and justified by verification/diff blocks.
