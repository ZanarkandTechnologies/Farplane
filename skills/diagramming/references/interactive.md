# One-Control Explainer Page

Use this when the reader asks how one value changes another ("what happens to
the matcher's wrong picks as the threshold drops?"). A static diagram shows
what connects; this page lets the reader move the value and watch the result.

## Rules

- One concept, one slider, one canvas. If the question needs two controls or
  real application logic, draw a diagram instead.
- The fixed shell is [explainer_page.py](../scripts/explainer_page.py). The
  helper writes only the JSON spec; it never writes page HTML or CSS.
- Budget: about 2 minutes and one fix attempt. If the page fails or runs over,
  answer with a diagram and say so in one line.
- Use real numbers from the task (measured curve, logged scores) when they
  exist; otherwise label the model "illustrative" in the caption.

## Build

1. Write the brief below with the question, the value to vary, its range, and
   any real data points inline.
2. In Claude, run it as an Agent with `model: "sonnet"`; elsewhere use the
   fastest available model, or write the spec directly when that is quicker.
3. Run `python3 scripts/explainer_page.py <spec.json>` from this skill's
   folder. It writes `.farplane/diagramming/<title>.html`.
4. Publish that path with the Artifact tool and link it in the reply with one
   line on what to try ("drag below 0.4 and watch wrong picks rise").

## Helper brief

```text
Write one JSON object and save it to <spec path>. Nothing else.
Question: <one sentence>
Vary: <name>, range <min>..<max>, step <step>, start at <value> <unit>
Data: <real points, or "none: make an illustrative model">
Fields: title (2-4 words), question, control {label, min, max, step, value,
unit}, caption (what to look for, 1-2 short sentences), draw.
draw is a JavaScript function body called as draw(ctx, v, w, h, c) on every
slider move: ctx is a 2D canvas context already cleared and scaled, v the
slider value, w and h the size in CSS pixels, c the colours {fg, muted, line,
accent, warn, surface}. Use only these colours. Draw axes with labels in
c.muted, the main curve or object in c.accent, the failure region in c.warn.
Leave a 48 px left margin and 32 px on the other sides. Write axis names
horizontally (the y-axis name above its top tick), never rotated, and keep
every label clear of the others. Return a short string for the readout, such as
"overshoots after 3 steps". No external libraries, no DOM access, no timers.
```
