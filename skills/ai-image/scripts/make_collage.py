#!/usr/bin/env python3
"""Create a 2x2 vertical reel collage from four image URLs or local paths."""

from __future__ import annotations

import argparse
import io
import sys
import urllib.request
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageEnhance, ImageFilter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", help="Image URLs or paths.")
    parser.add_argument("--output", "-o", required=True, help="Output image path.")
    parser.add_argument("--width", type=int, default=1080, help="Output width.")
    parser.add_argument("--height", type=int, default=1920, help="Output height.")
    parser.add_argument("--gutter", type=int, default=0, help="Pixels between panels.")
    parser.add_argument(
        "--fit",
        choices=("cover", "contain", "expand", "solid"),
        default="cover",
        help="Fit mode for all tiles: cover, contain, expand, or solid.",
    )
    parser.add_argument(
        "--fits",
        help="Comma-separated per-source fit modes, e.g. cover,solid,solid. Overrides --fit per tile.",
    )
    parser.add_argument(
        "--position",
        default="center",
        help="Crop/placement position for all tiles or comma-separated per source: center, top, bottom, left, right, top-left, top-right, bottom-left, bottom-right.",
    )
    parser.add_argument(
        "--zoom",
        default="1",
        help="Scale multiplier for all tiles or comma-separated per source. Values below 1 zoom out for cover crops.",
    )
    parser.add_argument(
        "--layout",
        choices=("single", "stack", "2x2", "top2-bottom1"),
        default="2x2",
        help="single uses one source; stack uses two vertical panels; 2x2 uses four; top2-bottom1 uses three.",
    )
    parser.add_argument(
        "--darken",
        type=float,
        default=0.10,
        help="Dark overlay strength from 0 to 1.",
    )
    parser.add_argument(
        "--center-safe",
        type=int,
        default=0,
        help="Width of a dark vertical safe strip for speaker/captions.",
    )
    parser.add_argument(
        "--no-center-safe",
        action="store_true",
        help="Disable center safe strip even if --center-safe is set.",
    )
    parser.add_argument("--notes", help="Optional markdown file for source notes.")
    return parser.parse_args()


