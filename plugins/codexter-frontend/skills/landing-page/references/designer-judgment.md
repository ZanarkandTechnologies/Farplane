# Designer Judgment Rubric

Use this for the last 5-15% of premium landing-page quality after mechanical QA
passes.

## Why

Scroll mechanics, visual richness, and asset loading can pass while the page
still feels under-authored. This rubric judges whether a competent product or
brand designer would defend the page.

## Score

Total: 100. Passing premium bar: 85. Terminal-level aspiration: 92+.

| Dimension | Points | What It Judges |
| --- | ---: | --- |
| Narrative clarity | 20 | The page has a clear claim, tension, mechanism, proof, and action. |
| Section intentionality | 15 | Every section earns its place and advances the story. |
| Visual authorship | 20 | Visuals feel selected/composed/designed, not filler. |
| Motion direction | 15 | Motion reveals meaning and guides attention. |
| Proof credibility | 15 | Metrics, logos, claims, and CTAs feel enterprise-plausible. |
| Taste consistency | 15 | Typography, spacing, density, palette, contrast, and rhythm are coherent. |

## Hard Gates

- Runtime page errors.
- Placeholder proof values visible to users.
- Blank or under-rendered primary visual panes.
- Missing mobile first-viewport proof.
- Missing reduced-motion fallback.
- Missing approved `LANDING_SPEC`.

## Review Prompts

- What does the section make the user believe that they did not believe before?
- If the visual were removed, would the section become more honest?
- Is the motion explaining state or merely decorating scroll?
- Would the proof survive a skeptical enterprise buyer?
- Does the page have enough density to feel authored without becoming noisy?
- Does the first viewport promise match the later sections?

## Output Shape

```json
{
  "percent_score": 0,
  "verdict": "pass|revise|fail",
  "hard_gates": [],
  "dimensions": [
    {
      "name": "narrative_clarity",
      "score": 0,
      "max_score": 20,
      "findings": []
    }
  ],
  "next_action": ""
}
```
