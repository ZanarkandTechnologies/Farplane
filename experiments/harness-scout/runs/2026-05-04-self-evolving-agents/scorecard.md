# Manual Benchmark Scorecard

## Task
Given the video source, identify useful harness features, dedupe them against
Codexter, decide what to adopt/adapt/reject/defer, and produce a ticket-ready
handoff only for high-value missing features.

## Variants

1. `current-codexter`: use existing summarize, parity/gap/best-of-worlds,
   tickets, and Markdown inventory without the new registry/scout workflow.
2. `source-proposed`: emulate the video's memory/skill-learning proposal as the
   main workflow.
3. `best-of-worlds`: use the new feature registry plus harness-scout workflow,
   while importing only source ideas that pass local evidence and fit checks.

## Scores

| Dimension | Current Codexter | Source-proposed | Best-of-worlds |
| --- | ---: | ---: | ---: |
| task-completion | 7 | 6 | 9 |
| evidence-quality | 7 | 5 | 9 |
| operator-trust | 8 | 5 | 9 |
| autonomy-resume-quality | 8 | 6 | 9 |
| overhead-cost | 8 | 4 | 7 |
| maintainability | 8 | 4 | 9 |
| average | 7.7 | 5.0 | 8.7 |

## Winner
`best-of-worlds`

## Confidence
Medium. The scorecard is a manual judgment over one source and one task. It is
useful for choosing the next implementation slice, not for claiming scientific
benchmark superiority.

## Anti-Metrics

- Do not reward hidden transcript memory over visible ticket/docs evidence.
- Do not reward autonomous skill writing unless safety, review, and dedupe are
  proven.
- Do not reward higher automation when it creates duplicate tickets or stale
  memory.
- Do not reward a source-proposed variant that depends on unapproved background
  agents.

## Notes
The new workflow wins because it keeps Codexter's visible artifact discipline
while borrowing the source's feature-extraction and self-learning lens. The
source-proposed approach is interesting but too eager to mutate memory and
skills without first proving dedupe, safety, and review quality.
