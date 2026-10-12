---
name: copywriting
description: "Use for \"write the copy\", \"write an SEO article\", \"make this sound human\" or \"tighten this\": page or article copy from mined source phrases, or a final-pass rewrite that keeps every fact."
source: local
department: marketing
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash, web_search
---

# Copywriting

## Context

Use this when words are the deliverable: page copy for an audience and offer,
an SEO article brief or draft, or a cleaned rewrite of prose someone supplies.
One pass runs one mode and returns one packet. Research is the work: copy
comes from the reader's own words in source material, not from generic
marketing principles.

It does not own page structure, sections, assets, or motion
([landing-page](../landing-page/SKILL.md)), social posts or newsletters
([social-content](../social-content/SKILL.md)), ad creative
([ads](../ads/SKILL.md)), images ([ai-image](../ai-image/SKILL.md)), or
publishing. Generated copy is never approved public copy; a human gate stays
visible.

## Skill Signature

```text
copywriting(mode?: page | seo | final-pass, audience?, product?, goal?,
            offer?, proof?, sources?, swipes?, topic?, keywords?, text?, tone?)
  -> copy_packet | article_packet | revised_text, + qa_verdict | format_block | blocked_report
reads: the brief, supplied sources (customer words, calls, reviews, swipes, Tasty Pack), existing copy, live SERP for seo
does: mines source phrases, writes to the reader's awareness stage, runs the final pass last
writes: the caller's artifact, else inline; files only when asked to edit one
returns: the packet, a pass | revise | blocked verdict, source gaps, human gate, next owner
```

## Modes

- `page`: emotional story, page copy by section, CTA variants, word bank, copy
  QA. Detail in [page](references/page.md).
- `seo`: SERP check, brief or outline, article draft, SEO QA. Detail in
  [seo](references/seo.md).
- `final-pass`: rewrite supplied prose so it reads clear and human while
  keeping its meaning. The full procedure is
  [final-pass](references/final-pass.md); other writing skills link to it as
  their last step.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Pick the mode and bind the reader.**
  `request -> mode + reader + product + job | route out | one narrow question`

  Rule: Supplied text with "unslop", "humanize", "tighten", or "make this
  sound human" is `final-pass`; go to N6. A search query, keyword, or article
  is `seo`. Hero, page, CTA, or positioning words are `page`. Page layout or
  motion routes to `landing-page`, posts to `social-content`, ad creative to
  `ads`, images to `ai-image`. Bind one reader, product, offer, proof, tone,
  and the one action. Ask only when a missing input changes the claim.

  Assert:
  - One mode and one reader are named, or the missing input is the blocker.
- [ ] **N2 — Mine source phrases before writing.**
  `brief + sources -> copy atoms + swipe moves + source mode`

  Rule: Before any draft line, extract `CopyAtom` rows (pain, desire,
  objection, trigger, proof, phrase, CTA) from customer words, call notes,
  reviews, support tickets, competitor pages, swipes, or Tasty Pack captures.
  Swipes give moves (structure, rhythm, proof placement), never prose. With
  no source material, label `source_mode: hypothesis` and keep claims and
  voice conservative. Load
  [source mining](references/source-mining-and-swipe-workflow.md) whenever
  sources or swipes are supplied.

  Example: review says "I forget who I promised what" -> hero tension "Stop
  losing the promise you made on the call", not "streamline your pipeline".

  Assert:
  - Every confident emotional claim traces to an atom, product truth, or proof.
  - No swipe wording is copied; no customer language is invented.
- [ ] **N3 — page: choose the persuasion path by awareness, then draft short.**
  `atoms -> message map + persuasion path + page copy (< 100 lines)`

  Rule: Name the reader's awareness stage first (problem, solution, product,
  most aware) and pick the story shape and persuasion path from it (AIDA cold,
  PAS pain-aware, 4Cs trust-sensitive, FAB feature-heavy, ACC education, SLAP
  short offer); say why. Name the lead posture and weakest conversion factor.
  Rewrites start with a copy-gap audit. Page copy stays under 100 non-empty
  lines unless long-form is asked for. Load [page](references/page.md).

  Assert:
  - Persuasion path and awareness stage are named and justified.
  - Page copy line count is reported and under 100.
