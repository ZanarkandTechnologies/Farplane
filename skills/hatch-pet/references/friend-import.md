# Friend Import

Load this reference when the pet represents a real person and the caller supplies an image plus optional public profile URLs, notes, style anchors, or animation ideas.

```text
friend_import(image, profile_urls?, user_notes?, animation_ideas?, style_anchor?)
  -> person-discovery.md + hatch-pet run + packaged pet
```

## Intake And Priority

Use this precedence order:

1. Explicit user corrections and constraints.
2. Supplied image for face, hair, wardrobe, accessories, and overall likeness.
3. Explicit animation ideas and style anchor.
4. Public profile facts relevant to profession, domain, recognizable props, and tone.
5. Clearly labeled low-confidence inference, only when useful to sprite direction.

At least one image is required. A profile URL is optional. Do not block when the image and user notes are already enough.

Style anchors may be a supplied image, an existing pet package, or a plain-language direction such as `Mini Kenji pixel style` or `Mini Chua energy`. Existing local pets are optional references and must not be assumed to exist on another machine.

## Bounded Research

Research 1-4 public sources, starting with the supplied URL. Use only material needed to make the pet recognizable and delightful: current role or domain, public creative themes, signature work-safe objects, stated interests that translate visually, and communication tone.

Do not collect private contact details, family or relationship information, precise location, sensitive or protected traits, health, wealth, politics, religion, sexuality, personality diagnoses, or speculative personal history. Do not treat a LinkedIn page as permission for broad people search. Separate `public fact`, `user-provided`, `inference`, and `unknown`.

If a page cannot be accessed, record that limitation and continue from the image and user notes. Never invent profile details.

## Person Brief

Write `person-discovery.md` with:

- `Identity anchor`: supplied image paths and what must remain recognizable.
- `Public cues`: concise sourced facts relevant to the avatar.
- `User direction`: notes, style anchor, and requested animation ideas.
- `Pet translation`: silhouette, palette, wardrobe, props, expression language, and avoidances.
- `Animation map`: each idea mapped to one or more fixed Codex states.
- `Sources and confidence`: URLs with fact/inference labels.
- `Generation handoff`: `pet_name`, `pet_notes`, `style_notes`, `animation_notes`, `avoid`, and `profile_sources`.

Keep the handoff compact. Research prose is review evidence, not an instruction dump for image generation.

## Animation Mapping

The atlas remains `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, and `review`.

Map personal ideas onto state semantics. Examples:

- coffee sip or thoughtful fidget -> `idle`
- friendly salute or signature greeting -> `waving`
- focused typing, sketching, mixing, presenting, or tinkering -> `running`
- checking a design, document, dashboard, or finished artifact -> `review`
- asking pose with an existing signature prop -> `waiting`
- comic deflation tied to their domain -> `failed`

Props must be large enough to read at pet scale and stable across rows. Prefer one signature prop already present in the base identity. Reject an idea when it requires text, UI, detached effects, a scene, or a new atlas row.

## Run Handoff

Prepare the run with the supplied image as `--reference`, the brief as `--person-discovery-file`, each public source as `--profile-source`, and the compact handoff as `--pet-notes` plus `--style-notes`. Then continue through the normal hatch-pet generation, deterministic assembly, visual QA, and packaging path.
