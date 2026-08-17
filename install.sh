#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$HOME/.codex"
TARGET_DIR_SET=0
SKILLS_ONLY=0
SKILL_INSTALL_ARGS=()

usage() {
  cat <<'EOF'
Usage:
  bash install.sh [TARGET_DIR]
  bash install.sh --skills-only --list-skills [--target TARGET_DIR]
  bash install.sh --skills-only --search QUERY [--target TARGET_DIR]
  bash install.sh --skills-only --skills skill-a,skill-b [--target TARGET_DIR]

Full install installs the Farplane harness, renders skills, and renders config.toml.
Skills-only mode renders selected skills without rendering config.toml.

Options:
  --target DIR          Codex home target. Defaults to ~/.codex.
  --skills-only         Use selected skill installer mode.
  --list-skills         List available skills.
  --search QUERY        Search skill names and descriptions.
  --search-skills QUERY Alias for --search.
  --skills NAMES        Comma-separated skill names to install.
  --skill NAME          Skill name to install; can be repeated.
  --prune-skills        Remove unselected symlinks managed by this repo.
  --dry-run             Preview selected skill install changes.
  --json                Print selected skill output as JSON.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --help|-h)
      usage
      exit 0
      ;;
    --target)
      if [ "$#" -lt 2 ]; then
        echo "--target requires a directory" >&2
        exit 2
      fi
      TARGET_DIR="$2"
      TARGET_DIR_SET=1
      shift 2
      ;;
    --skills-only)
      SKILLS_ONLY=1
      shift
      ;;
    --list-skills)
      SKILLS_ONLY=1
      SKILL_INSTALL_ARGS+=("--list")
      shift
      ;;
    --search|--search-skills)
      if [ "$#" -lt 2 ]; then
        echo "$1 requires a query" >&2
        exit 2
      fi
      SKILLS_ONLY=1
      SKILL_INSTALL_ARGS+=("--search" "$2")
      shift 2
      ;;
    --skills)
      if [ "$#" -lt 2 ]; then
        echo "--skills requires a comma-separated list" >&2
        exit 2
      fi
      SKILLS_ONLY=1
      SKILL_INSTALL_ARGS+=("--skills" "$2")
      shift 2
      ;;
    --skill)
      if [ "$#" -lt 2 ]; then
        echo "--skill requires a skill name" >&2
        exit 2
      fi
      SKILLS_ONLY=1
      SKILL_INSTALL_ARGS+=("--skill" "$2")
      shift 2
      ;;
    --prune-skills)
      SKILLS_ONLY=1
      SKILL_INSTALL_ARGS+=("--prune")
      shift
      ;;
    --dry-run|--json)
      SKILLS_ONLY=1
      SKILL_INSTALL_ARGS+=("$1")
      shift
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [ "$TARGET_DIR_SET" -eq 1 ]; then
        echo "Only one target directory can be provided" >&2
        exit 2
      fi
      TARGET_DIR="$1"
      TARGET_DIR_SET=1
      shift
      ;;
  esac
done

# Global Codex links must never point into an ephemeral linked worktree. A task
# may test there, but only the primary checkout owns ~/.codex installation.
if command -v git >/dev/null 2>&1; then
  CURRENT_GIT_DIR="$(git -C "$REPO_DIR" rev-parse --path-format=absolute --git-dir 2>/dev/null || true)"
  COMMON_GIT_DIR="$(git -C "$REPO_DIR" rev-parse --path-format=absolute --git-common-dir 2>/dev/null || true)"
  if [ -n "$CURRENT_GIT_DIR" ] && [ -n "$COMMON_GIT_DIR" ] && [ "$CURRENT_GIT_DIR" != "$COMMON_GIT_DIR" ]; then
    echo "Install blocked: global Codex installation must come from the primary Farplane checkout, not linked worktree $REPO_DIR" >&2
    exit 2
  fi
fi

STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_ROOT="${TARGET_DIR}/.install-backups/${STAMP}"
LOCAL_TOML_FILE="${TARGET_DIR}/config.local.toml"
LOCAL_TOML_MARKER="# Machine-local config appended from config.local.toml"
INSTALL_BIN_FILES=(
  _compat.py
  capture_user_turn.py
  farplane
  farplane.py
  notify.py
)
INSTALL_HOOK_FILES=(
  final_response_gate.py
  farplane_console_ping.py
  skill_file_line_gate.py
  shared_checkout_guard.py
)
RETIRED_INSTALL_PATHS=(
  bin/ticket_runtime.py
  bin/ticket-runtime
  bin/farplane_boards.py
  bin/farplane_compute.py
  bin/farplane_invocation.py
  bin/runtime_telemetry.py
  bin/user_turn.py
  skills/pr-runtime
  skills/farplane-invocation
  bin/file_growth_hook.py
  hooks/farplane_file_change.py
  hooks/farplane_local_event.py
)

