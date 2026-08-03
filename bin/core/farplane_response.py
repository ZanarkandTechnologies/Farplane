"""Deterministic Markdown accounting for user-facing Farplane responses."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any


DEFAULT_MAX_PROSE_WORDS = 500
DEFAULT_MAX_PROSE_LINES = 20

_REFERENCE_HEADING = re.compile(
    r"^(?:#{1,6}\s+)?(?:references|citations)\s*:?\s*$", re.IGNORECASE
)
_REFERENCE_ENTRY = re.compile(
    r"^(?:[-*+]\s+)?\[[^\]]+\]\((?:<[^>]+>|[^)]+)\)\s*$"
)
_FENCE_OPEN = re.compile(r"^\s*(`{3,}|~{3,})\s*mermaid\s*$", re.IGNORECASE)
_MEDIA_EMBED = re.compile(
    r"^!\[[^\]]*\]\((?P<target><[^>]+>|[^)]+)\)\s*$", re.IGNORECASE
)
_MEDIA_EXTENSIONS = (
    ".avif",
    ".gif",
    ".jpeg",
    ".jpg",
    ".m4v",
    ".mov",
    ".mp4",
    ".png",
    ".webm",
    ".webp",
)


@dataclass(frozen=True)
class ResponseMeasure:
    total_words: int
    total_nonblank_lines: int
    prose_words: int
    prose_nonblank_lines: int
    mermaid_blocks: int
    mermaid_words: int
    mermaid_nonblank_lines: int
    media_embeds: int
    media_words: int
    media_nonblank_lines: int
    reference_entries: int
    reference_words: int
    reference_nonblank_lines: int

    def violations(self, max_prose_words: int, max_prose_lines: int) -> list[str]:
        violations: list[str] = []
        if self.prose_words > max_prose_words:
            violations.append("prose_words")
        if self.prose_nonblank_lines > max_prose_lines:
            violations.append("prose_nonblank_lines")
        return violations

    def result(self, max_prose_words: int, max_prose_lines: int) -> dict[str, Any]:
        violations = self.violations(max_prose_words, max_prose_lines)
        return {
            "ok": not violations,
            "limits": {
                "prose_words": max_prose_words,
                "prose_nonblank_lines": max_prose_lines,
            },
            "counts": asdict(self),
            "excluded": {
                "mermaid_blocks": self.mermaid_blocks,
                "mermaid_words": self.mermaid_words,
                "mermaid_nonblank_lines": self.mermaid_nonblank_lines,
                "media_embeds": self.media_embeds,
                "media_words": self.media_words,
                "media_nonblank_lines": self.media_nonblank_lines,
                "reference_entries": self.reference_entries,
                "reference_words": self.reference_words,
                "reference_nonblank_lines": self.reference_nonblank_lines,
            },
            "violations": violations,
        }


def _word_count(lines: list[str]) -> int:
    return sum(len(line.split()) for line in lines)


def _nonblank_count(lines: list[str]) -> int:
    return sum(1 for line in lines if line.strip())


def _reference_indices(lines: list[str]) -> tuple[set[int], int]:
    for heading_index in range(len(lines) - 1, -1, -1):
        if not _REFERENCE_HEADING.fullmatch(lines[heading_index].strip()):
            continue
        body = [line.strip() for line in lines[heading_index + 1 :] if line.strip()]
        if body and all(_REFERENCE_ENTRY.fullmatch(line) for line in body):
            indices = set(range(heading_index, len(lines)))
            return indices, len(body)
    return set(), 0


def _mermaid_indices(lines: list[str]) -> tuple[set[int], int]:
    indices: set[int] = set()
    blocks = 0
    index = 0
    while index < len(lines):
        match = _FENCE_OPEN.fullmatch(lines[index])
        if not match:
            index += 1
            continue
        fence = match.group(1)
        close_pattern = re.compile(rf"^\s*{re.escape(fence[0])}{{{len(fence)},}}\s*$")
        close_index = index + 1
        while close_index < len(lines) and not close_pattern.fullmatch(lines[close_index]):
            close_index += 1
        if close_index >= len(lines):
            index += 1
            continue
        indices.update(range(index, close_index + 1))
        blocks += 1
        index = close_index + 1
    return indices, blocks


def _is_media_embed(line: str) -> bool:
    match = _MEDIA_EMBED.fullmatch(line.strip())
    if not match:
        return False
    target = match.group("target").strip("<>").split("#", 1)[0].split("?", 1)[0]
    return target.lower().endswith(_MEDIA_EXTENSIONS) and (
        target.startswith("/") or target.startswith("https://")
    )


def measure_response(markdown: str) -> ResponseMeasure:
    lines = markdown.splitlines()
    reference_indices, reference_entries = _reference_indices(lines)
    mermaid_indices, mermaid_blocks = _mermaid_indices(lines)
    media_indices = {
        index
        for index, line in enumerate(lines)
        if index not in reference_indices
        and index not in mermaid_indices
        and _is_media_embed(line)
    }
    prose_indices = set(range(len(lines))) - reference_indices - mermaid_indices - media_indices

    def selected(indices: set[int]) -> list[str]:
        return [lines[index] for index in sorted(indices)]

    prose_lines = selected(prose_indices)
    mermaid_lines = selected(mermaid_indices)
    media_lines = selected(media_indices)
    reference_lines = selected(reference_indices)
    return ResponseMeasure(
        total_words=_word_count(lines),
        total_nonblank_lines=_nonblank_count(lines),
        prose_words=_word_count(prose_lines),
        prose_nonblank_lines=_nonblank_count(prose_lines),
        mermaid_blocks=mermaid_blocks,
        mermaid_words=_word_count(mermaid_lines),
        mermaid_nonblank_lines=_nonblank_count(mermaid_lines),
        media_embeds=len(media_indices),
        media_words=_word_count(media_lines),
        media_nonblank_lines=_nonblank_count(media_lines),
        reference_entries=reference_entries,
        reference_words=_word_count(reference_lines),
        reference_nonblank_lines=_nonblank_count(reference_lines),
    )


def check_response(
    markdown: str,
    max_prose_words: int = DEFAULT_MAX_PROSE_WORDS,
    max_prose_lines: int = DEFAULT_MAX_PROSE_LINES,
) -> dict[str, Any]:
    return measure_response(markdown).result(max_prose_words, max_prose_lines)
