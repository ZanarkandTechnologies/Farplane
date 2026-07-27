---
title: Storytelling, Asset Evidence, and Persona Review
status: active
owner: content-impl-plan
kind: reference
created_at: 2026-07-27
updated_at: 2026-07-27
---

# Storytelling, Asset Evidence, and Persona Review

Load this reference whenever the deliverable is narrative, persuasive,
editorial, documentary, explainer, launch, or otherwise depends on changing an
audience's understanding or action.

## Contract

```text
compile_story(idea, ICP, evidence, promise)
  -> ICPContract
   + causal_spine
   + TwoColumnBeat[]
   + AssetDecision[]
   + PersonaContentReview
   + creative_lock_verdict
```

This is a production decision system, not a list of storytelling tips. Story,
assets, and audience review are one connected contract: each beat changes a
viewer state, each selected asset performs a named job at an honest evidence
level, and decision-relevant persona lenses decide whether the result can
advance.

## 1. Resolve the ICP

Do not leave `icp` as a label such as “founders” or invent demographics. Resolve
the decision context:

```text
ICPContract {
  role_or_job
  context
  starting_belief
  friction
  knowledge_level
  emotional_stake
  objection
  must_believe_after
  desired_action
}
```

If the brief is incomplete, infer only low-risk fields from the idea and mark
them `assumption`; compile the strongest useful plan and block only the fields
that genuinely prevent production or claim support.

## 2. Build a causal story

Write one point of view plus stakes. Choose the simplest honest backbone:
chronology, mechanism, investigation, contrast, transformation, or question and
answer. Then use only the turns needed by the duration.

Required short-form spine:

```text
promise/question
  -> opening action or contradiction
  -> tension/escalation
  -> mechanism or discovery
  -> proof
  -> turn
  -> payoff/action
```

Every beat records:

```text
TwoColumnBeat {
  id
  narration_or_semantic_copy
  visual_direction
  story_function: evidence | explanation | soul
  viewer_question
  viewer_state_before
  viewer_state_after
  causal_link_to_next
  asset_ids[]
}
```

A beat earns its place when it changes knowledge, belief, feeling, stakes, or
decision. Merge or remove beats that repeat the same state. `soul` beats may
humanize, create contrast, or let meaning land, but cannot substitute for proof.

### Plan scene ideas before asset search

```text
plan_scene_concepts(beat, claim, adjacent_beats)
  -> three SceneConcept records
   -> selected_concept + rejected_rationales + asset_brief
```

Every beat receives three materially different candidates before files or
search queries are chosen:

1. `literal_evidence`: the source, person, place, object, chart, or observed
   artifact that most directly supports the clause;
2. `causal_physical`: a concrete mechanism that visibly performs the change;
3. `context_scale`: a comparison, environment, or scale relationship that
   changes how the viewer understands the clause.

Each `SceneConcept` records `concept_id`, `beat_id`, `relationship_type`,
`viewer_state_change`, `visual_thesis`, `main_topic_role`,
`foreground_world`, `meaningful_reveals`, and `selection_status`.
Different crops, palettes, styles, or search phrases for one composition remain
one concept. Select for causal clarity, evidence honesty, thumbnail recognition,
and contrast with adjacent scenes; record why the other two lost.

### Bind causal cadence and reveals

Measure the narration before final scene boundaries. Target 4-5 seconds per
causal unit, with 3.5-6 seconds as a calibrated exception band. Each scene owns
one viewer-state change and normally two or three meaningful reveals. A reveal
introduces, transforms, connects, removes, or recontextualizes a story-bearing
element. Transitions, decorative motion, text flicker, and arbitrary timestamp
splits do not count. When timing falls outside the band, revise the beat or
record why the state change needs the exception; do not solve it by cutting a
static composition into nominal scenes.

### Contrast and turns

- Alternate current reality and credible possible reality when persuasion needs
  tension; do not repeat aspiration without new evidence.
- Start with action, contradiction, a concrete observation, or a question whose
  answer the video will earn.
- Keep the opening promise visible in the first movement and pay it off.
- Use active, concrete language: who did what to whom.
- For claims, show the discovery or mechanism rather than only announce the
  conclusion.

## 3. Write narration and visuals together

Use a two-column script from the first draft. Every sentence or compact clause
receives a visual direction; no narration paragraph is handed downstream with
“find B-roll.”

Separate three beat functions:

- `evidence`: supports a factual or product claim.
- `explanation`: makes a mechanism, relationship, sequence, or contrast legible.
- `soul`: creates human meaning, emotion, atmosphere, or a deliberate breath.

The full story needs the applicable functions, not an even quota. A factual
explainer cannot use soul or motion polish to cover missing evidence.

## 4. Choose assets by job and evidence

```text
choose_asset(beat, claim, viewer_state)
  -> job + evidence_level + material_identity + motion_purpose
   + provenance + rights + acceptance
```

Allowed asset jobs:

- `prove`: support a claim.
- `orient`: establish who, where, when, scale, or source.
- `explain`: reveal a mechanism or relationship.
- `humanize`: create specific emotional or lived meaning.
- `atmosphere`: establish context or a deliberate pause.
- `bridge`: preserve continuity or move between story units.

Evidence ladder, strongest first:

1. `direct_evidence`: authentic source, observation, screenshot, quote, document,
   dataset, or footage.
2. `annotated_evidence`: direct evidence with crop, highlight, label, or guided
   camera movement.
3. `reconstruction`: clearly labeled recreation of a supported mechanism or
   event.
4. `metaphor`: conveys meaning or emotion but does not prove facts.
5. `decoration`: texture or polish only.

