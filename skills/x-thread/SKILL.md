---
name: x-thread
description: "Turn a content brief and supporting evidence into a review-ready X thread draft with a concrete tweet sequence and explicit publishing boundary."
tier: 3
group: marketing
source: local
capability:
  kind: artifact
  consumes: ["content-brief"]
  produces: ["x-thread-draft"]
template_uses:
  skill-template: "0.4.4"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Write
---

# X Thread

## Context

Use this skill when the requested artifact is an X post, thread, quote-post,
or reply-chain draft. It owns the reader promise and reviewable tweet sequence.
It does not own account credentials, posting, scheduling, or performance
claims; route an explicitly approved final draft to [X Account](../x-account/SKILL.md).

## Skill Signature

```text
x_thread(content_brief, audience?, source_pack?, voice?, constraints?)
  -> x_thread_draft + review_notes | blocked_report

reads: content brief, supplied sources/swipes, output.md, the first-load Todo List guardrails
writes: draft only at a caller-owned artifact path
does: turns one audience promise into a concrete X-native tweet sequence
returns: a review-ready draft with provenance, media notes, and an approval gate
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

1. Bind the audience, promise, evidence, voice, CTA, and exact draft stage.
   Read the first-load Todo List guardrails; if a factual claim lacks support, either cut it or
   mark it as a hypothesis before drafting.
2. Choose one thread spine: lesson, teardown, story, checklist, case, or
   announcement. State the reader value in one concrete sentence before the
   hook; do not substitute a topic label for a promise.
3. Draft the complete sequence with [output.md](output.md): standalone hook,
   numbered body tweets that each advance one idea, proof/examples where
   needed, payoff, and one CTA. Include media only when it changes the reader's
   understanding.
4. Check the draft for feed readability, character-budget risk, repeated
   claims, unsupported specifics, and whether a reviewer can decide from the
   actual copy rather than a summary.
5. Return the draft, source gaps, selected assumptions, and
   `publication_status: approval_required`. Do not post, schedule, or claim a
   delivery receipt.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Use [output.md](output.md) as the canonical artifact template. Keep the
artifact family stable (`x-thread-draft`) while treating locale, campaign,
account, and creative angle as invocation inputs rather than new skills.

## Gotchas

- Do not offer a thread direction without the actual tweet stack.
- Do not smuggle a publishing request into the draft; a final copy still needs
  explicit approval and the X Account integration boundary.
- Do not invent a personal anecdote, metric, customer quote, or result to make
  the hook stronger.

## Output

- `x_thread_draft`: one reviewable X-native copy artifact shaped by
  [output.md](output.md), with source/proof notes and an unchanged approval
  gate.
- `blocked_report`: the missing fact that prevents a truthful draft, one safe
  hypothesis, and the requested next input.
