---
template_uses:
  skill-method-reference: "0.1.0"
---

# Source Mining And Swipe Workflow

Use this reference when copy quality depends on real source material: Tasty
Pack captures, swipe files, reviews, competitor pages, sales/support notes,
customer interviews, testimonials, transcripts, or public copy examples.

Do not copy third-party prose. Extract reusable evidence, message structure,
specificity, proof placement, emotional triggers, and reader language, then
write original copy for the current product.

```text
source_mining_and_swipe_workflow(brief, sources?, swipes?, tasty_pack?)
  -> source_mining_packet + message_map_inputs
state: reads(user brief, supplied sources/swipes/Tasty Pack captures, public
       pages only when allowed); writes(no files unless caller owns artifact)
gates: source_set_bound; copy_atoms_extracted; swipe_moves_not_prose_copied;
       message_map_inputs_trace_to_sources
fails: source-free confident copy; copied swipe prose; fake customer language;
       unsupported demographics; vibe-only Tasty Pack use
```

## Use When

- The copy needs to feel specific, emotional, or conversion-oriented.
- The user supplies swipes, Tasty Pack/Inspiration Pack captures, reviews,
  competitor pages, sales notes, support notes, testimonials, or transcripts.
- The agent is tempted to write from generic marketing principles instead of
  evidence.
- Public final copy, landing-page copy, or high-visibility campaign copy is
  requested.

## Inputs

```text
input_packet:
  required:
    - brief: audience, product, page job, offer, proof if known
  optional:
    - sources: owned notes, reviews, testimonials, sales/support excerpts
    - swipes: ads, pages, emails, headlines, examples, competitor pages
    - tasty_pack: captures[].analysis and captures[].elements
  source_refs:
    - URLs, local paths, capture IDs, user notes, or supplied excerpts
```

## Workflow

1. Bind the source set.
   - `owned`: product docs, founder notes, sales calls, support tickets,
     testimonials, analytics, interviews.
   - `borrowed signal`: public reviews, Reddit/forums, competitor pages,
     public ads, swipe files, Tasty Pack references.
   - `hypothesis`: no source exists; only conservative assumptions allowed.

2. Extract `CopyAtom` rows.

   ```text
   CopyAtom := {
     type: pain | desire | objection | trigger | transformation |
           proof | phrase | metaphor | tone | CTA | section_job
     source: path | URL | captureId | user_note | supplied_brief
     quote_or_paraphrase: short excerpt or faithful paraphrase
     audience_stage: unaware | problem_aware | solution_aware |
                     product_aware | most_aware | unknown
     use: hero | subhead | section | proof | FAQ | CTA | cut
   }
   ```

3. Review-mine for language, not demographics.
   - Look for repeated "tired of", "finally", "I wish", "I hate",
     "the only thing", "before", "after", and "because" patterns.
   - Cluster by pain, desired future, failed alternative, objection, and proof.
   - Prefer concrete phrases customers would actually say over polished claims.

4. Analyze swipes as moves.
   - Extract promise shape, first-line tension, specificity, contrast,
     mechanism reveal, proof placement, risk reversal, CTA posture, and rhythm.
   - Record `swipe_move`, not copied wording:

   ```text
   SwipeMove := {
     source:
     move:
     why_it_works:
     adapt_as:
     do_not_copy:
   }
   ```

5. Build the message map from evidence.
   - `one_reader`: the clearest source-backed reader.
   - `awareness_stage`: how much the reader already knows.
   - `dominant_pain`: the pain with the strongest source evidence.
   - `desired_future`: the outcome with the strongest emotional pull.
   - `mechanism`: how the product creates the change.
   - `proof`: evidence that makes the mechanism believable.
   - `objection`: the objection most likely to block action.
   - `page_story`: pain mirror, mechanism, proof, objection, or offer/action.

6. Draft by section job.
   - Hero: outcome or pain relief + specificity.
   - Subhead: mechanism + reason to believe.
   - Pain section: mirror the source language without dramatizing.
   - Mechanism section: explain the product move in plain words.
   - Proof section: use evidence, example, demo, testimonial, or concrete
     behavior.
   - Objection section: remove friction or name the tradeoff honestly.
   - CTA: ask for one action in the reader's language.

7. Cut every line that lacks a job.
   - Keep a line only if it carries source-backed pain, desire, proof,
     mechanism, objection handling, specificity, or action.
   - Replace generic adjectives with source atoms or product behavior.
   - If a claim is attractive but unsupported, move it to `source_gaps`.

## Output Shape

```text
source_mining_packet:
  source_mode: owned_sources | borrowed_signal | mixed | hypothesis
  copy_atoms:
    - CopyAtom
  swipe_moves:
    - SwipeMove
  reference_leverage_map:
    - source_element: copy_use
  message_map_inputs:
    one_reader:
    awareness_stage:
    dominant_pain:
    desired_future:
    mechanism:
    proof:
    objection:
    page_story:
  source_gaps:
  blockers:
```

## Quality Gates

- Every confident emotional claim traces to a CopyAtom, product truth, proof
  point, or supplied brief fact.
- Swipe files produce `SwipeMove` records, not copied phrasing.
- Tasty Pack elements map to concrete copy uses; pinned elements matter more
  than unpinned context.
- Hypothesis mode is explicit when no source material exists.
- The message map exposes source gaps before page copy is drafted.

## Bad Output

- Generic persona claims such as "busy professionals want simplicity" without
  source atoms.
- Swipe-file wording copied into the draft.
- Tasty Pack references reduced to "make it punchy" or other vibe notes.
- A word bank with polished adjectives but no reader language.
- A beautiful hero claim that the product proof cannot support.

## Tasty Pack Integration

When a Tasty Pack or Inspiration Pack is supplied, use:

- `captures[].analysis` for why the reference works.
- `captures[].elements` with `kind: copy | hook | format | constraint |
  storyboard | visual` for reusable copy and structure moves.
- `pinned: true` as the operator's taste signal.
- `analysis.operatorNote` to avoid using a reference as a vague moodboard.

Return a `reference_leverage_map`:

```text
capture element -> copy use
pinned hook -> hero tension
pinned copy -> tone or rhythm
format -> section order
constraint -> do-not-copy / rights-safe rewrite
```

## Source Grounding

This workflow adapts public guidance from Copyhackers voice-of-customer and
review-mining processes, CXL voice-of-customer guidance, VWO landing-page
copywriting, swipe-file guidance, and Farplane's own Resource Bank/Tasty Pack
contract.
