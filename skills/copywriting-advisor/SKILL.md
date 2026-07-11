---
name: copywriting-advisor
description: "Turn an audience, product, and page goal into a concise emotional story, page copy, word bank, and copy QA verdict."
tier: 3
group: marketing
source: local
template_uses:
  skill-template: "0.3.7"
  skill-surface-budget: "0.1.0"
allowed-tools: Read, Glob, Grep, web_search
eval: evals/evals.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["landing-page", "social-content", "storyboard"]
---

# Copywriting Advisor

## Context

Use this skill when a demographic group, customer segment, ICP, or audience and
a product or offer need source-backed page copy, positioning language, section
messaging, CTA variants, or a copy-quality check. It owns the message, story,
words, source-mining packet, and QA verdict. It does not own page visual design,
frontend implementation, social distribution, article SEO, publishing, or final
brand approval.

Grounding from current conversion-copy guidance: research is the work. Start by
mining voice-of-customer, Tasty Pack/reference captures, sales/support notes,
reviews, competitor pages, or supplied swipes for exact pains, desires,
objections, proof, and wording patterns. Use swipe files for structure and
message moves, not copied prose. If no source material exists, mark the output
as hypothesis copy.

## Skill Signature

```text
copywriting_advisor(demographic_group, product, page_goal?,
                    offer?, proof?, existing_copy?, tone?,
                    source_pack?, swipe_file?, tasty_pack?)
  -> copy_packet + copy_qa_verdict | blocked_report
state:
  reads(user brief, supplied voice-of-customer notes, proof, source/swipe/Tasty
        Pack material, existing page copy, qa_checklist.md,
        references/source-mining-and-swipe-workflow.md when source mining matters,
        current web sources when external guidance matters)
  writes(copy packet only when caller owns an artifact path)
gates:
  one_reader_bound; source_atoms_or_hypothesis_mode; product_truth_named;
  awareness_stage_named; persuasion_path_selected; lead_posture_named;
  message_layer_checked; story_spine_present; line_budget_checked;
  proof_matches_claims; final_public_copy_gate_named
routes:
  ingest-content | landing-page | social-content | storyboard |
  seo-content-advisor | review
fails:
  generic_ai_copy; source_free_confident_copy; swipe_copying; bloated_page_copy;
  unsupported_emotional_claims; vague_word_bank; public_copy_without_human_review
```

## Phase Boundary

Draft and QA copy inline. Use `landing-page` when page structure, sections,
assets, motion, or frontend implementation are the main work. Use
`social-content` for platform posts, threads, captions, or social campaigns.
Use `storyboard` when the copy must become video/script beats. Use
`seo-content-advisor` when search intent and article structure are the main
work. Use `review` before high-visibility final public copy.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the reader, product, and page job.
  - [ ] Resolve demographic group, emotional context, product, offer, page
        goal, proof, tone, CTA, output stage, source_pack, swipe_file, and
        Tasty Pack/reference availability.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Mine source material before writing.
  - [ ] Load
        [source-mining-and-swipe-workflow](references/source-mining-and-swipe-workflow.md)
        when swipes, Tasty Pack, reviews, competitor pages, sales notes,
        support notes, or quality-sensitive public copy are involved.
  - [ ] Extract `CopyAtom` rows for pain, desire, objection, trigger,
        transformation, proof, phrase, metaphor, tone, CTA, and section job.
  - [ ] If no source material exists, label `source_mode: hypothesis` and keep
        demographic psychology, claims, and voice conservative.
- [ ] 3. Build the source-backed message map.
  - [ ] Name the one reader, awareness stage, emotional job, product truth,
        dominant desire, market sophistication, promised transformation,
        mechanism, reason to believe, main objection, one action, and the
        source atoms that justify each choice.
  - [ ] If rewriting existing copy, run a copy-gap audit before drafting:
        compare current copy against source atoms for missing needs, benefits,
        anxieties, proof, differentiation, and reader language.
  - [ ] Choose the page story shape from the evidence: problem-aware pain
        mirror, solution-aware mechanism, product-aware proof, or most-aware
        offer/action.
  - [ ] Select one persuasion path and explain why it fits the reader stage:
        AIDA for cold attention, PAS for pain-aware urgency, 4Cs for
        trust-sensitive clarity, FAB for feature-heavy products, ACC for
        education-to-conversion, or SLAP for short urgency/offer moments.
  - [ ] Select the opening posture separately: direct offer, promise,
        problem/solution, secret, proclamation, or story, based on what the
        reader already knows and how skeptical the market is.
