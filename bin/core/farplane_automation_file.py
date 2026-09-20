"""Read one Markdown-backed Farplane automation record."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from lint.source import MarkdownFrontmatterError, parse_markdown_frontmatter_document
except ImportError:  # pragma: no cover - package import path used by validators
    from bin.core.lint.source import MarkdownFrontmatterError, parse_markdown_frontmatter_document


class AutomationMarkdownError(ValueError):
    """Raised when an automation Markdown file is malformed."""


def load_automation_markdown(path: Path) -> dict[str, Any]:
    """Return YAML front matter plus the Markdown body as ``prompt``."""
    try:
        metadata, _raw, body = parse_markdown_frontmatter_document(
            path.read_text(encoding="utf-8"), path, required=True
        )
    except MarkdownFrontmatterError as exc:
        raise AutomationMarkdownError(str(exc)) from exc
    assert metadata is not None
    if "prompt" in metadata:
        raise AutomationMarkdownError("prompt must be the Markdown body, not front matter")
    return {**metadata, "prompt": body}
