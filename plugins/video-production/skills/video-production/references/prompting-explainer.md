# Explainer Video Prompting

Use this for product explainers, how-it-works scenes, onboarding videos, tutorials, walkthroughs, and product demos.

## Prompt Shape

```text
[script section] + [one key idea] + [visual metaphor or product action] + [motion] + [camera/framing] + [style] + [readability constraint]
```

## Artifact-Specific Rules

- One scene equals one message. Do not ask one shot to explain the problem, feature, result, and CTA.
- Tie every prompt to the script section: hook, problem, solution, step 1, step 2, step 3, result, CTA.
- Use motion that clarifies the explanation: data flowing, UI element highlighting, before/after split, object assembling, or user completing a task.
- Keep UI/product scenes readable: avoid extreme motion blur, tiny text, or dense dashboards unless Remotion will overlay the exact UI.
- Use `remotion` for deterministic text, charts, captions, UI callouts, and exact timing.

## Templates

```text
Problem scene:
"Explainer video problem scene for [audience pain], [persona] encountering [problem], simple readable composition, subtle camera push-in, clean modern style, emotion is clear but not exaggerated"

How-it-works scene:
"Clean motion graphics scene showing [process step], [objects/data] moving from [source] to [destination], smooth explanatory motion, high contrast, simple background, space for labels"

Product demo scene:
"Product demo scene showing [user action] in [product/interface/context], hands or cursor moving through one clear step, bright professional lighting, readable screen area, calm pace"
```

## Avoid

- Prompting exact text inside generated video when Remotion or frontend overlays should own it.
- Packing multiple steps into one visual.
- Purely atmospheric clips that do not teach the viewer anything.
