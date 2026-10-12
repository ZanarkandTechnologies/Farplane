---
name: social-content
description: "Use for \"write a thread\", \"draft a LinkedIn post\", \"make a carousel\" or \"write the newsletter\": approval-ready posts, threads, carousels and newsletter issues; posting stays with zernio."
source: local
department: marketing
capability:
  kind: artifact
  produces: [social-post-draft]
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
methods:
  - id: social-content:x
    class: artifact
    output: x-draft
  - id: social-content:linkedin
    class: artifact
    output: linkedin-post-draft
  - id: social-content:carousel
    class: artifact
    output: social-carousel-draft
  - id: social-content:cross-platform
    class: artifact
    output: cross-platform-content-bundle
  - id: social-content:newsletter
    class: artifact
    output: newsletter-issue
allowed-tools: Read, Glob, Grep, Bash
---

# Social Content

## Context

Use this when the operator wants a social post, X thread, LinkedIn post,
carousel, content calendar, cross-platform bundle, or a recurring newsletter
issue. One pass returns one approval-ready draft bundle in one mode. Drafts
only: nothing is posted, scheduled, sent, replied to, or cross-posted here.

It does not post, schedule, or read account metrics
([zernio](../zernio/SKILL.md)), generate images ([ai-image](../ai-image/SKILL.md))
or clips ([ai-video](../ai-video/SKILL.md)), write video scripts or
storyboards ([storyboard](../storyboard/SKILL.md)), or write page, article,
email-sequence, or ad copy ([copywriting](../copywriting/SKILL.md)).

## Skill Signature

```text
social_content(brief, mode?: x | linkedin | carousel | cross-platform | newsletter,
               audience?, source_pack?, voice_examples?, constraints?)
  -> draft_bundle { full copy + review notes + source receipt } | blocked_report
reads: the brief, supplied sources, swipes and voice examples, prior posts or issues, references by mode
does: binds one mode and reader promise, drafts the complete artifact, routes assets, runs the final pass
writes: the caller's artifact or GitHub issue comment, else .farplane/social-content/<date>-<slug>/; inline for chat review
returns: the draft with publication_status: approval_required, source gaps, and the next owner
```

## Modes

| Mode | Use for | Load |
| --- | --- | --- |
| `x` | X post, thread, quote-post, reply chain | [x-output](references/x-output.md), [upstream-twitter](references/upstream-twitter.md) |
| `linkedin` | Founder, B2B, hiring, thought-leadership post | [upstream-linkedin](references/upstream-linkedin.md) |
| `carousel` | Multi-slide post on Instagram, LinkedIn, X, Facebook | [upstream-carousel](references/upstream-carousel.md), [examples](references/examples.md) |
| `cross-platform` | Campaign bundle, content calendar, captions, hooks, thumbnails plan | [model](references/model.md), [upstream-social](references/upstream-social.md) |
| `newsletter` | Recurring newsletter issue or newsletter blueprint | [newsletter](references/newsletter.md) |

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Pick the mode and bind the brief.**
  `request + sources -> mode + audience + reader promise + evidence + voice mode | one blocking question`

  Rule: Infer the mode from the requested artifact: a tweet, thread,
  quote-post, or reply chain is `x`; a LinkedIn post is `linkedin`; slides are
  `carousel`; several platforms or a calendar is `cross-platform`; an email
  issue for subscribers is `newsletter`. A campaign that spans formats takes
  `cross-platform` as primary and the others as supporting modes. Bind
  audience, one concrete reader promise, verified evidence, voice, CTA, and
  stage. No voice examples means `voice_mode: hypothesis`. Draft on stated
  assumptions when the topic is enough; ask for one fact only when its absence
  would force fabrication. Use [method-selection-smoke](references/method-selection-smoke.md)
  when the mode is unclear.

  Example: "turn this essay into a thread and a carousel for launch week" ->
  `cross-platform` primary, `x` and `carousel` supporting.

  Assert:
  - One primary mode and a reader promise stated as value, not a topic label.
  - Every factual claim is sourced, cut, or marked as a hypothesis.
- [ ] **N2 — Ground the format and pick the direction.**
  `bound brief -> platform constraints + chosen spine or format | compared options`

  Rule: Load the mode's reference from the Modes table only for the specs,
  limits, or format rules the draft needs. Use `research` or supplied swipes
  when peer examples or current platform norms change the output; never claim
  current norms without a loaded source. For `x` pick one spine (lesson,
  teardown, story, checklist, case, announcement). For `newsletter` the
  available material chooses the format per [newsletter](references/newsletter.md):
  a weekly recap or changelog is a `release-digest` with no editorial arc.
  When platform, format, hook, or CTA is a real choice, compare complete
  directions and recommend one.

  Assert:
  - The chosen spine or format follows from the material, not taste alone.
  - A release digest is never forced into a founder story.
