# Goal Algebra

`goal-crafter` compiles named workflow skills into one native Goal contract.

```text
Goal := Task + Metric + Review + Resolve
```

- `Task` names the desired end state, boundaries, constraints, and non-goals.
- `Metric` names the mechanical, human, or hybrid signal that proves progress.
- `Review` names the proof providers such as agent QA, human feedback, or final
  review.
- `Resolve` names how the agent accepts, reruns, fixes, asks for feedback, or
  stops blocked.

Composition examples:

- `agent-qa-test` supplies adversarial proof and rerun/fix thresholds.
- `hitl-autoresearch` supplies human feedback files and human-score metrics.
- `review` supplies the final proof-bundle judgment.
