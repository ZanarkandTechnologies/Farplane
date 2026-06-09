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

STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_ROOT="${TARGET_DIR}/.install-backups/${STAMP}"
LOCAL_ENV_FILE="${TARGET_DIR}/config.local.env"
LOCAL_TOML_FILE="${TARGET_DIR}/config.local.toml"

if [ "$SKILLS_ONLY" -eq 1 ]; then
  if [ "${#SKILL_INSTALL_ARGS[@]}" -eq 0 ]; then
    SKILL_INSTALL_ARGS+=("--list")
  fi
  python3 "$REPO_DIR/bin/install_selected_skills.py" \
    --repo "$REPO_DIR" \
    --target "$TARGET_DIR" \
    "${SKILL_INSTALL_ARGS[@]}"
  exit 0
fi

ensure_local_env() {
  if [ ! -e "$LOCAL_ENV_FILE" ]; then
    cp "$REPO_DIR/config.local.env.example" "$LOCAL_ENV_FILE"
    if command -v python3 >/dev/null 2>&1; then
      python3 - "$LOCAL_ENV_FILE" "$TARGET_DIR" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
target_dir = sys.argv[2]
text = path.read_text()
text = text.replace("__CODEX_HOME__", target_dir)
path.write_text(text)
PY
    fi
    echo "Created $LOCAL_ENV_FILE from config.local.env.example"
    echo "Edit it before relying on secret-backed MCPs."
  fi
}

render_config() {
  ensure_local_env

  if [ -e "$TARGET_DIR/config.toml" ]; then
    mkdir -p "$BACKUP_ROOT"
    cp "$TARGET_DIR/config.toml" "$BACKUP_ROOT/config.toml"
  fi

  python3 - "$REPO_DIR/config.toml.example" "$TARGET_DIR/config.toml" "$LOCAL_ENV_FILE" "$LOCAL_TOML_FILE" "$TARGET_DIR" <<'PY'
from pathlib import Path
import os
import re
import sys

template_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
env_path = Path(sys.argv[3])
local_toml_path = Path(sys.argv[4])
target_dir = sys.argv[5]

env = {"CODEX_HOME": target_dir}
if env_path.exists():
    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise SystemExit(f"Invalid line in {env_path}: {raw_line}")
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()

required = ["CODEX_HOME", "REF_API_KEY", "NOTION_TOKEN"]
missing = [key for key in required if not env.get(key) or env[key].startswith("YOUR_") or env[key].startswith("__")]
if missing:
    raise SystemExit(
        f"Missing required values in {env_path}: {', '.join(missing)}"
    )

text = template_path.read_text()
replacements = {
    "__CODEX_HOME__": env["CODEX_HOME"],
    "__REF_API_KEY__": env["REF_API_KEY"],
    "__NOTION_TOKEN__": env["NOTION_TOKEN"],
}
for needle, value in replacements.items():
    text = text.replace(needle, value)

if local_toml_path.exists():
    local_text = local_toml_path.read_text().strip()
    if local_text:
        text = text.rstrip() + "\n\n# Machine-local config appended from config.local.toml\n\n" + local_text + "\n"
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

echo "Installing Codex harness from $REPO_DIR to $TARGET_DIR"

mkdir -p "$TARGET_DIR" "$TARGET_DIR/agents" "$TARGET_DIR/skills" "$TARGET_DIR/rules" "$TARGET_DIR/bin"

if [ "$REPO_DIR" = "$(cd "$TARGET_DIR" && pwd)" ]; then
  echo "Repo is already the live Codex home. Skipping symlink install."
  render_config

  echo "Done."
  echo "Next: keep secrets in $LOCAL_ENV_FILE and trust entries or machine-local overrides in $LOCAL_TOML_FILE."
  exit 0
fi

copy_path "$REPO_DIR/templates/global/AGENTS.md" "$TARGET_DIR/AGENTS.md"
link_path "$REPO_DIR/PROJECT_RULES.md" "$TARGET_DIR/PROJECT_RULES.md"
if [ -f "$REPO_DIR/hooks.json" ]; then
  link_path "$REPO_DIR/hooks.json" "$TARGET_DIR/hooks.json"
fi

for bin_file in "$REPO_DIR"/bin/*; do
  link_path "$bin_file" "$TARGET_DIR/bin/$(basename "$bin_file")"
done

for agent_file in "$REPO_DIR"/agents/*.toml; do
  link_path "$agent_file" "$TARGET_DIR/agents/$(basename "$agent_file")"
done

python3 "$REPO_DIR/bin/install_selected_skills.py" \
  --repo "$REPO_DIR" \
  --target "$TARGET_DIR" \
  --all

for rule_file in "$REPO_DIR"/rules/*; do
  link_path "$rule_file" "$TARGET_DIR/rules/$(basename "$rule_file")"
done

render_config

echo "Done."
echo "Next: keep secrets in $LOCAL_ENV_FILE and trust entries or machine-local overrides in $LOCAL_TOML_FILE."
echo "Hooks config is linked when hooks.json exists; hook env vars remain available as explicit overrides but normal Farplane runtime context should auto-activate the Stop hook."
echo "Backups (when needed) are stored under $BACKUP_ROOT"
