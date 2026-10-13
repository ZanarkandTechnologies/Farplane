#!/usr/bin/env python3
"""Scan the copy an outsider receives for mechanical release blockers.

Input is the delivered copy: a saved email (.eml), an HTML or text file, stdin
(-), or a public page URL. It flags unrendered placeholders, template or
editor sample text, non-production links, and links that fail or end at a
login wall. A clean scan is necessary, not sufficient: read the copy too.
"""

from __future__ import annotations

import argparse
import email
import re
import sys
import urllib.error
import urllib.request
from email import policy
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


PLACEHOLDERS = [
    (r"\{\{[^}]*\}\}|\{%[^%]*%\}", "unrendered template tag"),
    (r"\*\|[A-Z0-9_]+\|\*|%%[A-Za-z_]+%%", "unrendered merge field"),
    (r"\[(?:first ?name|last ?name|name|company|insert[^\]]*|your [^\]]*|link|url|date|price)\]", "bracket placeholder"),
    (r"<insert [^>]*>", "bracket placeholder"),
    (r"\b(?:TODO|TBD|FIXME)\b|\bXXX+\b", "unfinished marker"),
    (r"lorem ipsum", "lorem ipsum"),
    (r"\bexample\.(?:com|org|net)\b", "example domain"),
    (r"remove before publish", "internal note"),
    (r"\b(?:Hi|Hello|Hey|Dear)\s+,", "greeting with an empty name"),
]

# Default copy that platforms ship inside new emails, pages, and sequences.
TEMPLATE_FINGERPRINTS = [
    "sequences are an automated series of emails",
    "you can add more emails by clicking",
    "use this area to offer a short preview of your email",
    "it's easy to create a beautiful email",
    "just another wordpress site",
]

EDITOR_PHRASES = [
    r"\bclick(?:ing)? (?:on )?[\"“']?(?:add|edit|insert)\b",
    r"\bdrag(?:ging)? (?:and drop|[^.]{0,40}\bto)\b",
    r"\b(?:on|to) the (?:right|left)(?: side| panel| sidebar)?\b",
    r"\b(?:in|within) this (?:popover|editor|block|module|content area)\b",
    r"\breplace this (?:text|copy|image)\b",
    r"\b(?:your|add your) (?:text|content|headline|title|copy) here\b",
    r"\bthis is (?:a|an|your) (?:sample|example|placeholder|template)\b",
    r"\bsample (?:text|content|email)\b",
]

LOGIN_WALLS = [
    ("vercel.com", ("/login", "/sso-api")),
    ("accounts.google.com", ("",)),
    ("login.microsoftonline.com", ("",)),
    ("notion.so", ("/login",)),
    ("www.notion.so", ("/login",)),
    ("github.com", ("/login",)),
]

SKIP_FOLLOW = re.compile(r"unsubscribe|opt-?out|preferences|manage[-_ ]?subscription|update[-_ ]?(?:your[-_ ]?)?profile", re.I)
URL_RE = re.compile(r"https?://[^\s<>\"'\])]+")


