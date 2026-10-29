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
import select
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mechanical import Piece, load_piece, scan


CHECKLIST = Path(__file__).resolve().parent.parent / "references" / "checklist.md"
MODEL_ENV = "OUTBOUND_JUDGE_MODEL"
DEFAULT_MODEL = "sonnet"
# The judge is `claude -p` on the Claude Code subscription, never a paid API key:
# no tools, settings, MCP or hooks, and paid-key variables removed from its env.
CLAUDE_ARGS = ("-p", "--input-format", "stream-json", "--output-format", "stream-json", "--verbose",
               "--no-session-persistence", "--tools", "", "--strict-mcp-config",
               "--disable-slash-commands", "--setting-sources", "",
               "--settings", '{"disableAllHooks":true}')
PAID_KEYS = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_USE_BEDROCK",
             "CLAUDE_CODE_USE_VERTEX")
BROWSER_ENV = "OUTBOUND_BROWSER"
BROWSER_GLOB = "Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell"
MAX_TEXT = 20_000
MAX_IMAGES = 32
PHONE_WIDTH, PHONE_HEIGHT, TILE, MAX_TILES = 390, 844, 1600, 6
# Scroll to the bottom and back so scroll-triggered content is drawn before capture.
SCROLL_THROUGH = """new Promise(done => { let y = 0; const step = () => { window.scrollTo(0, y);
  y += innerHeight; if (y < document.documentElement.scrollHeight) setTimeout(step, 150);
  else { window.scrollTo(0, 0); setTimeout(done, 500); } }; step(); })"""
PAGE_HEIGHT = "Math.max(document.documentElement.scrollHeight, document.body ? document.body.scrollHeight : 0)"
VERDICTS = ("PASS", "FAIL", "NOT_PROVABLE")
# One judge run misses different faults on different runs, so two run in
# parallel and each row keeps its worst grade.
JUDGE_PASSES = 2
SEVERITY = {"PASS": 0, "NOT_PROVABLE": 1, "FAIL": 2}

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


class Browser:
    """Headless Chromium driven over the DevTools pipe: commands on fd 3, replies on fd 4."""

    def __init__(self, path: str):
        to_child_r, self._out = os.pipe()
        self._in, from_child_w = os.pipe()

        def wire():  # dup2 onto an fd's own number keeps close-on-exec, so clear it after
            reader, writer = os.dup(to_child_r), os.dup(from_child_w)
            os.dup2(reader, 3)
            os.dup2(writer, 4)
            os.set_inheritable(3, True)
            os.set_inheritable(4, True)

        self.proc = subprocess.Popen(
            [path, "--headless", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
             "--remote-debugging-pipe", "about:blank"],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            close_fds=False, preexec_fn=wire)
        os.close(to_child_r)
        os.close(from_child_w)
        self._buffer, self._last_id, self.events = b"", 0, []

    def _read(self, timeout: float) -> dict:
        deadline = time.monotonic() + timeout
        while b"\0" not in self._buffer:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([self._in], [], [], remaining)[0]:
                raise TimeoutError("the browser did not answer")
            chunk = os.read(self._in, 1 << 20)
            if not chunk:
                raise RuntimeError("the browser closed")
            self._buffer += chunk
        message, self._buffer = self._buffer.split(b"\0", 1)
        return json.loads(message)

    def send(self, method: str, params: dict | None = None, session: str | None = None, timeout: float = 30) -> dict:
        self._last_id += 1
        message = {"id": self._last_id, "method": method, "params": params or {}}
        if session:
            message["sessionId"] = session
        os.write(self._out, json.dumps(message).encode() + b"\0")
        while True:
            reply = self._read(timeout)
            if reply.get("id") != self._last_id:
                self.events.append(reply)
            elif "error" in reply:
                raise RuntimeError(f"{method}: {reply['error'].get('message')}")
            else:
                return reply.get("result", {})

    def wait_for(self, event: str, timeout: float) -> None:
        deadline = time.monotonic() + timeout
        while not any(e.get("method") == event for e in self.events):
            self.events.append(self._read(max(deadline - time.monotonic(), 0)))

    def close(self) -> None:
        try:
            self.send("Browser.close", timeout=5)
        except Exception:
            pass
        if self.proc.poll() is None:
            self.proc.kill()
        os.close(self._in)
        os.close(self._out)


