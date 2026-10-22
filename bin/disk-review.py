#!/usr/bin/env python3
"""Weekly read-only review of this Mac's disk and apps. Proposes; never deletes.

Run by the disk-review scheduled task. Measures free space, the largest
folders, regenerable caches and build outputs, temp-folder leftovers and
installed apps, compares against the last saved snapshot to find folders that
keep growing, and writes one Markdown report with, for every proposal, the
exact command to remove it and how to get it back.

  disk-review.py            scan, save snapshot + report, print JSON summary
  disk-review.py --no-save  scan and print the report, save nothing

Nothing here removes, moves or rewrites anything outside its own state folder
(.farplane/disk-review/). The commands in the report are for Kenji to run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import plistlib
import re
import shlex
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".farplane" / "disk-review"
HOME = Path.home()
TODAY = dt.date.today()

GB = 1024 * 1024  # du -k units per GiB
MIN_SNAPSHOT_KB = 100 * 1024       # keep folders >= 100 MB in the snapshot
APP_UNUSED_DAYS = 60
APP_PROPOSE_MIN_KB = 100 * 1024      # smaller unused apps are listed, not proposed
STALE_PROJECT_DAYS = 30
INSTALLER_AGE_DAYS = 30
LEAK_ONE_RUN_KB = 2 * GB           # grew this much since the last run
LEAK_STEADY_KB = 512 * 1024        # or grew this much in each of the last runs
TEMP_GROUP_MIN_KB = 512 * 1024    # temp patterns smaller than this are summed into one line
CACHE_PROPOSE_MIN_KB = GB          # smaller caches are not worth a proposal
TEMP_SAFE_AGE_DAYS = 1             # proposed temp removals skip anything newer

# Kenji's own data: listed for size, never proposed for deletion.
DATA_ROOTS = [
    "Movies", "Pictures", "Music", "Documents", "Desktop", "Downloads",
    "Zanarkand Technologies", "Eddison", "Library/Mobile Documents",
    "Library/Messages", "Library/Mail", "Library/Photos",
    "Library/Developer/Xcode/Archives", ".farplane", "projects", "archive", "job-apps",
    ".codex", ".claude",
]

# Regenerable locations: label, exact remove command, how to get it back.
# keep=True means regenerable but in active use, so it is reported, not proposed.
RULES = [
    (".cache/uv", "uv package cache", "uv cache clean", "uv re-downloads packages on the next `uv sync` / `uv run`", False),
    (".cache/huggingface", "Hugging Face model cache (Oures uses it)", "hf cache scan, then hf cache delete <model>", "models re-download on next load", True),
    (".cache/pip", "pip cache", "python3 -m pip cache purge", "pip re-downloads on next install", False),
    ("Library/Caches/pip", "pip cache", "python3 -m pip cache purge", "pip re-downloads on next install", False),
    (".cache/torch", "PyTorch hub/model cache", "rm -rf ~/.cache/torch", "weights re-download on next load", False),
    (".cache/puppeteer", "Puppeteer browsers", "rm -rf ~/.cache/puppeteer", "`npx puppeteer browsers install chrome`", False),
    ("Library/Caches/ms-playwright", "Playwright browsers", "rm -rf ~/Library/Caches/ms-playwright", "`npx playwright install`", False),
    (".npm/_cacache", "npm cache", "npm cache clean --force", "npm re-downloads on next install", False),
    ("Library/pnpm/store", "pnpm store", "pnpm store prune", "pnpm re-downloads on next install", False),
    ("Library/Caches/pnpm", "pnpm cache", "pnpm store prune", "pnpm re-downloads on next install", False),
    ("Library/Caches/Yarn", "Yarn cache", "yarn cache clean", "yarn re-downloads on next install", False),
    (".bun/install/cache", "Bun cache", "bun pm cache rm", "bun re-downloads on next install", False),
    ("Library/Caches/Homebrew", "Homebrew downloads", "brew cleanup --prune=all", "brew re-downloads on next install/upgrade", False),
    ("Library/Developer/Xcode/DerivedData", "Xcode build outputs", "rm -rf ~/Library/Developer/Xcode/DerivedData", "Xcode rebuilds on the next build", False),
    ("Library/Developer/Xcode/iOS DeviceSupport", "Xcode device symbols", "rm -rf ~/Library/Developer/Xcode/iOS\\ DeviceSupport", "Xcode re-copies them when a device connects", False),
    ("Library/Developer/CoreSimulator/Caches", "Simulator caches", "rm -rf ~/Library/Developer/CoreSimulator/Caches", "recreated on next simulator boot", False),
    ("Library/Developer/CoreSimulator/Devices", "iOS simulators", "xcrun simctl delete unavailable", "recreate simulators in Xcode > Devices", False),
    (".gradle/caches", "Gradle cache", "rm -rf ~/.gradle/caches", "Gradle re-downloads on next build", False),
    (".android/avd", "Android emulators", "delete unused ones in Android Studio > Device Manager", "recreate in Device Manager", False),
    ("Library/Containers/com.docker.docker", "Docker images and volumes", "docker system prune -a", "start Docker first; images re-pull or rebuild. Volumes are kept (add --volumes only if no database in them matters)", False),
    (".ollama/models", "Ollama models", "ollama list, then ollama rm <model>", "`ollama pull <model>`", False),
    (".lmstudio/models", "LM Studio models", "delete unused models in LM Studio > My Models", "re-download in LM Studio", False),
    (".cache/lm-studio", "LM Studio models", "delete unused models in LM Studio > My Models", "re-download in LM Studio", False),
    (".cargo/registry", "Cargo registry", "rm -rf ~/.cargo/registry/cache ~/.cargo/registry/src", "cargo re-downloads on next build", False),
    ("go/pkg/mod", "Go module cache", "go clean -modcache", "go re-downloads on next build", False),
    (".conda/pkgs", "conda package cache", "conda clean --all", "conda re-downloads on next install", False),
    ("miniconda3/pkgs", "conda package cache", "conda clean --all", "conda re-downloads on next install", False),
]

# Per-project build outputs: dir name -> (sibling that confirms it, restore hint).
BUILD_DIRS = {
    "node_modules": (None, "reinstall with the project's package manager (pnpm/npm/yarn/bun install)"),
    ".venv": (None, "`uv sync` (or recreate the venv and reinstall)"),
    "venv": (None, "recreate the venv and reinstall requirements"),
    ".next": (None, "`next build` / `next dev` recreates it"),
    ".turbo": (None, "recreated by the next turbo run"),
    "target": ("Cargo.toml", "`cargo build` recreates it"),
}
BUILD_MIN_KB = 500 * 1024
SKIP_HOME_CHILDREN = {"Library", "Movies", "Pictures", "Music", ".Trash"}


def run(cmd: list[str], timeout: int = 1800) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


# macOS app-data protection makes reads of a sandboxed app's container block
# (waiting on a consent prompt) instead of failing, so containers are measured
# one by one under a timeout and the blocked ones are reported as skipped.
CONTAINER_DIRS = ("Containers", "Group Containers")
CONTAINER_TIMEOUT_S = 90
SKIPPED: list[str] = []


def du_tree(root: Path, depth: int, ignore: tuple[str, ...] = ()) -> dict[str, int]:
    """du -k at up to `depth` levels below root, one filesystem only."""
    flags = [a for name in ignore for a in ("-I", name)]
    out = run(["du", "-xk", *flags, "-d", str(depth), str(root)])
    sizes: dict[str, int] = {}
    for line in out.splitlines():
        kb, _, path = line.partition("\t")
        if kb.isdigit():
            sizes[path] = int(kb)
    return sizes


def du_one(path: Path, timeout: int = 1800) -> int:
    out = run(["du", "-sxk", str(path)], timeout=timeout)
    head = out.split("\t", 1)[0]
    return int(head) if head.isdigit() else 0


def gb(kb: int) -> str:
    return f"{kb / GB:.1f} GB"


def tilde(path: str) -> str:
    home = str(HOME)
    return "~" + path[len(home):] if path.startswith(home) else path


def under(path: str, base: Path) -> bool:
    b = str(base)
    return path == b or path.startswith(b + "/")


def classify(path: str) -> str:
    for rel, *_ in RULES:
        if under(path, HOME / rel):
            return "regenerable"
    if under(path, Path(os.environ.get("TMPDIR", "/nonexistent")).resolve()) or "/var/folders/" in path:
        return "temp"
    if under(path, HOME / "Library/Caches") or under(path, HOME / ".cache"):
        return "regenerable"
    for rel in DATA_ROOTS:
        if under(path, HOME / rel):
            return "data"
    return "unknown"


# ---------------------------------------------------------------- scans


def free_space() -> dict:
    st = shutil.disk_usage("/System/Volumes/Data")
    return {"free_kb": st.free // 1024, "total_kb": st.total // 1024}


def scan_rules() -> list[dict]:
    rows = []
    for rel, label, remove, restore, keep in RULES:
        path = HOME / rel
        if not path.exists() or not readable(path):
            continue
        kb = du_one(path, timeout=CONTAINER_TIMEOUT_S * 4)
        if kb < MIN_SNAPSHOT_KB:
            continue
        rows.append({"path": str(path), "label": label, "kb": kb, "remove": remove,
                     "restore": restore, "keep": keep})
    rows.sort(key=lambda r: -r["kb"])
    return rows


def group_key(name: str) -> str:
    """eval-prof-AbC123 -> eval-prof-*, tmpk2j3h4 -> tmp*; plain names stay."""
    m = re.match(r"^(.*?[-_.])[A-Za-z0-9]{5,}$", name)
    if m and len(m.group(1)) >= 3:
        return m.group(1) + "*"
    m = re.match(r"^([A-Za-z]{3,}?)[A-Za-z0-9_]{6,}$", name)
    if m and re.search(r"\d", name[len(m.group(1)):]):
        return m.group(1) + "*"
    return name


def scan_temp() -> tuple[dict[str, int], list[dict], dict]:
    tmp = Path(os.environ.get("TMPDIR") or run(["getconf", "DARWIN_USER_TEMP_DIR"]).strip()).resolve()
    var_root = tmp.parent
    totals = {p: kb for p, kb in du_tree(var_root, 1).items()}
    children = du_tree(tmp, 1)
    groups: dict[str, dict] = {}
    now = dt.datetime.now().timestamp()
    for path, kb in children.items():
        if path.rstrip("/") == str(tmp):
            continue
        name = Path(path).name
        key = group_key(name)
        g = groups.setdefault(key, {"pattern": key, "count": 0, "kb": 0, "old_kb": 0,
                                    "newest_days": None, "oldest_days": None})
        g["count"] += 1
        g["kb"] += kb
        try:
            age = (now - Path(path).stat().st_mtime) / 86400
        except OSError:
            age = 0
        if age >= TEMP_SAFE_AGE_DAYS:
            g["old_kb"] += kb
        g["newest_days"] = age if g["newest_days"] is None else min(g["newest_days"], age)
        g["oldest_days"] = age if g["oldest_days"] is None else max(g["oldest_days"], age)
    rows = [g for g in groups.values() if g["kb"] >= TEMP_GROUP_MIN_KB]
    small = [g for g in groups.values() if g["kb"] < TEMP_GROUP_MIN_KB]
    rest = {"patterns": len(small), "count": sum(g["count"] for g in small), "kb": sum(g["kb"] for g in small)}
    for g in rows:
        pat = g["pattern"]
        q_tmp = shlex.quote(str(tmp))
        g["remove"] = (f"find {q_tmp} -maxdepth 1 -name {shlex.quote(pat)} -mtime +{TEMP_SAFE_AGE_DAYS - 1} "
                       f"-exec rm -rf {{}} +")
        g["restore"] = "nothing to restore: temp copies are recreated by the tool on its next run"
        g["creator"] = find_creator(pat)
    rows.sort(key=lambda r: -r["kb"])
    return {"tmp": str(tmp), **totals}, rows, rest


def find_creator(pattern: str) -> list[str]:
    """Search code for the literal prefix of a temp-folder name."""
    prefix = pattern.rstrip("*")
    if len(prefix.strip("-_.")) < 5 or prefix.lower().startswith(("tmp", "temp", "com.", "org.")):
        return []
    roots = [p for p in (HOME / "Eddison", HOME / "Zanarkand Technologies/projects", HOME / ".claude/skills")
             if p.exists()]
    if not roots or not shutil.which("rg"):
        return []
    code = ["*.mjs", "*.js", "*.cjs", "*.ts", "*.tsx", "*.py", "*.sh", "*.go", "*.rs", "*.swift"]
    globs = [a for g in code for a in ("-g", g)]
    out = run(["rg", "-l", "-F", "--max-count", "1", *globs, "-g", "!node_modules", "-g", "!*.min.js",
               "-g", "!dist", "-g", "!.farplane", prefix, *map(str, roots)], timeout=120)
    hits = [l for l in out.splitlines() if l.strip()]
    hits.sort(key=lambda p: (".test." in p or "/tests/" in p, len(p)))
    return hits[:3]


def project_root(path: Path) -> Path:
    for parent in path.parents:
        if (parent / ".git").exists():
            return parent
        if parent == HOME:
            break
    return path.parent


def last_activity_days(project: Path) -> float:
    candidates = [project / ".git" / "index", project / ".git" / "HEAD", project]
    newest = 0.0
    for c in candidates:
        try:
            newest = max(newest, c.stat().st_mtime)
        except OSError:
            pass
    return (dt.datetime.now().timestamp() - newest) / 86400 if newest else 9999


def scan_build_outputs() -> list[dict]:
    roots = [p for p in HOME.iterdir()
             if p.is_dir() and not p.name.startswith(".") and p.name not in SKIP_HOME_CHILDREN]
    names = list(BUILD_DIRS)
    expr: list[str] = []
    for i, n in enumerate(names):
        expr += (["-o"] if i else []) + ["-name", n]
    found: list[Path] = []
    for root in roots:
        out = run(["find", str(root), "-maxdepth", "7", "-type", "d", "(", *expr, ")", "-prune", "-print"],
                  timeout=600)
        found += [Path(l) for l in out.splitlines() if l]
    rows = []
    for path in found:
        sibling, restore = BUILD_DIRS[path.name]
        if sibling and not (path.parent / sibling).exists():
            continue
        kb = du_one(path)
        if kb < BUILD_MIN_KB:
            continue
        proj = project_root(path)
        idle = last_activity_days(proj)
        rows.append({"path": str(path), "kb": kb, "project": str(proj), "idle_days": round(idle),
                     "stale": idle >= STALE_PROJECT_DAYS,
                     "remove": f"rm -rf {shlex.quote(str(path))}", "restore": restore})
    rows.sort(key=lambda r: -r["kb"])
    return rows


def scan_installers() -> list[dict]:
    rows = []
    dl = HOME / "Downloads"
    if not dl.exists():
        return rows
    now = dt.datetime.now().timestamp()
    for p in dl.iterdir():
        if p.suffix.lower() not in {".dmg", ".pkg", ".iso"}:
            continue
        try:
            st = p.stat()
        except OSError:
            continue
        age = (now - st.st_mtime) / 86400
        kb = st.st_size // 1024 if p.is_file() else du_one(p)
        if age >= INSTALLER_AGE_DAYS and kb >= 100 * 1024:
            rows.append({"path": str(p), "kb": kb, "age_days": round(age),
                         "remove": trash_cmd(p), "restore": "re-download from the vendor"})
    rows.sort(key=lambda r: -r["kb"])
    return rows


def trash_cmd(path: Path) -> str:
    script = f'tell application "Finder" to delete POSIX file "{path}"'
    return f"osascript -e {shlex.quote(script)}"


def mdls_last_used(path: Path) -> dt.date | None:
    """Spotlight's last-used date; None when indexing is off (it is on this Mac)."""
    out = run(["mdls", "-name", "kMDItemLastUsedDate", str(path)], timeout=30)
    k, sep, v = out.partition("=")
    v = v.strip()
    if not sep or v == "(null)":
        return None
    try:
        return dt.datetime.strptime(v[:19], "%Y-%m-%d %H:%M:%S").date()
    except ValueError:
        return None


