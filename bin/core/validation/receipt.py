"""Deterministic validation receipt serialization."""

from __future__ import annotations

import json
from pathlib import Path

from .models import ValidationReceipt


def render_markdown(receipt: ValidationReceipt) -> str:
    lines = [
        "---",
        "kind: validation-receipt",
        f"phase: {receipt.phase}",
        f"status: {'pass' if receipt.ok else 'fail'}",
        "---",
        "",
        "# Validation Receipt",
        "",
        f"- Ticket: `{receipt.ticket}`",
        f"- Phase: `{receipt.phase}`",
        f"- Path source: `{receipt.path_source}`",
        f"- Base: `{receipt.base or 'none'}`",
        f"- Changed paths: {len(receipt.changed_paths)}",
        "",
        "## Results",
        "",
        "| Check | Mode | Status |",
        "| --- | --- | --- |",
    ]
    lines.extend(
        f"| `{result.check_id}` | {result.mode} | {result.status} |"
        for result in receipt.results
    )
    lines.extend(["", "## Changed Paths", ""])
    lines.extend(f"- `{path}`" for path in receipt.changed_paths)
    if not receipt.changed_paths:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def write_receipt(receipt: ValidationReceipt, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{receipt.phase}.json"
    markdown_path = output_dir / f"{receipt.phase}.md"
    json_path.write_text(json.dumps(receipt.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(receipt), encoding="utf-8")
    return json_path, markdown_path