`metaphor` and `decoration` cannot prove claims. Prefer the highest honest
evidence level available. Preserve material identity: screens should read as
screens, paper as paper, archive as archive, and charts as sourced or clearly
labeled illustrative charts.

Every selected asset records:

```text
AssetDecision {
  asset_id
  beat_id
  job
  claim_supported_or_none
  evidence_level
  material_identity
  motion_purpose: direct_eye | reveal_cause | compare | preserve_continuity |
    establish_context | deliberate_hold
  provenance
  rights_status
  acceptance_check
  decision: select | quarantine | reject
}
```

Reject or quarantine wallpaper: an asset whose only rationale is “adds polish,”
“keeps it dynamic,” “visual variety,” or “use B-roll.” Atmosphere is valid only
when the beat names the context or emotional state it establishes. Do not allow
more than two consecutive beats whose dominant asset is abstract,
metaphorical, or decorative unless the format explicitly requires it and the
persona review accepts the loss of proof.

## 5. Prototype story before design

Work in passes:

1. `thumbnails`: story structure, pacing, composition, viewer turns.
2. `boards`: readable scene logic, material identity, evidence placement.
3. `timed_animatic`: measured timing master, silent test, mute test.
4. `style_frames`: one anchor for opening, mechanism/proof, turn, and payoff.
5. `asset_lock`: only after evidence, rights, timing, and persona gates pass.

For the opening, main mechanism, and payoff, create three cheap thumbnail
alternatives. Record the selected option and why the others lost. Do not spend
design or provider budget to discover a structural problem that thumbnails
could expose.

Silent test: the visual sequence alone communicates the causal change.
Mute test: visuals change with or slightly before the relevant spoken clause,
direct the eye, and hold long enough to inspect.

### Separate mechanical proof from story judgment

Mechanical receipts may verify duration, reveal counts, asset-family
uniqueness, visible foreground geometry, and final-resolution treatment. They
cannot prove that a scene is interesting, comprehensible, honest, or causally
effective.

Before creative lock, an independent reviewer cites scenes while judging:

1. `specificity`: the visual is specific to the spoken clause;
2. `causal_clarity`: the before/after change and handoff are legible;
3. `hierarchy_depth`: one dominant subject and a genuine foreground read;
4. `neighbor_novelty`: the relationship changes rather than merely restyling;
5. `silent_comprehension`: the sequence is understandable without narration;
6. `evidence_integrity`: the image does not overclaim or disguise metaphor as
   proof.

Compare viable boards pairwise instead of hiding preference in one unexplained
“interestingness” score. False evidence, missing state change, failed silent
comprehension, absent foreground mass, adjacent family reuse, and dirty global
treatment are blockers and cannot be averaged away.

## 6. Derive the persona content review

Build two to four lenses from ICP roles, jobs, contexts, objections, and
decision authority. Typical lenses include champion/buyer, daily user/operator,
skeptic/risk owner, and affected executive. Do not add a persona unless it
changes a content decision.

```text
PersonaLens {
  name
  source_icp_field
  decision_job
  context
  objection
  must_see
  likely_rejection
}

PersonaVerdict {
  persona
  comprehension: 1..5
  relevance: 1..5
  trust: 1..5
  action_clarity: 1..5
  evidence_blockers[]
  changes_required[]
  verdict: pass | revise | reject
}

PersonaContentReview {
  icp_ref
  artifact_ref
  lenses[]
  verdicts[]
  conflicts[]
  evidence_refs[]
  overall: pass | revise | reject
  reviewer_independence
}
```

Run the gate twice:

1. after the timed animatic and before `creative_lock`;
2. on the final render before completion.

Pass when:

- the primary ICP lens scores at least 4/5 in every category;
- required secondary lenses score at least 3/5 in every category;
- no unresolved factual, provenance, rights, trust, or comprehension blocker
  remains;
- persona conflicts are resolved or explicitly accepted as residual risk by
  the artifact owner;
- an independent reviewer, not the plan author alone, signs the receipt for
  material/public work.

Do not average away a blocker. One unsourced claim for the risk-owner persona or
one incomprehensible mechanism for the primary ICP keeps the gate at `revise`.

## Creative-lock additions

Block `creative_lock` when any applicable item is missing:

- resolved `ICPContract`;
- promise/payoff and causal spine;
- beat-level viewer-state changes;
- two-column narration and visual direction;
- evidence/explanation/soul function labels;
- asset decisions with jobs, evidence levels, provenance, rights, and motion
  purposes;
- wallpaper decisions;
- thumbnail alternatives for key beats;
- measured animatic plus silent/mute test;
- pre-production `PersonaContentReview` receipt at the threshold above.

The output should still compile useful sections before reporting a blocker. Do
not answer with a generic request for more context when the brief contains
enough to draft the story, map named elements, or construct provisional
realization packets.

## Source basis

This contract adapts, rather than copies, convergent mechanisms from:

- Johnny Harris's public workflow interview: coupled script/visual direction,
  promise/payoff, eye direction, evidence and human moments;
- Ben Marriott's public storyboarding tutorial: thumbnail, board, style-frame
  passes and cheap alternatives;
- Inside the Edit's B-roll tutorial: literal proof, suggestive relationship,
  atmosphere, and wallpaper rejection;
- John Yorke's public five-act notes: story as encounter, exploration, and
  assimilation;
- Nancy Duarte's public storytelling framework: one idea plus stakes and
  present/possible contrast;
- Robert McKee's public scene-turn excerpt: perceptible value change as a
  diagnostic.

Full source links and dispositions live in the TASK-0416 audit receipt.