def newest_mtime(paths: list[Path], stop_at: float, budget: int = 50000) -> tuple[float, bool]:
    """Newest mtime under paths; stops early once it reaches stop_at.

    Returns (newest, complete). complete is False when the walk ran out of
    budget before finding anything recent, so the answer is unknown."""
    newest, seen = 0.0, 0
    stack = list(paths)
    while stack:
        p = stack.pop()
        try:
            st = p.stat()
        except OSError:
            continue
        newest = max(newest, st.st_mtime)
        if newest >= stop_at:
            return newest, True
        if p.is_dir() and not p.is_symlink():
            try:
                for e in os.scandir(p):
                    seen += 1
                    if seen > budget:
                        return newest, False
                    stack.append(Path(e.path))
            except OSError:
                pass
    return newest, True


def app_data_paths(app: Path, info: dict) -> list[Path]:
    bundle = info.get("CFBundleIdentifier", "")
    names = {app.stem, info.get("CFBundleName", ""), info.get("CFBundleDisplayName", "")} - {""}
    lib = HOME / "Library"
    cands = [lib / "Application Support" / n for n in names] + [lib / "Logs" / n for n in names]
    if bundle:
        cands += [lib / "Containers" / bundle, lib / "Caches" / bundle, lib / "HTTPStorages" / bundle,
                  lib / "WebKit" / bundle, lib / "Application Support" / bundle,
                  lib / "Preferences" / f"{bundle}.plist",
                  lib / "Saved Application State" / f"{bundle}.savedState"]
    return [c for c in dict.fromkeys(cands) if c.exists() and readable(c)]


