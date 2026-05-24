# Talking Head Prompting

Use this for avatar behavior, presenter video, lipsync, portrait generation, voice direction, and talking-head background prompts.

## Prompt Shapes

```text
Portrait:
[presenter identity] + [head-and-shoulders framing] + [direct eye contact] + [neutral expression] + [lighting] + [background] + [resolution/detail]

Avatar behavior:
[presenter role] + [delivery context] + [body language] + [background behavior] + [camera stability] + [tone]

Voice:
[tone] + [pace] + [emotion] + [audience] + [pronunciation constraints]
```

## Artifact-Specific Rules

- Portrait prompts should optimize for animation: centered face, eyes to camera, no sunglasses, no heavy shadows, head and shoulders visible.
- Keep the script conversational and segmented. Long monologues should be split into scenes/jobs.
- Use `voice_prompt` for delivery style and `video_prompt` for body language/background when the model supports them.
- Avoid asking the avatar model to create complex scene action; use Remotion overlays or separate clips for product/UI detail.
- Captions, lower thirds, exact text, and charts belong in `remotion`.

## Templates

```text
Portrait:
"Professional head-and-shoulders portrait of [persona], direct eye contact, neutral friendly expression, centered face, clean [background], soft studio lighting, high-resolution photorealistic"

Avatar behavior:
"The presenter speaks clearly to camera in a [setting], natural small hand gestures, calm posture, subtle head movement, professional lighting, stable camera"

Voice:
"Warm confident presenter voice, conversational pace, clear pronunciation, slightly energetic but not salesy, speaking to [audience]"
```

## Avoid

- Side-profile portraits or dramatic expressions for avatar inputs.
- Busy backgrounds that fight face tracking.
- Scripts with dense clauses that create unnatural mouth movement.
