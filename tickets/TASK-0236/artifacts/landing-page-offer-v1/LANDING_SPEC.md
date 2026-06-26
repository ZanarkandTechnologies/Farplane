---
kind: landing-spec
ticket_id: TASK-0236
artifact_id: landing-page-offer-v1
target: trust_distribution / landing_page_offer
status: review
phase: implementation
approval_source: pending_human_feedback
created_at: 2026-06-26T22:08:00+08:00
owner: taste-loop-worker
---

# Farplane Landing Page Offer V1

## Offer

Farplane is a local-first harness for people running serious Codex work: it
turns agent activity into ticketed loops, bounded skills, proof artifacts, and
human feedback checkpoints that can be kept, revised, or rejected quickly.

## Audience

The first buyer is a technical founder, AI operator, or research builder who is
already running multiple Codex or agent threads and needs the work to become
auditable instead of scattered across chat history.

## Promised Transformation

From "I have several agents doing vague work" to "I have a visible work loop
with a contract, artifacts, evidence, and a clear next human decision."

## Non-goals

- Do not present Farplane as a hosted agent cloud, managed scheduler, or public
  control plane.
- Do not claim customer adoption, revenue, enterprise security, or third-party
  integrations not proven by the repo.
- Do not ask for publishing, spend, or external customer contact from this
  pilot.

## Decision Boundaries

- This artifact is a first offer test, not a final public website.
- The review question is only whether to keep, revise, or reject the offer and
  page direction.
- A future build can become premium/cinematic only after Kenji accepts the
  narrative and asset plan.

## Reference Research

| Source | Asset strategy | Storyline | Layout / motion | Proof pattern | Claim boundary |
| --- | --- | --- | --- | --- | --- |
| Terminal Industries, AI-native yard operations | Operational world, command-center language, yard-as-system imagery | Physical chaos becomes an AI operating layer | Cinematic industrial page, strong first viewport, demo CTA | Specific category, Gartner/yard-management positioning, demo request | Stays inside logistics yard operations rather than generic AI |
| Palantir AIP | Real-world operational systems, platform screens, enterprise language | AI connects to data, actions, and operational decisions | Dense enterprise product navigation, proof-heavy platform pages | Mission-critical customers and operating-system framing | Avoids casual productivity claims; focuses on institutions and operations |
| LangGraph | Framework diagrams, code/product snippets, reliability language | Build reliable agents with durable execution and human oversight | Developer-product page with docs, use cases, and proof quotes | Durable execution, human-in-the-loop, ecosystem credibility | It is an agent framework, not a taste/proof harness |
| CrewAI | Product UI, CLI/no-code modes, enterprise agent platform claims | Build, deploy, manage agents from first automation to many | Clear hero, segmented product modes, enterprise CTAs | Fortune 500 usage and adoption language | Sells agent production, not artifact-first review loops |

## Best-of-worlds Decisions

| Pattern | Source | Decision | Local use |
| --- | --- | --- | --- |
| One concrete operational world in the hero | Terminal / Palantir | Adapt | Use a "work loop control room" instead of logistics imagery. |
| Enterprise proof language | Palantir / CrewAI | Defer | Farplane does not yet have public customers or enterprise claims. |
| Durable execution and human oversight | LangGraph | Adapt | Reframe as visible ticket/program/progress plus Telegram feedback. |
| Multi-agent platform adoption metrics | CrewAI | Reject | Too easy to overclaim; this pilot should avoid unsupported scale numbers. |
| Demo CTA over abstract signup | Terminal / Palantir | Adopt | Use "Review the loop" and "See the artifact packet" CTAs. |

## Unique Take

Farplane should not sound like a broader agent platform. The sharper take is:

> The agent is not the product. The reviewable work loop is the product.

The page should make the visitor feel the difference between a chat transcript
and an inspectable loop. The hero visual is a live-feeling evidence packet:
ticket, program, progress, artifact, feedback, and next decision.

## Recipe Route

- `recipe_id:` `industrial-mission-control`
- `taste_profile_id:` `terminal-palantir`
- `effect_stack_id:` `cinematic-frame-sequence` for future premium build
- `current downgrade:` static HTML prototype with code-native visual carrier
  and screenshot proof. No generated media or premium/cinematic parity is
  claimed in this attempt.

## Story Arc

1. Problem: agent work disappears into chat and cannot be trusted later.
2. Shift: Farplane makes every serious agent job name its contract, method,
   proof, and human feedback path before it asks for trust.
3. Mechanism: ticket -> skill -> artifact -> proof -> feedback -> revision.
4. Proof: TASK-0236 itself is the example packet.
5. Action: keep, revise, or reject the offer direction.

