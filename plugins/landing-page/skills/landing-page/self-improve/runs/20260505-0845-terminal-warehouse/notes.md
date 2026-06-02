# Notes: Terminal Warehouse Benchmark

## Gold Reference

- URL: `https://terminal-industries.com/`
- Desktop screenshot:
  `/Users/kenjipcx/coding-harness/Farplane/.harness/gold-terminal-industries/desktop.png`
- Mobile screenshot:
  `/Users/kenjipcx/coding-harness/Farplane/.harness/gold-terminal-industries/mobile.png`

## Generated Output

- Site directory:
  `/Users/kenjipcx/coding-harness/Farplane/.harness/warehouse-cv-terminal-style`
- Desktop screenshot:
  `/Users/kenjipcx/coding-harness/Farplane/.harness/warehouse-cv-terminal-style/desktop.png`
- Mobile screenshot:
  `/Users/kenjipcx/coding-harness/Farplane/.harness/warehouse-cv-terminal-style/mobile.png`
- Full-page screenshot:
  `/Users/kenjipcx/coding-harness/Farplane/.harness/warehouse-cv-terminal-style/fullpage.png`

## What Loaded Correctly

- The external CLI command used profile `frontend-pi-kimi`.
- Session logs record provider `openrouter` and model `moonshotai/kimi-k2.6`.
- The prompt mounted `landing-page`, `frontend-craft`, `visual-design`,
  `visual-qa`, `review`, and `web-design-guidelines`.
- Static asset URL checks returned 200 for `index.html`, `styles.css`,
  `app.js`, and all six generated SVG files.
- `node --check app.js` passed.

## Terminal Gap

- Terminal uses a real photographic or pre-rendered truck hero. The generated
  page uses SVG/CSS stand-ins, so the first viewport feels lower fidelity.
- Terminal's object scale fills the viewport with a deliberate crop. The
  generated page leaves a large empty dark band and pushes the product claim
  too low.
- Terminal's mobile crop is intentionally cab-focused. The generated page's
  mobile viewport has the CTA/nav squeezed and the hamburger peeking off the
  right edge.
- Terminal's restraint makes the physical operation the hero. The generated
  page copies the palette and nav, but the media lacks the same production
  weight.
- Pi/Kimi did not complete self-review or visual QA in any run; Farplane had to
  capture screenshots and compare manually.

## Skill Improvement Hypothesis

Terminal-quality cinematic landing tasks need a hard phase split:

1. `spec`: write `SPEC.md` with recipe/taste/effect IDs and asset prompts.
2. `assets`: generate media or code-native placeholders with manifest checks.
3. `implementation`: build in file slices and verify syntax/assets.
4. `visual-review`: compare desktop/mobile screenshots against the gold
   reference and write the next skill hypothesis.

The skill should make code-native SVG placeholders legal only as a fallback,
not as a final Terminal-quality result.
