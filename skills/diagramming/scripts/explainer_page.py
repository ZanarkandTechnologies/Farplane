#!/usr/bin/env python3
"""Build a one-control explainer page from a small JSON spec.

The page answers "how does X change when Y changes?": one slider, one canvas,
one caption. The shell (layout, themes, canvas sizing, slider wiring) is fixed
here, so the helper that writes the spec only writes the drawing function.

    python3 skills/diagramming/scripts/explainer_page.py spec.json
    python3 skills/diagramming/scripts/explainer_page.py - < spec.json

Spec fields:
    title     page title, a name of two to four words
    question  the reader's question, one sentence
    control   {"label", "min", "max", "step", "value", "unit"?}
    caption   what to look for, one or two short sentences
    draw      JavaScript function body run with (ctx, v, w, h, c):
              ctx canvas 2D context, v slider value, w/h canvas size in CSS px,
              c colours {fg, muted, line, accent, warn, surface}.
              It may return a short string shown under the canvas.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

from mermaid_artifact import DEFAULT_DIR, STYLE

REQUIRED = ("title", "question", "control", "caption", "draw")
CONTROL = ("label", "min", "max", "step", "value")

EXTRA_STYLE = """<style>
:root { --warn: #b3261e }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --warn: #f2948a } }
:root[data-theme="dark"] { --warn: #f2948a }
main { max-width: 760px }
canvas { display: block; width: 100%; height: min(56vh, 380px); touch-action: pan-y }
.control { display: grid; grid-template-columns: auto 1fr auto; gap: 12px; align-items: center }
.control label { color: var(--muted); font-size: 14px }
.control input { width: 100%; accent-color: var(--accent); min-width: 0 }
.control output { font: 500 14px var(--mono); font-variant-numeric: tabular-nums; min-width: 6ch; text-align: right }
#readout { font: 14px var(--mono); color: var(--muted); margin: 8px 0 0; min-height: 1.6em }
</style>"""

SCRIPT = """<script>
(() => {
  const canvas = document.getElementById("view");
  const input = document.getElementById("control");
  const out = document.getElementById("value");
  const readout = document.getElementById("readout");
  const unit = %(unit)s;
  const draw = new Function("ctx", "v", "w", "h", "c", %(draw)s);
  function colours() {
    const s = getComputedStyle(document.documentElement);
    const get = (n) => s.getPropertyValue("--" + n).trim();
    return { fg: get("fg"), muted: get("muted"), line: get("line"),
             accent: get("accent"), warn: get("warn"), surface: get("surface") };
  }
  function render() {
    const dpr = window.devicePixelRatio || 1;
    const w = canvas.clientWidth, h = canvas.clientHeight;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    const ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    const v = Number(input.value);
    out.textContent = input.value + (unit ? " " + unit : "");
    let note = "";
    try { note = draw(ctx, v, w, h, colours()) || ""; }
    catch (err) { note = "Drawing failed: " + err.message; }
    readout.textContent = note;
  }
  input.addEventListener("input", render);
  new ResizeObserver(render).observe(canvas);
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", render);
  render();
})();
</script>"""


def validate(spec: dict) -> list[str]:
    errors = [f"missing {key}" for key in REQUIRED if key not in spec]
    control = spec.get("control")
    if not isinstance(control, dict):
        return errors + ["control must be an object"]
    errors += [f"control missing {key}" for key in CONTROL if key not in control]
    if not errors and not control["min"] <= control["value"] <= control["max"]:
        errors.append("control value is outside min..max")
    return errors


def build(spec: dict) -> str:
    control = spec["control"]
    esc = html.escape
    attrs = " ".join(f'{key}="{esc(str(control[key]))}"' for key in ("min", "max", "step", "value"))
    body = (
        f"<h1>{esc(spec['title'])}</h1>\n"
        f"<p>{esc(spec['question'])}</p>\n"
        '<figure>\n<canvas id="view" aria-label="Interactive view"></canvas>\n'
        '<p id="readout" aria-live="polite"></p>\n</figure>\n'
        '<div class="control">'
        f'<label for="control">{esc(control["label"])}</label>'
        f'<input id="control" type="range" {attrs}>'
        '<output id="value" for="control"></output></div>\n'
        f"<p>{esc(spec['caption'])}</p>\n"
    )
    script = SCRIPT % {"unit": json.dumps(control.get("unit", "")),
                       "draw": json.dumps(spec["draw"]).replace("</", "<\\/")}
    return (f"<title>{esc(spec['title'])}</title>\n{STYLE}\n{EXTRA_STYLE}\n"
            f"<main>\n{body}</main>\n{script}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("spec", help="JSON spec file, or - for stdin")
    parser.add_argument("-o", "--out", type=Path, help=f"output .html (default {DEFAULT_DIR}/<title>.html)")
    args = parser.parse_args(argv)

    text = sys.stdin.read() if args.spec == "-" else Path(args.spec).read_text(encoding="utf-8")
    spec = json.loads(text)
    errors = validate(spec)
    if errors:
        print("error: " + "; ".join(errors), file=sys.stderr)
        return 1
    slug = "-".join(spec["title"].lower().split())
    out = args.out or DEFAULT_DIR / f"{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(spec), encoding="utf-8")
    print(out.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
