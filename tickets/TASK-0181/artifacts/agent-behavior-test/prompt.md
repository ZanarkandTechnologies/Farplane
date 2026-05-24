You are testing Codexter's rendered skill install behavior as a fresh skill caller.

Target file:
`tickets/TASK-0181/artifacts/agent-behavior-test/rendered-target/skills/advise/SKILL.md`

Target checklist file:
`tickets/TASK-0181/artifacts/agent-behavior-test/rendered-target/skills/advise/todos.md`

Behavior under test:
The installed `SKILL.md` should be self-contained enough that a skill caller can
see the required checklist on first load, without relying on a second
`todos.md` read.

Required visible checkpoints:
1. Read the target installed `SKILL.md`.
2. Confirm whether it contains `<!-- BEGIN CODEXTER_EMBEDDED_TODOS -->`.
3. Confirm whether it contains the heading `## Embedded Skill Checklist`.
4. Count at least three checklist lines in the embedded section.
5. Do not read the target `todos.md` until after the embedded checklist result
   is determined. If you read it later, report that separately.

Return only this JSON object, with no Markdown fence:

{
  "target": "embedded-skill-checklist-install",
  "persona": "fresh skill caller",
  "checkpoints": [
    {
      "name": "read_installed_skill_md",
      "status": "done | skipped | blocked",
      "evidence": "what file was read"
    },
    {
      "name": "embedded_marker_visible",
      "status": "done | skipped | blocked",
      "evidence": "marker observed or missing"
    },
    {
      "name": "embedded_heading_visible",
      "status": "done | skipped | blocked",
      "evidence": "heading observed or missing"
    },
    {
      "name": "embedded_checklist_count",
      "status": "done | skipped | blocked",
      "evidence": "number of checklist lines counted"
    },
    {
      "name": "todos_file_not_needed_for_first_result",
      "status": "done | skipped | blocked",
      "evidence": "state whether todos.md was avoided until after the result"
    }
  ],
  "artifacts": [
    "tickets/TASK-0181/artifacts/agent-behavior-test/rendered-target/skills/advise/SKILL.md"
  ],
  "deviations": [],
  "verdict": "pass | fail | blocked"
}
