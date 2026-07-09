---
kind: product-loop
id: distribution
label: Evidence content
status: active
created_at: 2026-07-08
updated_at: 2026-07-08
sort_order: 40
lane: trust_distribution
lane_purpose: distribute proven evidence
default_weight: 15
audience: potential users and serious builders
output: post, demo, video, paper, or launch note
reward: qualified attention, useful feedback, adoption
owner_skill: farplane-evidence-content
skill_ref: farplane/products/distribution/skill.md
progress_ref: farplane/products/distribution/progress.md
worker_budget_min: 2
max_tickets_in_review: 3
review_channel: telegram through worker-artifact-review-request
human_gates:
  - post
  - publish
  - spend
  - account_mutation
  - external_contact
kpis:
  primary:
    - x_views
    - instagram_views
  supporting:
    - evidence_distribution_reach
    - posts_published
    - x_likes
    - instagram_likes
    - instagram_comments
    - instagram_shares
    - instagram_saves
    - instagram_reach
    - instagram_total_interactions
    - instagram_avg_watch_time
    - instagram_total_watch_time
    - instagram_retention_score
    - x_followers
    - instagram_followers
  guardrail: []
supporting_skills:
  - content-impl-plan
  - storyboard
  - asset-advisor
  - avatar-advisor
  - audio-advisor
  - remotion
  - social-content
  - landing-page
  - video-production
  - infographic
  - reel-collage
  - product-photography
  - ai-image-advisor
  - ai-video-advisor
  - x-account
  - instagram-account
goals:
  - id: evidence_distribution_loop
    scope: product
    target: Turn accepted Farplane evidence into qualified attention, useful feedback, and adoption signals.
    kpis:
      - x_views
      - instagram_views
      - evidence_distribution_reach
    interpretation: Distribution is working when content is tied to real harness evidence and produces audience or user signals worth feeding back into strategy.
artifact_workflows:
  - id: landing_page_offer
    lane: trust_distribution
    owner: landing-page
    planning_artifact: offer angle, hero premise, or concept card
    execution_artifact: landing page draft, HTML, screenshot, or preview URL
    feedback_question: keep / revise / reject the offer and page direction
  - id: social_thread
    lane: trust_distribution
    owner: social-content:twitter-thread
    planning_artifact: hook and argument concept card
    execution_artifact: draft thread
    feedback_question: keep / revise / reject the hook and argument
  - id: evidence_carousel
    lane: trust_distribution
    owner: social-content:carousel
    planning_artifact: proof story concept card
    execution_artifact: carousel outline or slides
    feedback_question: keep / revise / reject the proof story
  - id: explainer_script
    lane: trust_distribution
    owner: content-impl-plan
    planning_artifact: explanation angle, Tasty Pack/reference, or storyboard premise
    execution_artifact: short script, storyboard, and advisor action list
    feedback_question: keep / revise / reject the explanation
  - id: demo_video_brief
    lane: trust_distribution
    owner: content-impl-plan
    planning_artifact: demo angle, proof claim, or Tasty Pack/reference
    execution_artifact: video concept, storyboard, asset plan, and Remotion route
    feedback_question: keep / revise / reject the demo angle
notes: Turns accepted evidence into distribution artifacts; content-impl-plan compiles idea plus Tasty Pack/reference into an advisor action list, while child skills own craft, assets, generation routes, composition, and platform constraints.
---

# Evidence Content

This product loop distributes proof Farplane has actually earned. It should
market evidence, demos, learnings, and adoption gaps without inflating claims.

## Current Strategy

```yaml
strategy:
  owner: interval-update
  cadence: daily evidence refresh, weekly strategy review
  horizon: current week
  status: active
  focus: turn accepted Farplane evidence into qualified attention and useful adoption signals
  current_hypothesis: proof-backed content works when it starts from a real harness contrast and ends in a reviewable artifact
  allocation_hint: 15
  next_moves:
    - choose one accepted proof or surprising lesson with audience tension
    - create or resume one bounded content ticket below the review cap
    - stop before posting, publishing, spend, account mutation, or external contact
  last_interval_ref:
  next_review: next daily or weekly interval
```

Intervals may update this strategy block and nearby prose after reading all
products, product progress logs, tickets, metrics, reports, and registry state.
`product.md` is the tracked product loop program. Generated `products.json` must be regenerated only when frontmatter changes.

## Loop Contract

- `primary_output:` trust-building content from accepted evidence: post, demo,
  video, paper, launch note, script, storyboard, carousel, or publish-ready
  draft.
- `primary_metric:` qualified attention, useful feedback, adoption, or accepted
  reviewable artifact before publish.
- `worker_budget:` derive from `default_weight`; default minimum `2`.
- `max_tickets_in_review:` `3`.
- `review_channel:` `telegram` through `worker-artifact-review-request`.
- `human_gates:` post, publish, spend, account mutation, external contact.
- `runtime_progress:` `progress.md` is local ignored runtime learning. Do not
  promote or install it as product skill doctrine.

## Product Loop

1. Read accepted proof, recent content attempts, Feed Scout signals, Kenji
   approvals/rejections, and product-loop progress.
2. Rank content moves by ICP resonance, trend relevance, surprise, proof
   strength, artifact ambition, and local autonomy.
3. Create or resume one bounded content ticket when tickets in review are below
   `max_tickets_in_review`.
4. Judge the artifact from Kenji/reviewer feedback and honest market or review
   signals.
5. Record what worked, what missed, and the next distribution lever in
   `progress.md`.

## Progress Entry Shape

Append compact runtime entries to `progress.md` using this shape:

```markdown
## <YYYY-MM-DD HH:MM +TZ> - cycle <n>

- `metric:` <primary reward being optimized>
- `tickets_in_review:` <count or unknown>
- `workers:` <worker count/threads if known>
- `prior_attempt:` <recent ticket/artifact/learning refs>
- `candidate_moves:` <ranked ideas or pointer to artifact>
- `selected_move:` <chosen lever>
- `why:` <strategy/reward rationale>
- `ticket_refs:` <tickets created/resumed>
- `artifact_refs:` <outputs/proof/review refs>
- `feedback_result:` <accepted/rejected/revised/blocked/pending>
- `learning:` <what worked or missed>
- `next_lever:` <next highest-leverage move>
- `blocker:` <none or blocker>
```
