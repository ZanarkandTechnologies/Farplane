#!/usr/bin/env python3
"""Create and update immutable-checkpoint visual reasoning workspaces."""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps


SUPPORTED_OPERATIONS = {"point", "box", "path", "arrow", "label", "grid", "crop"}
DEFAULT_COLOR = "#ff3b30"
LABEL_FILL = "#111827"
LABEL_TEXT = "#ffffff"


class WorkspaceError(ValueError):
    """Raised when a workspace or operation batch is invalid."""


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def _save_png_atomic(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "wb", dir=path.parent, prefix=f".{path.name}.", suffix=".png", delete=False
    ) as handle:
        temp_path = Path(handle.name)
    try:
        image.save(temp_path, format="PNG")
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)


def _workspace_paths(workspace: Path) -> tuple[Path, Path, Path, Path]:
    return (
        workspace / "source.png",
        workspace / "latest.png",
        workspace / "checkpoints",
        workspace / "operations",
    )


def _checkpoint_paths(checkpoints_dir: Path) -> list[Path]:
    paths = [path for path in checkpoints_dir.glob("[0-9][0-9][0-9].png") if path.is_file()]
    return sorted(paths, key=lambda path: int(path.stem))


def _assert_workspace(workspace: Path) -> tuple[Path, Path, Path, Path, list[Path]]:
    source, latest, checkpoints_dir, operations_dir = _workspace_paths(workspace)
    if not source.is_file() or not latest.is_file() or not checkpoints_dir.is_dir():
        raise WorkspaceError(f"not an initialized visual workspace: {workspace}")
    checkpoints = _checkpoint_paths(checkpoints_dir)
    if not checkpoints or checkpoints[0].name != "000.png":
        raise WorkspaceError("workspace is missing checkpoints/000.png")
    expected = list(range(len(checkpoints)))
    observed = [int(path.stem) for path in checkpoints]
    if observed != expected:
        raise WorkspaceError(f"checkpoint sequence is not contiguous: {observed}")
    for number in observed[1:]:
        receipt = operations_dir / f"{number:03d}.json"
        if not receipt.is_file():
            raise WorkspaceError(f"missing operation receipt: {receipt}")
    return source, latest, checkpoints_dir, operations_dir, checkpoints


def init_workspace(source_path: Path, workspace: Path) -> dict[str, Any]:
    if not source_path.is_file():
        raise WorkspaceError(f"source image does not exist: {source_path}")
    if workspace.exists() and any(workspace.iterdir()):
        raise WorkspaceError(f"refusing to reinitialize populated workspace: {workspace}")

    source, latest, checkpoints_dir, operations_dir = _workspace_paths(workspace)
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    operations_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(source_path) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGBA")
    _save_png_atomic(image, source)
    _save_png_atomic(image, checkpoints_dir / "000.png")
    _save_png_atomic(image, latest)
    return inspect_workspace(workspace)


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise WorkspaceError(f"{label} must be a number")
    result = float(value)
    if not math.isfinite(result) or result < 0 or result > 1:
        raise WorkspaceError(f"{label} must be within [0,1]")
    return result


def _point(value: Any, label: str) -> tuple[float, float]:
    if not isinstance(value, list) or len(value) != 2:
        raise WorkspaceError(f"{label} must be [x,y]")
    return _number(value[0], f"{label}[0]"), _number(value[1], f"{label}[1]")


def _box(value: Any, label: str) -> tuple[float, float, float, float]:
    if not isinstance(value, list) or len(value) != 4:
        raise WorkspaceError(f"{label} must be [x1,y1,x2,y2]")
    x1, y1, x2, y2 = (_number(part, f"{label}[{index}]") for index, part in enumerate(value))
    if x2 <= x1 or y2 <= y1:
        raise WorkspaceError(f"{label} must have x2>x1 and y2>y1")
    return x1, y1, x2, y2


def _points(value: Any, label: str, minimum: int = 2) -> list[tuple[float, float]]:
    if not isinstance(value, list) or len(value) < minimum:
        raise WorkspaceError(f"{label} must contain at least {minimum} points")
    return [_point(item, f"{label}[{index}]") for index, item in enumerate(value)]