def capture(path: str, target: str, stem: Path, dark: bool) -> tuple[list[Path], int]:
    """Full-length phone-width screenshots of one page, in tiles; returns tiles and page height."""
    browser = Browser(path)
    try:
        target_id = browser.send("Target.createTarget", {"url": "about:blank"})["targetId"]
        session = browser.send("Target.attachToTarget", {"targetId": target_id, "flatten": True})["sessionId"]
        browser.send("Emulation.setDeviceMetricsOverride", {"width": PHONE_WIDTH, "height": PHONE_HEIGHT,
                                                            "deviceScaleFactor": 1, "mobile": True}, session)
        browser.send("Emulation.setEmulatedMedia", {"features": [
            {"name": "prefers-color-scheme", "value": "dark" if dark else "light"}]}, session)
        browser.send("Page.enable", {}, session)
        browser.send("Page.navigate", {"url": target}, session)
        browser.wait_for("Page.loadEventFired", 45)
        browser.send("Runtime.evaluate", {"expression": SCROLL_THROUGH, "awaitPromise": True}, session, timeout=90)
        height = int(browser.send("Runtime.evaluate", {"expression": PAGE_HEIGHT, "returnByValue": True},
                                  session)["result"]["value"])
        tiles = []
        for index, top in enumerate(range(0, min(height, TILE * MAX_TILES), TILE), 1):
            clip = {"x": 0, "y": top, "width": PHONE_WIDTH, "height": min(TILE, height - top), "scale": 1}
            data = browser.send("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True,
                                                           "clip": clip}, session)["data"]
            tile = stem.with_name(f"{stem.name}-{index}.png")
            tile.write_bytes(base64.b64decode(data))
            tiles.append(tile)
        return tiles, height
    finally:
        browser.close()


def render(pieces: list[Piece], out_dir: Path) -> tuple[list[Path], str | None]:
    """Full-length phone-width light and dark screenshots of every piece with HTML or a URL."""
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
    shots, gaps = [], []
    for index, target in targets:
        for mode in ("light", "dark"):
            try:
                tiles, height = capture(browser, target, out_dir / f"piece-{index}-{mode}", mode == "dark")
            except (OSError, RuntimeError, TimeoutError, KeyError, ValueError) as error:
                gaps.append(f"piece {index} {mode}: {error}")
                continue
            shots += tiles
            if height > TILE * MAX_TILES:
                gaps.append(f"piece {index} {mode}: only the first {TILE * MAX_TILES}px of {height}px captured")
    return shots, "; ".join(gaps) or None


def judge_request(rows, pieces, findings, context, images, model) -> dict:
    checklist = "\n".join(f"{r['id']}. {r['mistake']}: passes when {r['passes_when']}" for r in rows)
    facts = "\n".join(f"{level} row {row} [{Path(source).name}] {label}: {detail}"
                      for source, level, row, label, detail in findings) or "none"
    copies = "\n\n".join(
        f"--- PIECE {i}: {p.source} ---\n{p.text[:MAX_TEXT] or '(image only)'}"
        + (f"\n[HIDDEN ON LOAD: shown only if a script reveals it, such as a form's done state; "
           f"otherwise visible only in the page source]\n{p.hidden[:MAX_TEXT]}" if p.hidden.strip() else "")
        for i, p in enumerate(pieces, 1))
    text = (f"CHECKLIST:\n{checklist}\n\nSENDER FACTS:\n{context or 'none given'}\n\n"
            f"FIXED-RULE FINDINGS AND LINK RESULTS:\n{facts}\n\nDELIVERED COPY:\n{copies}\n\n"
            f"SCREENSHOTS: {', '.join(p.name for p in images) or 'none'}")
    content = [{"type": "text", "text": text}]
    for image in images[:MAX_IMAGES]:
        kind = "jpeg" if image.suffix.lower() in {".jpg", ".jpeg"} else image.suffix.lower().lstrip(".")
        data = base64.b64encode(image.read_bytes()).decode()
        content.append({"type": "image", "source": {"type": "base64", "media_type": f"image/{kind}",
                                                    "data": data}})
    return {"model": model, "system": PROMPT, "messages": [{"role": "user", "content": content}]}


