# Visual Critique And Audit

Use this to review a visual direction before or after implementation. Score
the rendered screen at its real viewport, never a description of it.

## Quick Score

Score each 0-4:

| Dimension | Question |
| --- | --- |
| Hierarchy | Is the primary action or message obvious? |
| Rhythm | Do spacing, scale, and density create a deliberate cadence? |
| Typography | Are font, scale, weight, and line length appropriate? |
| Color | Does the palette have roles instead of decoration? |
| Responsiveness | Does the design survive mobile and long text? |
| Accessibility | Are contrast, focus, hit targets, and motion preferences respected? |
| Concept | Does one idea from the product's world carry through type, color, and media at the register's loudness? N/A for polish with `none recorded`. |
| Focus & simplicity | Is the focal action unmistakable, with nonessential layers removed or deferred? |
| Anti-slop | Does it avoid AI tells? 4 = no tells; 0 = someone would instantly say an AI made it. |

## Output

- `Verdict:` pass, revise, or rethink.
- `Top issues:` severity-ranked.
- `Keep:` what is working.
- `Fix next:` one best immediate improvement.

## Refine Loop

- Score N/A where a dimension cannot apply (Concept on polish, Responsiveness
  for a single-viewport surface) and say why.
- `pass`: every scored dimension is 3 or more, and Anti-slop and Hierarchy
  are 4.
- `revise`: fix the dimension blocking `pass` first, re-render, and re-score.
- `rethink`: the concept fails; switch to the next-best direction. On polish,
  treat it as `revise`. A rethink counts toward the two-refine-pass cap.
- After two passes, hand off with `verdict: revise` and the open issue, and ask
  the operator whether to continue.

## Common Fixes

- Weak hierarchy: increase contrast between primary and secondary elements before adding decoration.
- Flat rhythm: vary spacing and section scale with purpose.
- Card overuse: remove containers and use bands, dividers, alignment, or whitespace.
- Visual noise: delete decorative elements until one idea remains.
- Template feel: pull one more concrete move from the concept (a type choice,
  a shape, an empty-state illustration) instead of adding decoration.
- Competing focal points: keep the action that serves the primary job and defer
  the rest rather than shrinking everything equally.