def app_paths() -> list[Path]:
    paths: list[Path] = []
    for base in (Path("/Applications"), HOME / "Applications"):
        if not base.exists():
            continue
        for p in sorted(base.iterdir()):
            if p.suffix == ".app":
                paths.append(p)
            elif p.is_dir() and p.name != "Utilities":
                paths += sorted(q for q in p.iterdir() if q.suffix == ".app")
    return paths


def scan_apps() -> list[dict]:
    """Size and last activity of every non-Apple app.

    Spotlight is off here, and APFS only bumps a file's access time when the
    file changed since the last access, so the executable's atime is the first
    launch after the last update. Last activity is therefore the newest of:
    Spotlight's date (if indexing is on), that atime, and the newest file the
    app wrote in its own Library folders. Every signal can only understate how
    recently the app ran, never overstate it, except that a background helper
    also counts as use; an app is proposed only when every signal is old."""
    running = run(["ps", "-axo", "comm="])
    cutoff = dt.datetime.now().timestamp() - APP_UNUSED_DAYS * 86400
    rows = []
    for app in app_paths():
        try:
            info = plistlib.loads((app / "Contents/Info.plist").read_bytes())
        except Exception:  # unreadable or malformed Info.plist
            info = {}
        bundle = info.get("CFBundleIdentifier", "")
        if bundle.startswith("com.apple."):
            continue
        data = app_data_paths(app, info)
        stamps = []
        spot = mdls_last_used(app)
        if spot:
            stamps.append(dt.datetime.combine(spot, dt.time()).timestamp())
        exe = app / "Contents/MacOS" / info.get("CFBundleExecutable", app.stem)
        try:
            stamps.append(exe.stat().st_atime)
        except OSError:
            pass
        newest, complete = newest_mtime(data, cutoff)
        if newest:
            stamps.append(newest)
        last_ts = max(stamps) if stamps else 0
        last = dt.date.fromtimestamp(last_ts) if last_ts else None
        is_running = f"{app}/" in running
        basis = "app data" if data else "first launch after update only"
        unused = (not is_running and complete and last is not None
                  and (TODAY - last).days >= APP_UNUSED_DAYS)
        app_kb = du_one(app)
        support = [(c, du_one(c, timeout=CONTAINER_TIMEOUT_S)) for c in data if c.is_dir()]
        support = [(c, kb) for c, kb in support if kb >= 50 * 1024]
        app_store = (app / "Contents/_MASReceipt").exists()
        rows.append({
            "name": app.stem, "path": str(app), "bundle": bundle, "kb": app_kb,
            "last_used": last.isoformat() if last else None,
            "idle_days": (TODAY - last).days if last else None, "basis": basis,
            "running": is_running, "unused": unused,
            "propose": unused and app_kb + sum(kb for _, kb in support) >= APP_PROPOSE_MIN_KB,
            "support_kb": sum(kb for _, kb in support),
            "support_paths": [tilde(str(c)) for c, _ in support],
            "remove": trash_cmd(app),
            "restore": "App Store > Purchased" if app_store else "re-download from the vendor's site",
        })
    rows.sort(key=lambda r: -(r["kb"] + r["support_kb"]))
    return rows


