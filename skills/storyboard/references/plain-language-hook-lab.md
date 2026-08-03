---
title: Plain-Language Hook Lab
owner: storyboard
status: active
kind: reference
created_at: 2026-07-29
updated_at: 2026-07-29
---

# Plain-Language Hook Lab

Load this before scripting short-form, latest-news, title-led, or
retention-sensitive content. The hook is not the first accurate sentence. It is
the smallest evidence-safe sentence that an unfamiliar viewer understands,
feels, and can picture immediately.

```text
hook_lab(idea, proof, audience, source_title?)
  -> candidates[10+]
   + finalists[3+]
   + winner
   + first_3_seconds
   + rejected_reasons
```

## Candidate Pass

Write at least ten materially different hooks. Vary the causal frame, not only
the wording:

1. recognizable actor causes a consequence;
2. recognizable actor stops or reverses a consequence;
3. simple contradiction;
4. visible before -> after change;
5. unexpected helper, winner, loser, buyer, or payer;
6. concrete threat or deadline;
7. familiar comparison;
8. surprising scale translated into an ordinary object or outcome;
9. rule change and who it affects;
10. unanswered `how can that be true?` claim.

Keep uncertainty words such as `may`, `could`, or `reportedly` when the evidence
requires them. Do not compensate for uncertainty with legal or financial jargon.

## Child-Simple Gate

Apply the draw test:

> Could an unfamiliar viewer draw the actor, action, and consequence after
> hearing the line once?

A strong general-audience hook normally has:

- one recognizable actor;
- one concrete verb;
- one familiar consequence or object;
- normally at most eight words for the display hook, with necessary detail
  moved into the following voiceover;
- one breath of spoken language;
- no definition required before the stakes become interesting.

Reject hooks led by abstract verbs or bridge phrases such as `back`, `backing`,
`secure`, `facilitate`, `support`, `finance`, `fund`, `get the money`, or
`help fund` when a concrete everyday verb can carry the same evidence safely.
Reject unexplained nouns such as `guarantee`, `backstop`, `capex`,
`interconnection`, `off-balance-sheet vehicle`, or `lease facility`. These
terms may appear later in the explanation.

`Help` may remain only as a qualifier on a concrete visible verb: `help buy`,
`help build`, or `help pay`. With two named actors, avoid pronouns whose owner
could be either actor. Repeat the company or product name:

```text
ambiguous: Company A may help Company B buy its own product
clear:     Company A may help Company B buy Company A products
```

Translate the mechanism into the ordinary action it makes possible, without
changing the evidence:

| Mechanism language | Possible ordinary action, when supported |
| --- | --- |
| guarantee / backstop | help pay; promise to cover the bill |
| financing / funding | help buy; help build |
| capital expenditure | spending on chips, buildings, or power |
| interconnection approval | permission to plug into the grid |

The display hook may name the simple paradox while the qualifier and next
voiceover sentence carry the technical mechanism. For example, replace
“Chipmaker may back customer infrastructure financing” with “The chipmaker may
help buy its own chips,” only when the source actually supports that
relationship.

Do not invent a supposedly simple replacement noun—such as `AI factory`,
`computer hub`, or `money machine`—when it creates a second metaphor the viewer
must decode. Prefer the familiar source object when it is already ordinary
enough, or leave the object for sentence two. If the evidence puts one company
on both sides of a transaction, surface the loop:

```text
supplier may help customer obtain supplier_product
```

This is often clearer than leading with the financing mechanism.

Before finalist selection, reject any candidate that is only a synonym swap,
weakens the reported relationship, or fails to change at least one of actor,
action, consequence, or question opened. A rejected candidate may remain in
the candidate table only with its rejection reason and cannot advance. Lens
labels do not make duplicates materially different.

Child-simple does not mean false, childish, or stripped of necessary
uncertainty. Never turn talks into a signed deal, assistance into a purchase, a
forecast into an outcome, or correlation into causation.

## Source-Title Contest

Put the source title beside at least three finalists:

| Line | Immediate meaning | Curiosity | Accuracy | One breath | Drawable first frame | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Source title |  |  |  |  |  | keep / beat |
| Finalist A |  |  |  |  |  |  |
| Finalist B |  |  |  |  |  |  |
| Finalist C |  |  |  |  |  |  |

The winner must beat the source title on the combined test. A shorter paraphrase
does not win automatically. If no candidate wins, keep the source title or
generate another candidate pass; do not lock a weaker hook merely to be
original.

Hard blockers:

- the viewer must decode jargon before understanding the conflict;
- the main verb is abstract or visually inert;
- the sentence needs two explanations before the consequence is clear;
- the line has no recognizable actor or consequence;
- the first frame cannot show the claim;
- the drama erases an evidence qualifier;
- the line merely shortens the source title.

## First Three Seconds

```text
first_3_seconds:
  on_screen_copy: exact winning hook
  voiceover: same promise or a simpler spoken form
  dominant_visual_action: actor + action + consequence
  evidence_qualifier: compact source-status language
  question_opened:
```

The visual must make the sentence easier to understand, not decorate it. Keep
the qualifier readable without making it the dominant headline.