if [ "$SKILLS_ONLY" -eq 1 ]; then
  if [ "${#SKILL_INSTALL_ARGS[@]}" -eq 0 ]; then
    SKILL_INSTALL_ARGS+=("--list")
  fi
  python3 "$REPO_DIR/skills/skill-maintenance/scripts/install_selected_skills.py" \
    --repo "$REPO_DIR" \
    --target "$TARGET_DIR" \
    "${SKILL_INSTALL_ARGS[@]}"
  exit 0
fi

render_config() {
  if [ -e "$TARGET_DIR/config.toml" ]; then
    python3 - "$TARGET_DIR/config.toml" "$LOCAL_TOML_FILE" "$LOCAL_TOML_MARKER" <<'PY'
from pathlib import Path
import re
import sys

config_path = Path(sys.argv[1])
local_path = Path(sys.argv[2])
marker = sys.argv[3]

text = config_path.read_text()
local_text = local_path.read_text() if local_path.exists() else ""

if marker in text:
    candidate_text = text.split(marker, 1)[1]
else:
    candidate_text = text

header_re = re.compile(r"^\[([^\]]+)\]\s*$")
preserve_exact = {"hooks.state"}
preserve_prefixes = ("projects.", "hooks.state.", "marketplaces.")


def table_blocks(source: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    current_header: str | None = None
    current_lines: list[str] = []
    for line in source.splitlines():
        match = header_re.match(line)
        if match:
            if current_header is not None:
                blocks.append((current_header, "\n".join(current_lines).rstrip() + "\n"))
            current_header = match.group(1)
            current_lines = [line]
        elif current_header is not None:
            current_lines.append(line)
    if current_header is not None:
        blocks.append((current_header, "\n".join(current_lines).rstrip() + "\n"))
    return blocks


def should_preserve(header: str) -> bool:
    return header in preserve_exact or header.startswith(preserve_prefixes)


local_headers = {header for header, _block in table_blocks(local_text)}
missing_blocks = [
    block
    for header, block in table_blocks(candidate_text)
    if should_preserve(header) and header not in local_headers
]

if missing_blocks:
    prefix = local_text.rstrip()
    if prefix:
        prefix += "\n\n"
    else:
        prefix = "# Machine-local TOML appended after the managed template.\n\n"
    local_path.write_text(prefix + "\n".join(missing_blocks).rstrip() + "\n")
    print(f"Preserved {len(missing_blocks)} machine-local TOML table(s) in {local_path}")
PY
  fi

  if [ -e "$TARGET_DIR/config.toml" ]; then
    mkdir -p "$BACKUP_ROOT"
    cp "$TARGET_DIR/config.toml" "$BACKUP_ROOT/config.toml"
  fi

  python3 - "$REPO_DIR/config.toml.example" "$TARGET_DIR/config.toml" "$LOCAL_TOML_FILE" "$TARGET_DIR" <<'PY'
from pathlib import Path
import os
import re
import sys

template_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
local_toml_path = Path(sys.argv[3])
target_dir = sys.argv[4]
repo_dir = template_path.parent
core_dir = repo_dir / "bin" / "core"
if str(core_dir) not in sys.path:
    sys.path.insert(0, str(core_dir))

from runtime_config import load_runtime_env

env = load_runtime_env({"CODEX_HOME": target_dir, **os.environ})

required = ["CODEX_HOME", "REF_API_KEY", "NOTION_TOKEN"]
missing = [key for key in required if not env.get(key) or env[key].startswith("YOUR_") or env[key].startswith("__")]
if missing:
    raise SystemExit(
        "Missing required runtime values. Run through a secret injector such as "
        "`doppler run -- farplane install`, export env vars for this run, or "
        "use private ~/.farplane/config.toml as a fallback/cache: "
        + ", ".join(missing)
    )

text = template_path.read_text()
replacements = {
    "__CODEX_HOME__": env["CODEX_HOME"],
    "__REF_API_KEY__": env["REF_API_KEY"],
    "__NOTION_TOKEN__": env["NOTION_TOKEN"],
    "__FARPLANE_CONVEX_SITE_URL__": env.get("FARPLANE_CONVEX_SITE_URL", ""),
    "__FARPLANE_TELEMETRY_TOKEN__": env.get("FARPLANE_TELEMETRY_TOKEN", ""),
    "__FARPLANE_CONSOLE_KEY__": env.get("FARPLANE_CONSOLE_KEY", ""),
    "__LIVEKIT_URL__": env.get("LIVEKIT_URL", ""),
    "__LIVEKIT_API_KEY__": env.get("LIVEKIT_API_KEY", ""),
    "__LIVEKIT_API_SECRET__": env.get("LIVEKIT_API_SECRET", ""),
    "__LIVEKIT_PHONE_NUMBER__": env.get("LIVEKIT_PHONE_NUMBER", ""),
    "__LIVEKIT_PHONE_NUMBER_ID__": env.get("LIVEKIT_PHONE_NUMBER_ID", ""),
    "__LIVEKIT_SIP_DISPATCH_RULE_ID__": env.get("LIVEKIT_SIP_DISPATCH_RULE_ID", ""),
    "__LIVEKIT_SIP_TRUNK_ID__": env.get("LIVEKIT_SIP_TRUNK_ID", ""),
    "__LIVEKIT_SIP_NUMBER__": env.get("LIVEKIT_SIP_NUMBER", ""),
    "__LIVEKIT_SIP_OUTBOUND_ADDRESS__": env.get("LIVEKIT_SIP_OUTBOUND_ADDRESS", ""),
    "__LIVEKIT_SIP_AUTH_USERNAME__": env.get("LIVEKIT_SIP_AUTH_USERNAME", ""),
    "__LIVEKIT_SIP_AUTH_PASSWORD__": env.get("LIVEKIT_SIP_AUTH_PASSWORD", ""),
    "__TELNYX_API_KEY__": env.get("TELNYX_API_KEY", ""),
    "__FISH_API_KEY__": env.get("FISH_API_KEY", ""),
    "__FISH_AUDIO_REFERENCE_ID__": env.get("FISH_AUDIO_REFERENCE_ID", ""),
    "__FISH_AUDIO_MODEL__": env.get("FISH_AUDIO_MODEL", ""),
    "__FISH_AUDIO_LATENCY_MODE__": env.get("FISH_AUDIO_LATENCY_MODE", ""),
    "__FARPLANE_REMINDER_PHONE__": env.get("FARPLANE_REMINDER_PHONE", ""),
    "__FARPLANE_PHONE_REMINDER_AGENT_NAME__": env.get("FARPLANE_PHONE_REMINDER_AGENT_NAME", ""),
}
for needle, value in replacements.items():
    text = text.replace(needle, value)

marker = "# Machine-local config appended from config.local.toml"

if local_toml_path.exists():
    local_text = local_toml_path.read_text().strip()
    if local_text:
        text = text.rstrip() + "\n\n" + marker + "\n\n" + local_text + "\n"
else:
    text = text.rstrip() + "\n"

output_path.write_text(text)
PY

  echo "Rendered $TARGET_DIR/config.toml from config.toml.example"
  if [ -e "$LOCAL_TOML_FILE" ]; then
    echo "Appended machine-local TOML from $LOCAL_TOML_FILE"
  fi
}

link_path() {
  local src="$1"
  local dest="$2"
  local relative
  local backup_dest

  mkdir -p "$(dirname "$dest")"

  if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$src" ]; then
    return 0
  fi

  if [ -e "$dest" ] || [ -L "$dest" ]; then
    relative="${dest#${TARGET_DIR}/}"
    backup_dest="${BACKUP_ROOT}/${relative}"
    mkdir -p "$(dirname "$backup_dest")"
    mv "$dest" "$backup_dest"
  fi

  ln -s "$src" "$dest"
}

copy_path() {
  local src="$1"
  local dest="$2"
  local relative
  local backup_dest

  mkdir -p "$(dirname "$dest")"

  if [ -f "$dest" ] && [ ! -L "$dest" ] && cmp -s "$src" "$dest"; then
    return 0
  fi

  if [ -e "$dest" ] || [ -L "$dest" ]; then
    relative="${dest#${TARGET_DIR}/}"
    backup_dest="${BACKUP_ROOT}/${relative}"
    mkdir -p "$(dirname "$backup_dest")"
    mv "$dest" "$backup_dest"
  fi

  cp "$src" "$dest"
}

link_global_cli() {
  local src="$1"
  local link_dir="${FARPLANE_CLI_LINK_DIR:-$HOME/.local/bin}"
  local dest="$link_dir/farplane"
  local backup_dest

  if [ "${FARPLANE_SKIP_GLOBAL_CLI:-0}" = "1" ]; then
    echo "Skipped global farplane CLI link because FARPLANE_SKIP_GLOBAL_CLI=1"
    return 0
  fi

  mkdir -p "$link_dir"

  if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$src" ]; then
    echo "Global farplane CLI already linked at $dest"
    return 0
  fi

  if [ -e "$dest" ] || [ -L "$dest" ]; then
    backup_dest="$BACKUP_ROOT/global-bin/farplane"
    mkdir -p "$(dirname "$backup_dest")"
    mv "$dest" "$backup_dest"
    echo "Backed up existing global farplane CLI to $backup_dest"
  fi

  ln -s "$src" "$dest"
  echo "Linked global farplane CLI at $dest"
  case ":$PATH:" in
    *":$link_dir:"*) ;;
    *) echo "Note: add $link_dir to PATH to run farplane from any shell." ;;
  esac
}