def readable(path: Path) -> bool:
    """False when listing the folder blocks (app-data protection) or fails."""
    if not under(str(path), HOME / "Library/Containers") and not under(str(path), HOME / "Library/Group Containers"):
        return True
    top = Path(*path.parts[: len((HOME / "Library/Containers").parts) + 1])
    if str(top) not in _READABLE:
        try:
            subprocess.run(["ls", str(top / "Data") if (top / "Data").exists() else str(top)],
                           capture_output=True, timeout=10, check=True)
            _READABLE[str(top)] = True
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, OSError):
            _READABLE[str(top)] = False
            SKIPPED.append(tilde(str(top)))
    return _READABLE[str(top)]


_READABLE: dict[str, bool] = {}


def scan_containers() -> dict[str, int]:
    """Size each app container separately so one blocked read can't hang the run."""
    sizes: dict[str, int] = {}

    def measure(child: Path) -> tuple[Path, int | None]:
        if not readable(child):
            return child, None
        out = run(["du", "-sxk", str(child)], timeout=CONTAINER_TIMEOUT_S)
        head = out.split("\t", 1)[0]
        if not head.isdigit():
            SKIPPED.append(tilde(str(child)))
            return child, None
        return child, int(head)

    for name in CONTAINER_DIRS:
        base = HOME / "Library" / name
        if not base.exists():
            continue
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(measure, [c for c in base.iterdir() if c.is_dir()]))
        total = sum(kb for _, kb in results if kb)
        sizes[str(base)] = total
        sizes.update({str(c): kb for c, kb in results if kb})
    return sizes


