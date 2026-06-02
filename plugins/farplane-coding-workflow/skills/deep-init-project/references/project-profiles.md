# Project Profiles

Use project profiles during bootstrap, deep interview, PRD writing, and
ticketization. A profile is not a full domain pipeline. It is the starting
shape that tells upstream planning which components, advice axes, prototype
gates, proof surfaces, and downstream skills matter for a project type.

## Algebra

```text
ProjectProfile :=
  ProjectType
+ ComponentSet
+ AdviceAxes
+ PRDTodos
+ PrototypeGates
+ PipelineHandoff
+ ProofSurfaces
+ HumanGates

Component :=
  id + job + advice_axes + candidate_options + selected_direction + proof

AdviceAxis :=
  id + prompt + option_count + option_shape + synthesis_target

PrototypeGate :=
  uncertainty + poc_artifact + pass_signal + ticket_rule

PipelineHandoff :=
  owner_skill + inputs + output_packet + proof
```

## Rules

- `deep-init-project` selects or records the profile in `docs/bootstrap-brief.md`.
- `deep-interview` asks along the profile's advice axes when the profile is
  present or when the operator names a project type.
- `prd` records explored options, selected directions, component matrix, and
  prototype gates.
- `spec-to-ticket` creates a PoC/proof ticket before full production tickets
  only when a prototype gate names a real uncertainty.
- Tier 3 domain skills consume the selected directions and handoff packets.
  They do not re-run the whole project discovery loop.
- Do not mechanically call `advise` for every field. Use `advise` for material
  choices; use profile defaults when the choice is obvious or low impact.

## Coding App

```text
ProjectType := coding-app

ComponentSet :=
  goal | user/workflow | data model | screens/routes | backend/API
| auth/permissions | observability | testability | deploy/runtime | proof

AdviceAxes :=
  product slice options | architecture/topology options | data ownership options
| UI workflow options | testability/proof options | deploy/runtime options

PRDTodos :=
  JTBD + SLC slice + non-goals + constraints + metric candidates
+ component matrix for data/screens/API/proof
+ selected direction for the first vertical slice

PrototypeGates :=
  riskiest integration | unknown UI workflow | unknown data model
| hard-to-QA surface

PipelineHandoff :=
  prd -> spec-to-ticket -> impl-plan -> impl
```

## Landing Page

```text
ProjectType := landing-page

ComponentSet :=
  offer | audience | positioning | story arc | hero | sections | assets
| motion | proof | CTA | QA

AdviceAxes :=
  offer/positioning options | section story options | hero media options
| layout options | asset route options | motion/scroll options
| proof/CTA options

PRDTodos :=
  offer + audience + story arc
+ section matrix
+ explored options per material section
+ selected complete directions
+ asset and motion proof gates

PrototypeGates :=
  hero visual/motion uncertainty | generated asset fidelity
| scroll interaction feasibility | mobile first-viewport fit

PipelineHandoff :=
  landing-page -> frontend-craft
```

## Video Project

```text
ProjectType := video-project

ComponentSet :=
  goal | audience | hook | story arc | scenes | assets | sound/voice/music
| motion | edit/pacing | export | proof

AdviceAxes :=
  hook/headline options | scene/story options | visual asset options
| motion style options | sound/voice/music options | edit/pacing options
| CTA/proof options

PRDTodos :=
  story arc + scene matrix
+ explored options for hook, visuals, sound, motion, edit, CTA
+ selected complete directions
+ prototype gate for the highest-risk scene or media route

PrototypeGates :=
  first scene fidelity | voice/sound direction | motion/transition feasibility
| generated asset consistency | export/platform constraints

PipelineHandoff :=
  video-production -> video-generation | remotion | remotion-render | frontend-craft
```

## Social Campaign

```text
ProjectType := social-campaign

ComponentSet :=
  campaign goal | audience | platforms | content pillars | artifacts
| copy hooks | assets | schedule | proof | publish boundary

AdviceAxes :=
  campaign angle options | platform mix options | artifact format options
| hook/copy options | asset route options | cadence/schedule options
| CTA/proof options

PRDTodos :=
  platform set + artifact matrix
+ explored options for hooks, formats, assets, cadence
+ selected complete directions
+ explicit publish/schedule boundary

PrototypeGates :=
  one representative post/thread/carousel | asset style proof | platform fit proof

PipelineHandoff :=
  social-content -> image-generation | video-generation | remotion | frontend-craft
```

## Product Photo Shoot

```text
ProjectType := product-photo-shoot

ComponentSet :=
  product facts | source assets | channel/marketplace | shot set | backgrounds
| generation/edit route | postprocess | product-page handoff | proof
| upload boundary

AdviceAxes :=
  shot set options | background/style options | realism vs stylization options
| source asset/edit options | marketplace/channel options | proof and handoff options

PRDTodos :=
  product facts + channel constraints
+ shot matrix
+ explored options for shot types, background/style, source/edit route
+ selected complete directions
+ upload/listing boundary

PrototypeGates :=
  one hero/packshot proof | product identity preservation
| background removal or upscale quality | marketplace compliance proof

PipelineHandoff :=
  product-photography -> imagegen | image-generation | frontend-craft
```
