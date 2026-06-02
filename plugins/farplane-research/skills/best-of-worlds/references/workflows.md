# Best Of Worlds Workflows

## Full Synthesis

1. Define target user, job, artifact, and local constraints.
2. Create the source inventory.
3. For each source, extract:
   - feature or pattern
   - evidence location
   - user job it serves
   - metric or success signal
   - risks and dependencies
4. Cluster duplicate or overlapping features.
5. Discover metrics for the target workflow.
6. Score candidates with the feature scoring rubric.
7. Decide adopt/adapt/reject/defer.
8. Write the combined workflow and implementation handoff.

## Fast Synthesis

Use when the user already gave a short source list and wants action:

1. Extract the top 3-7 concrete techniques.
2. Reject source-specific or high-cost ideas quickly.
3. Recommend one combined workflow.
4. Implement the obvious low-risk changes.
5. Leave follow-ups for anything requiring a new architecture decision.

## Metric-First Synthesis

Use when the target says "optimize" but not "optimize what":

1. Identify the target user and job.
2. Choose the artifact that changes.
3. List 3 candidate primary metrics.
4. Pick one guard metric and one anti-metric.
5. Use `advise` to recommend the metric set when tradeoffs remain.
6. Only then score source features against that metric set.