def _color(value: Any) -> str:
    if value is None:
        return DEFAULT_COLOR
    if not isinstance(value, str):
        raise WorkspaceError("color must be a CSS-style color string")
    try:
        ImageColor.getrgb(value)
    except ValueError as exc:
        raise WorkspaceError(f"invalid color: {value}") from exc
    return value


def _optional_label(operation: dict[str, Any]) -> str | None:
    value = operation.get("label")
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceError("label must be a non-empty string")
    return value.strip()


def validate_operations(payload: Any) -> list[dict[str, Any]]:
    operations = payload.get("operations") if isinstance(payload, dict) else payload
    if not isinstance(operations, list) or not operations:
        raise WorkspaceError("operation payload must contain a non-empty operations list")

    validated: list[dict[str, Any]] = []
    for index, raw in enumerate(operations):
        if not isinstance(raw, dict):
            raise WorkspaceError(f"operation {index} must be an object")
        kind = raw.get("op")
        if kind not in SUPPORTED_OPERATIONS:
            raise WorkspaceError(f"operation {index} has unsupported op: {kind}")
        operation = dict(raw)
        operation["color"] = _color(raw.get("color"))
        label = _optional_label(raw)
        if label is not None:
            operation["label"] = label

        if kind in {"point", "label"}:
            operation["at"] = list(_point(raw.get("at"), f"operation {index}.at"))
        if kind in {"box", "crop"}:
            operation["box"] = list(_box(raw.get("box"), f"operation {index}.box"))
        if kind in {"path", "arrow"}:
            operation["points"] = [
                list(point) for point in _points(raw.get("points"), f"operation {index}.points")
            ]
        if kind == "label":
            text = raw.get("text")
            if not isinstance(text, str) or not text.strip():
                raise WorkspaceError(f"operation {index}.text must be a non-empty string")
            operation["text"] = text.strip()
        if kind == "grid":
            for field in ("rows", "columns"):
                value = raw.get(field)
                if isinstance(value, bool) or not isinstance(value, int) or not 2 <= value <= 100:
                    raise WorkspaceError(f"operation {index}.{field} must be an integer from 2 to 100")
                operation[field] = value
        validated.append(operation)
    return validated


def _pixel_point(point: tuple[float, float] | list[float], size: tuple[int, int]) -> tuple[int, int]:
    width, height = size
    return round(point[0] * (width - 1)), round(point[1] * (height - 1))


def _pixel_extent(box: list[float], size: tuple[int, int]) -> tuple[int, int, int, int]:
    width, height = size
    x1 = math.floor(box[0] * width)
    y1 = math.floor(box[1] * height)
    x2 = max(x1 + 1, math.ceil(box[2] * width))
    y2 = max(y1 + 1, math.ceil(box[3] * height))
    return x1, y1, min(width, x2), min(height, y2)


def _pixel_draw_box(box: list[float], size: tuple[int, int]) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = _pixel_extent(box, size)
    return x1, y1, x2 - 1, y2 - 1


def _draw_label(draw: ImageDraw.ImageDraw, at: tuple[int, int], text: str, image_size: tuple[int, int]) -> None:
    font = ImageFont.load_default()
    padding = 3
    left = min(max(0, at[0] + 4), max(0, image_size[0] - 1))
    top = min(max(0, at[1] + 4), max(0, image_size[1] - 1))
    bounds = draw.textbbox((left, top), text, font=font)
    text_width = bounds[2] - bounds[0]
    text_height = bounds[3] - bounds[1]
    left = min(left, max(0, image_size[0] - text_width - padding * 2))
    top = min(top, max(0, image_size[1] - text_height - padding * 2))
    draw.rectangle(
        (left, top, left + text_width + padding * 2, top + text_height + padding * 2),
        fill=LABEL_FILL,
    )
    draw.text((left + padding, top + padding), text, fill=LABEL_TEXT, font=font)