- [ ] **N4 — seo: check the SERP, then prove information gain.**
  `topic + live SERP -> intent fingerprint + information gain + article packet | format_block`

  Rule: Search the live query before outlining and record content type,
  format, dominant angle, SERP features, and freshness. Name the information
  gain over the current results (experience, data, example, comparison,
  decision rule); none means `revise`, not a paraphrase of the top pages.
  When a tool, calculator, comparison table, or template serves the query
  better than an article, return `format_block`, say so plainly, and name the
  better format. Load [seo](references/seo.md).

  Example: every top result for "loan repayment calculator" is a calculator
  -> block the article; recommend the calculator.

  Assert:
  - No outline exists without a recorded (or `unverified`) SERP fingerprint.
  - No rankings, traffic, or conversions are promised.
- [ ] **N5 — Cut every line without a job.**
  `draft -> cut draft + cut list + source gaps`

  Rule: Keep a line only if it carries a source-backed pain, desire,
  mechanism, proof, objection, or action. Replace generic adjectives with
  atoms or product behaviour. An attractive claim the proof cannot support
  moves to `source_gaps`. Emotional words name a concrete situation.

  Assert:
  - The cut list names the generic phrasing removed.
- [ ] **N6 — Run the final pass last.**
  `finished prose -> revised prose with every fact, number, and quantifier intact`

  Rule: In every mode the final pass is the last edit, after content is
  settled. Follow [final-pass](references/final-pass.md): never add or drop a
  quantifier ("42 tests passed" stays; "all 42" keeps "all"); delete a vague
  sentence rather than paraphrase it; judge each line, never a banned-word
  list; keep facts, certainty, tone, Markdown, code, links, and precise
  technical terms. Already-clear text gets little or no change.

  Example: "We facilitated a robust transition across the evolving data
  landscape. The backfill processed 18,420 rows." -> "The backfill processed
  18,420 rows."

  Assert:
  - Every number, identifier, and quantifier in the source survives unchanged.
  - Nothing is added: no opinion, judgment, example, or next step.
- [ ] **N7 — Return the packet with a verdict and human gate.**
  `packet -> qa_verdict + gaps + human gate + next owner`

  Rule: `page` and `seo` return the packet, a `pass | revise | blocked`
  verdict, source mode, riskiest claim, proof and freshness gaps, the human
  approval gate before publishing, and the next owner. `final-pass` returns
  only the revised text in its source format, no change log. Plans or
  receipts go on the active GitHub issue or the caller's artifact, else
  `.farplane/copywriting/<date>-<slug>/`.

  Assert:
  - Nothing is published or marked approved public copy.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- A copy request wants words for the page, not an essay on strategy.
- A swipe file is not a synonym finder; extract the move, write original words.
- Do not fake voice-of-customer detail; hypothesis copy says so.
- The final pass changes wording, never claims: "18 of 20 passed" never
  becomes "nearly all passed", and a hedge stays a hedge.
- Replacing one AI tell with forced slang, fake vulnerability, or fragments is
  still a tell.
- Do not rewrite code, commands, URLs, citations, or quoted source text in a
  final pass unless asked.
- Expert, medical, legal, or financial claims in an article need human review
  and dated sources before publication.

## Reference Map

- [source mining](references/source-mining-and-swipe-workflow.md) - N2:
  CopyAtom and SwipeMove rows, review mining, Tasty Pack mapping.
- [page](references/page.md) - N3: message map, persuasion paths, lead
  posture, copy-gap audit, copy packet template.
- [seo](references/seo.md) - N4: SERP fingerprint, information gain, format
  block, article packet template, SEO QA.
- [final-pass](references/final-pass.md) - N6: the standalone final-pass
  procedure other skills link to.
- [landing page example](examples/landing-page/example.md) and
  [article brief example](examples/article-brief/example.md) - calibrate
  packet length and tone.
- [ingest-content](../ingest-content/SKILL.md) - save swipes or references as
  reusable Resource Bank material.
- [review](../review/SKILL.md) - before high-visibility public copy.

## Output

```yaml
mode: page | seo | final-pass
source_mode: owned_sources | borrowed_signal | mixed | hypothesis
packet: <copy packet | article packet | revised text in source format>
verdict: pass | revise | blocked | format_block
line_count: <page copy non-empty lines>
gaps: <source, proof, freshness gaps>
human_gate: <who approves before publishing>
next_owner: landing-page | social-content | ads | review | none
```