class _HTMLCopy(HTMLParser):
    """Collect visible text, link targets with their text, and image sources."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text: list[str] = []
        self.links: list[tuple[str, str]] = []
        self._skip = 0
        self._href: str | None = None
        self._anchor: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style", "noscript", "template"}:
            self._skip += 1
        elif tag == "a" and attrs.get("href"):
            self._href, self._anchor = attrs["href"], []
        elif tag == "img" and attrs.get("src"):
            self.links.append((attrs["src"], "image"))
        if tag in {"p", "div", "br", "tr", "li", "h1", "h2", "h3", "td"}:
            self.text.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript", "template"} and self._skip:
            self._skip -= 1
        elif tag == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._anchor).strip()))
            self._href = None

    def handle_data(self, data):
        if self._skip:
            return
        self.text.append(data)
        if self._href is not None:
            self._anchor.append(data)


def parse_html(html: str) -> tuple[str, list[tuple[str, str]]]:
    parser = _HTMLCopy()
    parser.feed(html)
    return "".join(parser.text), parser.links


def load_copy(source: str, fetch=None) -> tuple[str, list[tuple[str, str]]]:
    """Return the visible text and (url, link text) pairs of the delivered copy."""
    if source.startswith(("http://", "https://")):
        text, links = parse_html((fetch or fetch_url)(source)[2])
        return text, [(source, "page")] + links
    data = sys.stdin.buffer.read() if source == "-" else Path(source).read_bytes()
    if source.endswith(".eml"):
        msg = email.message_from_bytes(data, policy=policy.default)
        texts = [f"Subject: {msg['subject'] or ''}\nFrom: {msg['from'] or ''}"]
        links: list[tuple[str, str]] = []
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                text, found = parse_html(part.get_content())
                texts.append(text)
                links += found
            elif part.get_content_type() == "text/plain":
                texts.append(part.get_content())
        return "\n".join(texts), links
    text = data.decode("utf-8", errors="replace")
    if source.endswith((".html", ".htm")) or "<html" in text[:500].lower():
        return parse_html(text)
    return text, []


def all_links(text: str, links: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen, out = set(), []
    for url, label in links + [(u, "") for u in URL_RE.findall(text)]:
        url = url.strip().rstrip(".,;:!?")
        if url.startswith(("http://", "https://")) and url not in seen:
            seen.add(url)
            out.append((url, label))
    return out


def host_problem(host: str) -> tuple[str, str] | None:
    host = host.lower()
    if host in {"localhost", "0.0.0.0"} or host.startswith("127.") or host.endswith((".local", ".localhost", ".test", ".internal")):
        return "BLOCKER", "local address"
    if re.match(r"^(?:10|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.", host):
        return "BLOCKER", "private network address"
    if host.endswith((".ngrok.io", ".ngrok-free.app", ".ngrok.app", ".trycloudflare.com", ".loca.lt")):
        return "BLOCKER", "tunnel address"
    if host.endswith(".vercel.app"):
        label = host[: -len(".vercel.app")]
        if "-git-" in label or re.search(r"-(?=[a-z]*\d)[a-z0-9]{9}-", label):
            return "BLOCKER", "Vercel preview deployment, not the live domain"
        return "WARN", "Vercel default domain, not the live domain"
    if host.endswith(".netlify.app") and "--" in host:
        return "BLOCKER", "Netlify deploy preview"
    if host.endswith(".pages.dev") and host.count(".") >= 3:
        return "BLOCKER", "Cloudflare Pages preview"
    if re.match(r"^(?:staging|stage|dev|preview|qa)[.-]", host):
        return "WARN", "staging-like host"
    return None


def fetch_url(url: str, timeout: float = 10.0) -> tuple[int, str, str]:
    """GET a URL following redirects; return (status, final url, body)."""
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (outbound-check)"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(500_000).decode("utf-8", errors="replace")
            return response.status, response.geturl(), body
    except urllib.error.HTTPError as error:
        return error.code, error.geturl() or url, ""


def link_problem(status: int, final_url: str) -> tuple[str, str] | None:
    parts = urlsplit(final_url)
    for host, paths in LOGIN_WALLS:
        if parts.hostname == host and any(parts.path.startswith(p) for p in paths):
            return "BLOCKER", f"ends at a login wall ({host}{parts.path})"
    if status == 401:
        return "BLOCKER", "401: login or access wall"
    if status in {403, 429, 999}:
        return "WARN", f"{status}: the site refused the automated check; open it by hand"
    if status in {404, 410} or 500 <= status < 600:
        return "BLOCKER", f"{status}: broken"
    return None


def scan(text: str, links: list[tuple[str, str]], follow: bool = True, fetch=fetch_url) -> list[tuple[str, str, str]]:
    findings: list[tuple[str, str, str]] = []
    lowered = " ".join(text.split()).lower()
    for pattern, label in PLACEHOLDERS:
        for match in re.finditer(pattern, text, re.I if label != "unfinished marker" else 0):
            findings.append(("BLOCKER", label, match.group(0)))
    for fingerprint in TEMPLATE_FINGERPRINTS:
        if fingerprint in lowered:
            findings.append(("BLOCKER", "template sample text", fingerprint))
    for pattern in EDITOR_PHRASES:
        for match in re.finditer(pattern, lowered):
            findings.append(("WARN", "reads like editor instructions", match.group(0)))
    for url, label in all_links(text, links):
        problem = host_problem(urlsplit(url).hostname or "")
        if problem:
            findings.append((problem[0], problem[1], url))
            if problem[0] == "BLOCKER":
                continue
        if SKIP_FOLLOW.search(url) or SKIP_FOLLOW.search(label):
            findings.append(("SKIP", "unsubscribe or preference link; test it by hand from a test contact", url))
            continue
        if not follow:
            continue
        try:
            status, final_url, _ = fetch(url)
        except (urllib.error.URLError, OSError, ValueError) as error:
            findings.append(("BLOCKER", f"does not open ({error})", url))
            continue
        problem = link_problem(status, final_url) or host_problem(urlsplit(final_url).hostname or "")
        if problem:
            findings.append((problem[0], problem[1], f"{url} -> {final_url}"))
        else:
            findings.append(("OK", f"{status}", url if final_url == url else f"{url} -> {final_url}"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="delivered copy: .eml, .html, .txt, - for stdin, or a page URL")
    parser.add_argument("--offline", action="store_true", help="do not follow links")
    args = parser.parse_args(argv)
    text, links = load_copy(args.source)
    findings = scan(text, links, follow=not args.offline)
    for level, label, detail in findings:
        print(f"{level:<8} {label}: {detail}")
    blockers = sum(level == "BLOCKER" for level, _, _ in findings)
    warnings = sum(level == "WARN" for level, _, _ in findings)
    verdict = "not ready to send" if blockers else "no mechanical blockers; now read it as the recipient"
    print(f"result: {blockers} blockers, {warnings} warnings - {verdict}")
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