echo "Installing Codex harness from $REPO_DIR to $TARGET_DIR"

mkdir -p "$TARGET_DIR" "$TARGET_DIR/agents" "$TARGET_DIR/skills" "$TARGET_DIR/rules" "$TARGET_DIR/bin" "$TARGET_DIR/hooks" "$TARGET_DIR/docs/review"

for relative in "${RETIRED_INSTALL_PATHS[@]}"; do
  retired_path="$TARGET_DIR/$relative"
  if [ -e "$retired_path" ] || [ -L "$retired_path" ]; then
    backup_dest="$BACKUP_ROOT/$relative"
    mkdir -p "$(dirname "$backup_dest")"
    mv "$retired_path" "$backup_dest"
    echo "Retired $retired_path (backup: $backup_dest)"
  fi
done

if [ "$REPO_DIR" = "$(cd "$TARGET_DIR" && pwd)" ]; then
  echo "Repo is already the live Codex home. Skipping symlink install."
  render_config
  link_global_cli "$TARGET_DIR/bin/farplane"

  echo "Done."
  echo "Next: prefer runtime env for secrets (for example: doppler run -- farplane install); use ~/.farplane/config.toml only as a private fallback/cache."
  echo "Run: farplane doctor"
  exit 0
fi

copy_path "$REPO_DIR/templates/global/AGENTS.md" "$TARGET_DIR/AGENTS.md"
link_path "$REPO_DIR/PROJECT_RULES.md" "$TARGET_DIR/PROJECT_RULES.md"
link_path "$REPO_DIR/docs/review/rubrics" "$TARGET_DIR/docs/review/rubrics"
if [ -f "$REPO_DIR/hooks.json" ]; then
  link_path "$REPO_DIR/hooks.json" "$TARGET_DIR/hooks.json"
