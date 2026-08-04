---
title: Landing Page Planning QA Checklist
owner: landing-page
status: active
kind: qa-checklist
created_at: 2026-06-26
applies_to:
  - landing-pages
  - premium-landing-pages
  - cinematic-scrolltelling
  - human-feedback-artifacts
---

# Landing Page Planning QA Checklist

Use this checklist before approving `LANDING_SPEC.md` and again before returning
it to the calling implementation planner. It prevents high-craft landing
requests from being specified as basic HTML merely because that path is faster.

```text
landing_page_plan_check(spec, quality_target, user_refs)
  -> approved_spec | violation | downgrade_blocker
```

## Preflight

- [ ] `quality_target` is explicit:
  `stunning | premium | standard | simple`.
- [ ] The ambition signal is recorded from the prompt, ticket, references, or
  supplied examples.
- [ ] If the operator supplied effects, examples, generated-media expectations,
  video-scroll, 3D/WebGL, cinematic, Terminal, Apple-style, or "stunning"
  language, the plan defaults to `stunning` or `premium`.
- [ ] Supplied visual/effect ingredients are inventoried and each is marked
  `adopt | adapt | reject | defer | blocker`.
- [ ] For `stunning` or `premium`, the primary visual carrier is one of:
  video/scroll scrub, 3D/WebGL object or world, generated/real media sequence,
  composed layered animation, or an equally authored carrier named in the spec.
- [ ] For `stunning` or `premium`, the spec compares at least three complete
  directions before choosing:
  `layout + asset carrier + motion lever + proof payload + fallback + QA`.
- [ ] A static HTML/CSS-only page is accepted only for `simple` or `standard`,
  or as a labeled blocker/prototype when richer assets cannot be produced.
- [ ] `asset-advisor-route` is explicit: missing media, external discovery,
  reference-led generation, and rights/recreation decisions have an Asset
  Advisor receipt before spec approval; a complete supplied asset set skips
  the route only with provenance, planned-use rights, and the skip reason. The
  landing brief contains an `Asset Advisor Route Decision` row for every page
  or materially different asset path; inference from prose is not enough.

## Downstream Proof Contract

- [ ] The spec requires the deployed or screenshot review surface to match the
  selected quality target.
- [ ] The spec requires any visually basic result under a `stunning` or
  `premium` target to be reported as a downgrade/blocker rather than presented
  as the intended page direction.
- [ ] Every main section has a planned visible carrier so lower sections cannot
  collapse into generic cards after a rich hero.
- [ ] Premium/cinematic/generated-media plans require asset evidence: manifest,
  source/provenance, poster or fallback, mobile path, and screenshots.
- [ ] Planned motion, 3D, video, or generated media reveals meaning tied to the
  offer rather than decoration around ordinary copy.
- [ ] The spec requires a deliberate mobile first viewport and phone-reviewable
  proof through a preview URL when available, with screenshots as fallback.
- [ ] The downstream feedback question asks for a small decision on the correct
  object: page direction, downgrade choice, or next revision hypothesis.
- [ ] The skill returns a named `LANDING_SPEC.md` artifact with
  `status: approved | blocked`; multiple pages receive separate spec artifacts,
  and a prose-only status summary fails the handoff. It does not implement,
  render, deploy, or invoke another implementation planner at the same scope.

## Violation Handling

- If the target is `stunning` or `premium` and the spec cannot support that
  ambition, return a blocker naming the missing asset, method, rights, proof,
  or implementation dependency, or ask for approval of an explicit downgrade.
- Do not approve a low-ambition spec while the request still requires richer
  creative machinery.

## Evidence Note

Record this in the ticket, artifact, or final response:

```text
landing_page_plan_check:
  quality_target:
  ambition_signal:
  supplied_effects_used:
  supplied_effects_rejected_or_deferred:
  primary_visual_carrier:
  downgrade_blocker:
  downstream_review_surface:
  handoff: approved_spec | blocked_spec
  verdict: pass | violation | downgrade_blocker
```