## Low-fi ASCII Flow

```text
[Hero: The work loop is the product]
| headline + CTA + evidence-board visual
|
[Problem: agent output is cheap; trust is expensive]
| before/after cards
|
[Mechanism: Farplane loop]
| ticket -> skill -> artifact -> proof -> feedback -> revision
|
[Proof packet]
| TASK-0236 files, screenshot, feedback request, stop conditions
|
[Use cases]
| landing offer tests, evidence posts, skill improvements, QA loops
|
[CTA]
| review this artifact packet; decide keep / revise / reject
```

## Section Matrix

| Section | Job | Claim | Layout | Asset carrier | Motion lever | Proof payload | Fallback | QA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Hero | Orient skeptical builder immediately | The reviewable work loop is the product | Full-bleed command-surface hero | Code-native evidence board plus local screenshot | CSS entrance only | TASK-0236 packet labels | Static hero board | H1 and CTA visible on mobile; board not blank |
| Problem | Name the pain | Agent output is cheap; trust is expensive | Two-column before/after | HTML proof cards | None | Chat history versus ticketed evidence | Text cards | Cards fit mobile |
| Mechanism | Show how Farplane works | Contract, method, artifact, proof, feedback | Horizontal loop steps | HTML timeline | Subtle hover/focus | Ticket/program/progress path | Vertical stack | All steps visible at 390px |
| Proof packet | Make this artifact credible | This page came from an actual worker ticket | Dense evidence panel | File refs and status chips | None | TASK-0236 files and screenshots | Markdown refs | No unsupported public claims |
| Use cases | Make the product useful | Repeatable artifact loops are the wedge | Compact cards | Product-lane cards | None | Products.md workflow rows | Text cards | No fake metrics |
| CTA | Ask for smallest human judgment | Keep, revise, or reject direction | Strong final band | Feedback schema card | None | feedback-request.md | Local review request | One clear decision question |

## Visual Scenes / Assets

- Hero scene: an "evidence board" showing ticket, program, progress, artifact,
  screenshot, Telegram feedback, and next decision.
- Supporting scenes: before/after cards, loop timeline, proof packet list, and
  use-case cards.
- Asset manifest: `assets/asset-manifest.json`.
- Screenshot proof: `screenshots/mobile.png` and `screenshots/desktop.png`
  after browser capture.

## Product Demo Plan

Farplane is not a physical product, so the demo should show a working packet
rather than a rendered object:

- First demo: TASK-0236 files create a page artifact and feedback request.
- Future demo: short screen recording from a worker thread receiving Telegram
  feedback, appending progress, and revising the artifact.
- Do not use abstract AI art as the product demo.

## Asset Evidence Plan

- Current attempt uses code-native visuals only and is explicitly a prototype.
- A later premium version needs a real or generated hero image/video showing a
  Codex worker loop becoming an evidence packet, plus mobile and reduced-motion
  fallbacks.
- Text, labels, CTA, and feedback schema remain HTML overlays.

## Product Clarity And Accessibility Plan

- Use high-contrast HTML text, no text baked into pixels.
- Keep CTAs visible in the first viewport and final section.
- Ensure the hero claim and review question fit at mobile width.
- Avoid placeholder metrics such as "10x" or "0M+".
- Treat local screenshot proof as the phone-friendly review fallback.

## Motion Plan

- V1: CSS-only entry and hover/focus states.
- Future premium: a scroll-scrub sequence that transforms "chat noise" into
  a visible ticket packet, then into a feedback/revision loop.
- Reduced motion: V1 is already readable without animation.

## Designer Judgment Plan

Judge V1 on:

- Does the hero say what Farplane is in one breath?
- Does the evidence-board visual feel like a product artifact rather than a
  generic dashboard?
- Is the proof honest, specific, and not over-claiming?
- Can Kenji decide keep/revise/reject from a phone screenshot?

## QA Plan

- Render the static page locally.
- Capture desktop and mobile screenshots.
- Check H1, CTA, and evidence board are visible in the mobile first viewport.
- Check no console errors in the capture run.
- Record screenshots as the phone-friendly review surface.

## Implementation Handoff

Files in this attempt:

- `index.html`
- `assets/asset-manifest.json`
- `feedback-request.md`
- `feedback.json`
- `screenshots/mobile.png`
- `screenshots/desktop.png`

Next iteration after feedback:

- `keep:` refine copy and prepare a public/private preview path.
- `revise:` edit offer, proof ladder, or hero visual according to Kenji's note.
- `reject:` record rejected angle and generate a different offer variant.