fi

for bin_name in "${INSTALL_BIN_FILES[@]}"; do
  link_path "$REPO_DIR/bin/$bin_name" "$TARGET_DIR/bin/$bin_name"
done
link_path "$REPO_DIR/bin/core" "$TARGET_DIR/bin/core"
link_global_cli "$TARGET_DIR/bin/farplane"

for hook_name in "${INSTALL_HOOK_FILES[@]}"; do
  link_path "$REPO_DIR/hooks/$hook_name" "$TARGET_DIR/hooks/$hook_name"
done

for agent_file in "$REPO_DIR"/agents/*.toml; do
  link_path "$agent_file" "$TARGET_DIR/agents/$(basename "$agent_file")"
done

python3 "$REPO_DIR/skills/skill-maintenance/scripts/install_selected_skills.py" \
  --repo "$REPO_DIR" \
  --target "$TARGET_DIR" \
  --all \
  --prune

for rule_file in "$REPO_DIR"/rules/*; do
  link_path "$rule_file" "$TARGET_DIR/rules/$(basename "$rule_file")"
done

render_config

echo "Done."
echo "Next: prefer runtime env for secrets (for example: doppler run -- farplane install); use ~/.farplane/config.toml only as a private fallback/cache."
echo "Run: farplane doctor"
echo "Hooks config is linked when hooks.json exists; Stop telemetry and the final-response length gate are active. Ticket-local QA/review owns completion."
echo "Backups (when needed) are stored under $BACKUP_ROOT"
