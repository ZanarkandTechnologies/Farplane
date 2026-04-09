#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$HOME/.codex}"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_ROOT="${TARGET_DIR}/.install-backups/${STAMP}"

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

echo "Installing Codex harness from $REPO_DIR to $TARGET_DIR"

mkdir -p "$TARGET_DIR" "$TARGET_DIR/agents" "$TARGET_DIR/skills" "$TARGET_DIR/rules" "$TARGET_DIR/bin"

if [ "$REPO_DIR" = "$(cd "$TARGET_DIR" && pwd)" ]; then
  echo "Repo is already the live Codex home. Skipping symlink install."

  if [ ! -e "$TARGET_DIR/config.toml" ]; then
    cp "$REPO_DIR/config.toml.example" "$TARGET_DIR/config.toml"
    echo "Created $TARGET_DIR/config.toml from config.toml.example"
  else
    echo "Left existing $TARGET_DIR/config.toml in place"
  fi

  echo "Done."
  echo "Next: edit $TARGET_DIR/config.toml and replace __CODEX_HOME__ plus any local MCP/project values."
  exit 0
fi

link_path "$REPO_DIR/templates/global/AGENTS.md" "$TARGET_DIR/AGENTS.md"
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

for skill_dir in "$REPO_DIR"/skills/*; do
  if [ "$(basename "$skill_dir")" = ".system" ]; then
    continue
  fi

  link_path "$skill_dir" "$TARGET_DIR/skills/$(basename "$skill_dir")"
done

for rule_file in "$REPO_DIR"/rules/*; do
  link_path "$rule_file" "$TARGET_DIR/rules/$(basename "$rule_file")"
done

if [ ! -e "$TARGET_DIR/config.toml" ]; then
  cp "$REPO_DIR/config.toml.example" "$TARGET_DIR/config.toml"
  echo "Created $TARGET_DIR/config.toml from config.toml.example"
else
  echo "Left existing $TARGET_DIR/config.toml in place"
fi

echo "Done."
echo "Next: edit $TARGET_DIR/config.toml and replace __CODEX_HOME__ plus any local MCP/project values."
echo "Hooks config is linked when hooks.json exists; hook env vars remain available as explicit overrides but normal Codexter runtime context should auto-activate the Stop hook."
echo "Backups (when needed) are stored under $BACKUP_ROOT"
