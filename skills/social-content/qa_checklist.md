---
title: Social Content QA / Review Checklist
owner: social-content
status: active
kind: qa-checklist
applies_to:
  - social-content
  - social-content:twitter-thread
  - social-content:carousel
  - social-content:linkedin
  - social-content:cross-platform
---

# Social Content QA / Review Checklist

Use this checklist before drafting and again before sending a review request or
claiming platform fit. For high-stakes campaign work, ask an independent
reviewer to inspect the finished artifact.

```text
social_content_check(content_packet, draft?, review_request?)
  -> pass | violation | deferral
```

## Preflight

- [ ] The artifact matrix is bound: platform, format, audience, message job,
  copy payload, asset carrier, publish boundary, and proof.
- [ ] One primary method owns the artifact. Supporting methods are listed only
  when the artifact truly spans formats.
- [ ] The output stage is explicit: premise, outline, draft, asset plan, final
  copy, or publish action.
- [ ] Current platform rules, peer examples, supplied swipe, or local campaign
  context are loaded when they materially affect the recommendation.
- [ ] External compute, uploads, API usage, posting, scheduling, comments, DMs,
  and cross-posting are blocked unless explicitly approved by the user.

## Twitter/X Thread Checks

- [ ] A thread plan includes a hook tweet, reader value promise,
  tweet-by-tweet stack, evidence/examples, payoff, CTA, and optional media.
- [ ] The hook works as a standalone post in the feed and makes a concrete
  promise rather than naming only a topic.
- [ ] Each body tweet has one job and advances the story, argument, teardown,
  checklist, or lesson.
- [ ] The plan provides value, news, proof, or a useful story. It is not just a
  product premise, positioning statement, or vague angle.
- [ ] The review request includes enough of the actual tweet stack for a human
  to judge the thread from the message itself.
- [ ] Character limits and media constraints are checked against the current
  platform rules when final copy or media is requested.

## Final Review

- [ ] The artifact is concrete enough for the requested decision. A request to
  choose among thread options shows actual tweet progression, not only labels.
- [ ] The CTA matches the artifact stage and does not imply posting permission.
- [ ] Saved files, prompts, inputs, outputs, and proof paths are listed when
  generation or external assets were involved.
- [ ] Any skipped research, source uncertainty, proof gap, or missing approval
  is reported as a deferral rather than hidden.

## Reviewer Prompt

```text
Review the social content artifact against skills/social-content/qa_checklist.md.
Return pass, violation, or deferral for failed checks. Focus on artifact
concreteness, platform fit, thread progression, user-review readability, and
publish-boundary safety. Do not publish or schedule anything.
```
