"""`farplane library`: search the Studio library of saved design references and footage. Its address and key come from the environment or Doppler."""

from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request

def _setting(name: str) -> str:
    value = os.environ.get(name)
    if value:
        return value
    return subprocess.run(
        ["doppler", "secrets", "get", name, "--project", "farplane", "--config", "dev_personal", "--plain"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()


def _describe(item: dict) -> str:
    bits = [item.get("title") or item.get("file_name") or item["id"]]
    label = item.get("design_type") or "/".join(item.get("useful_for") or []) or item.get("status")
    if label:
        bits.append(f"[{label}]")
    text = item.get("description") or item.get("summary")
    if text:
        bits.append(f"- {text[:160]}")
    return " ".join(bits)


def run_library(args) -> int:
    query = {"q": " ".join(args.query), "limit": args.limit, "in": args.source, "type": args.type, "use": args.use, "ready": "1" if args.ready else None}
    studio = _setting("CHAIRHORSE_URL")
    url = f"{studio}/api/library/search?{urllib.parse.urlencode({k: v for k, v in query.items() if v})}"
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {_setting('CHAIRHORSE_API_KEY')}"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            found = json.load(response)
    except urllib.error.HTTPError as error:
        print(f"Studio answered {error.code}: {error.read().decode()[:300]}")
        return 1
    if args.json:
        print(json.dumps(found, indent=1))
        return 0
    for item in found["design"]:
        print(f"design  {_describe(item)}\n        {item['large_url']}")
    for item in found["footage"]:
        print(f"footage {_describe(item)}\n        {studio}{item['page']}")
    if not found["design"] and not found["footage"]:
        print("Nothing found.")
    return 0


def add_library_parser(sub) -> None:
    library = sub.add_parser("library", help="Search Studio's saved design references and footage.")
    library.add_argument("query", nargs="*", help="Words to look for, in text, tags and transcripts.")
    library.add_argument("--in", dest="source", choices=["design", "footage"], help="Search one side only.")
    library.add_argument("--type", help="Design type: poster, logo, type, packaging, book, editorial, web, app, social, motion, character, illustration, pattern, render, photo.")
    library.add_argument("--use", help="Footage use: hook, b-roll, product demo, before and after, talking head, voiceover, screen recording, tutorial, behind the scenes, ad, thumbnail.")
    library.add_argument("--ready", action="store_true", help="Only footage someone has confirmed.")
    library.add_argument("--limit", type=int, default=20)
    library.add_argument("--json", action="store_true")
    library.set_defaults(func=run_library)
