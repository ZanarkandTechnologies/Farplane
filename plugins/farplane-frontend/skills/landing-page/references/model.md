# Landing Page Model

Use this as the compact planning model for landing-page work.

## Algebra

```text
LandingPage := Offer + Audience + StoryArc + SectionMatrix + AssetPlan + MotionPlan + ProofPlan

Section := Job + Claim + Layout + AssetCarrier + MotionLever + ProofPayload + Fallback + QA

LandingMethod := id + use_when + avoid_when + required_assets + motion_shape + proof

MethodSelection(section, methods, constraints) :=
  candidates = filter(methods, section, constraints)
  chosen = advise(top3(candidates))
  section.execution_packet = ExecutionPacket(section, chosen)
```

## Section Matrix

| Section | Job | Claim | Layout | Asset carrier | Motion lever | Proof payload | QA |
| --- | --- | --- | --- | --- | --- | --- | --- |

Default section set:

```text
Hero -> Problem -> Solution -> Proof -> CTA
```

Optional sections:

```text
Logos | Use cases | Comparison | Reviews | Security | Pricing | Contact
```

## Lever Sets

```text
Layout :=
  full-bleed hero
| split proof
| sticky section
| editorial band
| product grid
| comparison table
| CTA block

AssetCarrier :=
  real media
| generated image
| cutout layer set
| frame sequence
| generated/native video
| Three.js/WebGL scene
| screenshot/product UI
| HTML overlay

MotionLever :=
  none
| CSS/Motion transition
| GSAP timeline
| ScrollTrigger scrub
| frame sequence scrub
| video scrub
| composed-scroll-animation
| Three.js/WebGL interaction
```

## Method Selection Rule

For each major section, compare complete directions:

```text
Direction :=
  layout + asset carrier + motion lever + proof payload + fallback + QA
```

Do not advise isolated headlines, colors, images, or animations unless that
single variable is the actual blocker.

## Composed Scroll Animation Route

Choose `frontend-craft:composed-scroll-animation` when a section needs:

- 6-12 image/UI layers
- generated or cutout assets
- HTML text/control overlays kept separate from pixels
- scroll or timed phases
- layer manifest and debug/proof hooks
- source-frame or checkpoint comparison

Prefer other routes when:

- one strong still image is enough -> static generated/real asset
- a continuous authored transformation is primary -> cinematic frame sequence
- a product/object needs real-time inspection -> Three.js/WebGL
- text and proof carry the section -> normal HTML/CSS/Motion

## Execution Packet

```text
ExecutionPacket :=
  section_id
+ chosen_method
+ required_assets
+ implementation_owner
+ ordered_steps
+ fallback
+ qa_assertions
```

`landing-page` owns the section decision. `frontend-craft` owns frontend
implementation.