def claude_binary(environ) -> str | None:
    local = Path(environ.get("HOME", str(Path.home()))) / ".local/bin/claude"
    return shutil.which("claude", path=environ.get("PATH")) or (str(local) if local.exists() else None)


def post_claude(body: dict, binary: str, environ=os.environ) -> dict:
    """One judge reply from `claude -p`; earlier turns are folded into the one user message."""
    content = list(body["messages"][0]["content"])
    for message in body["messages"][1:]:
        content.append({"type": "text", "text": f"[{message['role'].upper()}]\n{message['content']}"})
    line = json.dumps({"type": "user", "message": {"role": "user", "content": content}})
    env = {key: value for key, value in environ.items() if key not in PAID_KEYS}
    env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
    done = subprocess.run([binary, *CLAUDE_ARGS, "--model", body["model"], "--system-prompt", body["system"]],
                          input=line + "\n", capture_output=True, text=True, timeout=600, env=env,
                          cwd=env.get("HOME") or None)
    events = [json.loads(line) for line in done.stdout.splitlines() if line.startswith("{")]
    reply = next(event for event in reversed(events) if event.get("type") == "result")
    if reply.get("is_error"):
        raise RuntimeError(str(reply.get("result"))[:300])
    return reply


def judge(body: dict, environ=os.environ, post=post_claude) -> tuple[dict[int, dict], str | None, float | None]:
    """Return graded rows by id and the reason the judge is unavailable (cost is always None:
    the subscription bills nothing per call)."""
    binary = claude_binary(environ)
    if not binary:
        return {}, "the claude CLI is not installed; install Claude Code and sign in", None
    error, content = None, None
    for _ in range(2):  # one retry, told what was wrong with the last reply
        try:
            reply = post(body, binary, environ)
            content = reply.get("result")
            if not content:
                raise ValueError(f"no text in the reply (stop_reason={reply.get('stop_reason')})")
            graded = json.loads(re.search(r"\{.*\}", content, re.S).group(0))["rows"]
            rows = {int(r["id"]): r for r in graded if str(r.get("verdict")) in VERDICTS}
            return rows, None, None
        except Exception as caught:  # a judge failure must never read as a pass
            error = caught
            if content is not None:
                body = {**body, "messages": body["messages"] + [
                    {"role": "assistant", "content": content},
                    {"role": "user", "content": f"That reply was not valid JSON ({caught}). Return the same "
                                                "grades as valid JSON only; escape double quotes inside strings."}]}
    return {}, f"judge call failed: {error}", None


def worst_of(passes: list[dict[int, dict]]) -> dict[int, dict]:
    """Per row, keep the most severe grade across judge passes, joining evidence that agrees."""
    worst: dict[int, dict] = {}
    for graded in passes:
        for number, row in graded.items():
            kept = worst.get(number)
            if kept is None or SEVERITY[row["verdict"]] > SEVERITY[kept["verdict"]]:
                worst[number] = dict(row)
            elif row["verdict"] == kept["verdict"] and row.get("evidence") and row["evidence"] != kept.get("evidence"):
                kept["evidence"] = f"{kept.get('evidence', '')} / {row['evidence']}"
                kept["fix"] = kept.get("fix") or row.get("fix", "")
    return worst


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
    findings = [(p.source, *finding) for p in pieces for finding in scan(p.text, p.links, follow=not args.offline, hidden=p.hidden)]
    shots, render_gap = render(pieces, out_dir)
    images = shots + [Path(p.image) for p in pieces if p.image]
    rows = load_rows()
    model = os.environ.get(MODEL_ENV) or DEFAULT_MODEL
    body = judge_request(rows, pieces, findings, context, images, model)
    with ThreadPoolExecutor(JUDGE_PASSES) as pool:
        passes = list(pool.map(lambda _: judge(body), range(JUDGE_PASSES)))
    judged = worst_of([graded for graded, _, _ in passes])
    gaps = [gap for _, gap, _ in passes if gap]
    judge_gap = gaps[0] if len(gaps) == JUDGE_PASSES else None
    cost = sum(spent or 0 for _, _, spent in passes)
    merged = merge(rows, findings, judged, judge_gap)
    verdict = overall(merged)

    judge_line = (judge_gap or f"{model}, {JUDGE_PASSES - len(gaps)} of {JUDGE_PASSES} passes") + (f" (USD {cost:.4f})" if cost else "")
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