- [ ] **N3 — Draft the complete artifact.**
  `direction -> full copy in the mode's shape`

  Rule: Write the real copy, never a direction or outline. `x` returns the
  full tweet stack in [x-output](references/x-output.md): every tweet written
  out and numbered, a standalone hook, one idea per body tweet, payoff, one
  CTA, and character-budget notes; several directions each get their own full
  stack. `linkedin` returns the post as it would appear, hook above the fold.
  `carousel` returns slide-by-slide copy plus visual direction. `cross-platform`
  returns the artifact matrix from [model](references/model.md) plus each
  platform's copy. `newsletter` returns three subjects (45 chars or fewer), one
  preview (90 chars or fewer), the body, zero or one CTA, and send notes;
  default cadence is biweekly when a blueprint is needed. Load
  [examples](references/examples.md) or the operator's swipe before the first
  quality-sensitive variant.

  Example: "three thread options for Telegram review" -> three numbered stacks
  of six to eight tweets, each judgeable from the message alone.

  Assert:
  - A reviewer can decide from the actual copy without opening a local path.
  - No invented anecdote, metric, quote, or result.
- [ ] **N4 — Route production assets.**
  `draft -> asset plan + owner per asset | none`

  Rule: Name each asset the draft needs and its owner: stills, slides,
  product shots, and infographics to [ai-image](../ai-image/SKILL.md); clips,
  voice, and presenters to [ai-video](../ai-video/SKILL.md); video scripts and
  storyboards to [storyboard](../storyboard/SKILL.md); landing-page or article
  copy to [copywriting](../copywriting/SKILL.md). Paid generation runs through
  `treg` inside the operator's weekly spend cap, with the price quoted first
  and the spend logged. Include media only when it changes the reader's
  understanding.

  Assert:
  - Every asset has one owner; no generation is claimed without a saved file.
- [ ] **N5 — Run the final pass and return with the approval gate.**
  `draft + assets -> draft_bundle + publication_status: approval_required`

  Rule: Run the [final pass](../copywriting/references/final-pass.md) on all
  prose. Check feed readability, character limits, repeated claims, CTA
  count, and promotion placement (value first; a soft plug goes in a P.S.).
  Return the copy, source receipt, voice mode, gaps, and next-issue or
  next-post seeds. Posting, scheduling, and metrics go to
  [zernio](../zernio/SKILL.md) only after the operator explicitly approves the
  final copy.

  Assert:
  - `publication_status: approval_required` is visible; no post, schedule,
    send, or delivery receipt is claimed.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- A thread direction without the tweet stack is not a deliverable; neither is
  a newsletter "angle" without the issue.
- Personalization pressure ("make it sound personal, add a story") never
  licenses an invented founder anecdote, feeling, or quote; use a sourced
  observation or label a hypothesis.
- Do not smuggle a publishing request into a draft; even "final" copy waits
  for explicit approval and goes out through zernio.
- When asking for review on mobile or Telegram, put the copy inline; desktop
  paths are unreadable there.
- Never open a newsletter with "Welcome to another issue".
- The upstream references contain `belt` commands; they are reference
  material only. Generation routes through ai-image or ai-video.

## Reference Map

- Mode references are in the Modes table; load them in N2-N3.
- [model](references/model.md) - artifact matrix and execution packet for
  multi-format work; [method-selection-smoke](references/method-selection-smoke.md)
  when the mode is unclear or when changing this skill.
- [newsletter](references/newsletter.md) credits the MIT upstream
  ([license](references/newsletter-UPSTREAM_LICENSE.txt)); its worked release
  digest is [examples/newsletter](examples/newsletter/example.md).

## Output

```yaml
mode: x | linkedin | carousel | cross-platform | newsletter
brief: <audience, reader promise, stage, voice_mode: evidence_matched | hypothesis>
draft: <full copy: numbered tweet stack | post | slide copy | artifact matrix + copy | subjects + preview + body>
assets: <asset -> owner (ai-image | ai-video | storyboard | copywriting) | none>
review_notes: <claims and sources, character-budget risks, CTA count, promotion placement>
source_receipt: <verified facts, public links, interpretation, material cut>
gaps: <missing facts or assumptions>
publication_status: approval_required
next_owner: zernio (after explicit approval) | review | none
```

`blocked_report`: the one missing fact that prevents a truthful draft, one
labelled hypothesis, voice mode, and the unchanged approval gate.
