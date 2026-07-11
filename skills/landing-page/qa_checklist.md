---
title: Landing Page Runtime QA Checklist
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

# Landing Page Runtime QA Checklist

Use this checklist before implementation and again before asking for review.
It prevents high-craft landing requests from collapsing into basic deployed
HTML merely because a simple page is faster.

```text
landing_page_runtime_check(spec, artifact, quality_target, user_refs)
  -> pass | violation | downgrade_blocker
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

## Final Review

- [ ] The deployed or screenshot review surface matches the quality target.
- [ ] If the artifact is visually basic while the target is `stunning` or
  `premium`, the review request names this as a downgrade/blocker instead of
  asking the operator to judge it as the page direction.
- [ ] Every main section has a visible carrier; lower sections are not generic
  cards after a rich hero.
- [ ] Asset evidence exists for premium/cinematic/generated-media claims:
  manifest, source/provenance, poster or fallback, mobile path, and screenshots.
- [ ] Motion, 3D, video, or generated media reveals meaning tied to the offer;
  it is not decoration pasted around ordinary copy.
- [ ] Mobile first viewport is deliberate and phone-reviewable through a public
  or mobile-viewable preview URL when available, with screenshots as fallback.
- [ ] The feedback question asks for a small decision on the correct object:
  page direction, downgrade choice, or next revision hypothesis.

## Violation Handling

- If the target is `stunning` or `premium` and the artifact is basic, do one of:
  - produce the richer artifact before asking for page-direction feedback;
  - send a blocker/status update naming the missing asset/method/deploy step;
  - ask for feedback only on whether to accept the downgrade.
- Do not mark the iteration complete merely because a URL exists.
- Do not ask for keep/revise/reject on a low-ambition artifact when the real
  question is why the worker ignored the requested creative machinery.

## Evidence Note

Record this in the ticket, artifact, or final response:

```text
landing_page_runtime_check:
  quality_target:
  ambition_signal:
  supplied_effects_used:
  supplied_effects_rejected_or_deferred:
  primary_visual_carrier:
  downgrade_blocker:
  review_surface:
  verdict: pass | violation | downgrade_blocker
```
