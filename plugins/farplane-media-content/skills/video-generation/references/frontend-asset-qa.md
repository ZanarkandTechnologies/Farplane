# Frontend Asset QA

Generated video used in a web surface is both an asset-generation task and a frontend QA task.

## Implementation Handoff

Tell `frontend-craft`:

- final video path
- poster path, if present
- intended viewport and aspect ratio
- autoplay/loop/muted/controls policy
- reduced-motion fallback
- loading strategy
- visual role: background, hero media, product demo, inline proof, tutorial, or decorative motion

## Browser Checks

- Video file loads from the workspace/public asset path.
- The element has stable dimensions and does not cause layout shift.
- Mobile viewport preserves the core subject and controls.
- Autoplay behavior matches browser constraints: usually muted if autoplaying.
- Reduced-motion users see a poster, still image, or non-motion equivalent.
- Text and CTAs are not covered by the video.
- Captions or transcript exist when the video carries semantic content.

## Visual QA

Run `visual-qa` when:

- the video is first-viewport hero media
- the clip establishes brand/taste quality
- layout depends on video dimensions
- animation or motion could distract from the main task
- generated content may show artifacts, identity drift, or product inaccuracies

Evidence should include a screenshot and, when motion matters, a short clip or trace showing playback.