def _render_operations(image: Image.Image, operations: list[dict[str, Any]]) -> Image.Image:
    current = image.convert("RGBA")
    for operation in operations:
        kind = operation["op"]
        if kind == "crop":
            current = current.crop(_pixel_extent(operation["box"], current.size))
            continue

        draw = ImageDraw.Draw(current)
        line_width = max(2, round(min(current.size) * 0.006))
        radius = line_width * 2
        color = operation["color"]
        label_at: tuple[int, int] | None = None

        if kind == "point":
            point = _pixel_point(operation["at"], current.size)
            draw.ellipse(
                (point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius),
                fill=color,
                outline="#ffffff",
                width=max(1, line_width // 2),
            )
            label_at = point
        elif kind == "box":
            box = _pixel_draw_box(operation["box"], current.size)
            draw.rectangle(box, outline=color, width=line_width)
            label_at = (box[0], box[1])
        elif kind in {"path", "arrow"}:
            points = [_pixel_point(point, current.size) for point in operation["points"]]
            draw.line(points, fill=color, width=line_width, joint="curve")
            label_at = points[0]
            if kind == "arrow":
                start, end = points[-2], points[-1]
                angle = math.atan2(end[1] - start[1], end[0] - start[0])
                head = max(8, line_width * 4)
                spread = math.pi / 7
                left = (
                    round(end[0] - head * math.cos(angle - spread)),
                    round(end[1] - head * math.sin(angle - spread)),
                )
                right = (
                    round(end[0] - head * math.cos(angle + spread)),
                    round(end[1] - head * math.sin(angle + spread)),
                )
                draw.polygon([end, left, right], fill=color)
        elif kind == "label":
            point = _pixel_point(operation["at"], current.size)
            _draw_label(draw, point, operation["text"], current.size)
        elif kind == "grid":
            for column in range(1, operation["columns"]):
                x = round(column * current.size[0] / operation["columns"])
                draw.line((x, 0, x, current.size[1] - 1), fill=color, width=line_width)
            for row in range(1, operation["rows"]):
                y = round(row * current.size[1] / operation["rows"])
                draw.line((0, y, current.size[0] - 1, y), fill=color, width=line_width)

        if label_at is not None and operation.get("label"):
            _draw_label(draw, label_at, operation["label"], current.size)
    return current


def apply_operations(workspace: Path, payload: Any) -> dict[str, Any]:
    _, latest, checkpoints_dir, operations_dir, checkpoints = _assert_workspace(workspace)
    operations = validate_operations(payload)
    base_number = int(checkpoints[-1].stem)
    next_number = base_number + 1
    checkpoint_path = checkpoints_dir / f"{next_number:03d}.png"
    receipt_path = operations_dir / f"{next_number:03d}.json"
    if checkpoint_path.exists() or receipt_path.exists():
        raise WorkspaceError(f"refusing to overwrite checkpoint {next_number:03d}")

    with Image.open(latest) as opened:
        base = opened.convert("RGBA")
    rendered = _render_operations(base, operations)
    receipt = {
        "base_checkpoint": f"checkpoints/{base_number:03d}.png",
        "operations": operations,
        "result_checkpoint": f"checkpoints/{next_number:03d}.png",
    }

    _save_png_atomic(rendered, checkpoint_path)
    _write_json_atomic(receipt_path, receipt)
    _save_png_atomic(rendered, latest)
    return inspect_workspace(workspace)


def inspect_workspace(workspace: Path) -> dict[str, Any]:
    source, latest, _, operations_dir, checkpoints = _assert_workspace(workspace)
    with Image.open(latest) as opened:
        width, height = opened.size
    latest_checkpoint = checkpoints[-1]
    return {
        "workspace": str(workspace),
        "source": str(source),
        "latest": str(latest),
        "latest_checkpoint": str(latest_checkpoint),
        "checkpoint_count": len(checkpoints),
        "operation_receipt_count": len(list(operations_dir.glob("[0-9][0-9][0-9].json"))),
        "width": width,
        "height": height,
    }


def _load_json(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkspaceError(f"cannot read operation JSON {path}: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize an immutable-checkpoint workspace")
    init_parser.add_argument("--source", type=Path, required=True)
    init_parser.add_argument("--workspace", type=Path, required=True)

    apply_parser = subparsers.add_parser("apply", help="Render one operation batch as the next checkpoint")
    apply_parser.add_argument("--workspace", type=Path, required=True)
    apply_parser.add_argument("--operations", type=Path, required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Print derived workspace state")
    inspect_parser.add_argument("--workspace", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "init":
            result = init_workspace(args.source, args.workspace)
        elif args.command == "apply":
            result = apply_operations(args.workspace, _load_json(args.operations))
        else:
            result = inspect_workspace(args.workspace)
    except WorkspaceError as exc:
        print(f"visual workspace error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