def scan_home() -> dict[str, int]:
    sizes = du_tree(HOME, 3, ignore=CONTAINER_DIRS)
    containers = scan_containers()
    extra = sum(kb for p, kb in containers.items() if Path(p).parent == HOME / "Library")
    for p in (str(HOME), str(HOME / "Library")):
        sizes[p] = sizes.get(p, 0) + extra
    sizes.update(containers)
    return {p: kb for p, kb in sizes.items() if kb >= MIN_SNAPSHOT_KB}


# ---------------------------------------------------------------- history


def load_snapshots() -> list[dict]:
    snaps = []
    for f in sorted((STATE / "snapshots").glob("*.json")):
        try:
            snaps.append(json.loads(f.read_text()))
        except (OSError, json.JSONDecodeError):
            pass
    return snaps


def find_leaks(cur: dict[str, int], history: list[dict]) -> list[dict]:
    if not history:
        return []
    prev = history[-1]["folders"]
    older = history[-2]["folders"] if len(history) >= 2 else None
    leaks = []
    for path, kb in cur.items():
        if path not in prev:
            continue
        growth = kb - prev[path]
        steady = older is not None and path in older and prev[path] - older[path] >= LEAK_STEADY_KB
        if growth >= LEAK_ONE_RUN_KB or (growth >= LEAK_STEADY_KB and steady):
            leaks.append({"path": path, "kb": kb, "growth_kb": growth, "steady": steady,
                          "class": classify(path)})
    # keep the deepest folder of each growing chain, so ~ and ~/Library don't crowd it out
    leaks.sort(key=lambda l: -l["growth_kb"])
    deepest = [l for l in leaks
               if not any(o is not l and o["path"].startswith(l["path"] + "/")
                          and o["growth_kb"] >= 0.8 * l["growth_kb"] for o in leaks)]
    return deepest[:10]