def load_image(source: str) -> Image.Image:
    if source.startswith(("http://", "https://")):
        request = urllib.request.Request(source, headers={"User-Agent": "reel-collage/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
        return Image.open(io.BytesIO(data)).convert("RGB")
    return Image.open(Path(source).expanduser()).convert("RGB")


def position_offsets(extra_w: int, extra_h: int, position: str) -> tuple[int, int]:
    horizontal, vertical = "center", "center"
    parts = position.lower().replace("_", "-").split("-")
    for part in parts:
        if part in {"left", "center", "right"}:
            horizontal = part
        if part in {"top", "center", "bottom"}:
            vertical = part

    left = 0 if horizontal == "left" else extra_w if horizontal == "right" else extra_w // 2
    top = 0 if vertical == "top" else extra_h if vertical == "bottom" else extra_h // 2
    return left, top


def cover_resize(img: Image.Image, size: tuple[int, int], position: str, zoom: float) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / img.width, target_h / img.height) * max(zoom, 0.1)
    if scale * img.width < target_w or scale * img.height < target_h:
        return solid_resize(img, size, position, 1.0)
    resized = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left, top = position_offsets(resized.width - target_w, resized.height - target_h, position)
    return resized.crop((left, top, left + target_w, top + target_h))


def contain_resize(img: Image.Image, size: tuple[int, int], position: str, zoom: float) -> Image.Image:
    target_w, target_h = size
    canvas = Image.new("RGB", size, (10, 10, 12))
    resized = img.copy()
    resized.thumbnail(size, Image.LANCZOS)
    if zoom != 1:
        resized = resized.resize((round(resized.width * zoom), round(resized.height * zoom)), Image.LANCZOS)
    left, top = position_offsets(target_w - resized.width, target_h - resized.height, position)
    canvas.paste(resized, (left, top))
    return canvas


def sampled_edge_color(img: Image.Image) -> tuple[int, int, int]:
    sample = img.copy()
    sample.thumbnail((64, 64), Image.LANCZOS)
    pixels = sample.load()
    colors: list[tuple[int, int, int]] = []
    for x in range(sample.width):
        colors.append(pixels[x, 0])
        colors.append(pixels[x, sample.height - 1])
    for y in range(sample.height):
        colors.append(pixels[0, y])
        colors.append(pixels[sample.width - 1, y])
    buckets: dict[tuple[int, int, int], int] = {}
    for red, green, blue in colors:
        bucket = (round(red / 24) * 24, round(green / 24) * 24, round(blue / 24) * 24)
        buckets[bucket] = buckets.get(bucket, 0) + 1
    return max(buckets.items(), key=lambda item: item[1])[0]


def solid_resize(img: Image.Image, size: tuple[int, int], position: str, zoom: float) -> Image.Image:
    target_w, target_h = size
    canvas = Image.new("RGB", size, sampled_edge_color(img))
    foreground = img.copy()
    foreground.thumbnail(size, Image.LANCZOS)
    if zoom != 1:
        foreground = foreground.resize((round(foreground.width * zoom), round(foreground.height * zoom)), Image.LANCZOS)
    left, top = position_offsets(target_w - foreground.width, target_h - foreground.height, position)
    canvas.paste(foreground, (left, top))
    return canvas


def expand_resize(img: Image.Image, size: tuple[int, int], position: str, zoom: float) -> Image.Image:
    target_w, target_h = size
    background = cover_resize(img, size, "center", 1.0).filter(ImageFilter.GaussianBlur(24))
    background = ImageEnhance.Brightness(background).enhance(0.45)
    foreground = img.copy()
    foreground.thumbnail(size, Image.LANCZOS)
    if zoom != 1:
        foreground = foreground.resize((round(foreground.width * zoom), round(foreground.height * zoom)), Image.LANCZOS)
    left, top = position_offsets(target_w - foreground.width, target_h - foreground.height, position)
    background.paste(foreground, (left, top))
    return background


def apply_tone(img: Image.Image, darken: float) -> Image.Image:
    img = ImageEnhance.Contrast(img).enhance(1.05)
    if darken <= 0:
        return img
    overlay = Image.new("RGB", img.size, (0, 0, 0))
    return Image.blend(img, overlay, max(0.0, min(darken, 1.0)))


def build_collage(args: argparse.Namespace) -> Image.Image:
    width, height, gutter = args.width, args.height, args.gutter
    resize_by_fit = {
        "cover": cover_resize,
        "contain": contain_resize,
        "expand": expand_resize,
        "solid": solid_resize,
    }
    positions = [p.strip() for p in args.position.split(",") if p.strip()]
    fits = [f.strip() for f in args.fits.split(",")] if args.fits else []
    zooms = [float(z.strip()) for z in args.zoom.split(",") if z.strip()]

    canvas = Image.new("RGB", (width, height), (8, 8, 10))

    if args.layout == "single":
        if len(args.sources) != 1:
            raise SystemExit(f"Expected exactly 1 source for single, got {len(args.sources)}.")
        slots = ((args.sources[0], (0, 0), (width, height)),)
    elif args.layout == "stack":
        if len(args.sources) != 2:
            raise SystemExit(f"Expected exactly 2 sources for stack, got {len(args.sources)}.")
        tile_h = (height - gutter) // 2
        slots = (
            (args.sources[0], (0, 0), (width, tile_h)),
            (args.sources[1], (0, tile_h + gutter), (width, height - tile_h - gutter)),
        )
    elif args.layout == "2x2":
        if len(args.sources) != 4:
            raise SystemExit(f"Expected exactly 4 sources for 2x2, got {len(args.sources)}.")
        tile_w = (width - gutter) // 2
        tile_h = (height - gutter) // 2
        slots = (
            (args.sources[0], (0, 0), (tile_w, tile_h)),
            (args.sources[1], (tile_w + gutter, 0), (tile_w, tile_h)),
            (args.sources[2], (0, tile_h + gutter), (tile_w, tile_h)),
            (args.sources[3], (tile_w + gutter, tile_h + gutter), (tile_w, tile_h)),
        )
    else:
        if len(args.sources) != 3:
            raise SystemExit(f"Expected exactly 3 sources for top2-bottom1, got {len(args.sources)}.")
        top_h = (height - gutter) // 2
        top_w = (width - gutter) // 2
        bottom_h = height - top_h - gutter
        slots = (
            (args.sources[0], (0, 0), (top_w, top_h)),
            (args.sources[1], (top_w + gutter, 0), (top_w, top_h)),
            (args.sources[2], (0, top_h + gutter), (width, bottom_h)),
        )

    for index, (source, paste_position, size) in enumerate(slots):
        tile_position = positions[index] if len(positions) > 1 and index < len(positions) else positions[0]
        tile_fit = fits[index] if index < len(fits) else args.fit
        if tile_fit not in resize_by_fit:
            raise SystemExit(f"Invalid fit mode '{tile_fit}'.")
        tile_zoom = zooms[index] if len(zooms) > 1 and index < len(zooms) else zooms[0]
        resize = resize_by_fit[tile_fit]
        tile = resize(load_image(source), size, tile_position, tile_zoom)
        canvas.paste(apply_tone(tile, args.darken), paste_position)

    if args.center_safe and not args.no_center_safe:
        strip_w = min(args.center_safe, width)
        left = (width - strip_w) // 2
        strip = Image.new("RGB", (strip_w, height), (0, 0, 0))
        region = canvas.crop((left, 0, left + strip_w, height))
        canvas.paste(Image.blend(region, strip, 0.45), (left, 0))

    return canvas


def write_notes(path: str | None, sources: Iterable[str], output: str) -> None:
    if not path:
        return
    lines = ["# Reel Collage Sources", "", f"- Output: `{output}`", ""]
    lines.extend(f"- {source}" for source in sources)
    Path(path).expanduser().write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    collage = build_collage(args)
    suffix = output.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        collage.save(output, quality=92, optimize=True)
    else:
        collage.save(output)
    write_notes(args.notes, args.sources, str(output))
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
