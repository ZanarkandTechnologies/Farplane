#!/usr/bin/env python3
"""Design-styles vocabulary backed by the bunker's Resource Bank.

Inputs: references/styles.json (the 50 named styles) and, for `seed`, one
example board image per style named NN.png in an image folder.
Outputs: `list` prints the vocabulary; `show` prints a style's stored recipe
and saves its board image locally; `seed` syncs styles.json into the Resource
Bank: one capture per new style (job, uploaded image asset, analysis, one
pinned visual element) and updated element text for changed styles.
Side effects: `seed` writes to the bunker's Convex deployment and storage;
`show` downloads images to .farplane/design-styles/refs/.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[1]
STYLES_PATH = SKILL_DIR / "references" / "styles.json"
REFS_DIR = REPO_ROOT / ".farplane" / "design-styles" / "refs"
BUNKER_DIR = Path(
    os.environ.get(
        "FARPLANE_BUNKER_DIR",
        Path.home() / "Zanarkand Technologies" / "projects" / "Farplane-UI-v2",
    )
)
LIBRARY_TAG = "style-library"
RB = "modules/resourceBank"


def load_catalog() -> dict:
    return json.loads(STYLES_PATH.read_text())


def style_tags(style: dict) -> list[str]:
    return [LIBRARY_TAG, f"style:{style['slug']}", f"style-family:{style['family']}"]


def resolve(catalog: dict, names: list[str]) -> list[dict]:
    by_key = {}
    for style in catalog["styles"]:
        for key in (style["slug"], style["name"].lower(), str(style["n"])):
            by_key[key] = style
    found = []
    for name in names:
        style = by_key.get(name.lower().removeprefix("style:"))
        if not style:
            sys.exit(f"unknown style: {name} (run `list`)")
        found.append(style)
    return found


def convex(function: str, payload: dict, push: bool = False):
    args = ["npx", "convex", "run"]
    if push:
        args.append("--push")
    args += [f"{RB}/{function}", json.dumps(payload)]
    result = subprocess.run(args, cwd=BUNKER_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"convex run {function} failed: {result.stderr.strip()[-800:]}")
    out = result.stdout.strip()
    return json.loads(out) if out else None


def find_element(style: dict) -> dict | None:
    """The stored element for one style, matched by its style tag (text search only narrows)."""
    rows = convex(
        "creativeElements:listCreativeElements",
        {"query": style["name"], "tags": [f"style:{style['slug']}"], "limit": 50},
    )
    if len(rows) > 1:
        print(f"warning: {len(rows)} stored elements for style:{style['slug']}", file=sys.stderr)
    return rows[0] if rows else None


def element_text(style: dict) -> dict:
    return {
        "title": f"{style['name']} style",
        "description": f"{style['cues']}.",
        "whyItWorks": (
            f"Reads as {style['mood']}; suits {style['use']}. Naming the style and its "
            "concrete cues steers a model far better than a mood word."
        ),
        "goldenRecipe": style["recipe"],
    }


def upload(path: Path) -> str:
    upload_url = convex("assets:generateResourceAssetUploadUrl", {})
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    request = urllib.request.Request(
        upload_url, data=path.read_bytes(), method="POST", headers={"Content-Type": mime}
    )
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())["storageId"]


def image_size(path: Path) -> tuple[int, int] | None:
    head = path.read_bytes()[:24]
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")
    return None


def analysis_markdown(style: dict, source: dict) -> str:
    return (
        f"## Breakdown\n{style['name']} ({style['family']}). Cues: {style['cues']}.\n"
        f"Example board: {style['board']}\n\n"
        f"## Why It Works\nReads as {style['mood']}. A named style plus its concrete cues "
        "gives an image model or designer a shared target instead of a vague mood word.\n\n"
        f"## Reuse Notes\nFits {style['use']}. Recreate the style from the recipe; the board's "
        "posters are other designers' work, so never copy a poster, logo, character or film "
        f"or brand property. Source: {source['title']}, {source['author']} ({source['publication']})."
    )


def seed_one(style: dict, catalog: dict, image_dir: Path, push: bool) -> str:
    source = catalog["source"]
    image = image_dir / f"{style['n']:02d}.png"
    if not image.exists():
        raise FileNotFoundError(image)
    tags = style_tags(style)
    source_ref = f"{source['url']}#{style['n']}-{style['slug']}"
    job_id = convex(
        "jobs:createIngestionJob",
        {
            "sourceKind": "image",
            "sourceRef": source_ref,
            "originalInstruction": "Store the 50 design styles and their example boards as design tags.",
            "note": "The operator asked to keep these style boards in the Tasty Pack as the design-tag vocabulary (2026-10-13).",
            "requestedFocus": f"{style['name']} style",
            "tags": tags,
            "requestedBy": "design-styles",
            "sourcePrivacy": "private",
        },
        push=push,
    )
    try:
        store_capture(style, source, image, tags, job_id)
    except Exception as error:
        convex("jobs:completeIngestionJob", {"jobId": job_id, "status": "failed", "error": str(error)[:1500]})
        raise
    return job_id


def store_capture(style: dict, source: dict, image: Path, tags: list[str], job_id: str) -> None:
    size = image_size(image)
    asset_id = convex(
        "assets:addResourceAsset",
        {
            "jobId": job_id,
            "assetRole": "primary",
            "assetKind": "image",
            "title": f"{style['name']} style board",
            "sourceUrl": source["url"],
            "canonicalUrl": source["url"],
            "storageId": upload(image),
            "mimeType": mimetypes.guess_type(image.name)[0],
            **({"width": size[0], "height": size[1]} if size else {}),
            "platform": "uxplanet",
            "author": f"{source['author']} ({source['publication']}); posters by various designers",
            "attributionStatus": "partial",
            "outputTypes": style["outputs"],
            "tags": tags,
            "searchableText": (
                f"{style['name']} design style {style['family']} {style['cues']} "
                f"{style['mood']} {style['use']}"
            ),
            "retentionNote": "Private style reference; recreate the style, never reuse the posters.",
        },
    )
    analysis_id = convex(
        "analyses:addResourceAnalysis",
        {
            "jobId": job_id,
            "assetId": asset_id,
            "sourceSkill": "design-styles",
            "analysisMarkdown": analysis_markdown(style, source),
            "confidence": "medium",
            "tags": tags,
        },
    )
    convex(
        "creativeElements:addCreativeElement",
        {
            "jobId": job_id,
            "assetId": asset_id,
            "analysisId": analysis_id,
            "kind": "visual",
            **element_text(style),
            "goldenExample": {"assetId": asset_id, "description": style["board"]},
            "anchor": "style board (four example posters)",
            "pinned": True,
            "tags": tags,
        },
    )
    convex("jobs:completeIngestionJob", {"jobId": job_id})


def cmd_list(catalog: dict, args) -> None:
    for family, blurb in catalog["families"].items():
        if args.family and family != args.family:
            continue
        print(f"\n{family} — {blurb}")
        for style in catalog["styles"]:
            if style["family"] == family:
                print(f"  style:{style['slug']:<22} {style['mood']} | {style['use']}")


def cmd_show(catalog: dict, args) -> None:
    REFS_DIR.mkdir(parents=True, exist_ok=True)
    for style in resolve(catalog, args.styles):
        print(f"\n## {style['name']}  (style:{style['slug']}, style-family:{style['family']})")
        try:
            row = find_element(style)
        except RuntimeError as error:
            print(f"Resource Bank unreachable ({error}); recipe from styles.json, no board image.")
            row = None
        if not row:
            print("Not in the Resource Bank; run `seed --only " + style["slug"] + "` once it is reachable.")
            print(f"Recipe (catalog): {style['recipe']}")
            continue
        print(f"Cues: {row['description']}")
        print(f"Why: {row['whyItWorks']}")
        print(f"Recipe: {row['goldenRecipe']}")
        print(f"Board: {row['goldenExample'].get('description', '')}")
        asset = row.get("goldenExampleAsset") or {}
        url = asset.get("storageUrl")
        if url and not args.no_image:
            extension = mimetypes.guess_extension(asset.get("mimeType") or "") or ".png"
            target = REFS_DIR / f"{style['slug']}{extension}"
            try:
                urllib.request.urlretrieve(url, target)
                print(f"Image: {target}")
            except OSError as error:
                print(f"Image download failed ({error}); URL: {url}")


def cmd_seed(catalog: dict, args) -> None:
    styles = resolve(catalog, args.only.split(",")) if args.only else catalog["styles"]
    push = args.push
    for style in styles:
        row = find_element(style)
        if row:
            changed = {k: v for k, v in element_text(style).items() if row.get(k) != v}
            if row["goldenExample"].get("description") != style["board"]:
                changed["goldenExample"] = {"assetId": row["goldenExample"]["assetId"], "description": style["board"]}
            if changed:
                convex("creativeElements:updateCreativeElement", {"elementId": row["_id"], **changed})
                print(f"updated {style['slug']}: {', '.join(changed)}", flush=True)
            else:
                print(f"unchanged {style['slug']}")
            continue
        job_id = seed_one(style, catalog, Path(args.images), push)
        push = False
        print(f"stored {style['slug']} job={job_id}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p_list = sub.add_parser("list", help="print the style vocabulary by family")
    p_list.add_argument("--family")
    p_show = sub.add_parser("show", help="print stored recipes and save board images")
    p_show.add_argument("styles", nargs="+", help="slug, name, number or style:<slug>")
    p_show.add_argument("--no-image", action="store_true")
    p_seed = sub.add_parser("seed", help="sync styles.json into the Resource Bank (new and changed styles)")
    p_seed.add_argument("--images", default=str(REPO_ROOT / ".farplane" / "design-styles" / "source"))
    p_seed.add_argument("--only", help="comma-separated slugs")
    p_seed.add_argument("--push", action="store_true", help="push bunker Convex code first")
    args = parser.parse_args()
    catalog = load_catalog()
    {"list": cmd_list, "show": cmd_show, "seed": cmd_seed}[args.command](catalog, args)


if __name__ == "__main__":
    main()
