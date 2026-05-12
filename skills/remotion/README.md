# Remotion

## Purpose

Remotion authoring and best-practice guidance for React video code: compositions, timing, media assets, captions, audio, transitions, and advanced effects.

## Entrypoints

- `SKILL.md` for first-load guidance and routing.
- `rules/*.md` for specific Remotion topics.
- `rules/assets/*.tsx` for example components referenced by the rules.

## Minimal Example

Load this skill when authoring Remotion code, then use `remotion-render` only if the code should be rendered through inference.sh.

## How To Test

For local Remotion projects, prefer a one-frame render check such as `npx remotion still <composition-id> --scale=0.25 --frame=30` before a full render.
