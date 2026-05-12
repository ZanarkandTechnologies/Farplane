# Storyboard Prompting

Use this for storyboard panels, shot lists, animatic frames, continuity passes, and image-to-video motion tests from panels.

## Panel Prompt Shape

```text
[panel number] + [shot type] + [subject] + [action] + [location] + [camera angle/lens] + [lighting] + [style suffix]
```

## Artifact-Specific Rules

- Maintain a shared style suffix across all panels: medium, color grade, lens feel, aspect ratio, and rendering style.
- Name shot vocabulary explicitly: wide shot, close-up, over-the-shoulder, low angle, bird's-eye, tracking shot.
- Keep panel prompts visual, not literary. The model needs visible action, framing, and mood.
- For continuity, repeat stable identity anchors: character age, wardrobe, key prop, location, time of day.
- For image-to-video tests, write motion prompts separately from panel prompts.

## Templates

```text
Panel:
"Panel [N], [shot type] of [character/product] [action] in [location], [camera angle/lens], [lighting], [mood], [shared style suffix]"

Continuity suffix:
"cinematic storyboard panel, consistent character design, slightly desaturated color, 16:9, clean linework, film pre-production board"

Motion test:
"Animate only [specific element], [motion description], camera [movement], keep [other elements] stable, preserve composition from storyboard panel"
```

## Avoid

- Changing style words between panels unless the scene intentionally changes.
- Asking for too many actions in one still panel.
- Generating final-video prompts before the shot list is stable.
