# Method Selection Smoke

Use this fixture to test whether an agent can choose a landing-page method from
the section constraints without rereading all prose.

## Input

```text
Section.id = Hero
Section.job = make the offer memorable in the first viewport
Section.claim = a generated portal world becomes an interactive page
Section.layout = full-bleed hero with HTML nav, headline, and CTA overlays
Section.asset_carrier = generated/cutout layer set
Section.motion = scroll or timed transformation
Section.proof = source-frame or checkpoint comparison
Constraints.assets = 6-12 layers
Constraints.text_policy = readable text stays in HTML
Constraints.qa = debug phase + screenshot comparison
```

## Candidate Directions

| Method | Fit | Reason |
| --- | --- | --- |
| `static-generated-hero` | weak | misses layer/timeline/debug proof requirements |
| `cinematic-frame-sequence` | partial | good for authored video transforms, but weaker for inspectable independent layers |
| `frontend-craft:composed-scroll-animation` | strong | matches layer manifest, generated/cutout assets, HTML overlays, scroll/timed phases, and source-frame QA |

## Expected Selection

```text
ChosenMethod = frontend-craft:composed-scroll-animation
OwnerSkill = frontend-craft
SupportingSkills = imagegen + image-generation + visual-qa
```

## Negative Control

For a simple launch page hero with one product screenshot, one headline, one CTA,
and no layer/timeline/source-frame proof requirement:

```text
ChosenMethod != frontend-craft:composed-scroll-animation
```
