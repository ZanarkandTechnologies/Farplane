"""`farplane library`: find, download, save and fix Studio's saved design references and footage. Its address and key come from the environment or Doppler."""

from __future__ import annotations

import json
import mimetypes
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

DESIGN_RIGHTS = "reference only: learn from it, never publish it"
SINGLE_UPLOAD_MAX = 4.5 * 1024**3  # a larger file goes through the Raw files page, which uploads in parts
DRAFT_WAIT_SECONDS = 300


class LibraryError(Exception):
    pass


def _setting(name: str) -> str:
    value = os.environ.get(name)
    if value:
        return value
    return subprocess.run(
        ["doppler", "secrets", "get", name, "--project", "farplane", "--config", "dev_personal", "--plain"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()


def _call(method: str, path: str, *, data: bytes | None = None, payload: dict | None = None, content_type: str | None = None) -> dict:
    headers = {"Authorization": f"Bearer {_setting('CHAIRHORSE_API_KEY')}"}
    if payload is not None:
        data, content_type = json.dumps(payload).encode(), "application/json"
    if content_type:
        headers["Content-Type"] = content_type
    request = urllib.request.Request(f"{_setting('CHAIRHORSE_URL')}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise LibraryError(f"Studio answered {error.code}: {error.read().decode()[:300]}") from error


def _search(**query) -> dict:
    return _call("GET", f"/api/library/search?{urllib.parse.urlencode({k: v for k, v in query.items() if v})}")


def _describe(item: dict) -> str:
    bits = [item.get("title") or item.get("file_name") or item["id"]]
    label = item.get("design_type") or "/".join(item.get("useful_for") or []) or item.get("status")
    if label:
        bits.append(f"[{label}]")
    text = item.get("description") or item.get("summary")
    if text:
        bits.append(f"- {text[:160]}")
    return " ".join(bits)


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50] or "asset"


def _download(item: dict, url: str, suffix: str, folder: Path) -> Path:
    path = folder / f"{_slug(item.get('title') or item['id'])}-{item['id'][:8]}{suffix}"
    with urllib.request.urlopen(url, timeout=600) as response, path.open("wb") as out:
        shutil.copyfileobj(response, out)
    return path


def _pull(found: dict, folder: Path) -> list[dict]:
    """Download every result and keep library.json beside the files, so the source, credit, method and rights travel with them."""
    folder.mkdir(parents=True, exist_ok=True)
    manifest = folder / "library.json"
    kept = {row["id"]: row for row in (json.loads(manifest.read_text()) if manifest.exists() else [])}
    rows = []
    for item in found["design"]:
        rows.append({
            "id": item["id"], "side": "design", "file": _download(item, item["large_url"], ".webp", folder).name, "title": item["title"], "type": item["design_type"],
            "description": item.get("description"), "recipe": item.get("recipe"), "why": item.get("why"), "source": item.get("source_title"),
            "source_url": item.get("source_url"), "credit": item.get("author"), "tags": item.get("tags"), "width": item.get("width"), "height": item.get("height"), "rights": DESIGN_RIGHTS,
        })
    for item in found["footage"]:
        rows.append({
            "id": item["id"], "side": "footage", "file": _download(item, item["url"], Path(item["file_name"]).suffix, folder).name, "title": item["title"], "kind": item["kind"],
            "summary": item.get("summary"), "transcript": item.get("transcript"), "useful_for": item.get("useful_for"), "use_note": item.get("use_note"), "tags": item.get("tags"),
            "duration_s": item.get("duration_s"), "width": item.get("width"), "height": item.get("height"), "status": item.get("status"),
            "rights": item.get("rights_status") or "unknown", "role": item.get("usage_role"),
        })
    kept.update({row["id"]: row for row in rows})
    manifest.write_text(json.dumps(list(kept.values()), indent=1) + "\n")
    return rows


def _multipart(fields: dict, name: str, content: bytes, content_type: str) -> tuple[bytes, str]:
    boundary = uuid.uuid4().hex
    parts = [f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode() for key, value in fields.items() if value]
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; filename="upload"\r\nContent-Type: {content_type}\r\n\r\n'.encode() + content + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def _fetch_link(link: str, folder: str) -> Path:
    request = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=300) as response:
        kind = response.headers.get_content_type()
        if kind == "text/html":
            raise LibraryError("That link is a web page, not a file. Download the picture or clip first, or use the intelligest skill to learn from the page.")
        name = Path(urllib.parse.urlparse(link).path).name or "download"
        path = Path(folder) / (name if Path(name).suffix else name + (mimetypes.guess_extension(kind) or ""))
        with path.open("wb") as out:
            shutil.copyfileobj(response, out)
    return path


def _probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", str(path)], capture_output=True, text=True)
    info = json.loads(out.stdout or "{}")
    stream = (info.get("streams") or [{}])[0]
    return {"duration_s": (info.get("format") or {}).get("duration"), "width": stream.get("width"), "height": stream.get("height")}


def _design_fields(args) -> dict:
    fields = {"title": args.title, "design_type": args.type, "description": args.description, "recipe": args.recipe, "why": args.why, "source_title": args.source_name, "source_url": args.source_url, "author": args.credit}
    fields = {key: value for key, value in fields.items() if value is not None}
    return {**fields, "tags": args.tags} if args.tags is not None else fields


def _footage_fields(args) -> dict:
    fields = {"title": args.title, "summary": args.description, "usage_role": args.role, "rights_status": args.rights, "use_note": args.note}
    fields = {key: value for key, value in fields.items() if value is not None}
    if args.tags is not None:
        fields["tags"] = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    if args.use:
        fields["useful_for"] = [use.strip() for use in args.use.split(",") if use.strip()]
    return fields


def _save_picture(path: Path, kind: str, args) -> None:
    fields = {**_design_fields(args), "note": args.note, "force": "1" if args.force else None}
    data, content_type = _multipart(fields, "file", path.read_bytes(), kind)
    saved = _call("POST", "/api/design-bank", data=data, content_type=content_type)
    item = saved["item"]
    if args.json:
        print(json.dumps(saved, indent=1))
    elif saved.get("duplicate"):
        print(f"Already in the library ({saved['duplicate']}): {item['id']} {_describe(item)}\nNothing new stored. Add --force to keep a look-alike anyway.")
    else:
        print(f"Saved {item['id']} {_describe(item)}")


def _save_footage(path: Path, kind: str, args) -> None:
    size = path.stat().st_size
    if size > SINGLE_UPLOAD_MAX:
        raise LibraryError("Files over 4.5 GB go through the Raw files page in Studio.")
    signed = _call("POST", "/api/raw-files/sign", payload={"method": "PUT", "name": path.name, "type": kind, "size": size})
    with path.open("rb") as handle:
        urllib.request.urlopen(urllib.request.Request(signed["url"], data=handle, method="PUT", headers={"Content-Length": str(size), **signed["headers"]}), timeout=3600).read()
    fields = {"key": signed["key"], "name": path.name, "type": kind}
    thumb = b""
    if kind.startswith("video/"):
        fields.update({key: str(value) for key, value in _probe(path).items() if value})
        made = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", "1", "-i", str(path), "-frames:v", "1", "-vf", "scale=640:-2", "-f", "image2", "-c:v", "mjpeg", "-"], capture_output=True)
        thumb = made.stdout if made.returncode == 0 else b""
    data, content_type = _multipart(fields, "thumb", thumb, "image/jpeg") if thumb else (_multipart(fields, "ignored", b"", "text/plain"))
    row = _call("POST", "/api/raw-files", data=data, content_type=content_type)
    print(f"Saved footage {row['id']}. AI is drafting its description; a person or --edit {row['id']} --confirm finishes it.")
    wanted = _footage_fields(args)
    if not wanted:
        return
    # The draft replaces the description when it lands, so what was given here goes on top of it.
    deadline = time.time() + DRAFT_WAIT_SECONDS
    status = None
    while time.time() < deadline:
        status = _search(id=row["id"], **{"in": "footage"})["footage"][0]["status"]
        if status in ("draft", "failed", "confirmed"):
            break
        time.sleep(5)
    _call("PATCH", f"/api/raw-files/{row['id']}", payload=wanted)
    print(f"Added your fields on top of the draft ({status}).")


def _save(args) -> None:
    with tempfile.TemporaryDirectory() as folder:
        path = _fetch_link(args.save, folder) if re.match(r"https?://", args.save) else Path(args.save).expanduser()
        if not path.is_file():
            raise LibraryError(f"No such file: {path}")
        kind = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if kind.startswith("image/"):
            _save_picture(path, kind, args)
        elif kind.startswith(("video/", "audio/")):
            _save_footage(path, kind, args)
        else:
            raise LibraryError(f"Save a picture, video or audio file, not {kind}.")


def _edit(args) -> None:
    found = _search(id=args.edit)
    if found["design"]:
        if args.confirm:
            raise LibraryError("Only footage is confirmed; pictures have no draft stage.")
        item = _call("PATCH", f"/api/design-bank/{args.edit}", payload=_design_fields(args))["item"]
        print(f"Updated {item['id']} {_describe(item)}")
    elif found["footage"]:
        payload = {**_footage_fields(args), **({"confirm": True} if args.confirm else {})}
        _call("PATCH", f"/api/raw-files/{args.edit}", payload=payload)
        print(f"Updated footage {args.edit}{' and confirmed it' if args.confirm else ''}.")
    else:
        raise LibraryError(f"Nothing in the library has the id {args.edit}.")


def _remove(args) -> None:
    found = _search(id=args.remove, **{"in": "design"})
    if not found["design"]:
        raise LibraryError(f"No picture has the id {args.remove}. Footage has no remove: it may be the only copy, so a person deletes it by hand.")
    _call("DELETE", f"/api/design-bank/{args.remove}")
    print(f"Removed {_describe(found['design'][0])}")


def _find(args) -> None:
    limit = args.limit or (6 if args.to else 20)
    found = _search(q=" ".join(args.query), id=args.id, limit=limit, type=args.type, use=args.use, ready="1" if args.ready else None, **{"in": args.source})
    if args.to:
        rows = _pull(found, Path(args.to).expanduser())
        if args.json:
            print(json.dumps(rows, indent=1))
        for row in rows if not args.json else []:
            print(f"{args.to.rstrip('/')}/{row['file']}  [{row['rights']}]")
        if not args.json:
            print(f"{len(rows)} downloaded, details in {args.to.rstrip('/')}/library.json" if rows else "Nothing found.")
        return
    if args.json:
        print(json.dumps(found, indent=1))
        return
    studio = _setting("CHAIRHORSE_URL")
    for item in found["design"]:
        print(f"design  {item['id']} {_describe(item)}\n        {item['large_url']}")
    for item in found["footage"]:
        print(f"footage {item['id']} {_describe(item)}\n        {studio}{item['page']}")
    if not found["design"] and not found["footage"]:
        print("Nothing found.")


def run_library(args) -> int:
    try:
        if args.save:
            _save(args)
        elif args.edit:
            _edit(args)
        elif args.remove:
            _remove(args)
        else:
            _find(args)
    except LibraryError as error:
        print(error)
        return 1
    return 0


def add_library_parser(sub) -> None:
    library = sub.add_parser("library", help="Find, download, save and fix Studio's saved design references and footage.")
    library.add_argument("query", nargs="*", help="Words to look for, in text, tags and transcripts.")
    library.add_argument("--in", dest="source", choices=["design", "footage"], help="Search one side only.")
    library.add_argument("--type", help="Design type: poster, logo, type, packaging, book, editorial, web, app, social, motion, character, illustration, pattern, render, photo.")
    library.add_argument("--use", help="Footage use: hook, b-roll, product demo, before and after, talking head, voiceover, screen recording, tutorial, behind the scenes, ad, thumbnail. Comma-separated with --save or --edit.")
    library.add_argument("--ready", action="store_true", help="Only footage someone has confirmed.")
    library.add_argument("--limit", type=int, help="At most this many from each side (default 20, or 6 with --to).")
    library.add_argument("--id", help="Fetch one picture or clip by id.")
    library.add_argument("--to", help="Download the results into this folder, with library.json holding source, credit, method and rights.")
    library.add_argument("--save", help="Save this file or direct file link. A picture joins the Design Bank, a video or audio file joins Raw files; AI writes what you leave out.")
    library.add_argument("--edit", metavar="ID", help="Change a saved picture or clip using the fields below.")
    library.add_argument("--remove", metavar="ID", help="Remove a picture and its files.")
    library.add_argument("--confirm", action="store_true", help="With --edit: confirm a footage draft.")
    library.add_argument("--force", action="store_true", help="With --save: keep a picture that looks like one already saved.")
    library.add_argument("--note", help="Why this is worth keeping. Guides the AI on a picture; becomes the use note on footage.")
    library.add_argument("--title")
    library.add_argument("--description", help="What it shows.")
    library.add_argument("--recipe", help="Picture: how to make something in this manner.")
    library.add_argument("--why", help="Picture: why it works.")
    library.add_argument("--source-name", help="Picture: where it came from.")
    library.add_argument("--source-url", help="Picture: link to where it came from.")
    library.add_argument("--credit", help="Picture: who made it.")
    library.add_argument("--tags", help="Comma-separated search words.")
    library.add_argument("--role", choices=["production_source", "generated", "cinematic_reference", "taste_discovery", "archive_reference"], help="Footage: what it is.")
    library.add_argument("--rights", choices=["cleared", "per_item_verification_required", "restricted_reference_only", "unknown"], help="Footage: whether we may use it.")
    library.add_argument("--json", action="store_true")
    library.set_defaults(func=run_library)
