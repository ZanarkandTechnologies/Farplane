#!/usr/bin/env python3
"""Check what an outsider receives before it goes live, in one command.

Runs the fixed-rule checks, screenshots HTML copy at phone width in light and
dark mode, then has an independent model grade every row of
references/checklist.md against the copy, the link results, the screenshots,
and the sender's facts. Writes report.md and result.json; exits 1 on hold.

  farplane run -- python3 skills/outbound-check/scripts/outbound_check.py \\
      step1.eml step2.eml https://plan.example.com --context "Sender: ..."
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mechanical import Piece, load_piece, scan


CHECKLIST = Path(__file__).resolve().parent.parent / "references" / "checklist.md"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
KEY_ENV = "OPENROUTER_API_KEY"
MODEL_ENV = "OUTBOUND_JUDGE_MODEL"
DEFAULT_MODEL = "anthropic/claude-sonnet-5.5"
BROWSER_ENV = "OUTBOUND_BROWSER"
BROWSER_GLOB = "Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell"
MAX_TEXT = 20_000
MAX_IMAGES = 8
VERDICTS = ("PASS", "FAIL", "NOT_PROVABLE")

PROMPT = """You review what an outside recipient will get from a business: emails, ads, posts, pages, or messages. You did not write any of it. Grade every checklist row strictly from the evidence given.
- Fixed-rule findings are verified facts. A row with a BLOCKER finding fails.
- FAIL when the evidence shows the mistake anywhere. Quote the exact words, link, or what the screenshot shows.
- PASS only when the evidence shows the row holds.
- NOT_PROVABLE only when the copy, link results, screenshots, and sender facts together cannot show the row; say what is missing.
- Judge sender details, domains, offer, price, and piece count against the sender facts. Anything that contradicts them fails.
Return JSON only:
{"rows": [{"id": <row number>, "verdict": "PASS" | "FAIL" | "NOT_PROVABLE", "evidence": "<quote or reason>", "fix": "<one concrete fix, or empty>"}]}"""


def load_rows(path: Path = CHECKLIST) -> list[dict]:
    rows = []
    for line in path.read_text().splitlines():
        match = re.match(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", line)
        if match:
            rows.append({"id": int(match[1]), "mistake": match[2], "passes_when": match[3]})
    return rows


def find_browser() -> str | None:
    if os.environ.get(BROWSER_ENV):
        return os.environ[BROWSER_ENV]
    for name in ("chrome-headless-shell", "chromium", "google-chrome"):
        if shutil.which(name):
            return shutil.which(name)
    cached = sorted(Path.home().glob(BROWSER_GLOB))
    if cached:
        return str(cached[-1])
    chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    return str(chrome) if chrome.exists() else None


def screenshot(browser: str, target: str, out: Path, dark: bool) -> Path | None:
    args = [browser, "--headless", "--disable-gpu", "--hide-scrollbars",
            "--window-size=390,2400", f"--screenshot={out}"]
    if dark:
        args.append("--blink-settings=preferredColorScheme=0")
    try:
        subprocess.run(args + [target], capture_output=True, timeout=60, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return out if out.exists() and out.stat().st_size else None


def render(pieces: list[Piece], out_dir: Path) -> tuple[list[Path], str | None]:
    """Phone-width light and dark screenshots of every piece with HTML or a URL."""
    targets = []
    for index, piece in enumerate(pieces, 1):
        if piece.url:
            targets.append((index, piece.url))
        elif piece.html:
            page = out_dir / f"piece-{index}.html"
            page.write_text(piece.html)
            targets.append((index, page.resolve().as_uri()))
    if not targets:
        return [], None
    browser = find_browser()
    if not browser:
        return [], f"no headless browser found; set {BROWSER_ENV}"
    shots = []
    for index, target in targets:
        for mode in ("light", "dark"):
            shot = screenshot(browser, target, out_dir / f"piece-{index}-{mode}.png", mode == "dark")
            if shot:
                shots.append(shot)
    return shots, None if shots else "the browser produced no screenshots"


def judge_request(rows, pieces, findings, context, images, model) -> dict:
    checklist = "\n".join(f"{r['id']}. {r['mistake']}: passes when {r['passes_when']}" for r in rows)
    facts = "\n".join(f"{level} row {row} [{Path(source).name}] {label}: {detail}"
                      for source, level, row, label, detail in findings) or "none"
    copies = "\n\n".join(f"--- PIECE {i}: {p.source} ---\n{p.text[:MAX_TEXT] or '(image only)'}"
                         for i, p in enumerate(pieces, 1))
    text = (f"CHECKLIST:\n{checklist}\n\nSENDER FACTS:\n{context or 'none given'}\n\n"
            f"FIXED-RULE FINDINGS AND LINK RESULTS:\n{facts}\n\nDELIVERED COPY:\n{copies}\n\n"
            f"SCREENSHOTS: {', '.join(p.name for p in images) or 'none'}")
    content = [{"type": "text", "text": text}]
    for image in images[:MAX_IMAGES]:
        kind = "jpeg" if image.suffix.lower() in {".jpg", ".jpeg"} else image.suffix.lower().lstrip(".")
        data = base64.b64encode(image.read_bytes()).decode()
        content.append({"type": "image_url", "image_url": {"url": f"data:image/{kind};base64,{data}"}})
    return {"model": model, "max_tokens": 4000, "temperature": 0, "usage": {"include": True},
            "messages": [{"role": "system", "content": PROMPT}, {"role": "user", "content": content}]}


def post_openrouter(body: dict, key: str) -> dict:
    request = Request(ENDPOINT, data=json.dumps(body).encode(),
                      headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urlopen(request, timeout=180) as response:
        return json.load(response)


def judge(body: dict, environ=os.environ, post=post_openrouter) -> tuple[dict[int, dict], str | None, float | None]:
    """Return graded rows by id, the reason the judge is unavailable, and its cost."""
    key = environ.get(KEY_ENV, "").strip()
    if not key:
        return {}, f"{KEY_ENV} is not set; run through farplane run or doppler run", None
    try:
        reply = post(body, key)
        content = reply["choices"][0]["message"]["content"]
        graded = json.loads(re.search(r"\{.*\}", content, re.S).group(0))["rows"]
    except Exception as error:  # a judge failure must never read as a pass
        return {}, f"judge call failed: {error}", None
    rows = {int(r["id"]): r for r in graded if str(r.get("verdict")) in VERDICTS}
    return rows, None, reply.get("usage", {}).get("cost")


def merge(rows, findings, judged, judge_gap) -> list[dict]:
    """Fixed-rule blockers fail their row whatever the judge says; no judge means NOT_PROVABLE."""
    merged = []
    for row in rows:
        blockers = [f"{label}: {detail}" for _, level, number, label, detail in findings
                    if number == row["id"] and level == "BLOCKER"]
        graded = judged.get(row["id"], {})
        verdict = "FAIL" if blockers else graded.get("verdict", "NOT_PROVABLE")
        evidence = "; ".join(blockers + ([graded["evidence"]] if graded.get("evidence") else []))
        merged.append({**row, "verdict": verdict, "fix": graded.get("fix", ""),
                       "evidence": evidence or (judge_gap or "the judge returned no grade for this row")})
    return merged


def overall(merged: list[dict]) -> str:
    verdicts = {row["verdict"] for row in merged}
    return "hold" if "FAIL" in verdicts else "ready" if verdicts == {"PASS"} else "check"


def cell(value: str) -> str:
    return " ".join(str(value).split()).replace("|", "\\|")


def report(verdict, merged, findings, pieces, shots, judge_line, context) -> str:
    lines = [f"# Outbound check: {verdict}", "",
             f"- Checked: {', '.join(p.source for p in pieces)}",
             f"- Judge: {judge_line}",
             f"- Sender facts: {cell(context) if context else 'none given'}", "",
             "| # | Mistake | Verdict | Evidence | Fix |", "| --- | --- | --- | --- | --- |"]
    lines += [f"| {r['id']} | {cell(r['mistake'])} | {r['verdict']} | {cell(r['evidence'])} | {cell(r['fix'])} |"
              for r in merged]
    lines += ["", "## Fixed-rule findings", ""]
    lines += [f"- {level} row {row} [{Path(source).name}] {label}: {detail}"
              for source, level, row, label, detail in findings] or ["- none"]
    lines += ["", "## Screenshots", ""] + ([f"- {shot}" for shot in shots] or ["- none"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("copies", nargs="+", help="delivered copies: .eml, .html, .txt, image, -, or URL")
    parser.add_argument("--context", default="", help="sender facts: name, postal address, live domains, offer, piece count")
    parser.add_argument("--context-file", help="file holding the sender facts")
    parser.add_argument("--offline", action="store_true", help="do not follow links")
    parser.add_argument("--out", help="output folder (default .farplane/outbound-check/<time>)")
    args = parser.parse_args(argv)

    context = "\n".join(filter(None, [args.context, Path(args.context_file).read_text() if args.context_file else ""]))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(args.out or f".farplane/outbound-check/{stamp}")
    out_dir.mkdir(parents=True, exist_ok=True)

    pieces = [load_piece(source) for source in args.copies]
    findings = [(p.source, *finding) for p in pieces for finding in scan(p.text, p.links, follow=not args.offline)]
    shots, render_gap = render(pieces, out_dir)
    images = shots + [Path(p.image) for p in pieces if p.image]
    rows = load_rows()
    model = os.environ.get(MODEL_ENV) or DEFAULT_MODEL
    judged, judge_gap, cost = judge(judge_request(rows, pieces, findings, context, images, model))
    merged = merge(rows, findings, judged, judge_gap)
    verdict = overall(merged)

    judge_line = judge_gap or f"{model}" + (f" (USD {cost:.4f})" if cost else "")
    if render_gap:
        judge_line += f"; rendering not checked: {render_gap}"
    text = report(verdict, merged, findings, pieces, shots, judge_line, context)
    (out_dir / "report.md").write_text(text)
    (out_dir / "result.json").write_text(json.dumps(
        {"verdict": verdict, "rows": merged, "findings": findings, "copies": [p.source for p in pieces],
         "screenshots": [str(s) for s in shots], "judge": judge_line, "context": context}, indent=2) + "\n")
    print(text)
    print(f"OUTBOUND_CHECK: verdict={verdict} report={out_dir / 'report.md'}")
    return 1 if verdict == "hold" else 0


if __name__ == "__main__":
    raise SystemExit(main())
