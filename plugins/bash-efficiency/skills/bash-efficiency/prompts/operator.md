Use the `bash-operator` subagent for this task.

Task:
<describe the shell-heavy job>

Requirements:
1) Prefer transform-in-place commands (`mv`, `cp -a`, pipes, redirection) over recreating/retyping.
2) Preview before mutation (`ls`, `tree`, `rg` as needed).
3) For risky operations, include dry-run or equivalent verification gate.
4) Return a structured report:
   - Command plan
   - Executed commands
   - Observed execution snapshot
   - Verification evidence
   - Expected vs observed diff + verdict
   - Fix plan (if fail/deviation)
   - Files changed
   - Rollback steps

Constraints:
- If scope is ambiguous, stop and ask.
- Keep command list minimal and deterministic.