def temp_group_growth(groups: list[dict], history: list[dict]) -> None:
    prev = {g["pattern"]: g for g in history[-1].get("temp_groups", [])} if history else {}
    for g in groups:
        p = prev.get(g["pattern"])
        g["growth_kb"] = g["kb"] - p["kb"] if p else None
        g["count_growth"] = g["count"] - p["count"] if p else None


# ---------------------------------------------------------------- report


def top_folders(home: dict[str, int]) -> list[tuple[str, int, list[tuple[str, int]]]]:
    """Home children >= 5 GB with their own children >= 2 GB."""
    h = str(HOME)
    depth = lambda p: p[len(h):].count("/")
    tops = sorted(((p, kb) for p, kb in home.items() if depth(p) == 1 and kb >= 5 * GB), key=lambda x: -x[1])
    out = []
    for p, kb in tops:
        kids = sorted(((q, k) for q, k in home.items() if depth(q) == 2 and q.startswith(p + "/") and k >= 2 * GB),
                      key=lambda x: -x[1])
        out.append((p, kb, kids[:6]))
    return out


LABELS = {"regenerable": "regenerable", "temp": "temp, regenerable", "data": "your data, never proposed",
          "unknown": "unknown, look before deleting"}


def render(r: dict) -> str:
    L: list[str] = []
    free, total = r["free"]["free_kb"], r["free"]["total_kb"]
    L.append(f"# Disk review, {r['date']}\n")
    line = f"**Free:** {gb(free)} of {gb(total)} ({free / total:.0%})"
    if r.get("prev_date"):
        d = free - r["prev_free_kb"]
        line += f"; {'+' if d >= 0 else '−'}{gb(abs(d))} since {r['prev_date']}"
    else:
        line += "; first run, no baseline yet"
    L.append(line + "\n")
    L.append(f"**Proposed total:** {gb(r['proposed_kb'])} you could free with the commands below. "
             "Nothing was deleted; every command is yours to run.\n")

    L.append("## Largest folders\n")
    for p, kb, kids in r["top_folders"]:
        L.append(f"- `{tilde(p)}` {gb(kb)} ({LABELS[classify(p)]})")
        for q, k in kids:
            L.append(f"  - `{tilde(q)}` {gb(k)} ({LABELS[classify(q)]})")
    temp_total = sum(v for k, v in r["temp_roots"].items() if k != "tmp" and Path(k).name in {"T", "C"})
    L.append(f"- temp + per-user cache folder (`/var/folders/...` T and C) {gb(temp_total)} (temp, regenerable)\n")

    L.append("## Leaks (folders that keep growing)\n")
    if not r["history_runs"]:
        L.append("No baseline yet; growth shows from the next run.\n")
    elif not r["leaks"]:
        L.append("None: nothing grew past the thresholds since the last run.\n")
    for l in r["leaks"]:
        L.append(f"- `{tilde(l['path'])}` now {gb(l['kb'])}, +{gb(l['growth_kb'])} since last run"
                 f"{' (grew in each of the last runs)' if l['steady'] else ''} ({LABELS[l['class']]})")
    for g in r["temp_groups"]:
        made = f"; created by `{tilde(g['creator'][0])}`" if g["creator"] else "; creator not found in code"
        grew = (f", +{g['count_growth']} folders / +{gb(g['growth_kb'])} since last run"
                if g.get("count_growth") is not None else "")
        L.append(f"- temp `{g['pattern']}`: {g['count']} folders, {gb(g['kb'])}{grew}{made}")
    rest = r["temp_rest"]
    L.append(f"- plus {rest['patterns']} smaller temp patterns: {rest['count']} folders, {gb(rest['kb'])} in total "
             "(test runs that leave folders behind; harmless in size)")
    L.append("")

    L.append("## Proposals\n")
    L.append("Each item: what, size, remove command, how to get it back.\n")
    n = 0
    for g in r["temp_groups"]:
        if g["old_kb"] < TEMP_GROUP_MIN_KB:
            continue
        n += 1
        made = f" Created by `{tilde(g['creator'][0])}`; fix the cleanup there or it comes back." if g["creator"] else ""
        L.append(f"{n}. **Temp `{g['pattern']}`** ({g['count']} folders, {gb(g['old_kb'])} older than a day).{made}\n"
                 f"   - Remove: `{g['remove']}`\n   - Get back: {g['restore']}")
    for c in r["caches"]:
        if c["keep"] or c["kb"] < CACHE_PROPOSE_MIN_KB:
            continue
        n += 1
        L.append(f"{n}. **{c['label']}** `{tilde(c['path'])}` {gb(c['kb'])}\n"
                 f"   - Remove: `{c['remove']}`\n   - Get back: {c['restore']}")
    stale = [b for b in r["builds"] if b["stale"]]
    for b in stale[:12]:
        n += 1
        L.append(f"{n}. **Build output** `{tilde(b['path'])}` {gb(b['kb'])} (project idle {b['idle_days']} days)\n"
                 f"   - Remove: `{b['remove']}`\n   - Get back: {b['restore']}")
    for i in r["installers"]:
        n += 1
        L.append(f"{n}. **Old installer** `{tilde(i['path'])}` {gb(i['kb'])} ({i['age_days']} days old)\n"
                 f"   - Remove (to Trash): `{i['remove']}`\n   - Get back: {i['restore']}")
    for a in [a for a in r["apps"] if a["propose"]]:
        n += 1
        when = f"last activity {a['last_used']}" + (" (weak signal: no app data, first launch after update only)"
                                                   if a["basis"] != "app data" else "")
        extra = (f"; its data {gb(a['support_kb'])} in {', '.join(f'`{p}`' for p in a['support_paths'])} "
                 "stays unless you remove it too") if a["support_kb"] else ""
        L.append(f"{n}. **App {a['name']}** {gb(a['kb'])}, {when}{extra}\n"
                 f"   - Remove (to Trash): `{a['remove']}`\n   - Get back: {a['restore']}")
    if not n:
        L.append("Nothing to propose this week.")
    L.append("")

    kept = [c for c in r["caches"] if c["keep"]]
    active = [b for b in r["builds"] if not b["stale"]]
    if kept or active:
        L.append("## Regenerable but in use (not proposed)\n")
        for c in kept:
            L.append(f"- {c['label']} `{tilde(c['path'])}` {gb(c['kb'])}; to prune: `{c['remove']}`")
        if active:
            L.append(f"- {len(active)} build folders in projects active in the last {STALE_PROJECT_DAYS} days, "
                     f"{gb(sum(b['kb'] for b in active))} total; largest `{tilde(active[0]['path'])}` {gb(active[0]['kb'])}")
        L.append("")

    L.append("## Apps\n")
    L.append(f"{len(r['apps'])} non-Apple apps, {gb(sum(a['kb'] for a in r['apps']))}. "
             f"Unused = no activity in {APP_UNUSED_DAYS}+ days. Spotlight indexing is off on this Mac, so "
             "`kMDItemLastUsedDate` is empty; last activity is the newest of the app's own Library files "
             "(prefs, saved state, support folders) and its first launch after the last update. "
             "These can only understate recent use, so check before trashing an app you open rarely.\n")
    L.append("| App | Size | Data | Last activity | |")
    L.append("| --- | ---: | ---: | --- | --- |")
    for a in r["apps"]:
        flag = "running" if a["running"] else ("**unused**" if a["unused"] else "")
        L.append(f"| {a['name']} | {gb(a['kb'])} | {gb(a['support_kb']) if a['support_kb'] else ''} | "
                 f"{a['last_used'] or 'unknown'} | {flag} |")
    L.append("")
    if r["skipped"]:
        named = [s for s in r["skipped"] if "com.apple." not in s]
        L.append(f"Skipped {len(r['skipped'])} app containers that macOS app-data protection blocks or denies "
                 f"(sizes not counted; mostly Apple's own)"
                 + (f", including {', '.join(f'`{s}`' for s in named[:8])}" if named else "") + ".\n")
    L.append(f"Scan: home to depth 3 (one filesystem), `/var/folders` temp + cache, {len(RULES)} known cache "
             f"locations, project build folders to depth 7, `~/Downloads` installers, `/Applications`. "
             f"Kenji's own data ({', '.join(DATA_ROOTS[:6])}, project and recording folders) is never proposed. "
             "Deletions by this job: none.")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-save", action="store_true", help="print the report, save nothing")
    args = ap.parse_args()

    history = load_snapshots()
    history = [h for h in history if h.get("date") != TODAY.isoformat()]
    started = dt.datetime.now()

    timings: dict[str, int] = {}

    def timed(name, fn):
        t = dt.datetime.now()
        out = fn()
        timings[name] = round((dt.datetime.now() - t).total_seconds())
        return out

    free = free_space()
    home = timed("home", scan_home)
    temp_roots, temp_groups, temp_rest = timed("temp", scan_temp)
    for p, kb in temp_roots.items():
        if p != "tmp" and kb >= MIN_SNAPSHOT_KB:
            home[p] = kb
    caches = timed("caches", scan_rules)
    for c in caches:
        home[c["path"]] = c["kb"]
    builds = timed("builds", scan_build_outputs)
    installers = timed("installers", scan_installers)
    apps = timed("apps", scan_apps)
    temp_group_growth(temp_groups, history)
    leaks = find_leaks(home, history)

    proposed = (sum(g["old_kb"] for g in temp_groups if g["old_kb"] >= TEMP_GROUP_MIN_KB)
                + sum(c["kb"] for c in caches if not c["keep"] and c["kb"] >= CACHE_PROPOSE_MIN_KB)
                + sum(b["kb"] for b in [b for b in builds if b["stale"]][:12])
                + sum(i["kb"] for i in installers)
                + sum(a["kb"] for a in apps if a["propose"]))

    prev = history[-1] if history else None
    report = {
        "date": TODAY.isoformat(), "free": free,
        "prev_date": prev["date"] if prev else None, "prev_free_kb": prev["free"]["free_kb"] if prev else None,
        "history_runs": len(history), "top_folders": top_folders(home), "temp_roots": temp_roots,
        "temp_groups": temp_groups, "temp_rest": temp_rest, "caches": caches, "builds": builds, "installers": installers,
        "apps": apps, "leaks": leaks, "proposed_kb": proposed,
        "skipped": sorted(set(SKIPPED)),
    }
    md = render(report)
    elapsed = round((dt.datetime.now() - started).total_seconds())

    report_path = None
    if not args.no_save:
        (STATE / "snapshots").mkdir(parents=True, exist_ok=True)
        (STATE / "reports").mkdir(parents=True, exist_ok=True)
        snap = {"date": TODAY.isoformat(), "free": free, "folders": home,
                "temp_groups": [{k: g[k] for k in ("pattern", "count", "kb")} for g in temp_groups],
                "apps": {a["name"]: {"kb": a["kb"], "last_used": a["last_used"]} for a in apps}}
        (STATE / "snapshots" / f"{TODAY.isoformat()}.json").write_text(json.dumps(snap))
        report_path = STATE / "reports" / f"{TODAY.isoformat()}.md"
        report_path.write_text(md)
    else:
        print(md)

    summary = {
        "date": TODAY.isoformat(), "report": str(report_path) if report_path else None,
        "free_gb": round(free["free_kb"] / GB, 1), "total_gb": round(free["total_kb"] / GB, 1),
        "free_change_gb": round((free["free_kb"] - prev["free"]["free_kb"]) / GB, 1) if prev else None,
        "since": prev["date"] if prev else None, "proposed_gb": round(proposed / GB, 1),
        "top_proposals": sorted(
            [{"what": f"temp {g['pattern']}", "gb": round(g["old_kb"] / GB, 1), "remove": g["remove"]}
             for g in temp_groups if g["old_kb"] >= TEMP_GROUP_MIN_KB]
            + [{"what": c["label"], "gb": round(c["kb"] / GB, 1), "remove": c["remove"]} for c in caches
               if not c["keep"] and c["kb"] >= CACHE_PROPOSE_MIN_KB]
            + [{"what": f"app {a['name']}", "gb": round(a["kb"] / GB, 1), "remove": a["remove"]} for a in apps if a["propose"]]
            + [{"what": f"build {tilde(b['path'])}", "gb": round(b["kb"] / GB, 1), "remove": b["remove"]}
               for b in builds if b["stale"]][:12],
            key=lambda x: -x["gb"])[:5],
        "unused_apps": [a["name"] for a in apps if a["propose"]],
        "unused_small_apps": sum(1 for a in apps if a["unused"] and not a["propose"]),
        "leaks": [{"path": tilde(l["path"]), "growth_gb": round(l["growth_kb"] / GB, 1)} for l in leaks]
                 + [{"temp": g["pattern"], "count": g["count"], "gb": round(g["kb"] / GB, 1),
                     "growth_gb": round(g["growth_kb"] / GB, 1) if g.get("growth_kb") is not None else None,
                     "creator": tilde(g["creator"][0]) if g["creator"] else None}
                    for g in temp_groups],
        "skipped_containers": len(set(SKIPPED)), "first_run": not history, "scan_seconds": elapsed, "stage_seconds": timings, "deletions": "none",
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
