#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(python3 - <<'PY' "${BASH_SOURCE[0]}"
import os, sys
print(os.path.realpath(sys.argv[1]))
PY
)"
ROOT="$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: bin/ralph_worker.sh --ticket PATH --phase PHASE [--run-state PATH] [--executor-target NAME] [--dry-run]

Launch one bounded Ralph phase worker through `codex exec` using the tracked prompt files.

If `--ticket` is omitted, the worker tries `.ralph/state/current-run.json`.

Phases:
  planning
  building
  documenting
EOF
}

die() {
  printf 'ralph_worker: %s\n' "$*" >&2
  exit 1
}

state_json_path() {
  printf '%s\n' "$ROOT/.ralph/state/current-run.json"
}

state_json_value() {
  local key="$1"
  local path
  path="$(state_json_path)"
  [[ -f "$path" ]] || return 1
  python3 - "$path" "$key" <<'PY'
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
key = sys.argv[2]
try:
    data = json.loads(path.read_text(encoding="utf-8"))
except Exception:
    raise SystemExit(1)
value = data.get(key)
if not isinstance(value, str) or not value.strip():
    raise SystemExit(1)
print(value)
PY
}

resolve_prompt() {
  case "$1" in
    planning) printf '%s\n' "$ROOT/prompts/ralphplan.md" ;;
    building) printf '%s\n' "$ROOT/prompts/ralph.md" ;;
    documenting) printf '%s\n' "$ROOT/prompts/ralph-docs.md" ;;
    *) return 1 ;;
  esac
}

PHASE=""
TICKET=""
RUN_STATE=""
EXECUTOR_TARGET=""
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ticket)
      [[ $# -ge 2 ]] || die "--ticket requires a value"
      TICKET="$2"
      shift 2
      ;;
    --phase)
      [[ $# -ge 2 ]] || die "--phase requires a value"
      PHASE="$2"
      shift 2
      ;;
    --run-state)
      [[ $# -ge 2 ]] || die "--run-state requires a value"
      RUN_STATE="$2"
      shift 2
      ;;
    --executor-target)
      [[ $# -ge 2 ]] || die "--executor-target requires a value"
      EXECUTOR_TARGET="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown arg '$1'"
      ;;
  esac
done

if [[ -z "$PHASE" ]]; then
  PHASE="$(state_json_value phase || true)"
fi
[[ -n "$PHASE" ]] || die "missing --phase"

if [[ -z "$TICKET" ]]; then
  TICKET="$(state_json_value ticket_path || true)"
fi
[[ -n "$TICKET" ]] || die "missing --ticket and no current-run ticket_path found"

PROMPT_FILE="$(resolve_prompt "$PHASE")" || die "unsupported phase '$PHASE'"
[[ -f "$PROMPT_FILE" ]] || die "prompt file not found: $PROMPT_FILE"

if [[ "$TICKET" != /* ]]; then
  if [[ -f "$TICKET" ]]; then
    TICKET="$(cd "$(dirname "$TICKET")" && pwd)/$(basename "$TICKET")"
  else
    TICKET="$ROOT/$TICKET"
  fi
fi
[[ -f "$TICKET" ]] || die "ticket not found: $TICKET"

if [[ -n "$RUN_STATE" && "$RUN_STATE" != /* ]]; then
  if [[ -e "$RUN_STATE" ]]; then
    RUN_STATE="$(cd "$(dirname "$RUN_STATE")" && pwd)/$(basename "$RUN_STATE")"
  else
    RUN_STATE="$ROOT/$RUN_STATE"
  fi
fi

if [[ -z "$RUN_STATE" ]]; then
  RUN_STATE="$(state_json_path)"
fi

if [[ "$DRY_RUN" -eq 1 ]]; then
  printf 'phase=%s\n' "$PHASE"
  printf 'ticket=%s\n' "$TICKET"
  printf 'prompt=%s\n' "$PROMPT_FILE"
  [[ -n "$RUN_STATE" ]] && printf 'run_state=%s\n' "$RUN_STATE"
  [[ -n "$EXECUTOR_TARGET" ]] && printf 'executor_target=%s\n' "$EXECUTOR_TARGET"
  printf 'command=codex exec --skip-git-repo-check -C %s - < %s\n' "$ROOT" "$PROMPT_FILE"
  exit 0
fi

export RALPH_TICKET="$TICKET"
[[ -n "$RUN_STATE" ]] && export RALPH_RUN_STATE="$RUN_STATE"
[[ -n "$EXECUTOR_TARGET" ]] && export RALPH_EXECUTOR_TARGET="$EXECUTOR_TARGET"

exec codex exec --skip-git-repo-check -C "$ROOT" - < "$PROMPT_FILE"