- [ ] 4. Draft the copy packet.
  - [ ] Produce the story spine, message map, page copy by section, CTA
        variants, word bank, source atom table, persuasion path, and swipe
        moves used.
  - [ ] Keep the default page-copy budget under 100 non-empty lines unless the
        caller explicitly asks for long-form copy.
  - [ ] Prefer short concrete sentences over complete explanation; each section
        should carry desire, clarity, proof, objection handling, or action.
- [ ] 5. Cut and sharpen against the source.
  - [ ] Remove generic AI phrasing, duplicated claims, unsupported emotion,
        throat-clearing, cleverness that hides the offer, and words the reader
        would not naturally use.
  - [ ] For each section, keep only lines backed by a source atom, product
        truth, proof point, objection, or CTA job.
  - [ ] Keep emotional language tied to a specific situation, pain, desire,
        proof point, or product behavior.
- [ ] 6. Finish with QA and handoff.
  - [ ] Apply `qa_checklist.md` to the finished packet.
  - [ ] Name source mode, source coverage gaps, line count, strongest message,
        riskiest claim, final public-copy human gate, and next owner.
  - [ ] If the operator wants reusable swipe/Tasty Pack ingestion rather than
        one-off copy, route source saving through `ingest-content`.
  - [ ] Route page execution to `landing-page`, article expansion to
        `seo-content-advisor`, social distribution to `social-content`, or
        material approval to `review`.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Copy packet:

```text
Audience:
Product:
Page job:
Source mode:
Source atoms:
  - type:
    source:
    quote_or_paraphrase:
    use:
One reader:
Awareness stage:
Emotional job:
Product truth:
Mechanism:
Promise:
Reason to believe:
Main objection:
Dominant desire:
Market sophistication:
Persuasion path:
Formula fit:
Lead posture:
Message layer verdict:
Conversion diagnostic:
Swipe moves used:
Story spine:
  tension:
  turn:
  proof:
  action:
Page copy:
  hero:
  subhead:
  sections:
  CTA variants:
Word bank:
Cut list:
Source gaps:
QA verdict:
Next owner:
```

Short positive example:
[examples/landing-page/example.md](examples/landing-page/example.md) shows a
compact page-copy packet with a message spine, word bank, and QA verdict.

## Gotchas

- Do not answer a copy request with a long essay about strategy when the user
  asked for words that can go on a page.
- Do not fake voice-of-customer detail. If no evidence exists, label the
  audience lens as a hypothesis.
- Do not use a swipe file as a synonym finder. Extract structure, specificity,
  proof placement, rhythm, and CTA posture; write original words from the
  product and audience evidence.
- Do not make emotional copy vague. Name the concrete before/after feeling or
  situation.
- Do not treat generated copy as approved final public copy; keep the human
  review gate visible.

## Reference Map

- [qa_checklist.md](qa_checklist.md) - read before drafting and apply before
  completion.
- [source-mining-and-swipe-workflow](references/source-mining-and-swipe-workflow.md)
  - read when source material, Tasty Pack, swipes, reviews, competitor pages,
  sales notes, support notes, or quality-sensitive public copy are involved.
- [ingest-content](../ingest-content/SKILL.md) - use when the
  operator wants to save links, screenshots, ads, landing pages, notes, or
  swipes as reusable Resource Bank/Tasty Pack material.
- [landing-page](../landing-page/SKILL.md) - use when the page
  needs section architecture, assets, motion, or frontend handoff.
- [social-content](../social-content/SKILL.md) - use for social
  posts, captions, hooks, carousels, or platform distribution.
- [storyboard](../storyboard/SKILL.md) - use when the copy becomes
  video/script beats and scenes.
- [seo-content-advisor](../seo-content-advisor/SKILL.md) - use when
  the same message needs to become a search-intent article or SEO brief.

## Output

- `copy_packet`: source mode, source atom table, audience lens, awareness
  stage, product truth, story spine, page copy, CTA variants, word bank, cut
  list, source gaps, and next owner.
- `copy_qa_verdict`: pass, revise, or blocked with line count, message clarity,
  emotion/proof fit, unsupported claims, and final human gate.
- `blocked_report`: missing audience, product, offer, proof, page job, approval
  boundary, or source access needed for truthful claims.
