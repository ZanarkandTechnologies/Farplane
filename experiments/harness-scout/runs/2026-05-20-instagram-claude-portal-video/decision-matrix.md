# Decision Matrix

| Feature | Source anchor | Source evidence | Local match | Scores | Decision | Reason | Ticket action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frame-grounded source reconstruction | Representative frames show the process sequence and final artifact. | Strong visual evidence from downloaded video frames; no audio transcript. | Partial: `harness-scout` handles source scouting but not frame storyboard extraction. | user-value 5, evidence-strength 4, local-fit 5, novelty 4, implementation-cost 4, risk-control 4, benchmarkability 5 | `adapt` | This directly improves the user's requested test: watch video, select relevant frames, infer a reproducible workflow, and propose a skill. | Create a ticket to add a `harness-scout` video-reconstruction method or a compact new Tier 3 skill after approval. |
| One-prompt interactive artifact replay | Burned-in captions say "in one prompt" and show a Claude artifact/prompt checklist. | Medium evidence; result exists, but exact prompt and debugging loop are not fully visible. | Partial: frontend skills can build the artifact, but Codexter should preserve iterative proof rather than worship one-prompt output. | user-value 4, evidence-strength 3, local-fit 4, novelty 3, implementation-cost 3, risk-control 3, benchmarkability 4 | `hybrid` | Adopt the reconstruction discipline, not the literal one-prompt constraint. | Include as an optional benchmark variant, not a default implementation rule. |
| Time-coded event extraction | Frame shows `0ms->2200ms: Landing` and `2200ms->3200ms: Transition`. | Strong single-frame evidence. | Partial: `remotion` and `visual-qa` can verify timing once specified. | user-value 4, evidence-strength 4, local-fit 4, novelty 3, implementation-cost 4, risk-control 5, benchmarkability 5 | `adapt` | Time-coded source evidence can become measurable acceptance criteria for reconstructed motion. | Add to proposed method output contract as `event_timeline`. |
| Source-to-skill proposal scorecard | User explicitly requested a test of video understanding and skill proposal quality. | Strong operator intent plus source run evidence. | Partial: `harness-advisor` places the work, `skill-creator` shapes skill quality, but no frame-grounding scorecard exists. | user-value 5, evidence-strength 5, local-fit 5, novelty 4, implementation-cost 4, risk-control 4, benchmarkability 5 | `adapt` | Codexter can use this as a repeatable benchmark for video-derived skill synthesis. | Add scorecard dimensions to the handoff. |

## Decision

Adapt the source into a Codexter-native video reconstruction workflow. Do not
adopt the source's one-prompt framing as a hard rule, and do not create a
general media crawler. The valuable capability is bounded, evidence-first
visual reconstruction from an operator-provided video URL or local file.
