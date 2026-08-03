---
title: "Response Frontier Baseline And Candidate"
status: active
owner: eval
created_at: 2026-08-03
refs:
  - skills/eval/examples/farplane-global-harness/response-frontier-tasks.json
  - templates/global/AGENTS.md
---

# Response Frontier Baseline And Candidate

The frozen three-task suite compared the existing concise-response policy with
the focus-first candidate overlay.

| Case | Baseline | Candidate | Observation |
|---|---:|---:|---|
| Executive delta | B | B | Candidate stayed concise but introduced a placeholder validation image. |
| Single frontier | A | A | Both selected the primary release decision without reopening lower-priority breadth. |
| Asset and flow | C | B | Candidate embedded the video and isolated references, but omitted the useful Mermaid flow. |

Baseline run: `20260803-072522-task9014-response-frontier-baseline-clean`.
Candidate run: `20260803-072730-task9014-response-frontier-candidate`.

The candidate improved one case without regression, but pass rate remained
`0.33`. Treat the policy as a bounded behavioral improvement, not a proven full
promotion. The missing Mermaid flow remains the strongest regression target.
