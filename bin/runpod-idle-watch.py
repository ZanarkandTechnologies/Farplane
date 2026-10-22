#!/usr/bin/env python3
"""Stop idle RunPod pods and flag storage that bills while nothing runs.

Run by the runpod-idle-watch scheduled task twice a day (09:00 and 21:00). Prints one JSON
summary; `notify` is true when Kenji should hear about it.

  runpod-idle-watch.py            check, stop idle pods, print summary
  runpod-idle-watch.py --dry-run  same, but stop nothing and save no state
  runpod-idle-watch.py keep <pod-id> [hours]   protect a pod (default 3 h),
                                  e.g. while pulling results off it
  runpod-idle-watch.py guard [--max-hours H]   run ON a pod: stop this pod
                                  after 20 min of idle GPU or H hours, so a
                                  sleeping Mac never leaves it billing. Start
                                  it at launch, before the job:
                                  nohup python3 runpod-idle-watch.py guard \
                                    --max-hours 6 > /workspace/guard.log 2>&1 &
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import tomllib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / ".farplane" / "runpod-idle-watch" / "state.json"

IDLE_GPU_PERCENT = 5          # below this on every GPU counts as idle
IDLE_SAMPLES_TO_STOP = 2      # consecutive idle checks before stopping
MIN_UPTIME_S = 20 * 60        # never stop a pod that just booted
INIT_STUCK_S = 25 * 60        # running but no container reported (image pull hang)
CPU_POD_FLAG_S = 6 * 3600     # CPU pods have no GPU signal: flag only
LOW_BALANCE_USD = 5
POD_DISK_USD_GB_MONTH = 0.20  # stopped-pod volume disk
NETWORK_VOLUME_USD_GB_MONTH = 0.07

QUERY = """query{myself{clientBalance currentSpendPerHr
 pods{id name desiredStatus costPerHr gpuCount volumeInGb lastStatusChange
  runtime{uptimeInSeconds gpus{gpuUtilPercent}}}
 networkVolumes{id name size dataCenterId}}}"""


def api_key() -> str:
    if os.environ.get("RUNPOD_API_KEY"):
        return os.environ["RUNPOD_API_KEY"]
    cfg = tomllib.loads((Path.home() / ".runpod" / "config.toml").read_text())
    return cfg["apikey"]


def fetch_account() -> dict:
    req = urllib.request.Request(
        "https://api.runpod.io/graphql",
        data=json.dumps({"query": QUERY}).encode(),
        headers={"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)
    if "data" not in body or not body["data"].get("myself"):
        raise RuntimeError(f"RunPod API error: {body.get('errors') or body.get('error')}")
    return body["data"]["myself"]


def load_state() -> dict:
    try:
        return json.loads(STATE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def stop_pod(pod_id: str) -> str:
    run = subprocess.run(["runpodctl", "pod", "stop", pod_id], capture_output=True, text=True)
    return "stopped" if run.returncode == 0 else f"stop failed: {(run.stderr or run.stdout).strip()[:200]}"


def check(account: dict, state: dict, now: float, act: bool) -> tuple[dict, dict]:
    keep = {k: v for k, v in state.get("keep", {}).items() if v > now}
    idle = state.get("idle", {})
    init_seen = state.get("init_seen", {})
    today = time.strftime("%Y-%m-%d", time.localtime(now))
    out = {"balance_usd": round(account["clientBalance"], 2),
           "spend_per_hr_usd": account["currentSpendPerHr"],
           "running": [], "stopped": [], "warnings": [], "daily": []}
    next_idle, next_init = {}, {}

    for pod in account["pods"]:
        if pod["desiredStatus"] != "RUNNING":
            if pod["volumeInGb"]:
                usd = pod["volumeInGb"] * POD_DISK_USD_GB_MONTH / 30
                out["daily"].append(f"stopped pod {pod['name']} ({pod['id']}) holds {pod['volumeInGb']} GB disk, ${usd:.2f}/day")
            continue
        pid, name, rt = pod["id"], pod["name"], pod["runtime"]
        label = f"{name} ({pid}, ${pod['costPerHr']}/h)"
        uptime = (rt or {}).get("uptimeInSeconds") or 0
        gpus = (rt or {}).get("gpus") or []
        util = max((g.get("gpuUtilPercent") or 0 for g in gpus), default=None)
        entry = {"id": pid, "name": name, "usd_per_hr": pod["costPerHr"],
                 "uptime_min": uptime // 60, "gpu_util": util}
        out["running"].append(entry)
        if pid in keep:
            entry["kept_until"] = time.strftime("%H:%M", time.localtime(keep[pid]))
            continue

        reason = None
        if rt is None:
            first = init_seen.get(pid, now)
            next_init[pid] = first
            if now - first >= INIT_STUCK_S:
                reason = f"no container after {int((now - first) // 60)} min (stuck image pull or boot)"
        elif not pod["gpuCount"]:
            if uptime >= CPU_POD_FLAG_S:
                out["warnings"].append(f"CPU pod {label} up {uptime // 3600} h; no GPU signal, not stopped")
        elif util is not None and util < IDLE_GPU_PERCENT and uptime >= MIN_UPTIME_S:
            streak = idle.get(pid, 0) + 1
            next_idle[pid] = streak
            if streak >= IDLE_SAMPLES_TO_STOP:
                reason = f"GPU under {IDLE_GPU_PERCENT}% for {streak} checks in a row"
            else:
                out["warnings"].append(
                    f"{label} GPU idle ({util}%); stops at the next check unless kept: "
                    f"bin/runpod-idle-watch.py keep {pid} 3")
        if reason:
            result = stop_pod(pid) if act else "dry run, not stopped"
            out["stopped"].append({"id": pid, "name": name, "usd_per_hr": pod["costPerHr"],
                                   "reason": reason, "result": result})
            next_idle.pop(pid, None)
            next_init.pop(pid, None)

    for vol in account["networkVolumes"]:
        usd = vol["size"] * NETWORK_VOLUME_USD_GB_MONTH / 30
        out["daily"].append(f"network volume {vol['name']} ({vol['id']}, {vol['dataCenterId']}) {vol['size']} GB, ${usd:.2f}/day")
    if account["clientBalance"] < LOW_BALANCE_USD:
        out["daily"].append(f"balance ${account['clientBalance']:.2f} (pods are terminated at zero)")

    daily_due = bool(out["daily"]) and state.get("daily_sent") != today
    if not daily_due:
        out["daily"] = []
    out["notify"] = bool(out["stopped"] or out["warnings"] or out["daily"])
    new_state = {"keep": keep, "idle": next_idle, "init_seen": next_init,
                 "daily_sent": today if daily_due else state.get("daily_sent"),
                 "last_run": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(now))}
    return out, new_state


GUARD_IDLE_S = 20 * 60       # on-pod guard: continuous idle GPU before self-stop
GUARD_SAMPLE_S = 60


def gpu_util() -> int | None:
    try:
        run = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True)
    except FileNotFoundError:  # CPU pod: only the hour limit applies
        return None
    values = [int(v) for v in run.stdout.split() if v.strip().isdigit()]
    return max(values) if run.returncode == 0 and values else None


def guard_reason(started: float, idle_since: float | None, now: float, max_hours: float) -> str | None:
    if max_hours and now - started >= max_hours * 3600:
        return f"reached the {max_hours:g} h limit"
    if idle_since is not None and now - started >= MIN_UPTIME_S and now - idle_since >= GUARD_IDLE_S:
        return f"GPU under {IDLE_GPU_PERCENT}% for {int((now - idle_since) // 60)} min"
    return None


def stop_self() -> str:
    pod_id = os.environ["RUNPOD_POD_ID"]
    mutation = 'mutation{podStop(input:{podId:"%s"}){id desiredStatus}}' % pod_id
    req = urllib.request.Request(
        "https://api.runpod.io/graphql", data=json.dumps({"query": mutation}).encode(),
        headers={"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.dumps(json.load(resp))


def guard(max_hours: float) -> int:
    started, idle_since = time.time(), None
    print(f"guard on {os.environ.get('RUNPOD_POD_ID')}: idle {GUARD_IDLE_S // 60} min or {max_hours:g} h", flush=True)
    while True:
        now, util = time.time(), gpu_util()
        idle = util is not None and util < IDLE_GPU_PERCENT
        idle_since = (idle_since or now) if idle else None
        reason = guard_reason(started, idle_since, now, max_hours)
        if reason:
            print(f"{time.strftime('%H:%M:%S')} stopping: {reason}", flush=True)
            print(stop_self(), flush=True)
            return 0
        time.sleep(GUARD_SAMPLE_S)


def save_state(state: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", choices=["check", "keep", "guard"], default="check")
    parser.add_argument("pod_id", nargs="?")
    parser.add_argument("hours", nargs="?", type=float, default=3.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-hours", type=float, default=6.0, help="guard: hard stop after this long (0 = none)")
    args = parser.parse_args()
    if args.command == "guard":
        return guard(args.max_hours)
    state, now = load_state(), time.time()

    if args.command == "keep":
        if not args.pod_id:
            parser.error("keep needs a pod id")
        state.setdefault("keep", {})[args.pod_id] = now + args.hours * 3600
        save_state(state)
        print(json.dumps({"kept": args.pod_id, "hours": args.hours}))
        return 0

    out, new_state = check(fetch_account(), state, now, act=not args.dry_run)
    if not args.dry_run:
        save_state(new_state)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
