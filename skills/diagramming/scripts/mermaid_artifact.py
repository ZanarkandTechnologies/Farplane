#!/usr/bin/env python3
"""Turn Markdown (or a bare .mmd file) with Mermaid blocks into an Artifact page.

Claude chat and Markdown files show Mermaid as source text; a published Artifact
renders `<pre class="mermaid">` natively. This builds that page with the
surrounding headings, prose, lists and tables kept, then prints its path for the
Artifact tool.

    python3 skills/diagramming/scripts/mermaid_artifact.py diagrams.md
    python3 skills/diagramming/scripts/mermaid_artifact.py flow.mmd --title "Webhook Retries"
    echo 'flowchart LR\n a-->b' | python3 skills/diagramming/scripts/mermaid_artifact.py - --title "A to B"
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

DEFAULT_DIR = Path(".farplane/diagramming")

STYLE = """<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
/* Layout: one reading column; each diagram sits in its own scrollable figure. */
:root {
  --bg: #f4f4f3; --surface: #ffffff; --fg: #1d1d1d; --muted: #5f5f5f;
  --line: #d9d9d7; --accent: #2c5fd4;
  --sans: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #161616; --surface: #1f1f1f; --fg: #ececec; --muted: #a3a3a3;
  --line: #333333; --accent: #8aa9ff; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #161616; --surface: #1f1f1f; --fg: #ececec; --muted: #a3a3a3;
  --line: #333333; --accent: #8aa9ff; color-scheme: dark }
body { background: var(--bg); color: var(--fg); font: 15px/1.6 var(--sans);
  padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 32px 48px }
main { max-width: 960px; margin: 0 auto; display: grid; gap: 14px; min-width: 0 }
main > p, main > ul, main > ol, main > blockquote { max-width: 68ch; margin: 0 }
h1, h2, h3, h4 { text-wrap: balance; line-height: 1.25; margin: 18px 0 0 }
h1 { font-size: 1.75rem; font-weight: 600; margin-top: 0 }
h2 { font-size: 1.25rem; font-weight: 600; padding-top: 14px; border-top: 1px solid var(--line) }
h3, h4 { font-size: 1.05rem; font-weight: 600 }
a { color: var(--accent) }
code { font: 0.9em var(--mono); background: var(--surface); border: 1px solid var(--line);
  border-radius: 4px; padding: 0 4px }
blockquote { border-left: 3px solid var(--line); padding-left: 12px; color: var(--muted) }
figure { margin: 0; background: var(--surface); border: 1px solid var(--line);
  border-radius: 8px; padding: 16px; overflow-x: auto; min-width: 0 }
pre.mermaid { margin: 0; display: flex; justify-content: center; background: transparent }
pre.code { margin: 0; overflow-x: auto; background: var(--surface); border: 1px solid var(--line);
  border-radius: 8px; padding: 12px; font: 13px/1.5 var(--mono) }
.table { overflow-x: auto; min-width: 0 }
table { border-collapse: collapse; font-size: 14px; font-variant-numeric: tabular-nums }
th, td { border-bottom: 1px solid var(--line); padding: 6px 10px; text-align: left; vertical-align: top }
th { color: var(--muted); font-weight: 500 }
</style>"""


def inline(text: str) -> str:
    """Escape text, then apply code spans, links, bold and italics."""
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        part = html.escape(part, quote=False)
        part = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                      lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', part)
        part = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", part)
        part = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", part)
        out.append(part)
    return "".join(out)


def table(rows: list[str]) -> str:
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], [r for r in cells[2:]]
    th = "".join(f"<th>{inline(c)}</th>" for c in head)
    trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    return f'<div class="table"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def render(markdown: str) -> tuple[str, str | None, int]:
    """Return (body_html, first_h1, mermaid_count)."""
    lines = markdown.splitlines()
    if lines and lines[0].strip() == "---":  # skip YAML front matter
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
        if end is not None:
            lines = lines[end + 1:]
    blocks: list[str] = []
    h1 = None
    count = 0
    i = 0
    para: list[str] = []

    def flush() -> None:
        if para:
            blocks.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        fence = re.match(r"^(\s*)(`{3,}|~{3,})\s*([\w-]*)", line)
        if fence:
            flush()
            marker, lang = fence.group(2), fence.group(3).lower()
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith(marker):
                body.append(lines[i])
                i += 1
            src = html.escape("\n".join(body), quote=False)
            if lang == "mermaid":
                count += 1
                blocks.append(f'<figure><pre class="mermaid">\n{src}\n</pre></figure>')
            else:
                blocks.append(f'<pre class="code"><code>{src}</code></pre>')
        elif m := re.match(r"^(#{1,4})\s+(.*)", line):
            flush()
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1 and h1 is None:
                h1 = re.sub(r"[`*]", "", text)
            blocks.append(f"<h{level}>{inline(text)}</h{level}>")
        elif line.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1]):
            flush()
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(lines[i])
                i += 1
            blocks.append(table(rows))
            continue
        elif m := re.match(r"^\s*([-*]|\d+\.)\s+(.*)", line):
            flush()
            tag = "ol" if m.group(1)[0].isdigit() else "ul"
            items = []
            while i < len(lines) and (m := re.match(r"^\s*([-*]|\d+\.)\s+(.*)", lines[i])):
                item = [m.group(2)]
                i += 1
                while i < len(lines) and lines[i].startswith("  ") and lines[i].strip() \
                        and not re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                    item.append(lines[i].strip())
                    i += 1
                items.append(f"<li>{inline(' '.join(item))}</li>")
            blocks.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue
        elif line.startswith(">"):
            flush()
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip(">").strip())
                i += 1
            blocks.append(f"<blockquote>{inline(' '.join(q for q in quote if q))}</blockquote>")
            continue
        elif not line.strip():
            flush()
        else:
            para.append(line.strip())
        i += 1
    flush()
    return "\n".join(blocks), h1, count


def build(source: str, name: str, title: str | None) -> tuple[str, int]:
    if name.endswith(".mmd"):
        source = f"```mermaid\n{source.strip()}\n```"
    body, h1, count = render(source)
    page_title = title or h1 or Path(name).stem.replace("-", " ").replace("_", " ").title()
    if not h1:
        body = f"<h1>{html.escape(page_title)}</h1>\n{body}"
    page = f"<title>{html.escape(page_title)}</title>\n{STYLE}\n<main>\n{body}\n</main>\n"
    return page, count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", help="Markdown or .mmd file, or - for stdin (read as Mermaid unless it has fences)")
    parser.add_argument("-o", "--out", type=Path, help=f"output .html (default {DEFAULT_DIR}/<name>.html)")
    parser.add_argument("--title", help="page title (default: first H1, else the file name)")
    args = parser.parse_args(argv)

    if args.source == "-":
        text = sys.stdin.read()
        name = "diagram.md" if "```" in text else "diagram.mmd"
    else:
        path = Path(args.source)
        text, name = path.read_text(encoding="utf-8"), path.name
    page, count = build(text, name, args.title)
    if count == 0:
        print("error: no Mermaid block found", file=sys.stderr)
        return 1
    out = args.out or DEFAULT_DIR / f"{Path(name).stem}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(out.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
