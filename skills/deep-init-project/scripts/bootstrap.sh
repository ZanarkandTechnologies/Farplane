#!/usr/bin/env bash
set -euo pipefail

#
# bootstrap.sh
#
# Scaffolds docs-first project state and base templates.
#
# Usage:
#   bootstrap.sh [--force] [target_project_dir]
#

FORCE=0
TARGET_DIR="."

while [ $# -gt 0 ]; do
  case "$1" in
    --force|-f)
      FORCE=1
      shift
      ;;
    --help|-h)
      echo "Usage: $(basename "$0") [--force] [target_project_dir]"
      exit 0
      ;;
    *)
      TARGET_DIR="$1"
      shift
      ;;
  esac
done

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
REF_DIR="${SKILL_DIR}/references"

if [ ! -d "$REF_DIR" ]; then
  echo "Error: references directory not found: $REF_DIR" >&2
  exit 1
fi

TARGET_DIR="$(cd -- "$TARGET_DIR" && pwd)"

copy_file() {
  local src="$1"
  local dest="$2"

  if [ ! -f "$src" ]; then
    echo "Error: missing source file: $src" >&2
    exit 1
  fi

  if [ -e "$dest" ] && [ "$FORCE" -ne 1 ]; then
    echo "Skip (exists): $dest"
    return 0
  fi

  mkdir -p "$(dirname "$dest")"
  cp "$src" "$dest"
  echo "Wrote: $dest"
}

write_file_if_missing() {
  local dest="$1"
  local content="$2"

  if [ -e "$dest" ] && [ "$FORCE" -ne 1 ]; then
    echo "Skip (exists): $dest"
    return 0
  fi

  mkdir -p "$(dirname "$dest")"
  printf "%b" "$content" > "$dest"
  echo "Wrote: $dest"
}

append_line_if_missing() {
  local dest="$1"
  local line="$2"

  if [ -e "$dest" ] && grep -Fxq "$line" "$dest"; then
    echo "Skip (line exists): $dest :: $line"
    return 0
  fi

  mkdir -p "$(dirname "$dest")"
  printf "%s\n" "$line" >> "$dest"
  echo "Updated: $dest"
}

echo "Bootstrapping docs-first scaffold into: $TARGET_DIR"
echo "Force overwrite: $FORCE"

copy_file "${REF_DIR}/AGENTS_TEMPLATE.md" "${TARGET_DIR}/AGENTS.md"
copy_file "${REF_DIR}/PROJECT_RULES_TEMPLATE.md" "${TARGET_DIR}/PROJECT_RULES.md"
copy_file "${REF_DIR}/ARCHITECTURE_TEMPLATE.md" "${TARGET_DIR}/ARCHITECTURE.md"

mkdir -p "${TARGET_DIR}/docs/specs"
copy_file "${REF_DIR}/SPECS_README_TEMPLATE.md" "${TARGET_DIR}/docs/specs/README.md"
copy_file "${REF_DIR}/BOOTSTRAP_BRIEF_TEMPLATE.md" "${TARGET_DIR}/docs/bootstrap-brief.md"
copy_file "${REF_DIR}/CODE_REVIEW_TEMPLATE.md" "${TARGET_DIR}/docs/code_review.md"
copy_file "${REF_DIR}/REVIEW_AGENT_TEMPLATE.md" "${TARGET_DIR}/docs/review-agent.md"

write_file_if_missing "${TARGET_DIR}/docs/prd.md" "# PRD\n\n## Problem / Context\n\n## Audience\n\n## JTBD\n\n## SLC Slice\n\n## Goals\n\n## Non-Goals\n\n## Constraints\n\n## Risks\n\n## Backpressure\n"
write_file_if_missing "${TARGET_DIR}/docs/HISTORY.md" "# HISTORY\n\nAppend-only change log.\n\nFormat:\nYYYY-MM-DD HH:mm Z | TYPE | summary\n\n"
write_file_if_missing "${TARGET_DIR}/docs/MEMORY.md" "# MEMORY\n\nCurated durable constraints and invariants future work must obey.\n\nFormat:\nYYYY-MM-DD HH:mm Z | TYPE | MEM-#### | tags | durable rule\n\n"
write_file_if_missing "${TARGET_DIR}/docs/TROUBLES.md" "# TROUBLES\n\nAppend-only raw log for repeated failures, blockers, user corrections, and preventable misses.\n\nFormat:\nYYYY-MM-DD HH:mm Z | area,tags | request | miss | correction | prevention\n\nPromote only stable patterns from here into docs/LESSONS.md, docs/MEMORY.md, or the relevant skill/contract.\n\n"
write_file_if_missing "${TARGET_DIR}/docs/LESSONS.md" "# LESSONS\n\nDistilled post-fix learning log for prompt, skill, eval, and policy improvements.\n\nFormat:\nYYYY-MM-DD HH:mm Z | area,tags | source | lesson | owner | next_prompt_or_skill_change\n\nUse docs/TROUBLES.md for raw pain; use this file for reusable lessons after a fix, correction pass, review, or drain.\n\n"
copy_file "${REF_DIR}/TASTE_TEMPLATE.md" "${TARGET_DIR}/docs/TASTE.md"

mkdir -p "${TARGET_DIR}/tickets" "${TARGET_DIR}/tickets/archive" "${TARGET_DIR}/tickets/templates"
copy_file "${SKILL_DIR}/../../tickets/README.md" "${TARGET_DIR}/tickets/README.md"
copy_file "${SKILL_DIR}/../../tickets/templates/ticket.md" "${TARGET_DIR}/tickets/templates/ticket.md"

mkdir -p "${TARGET_DIR}/.githooks"
copy_file "${REF_DIR}/GITHOOKS_README_TEMPLATE.md" "${TARGET_DIR}/.githooks/README.md"
copy_file "${REF_DIR}/PRE_COMMIT_HOOK_TEMPLATE.sh" "${TARGET_DIR}/.githooks/pre-commit"
copy_file "${REF_DIR}/PRE_PUSH_HOOK_TEMPLATE.sh" "${TARGET_DIR}/.githooks/pre-push"

mkdir -p "${TARGET_DIR}/scripts"
copy_file "${REF_DIR}/PRE_COMMIT_CHECK_TEMPLATE.sh" "${TARGET_DIR}/scripts/pre_commit_check.sh"
copy_file "${REF_DIR}/PRE_PUSH_CHECK_TEMPLATE.sh" "${TARGET_DIR}/scripts/pre_push_check.sh"
copy_file "${REF_DIR}/COLLECT_REVIEW_CONTEXT_TEMPLATE.sh" "${TARGET_DIR}/scripts/collect_review_context.sh"
copy_file "${REF_DIR}/CODEX_REVIEW_AGENT_TEMPLATE.ts" "${TARGET_DIR}/scripts/codex_review_agent.ts"
copy_file "${REF_DIR}/RUN_PRE_PUSH_REVIEW_TEMPLATE.sh" "${TARGET_DIR}/scripts/run_pre_push_review.sh"
append_line_if_missing "${TARGET_DIR}/.gitignore" ".farplane/reviews/"

mkdir -p "${TARGET_DIR}/qa/cookbook"
copy_file "${REF_DIR}/qa/AGENTS.md" "${TARGET_DIR}/qa/AGENTS.md"
copy_file "${REF_DIR}/qa/README.md" "${TARGET_DIR}/qa/README.md"
copy_file "${REF_DIR}/qa/cookbook/README.md" "${TARGET_DIR}/qa/cookbook/README.md"
copy_file "${REF_DIR}/qa/cookbook/TEMPLATE.md" "${TARGET_DIR}/qa/cookbook/TEMPLATE.md"

echo ""
echo "Done."
echo "Next:"
echo "  - Fill in PROJECT_RULES.md and AGENTS.md."
echo "  - In PROJECT_RULES.md, document one canonical app-only run path and one canonical QA/evidence run path, plus required services and port/env assumptions."
echo "  - Fill in ARCHITECTURE.md so the repo has one top-level system map."
echo "  - Start by refining docs/bootstrap-brief.md with a deep-interview-quality intake before locking stack or topology decisions."
echo "  - Fill the bootstrap brief's agent-experience section so the repo knows how agents should reach, inspect, and verify important app states."
echo "  - Refine docs/TASTE.md so UI tickets and QA share one visual doctrine."
echo "  - Use qa/cookbook/ to document evidence-capture launch paths, shortcuts, deep links, seed/reset paths, target URLs, and debug probes for repeatable QA."
echo "  - Use docs/TROUBLES.md for repeated misses and blockers; distill recurring lessons into docs/LESSONS.md."
echo "  - Fill in docs/bootstrap-brief.md with explicit local-hook, heavy-check, CI/deploy gate, runtime-command, and service-assumption decisions before finalizing the scaffold."
echo "  - Fill in scripts/pre_push_check.sh with the repo's lint, typecheck, test, build, and optional desloppify commands."
echo "  - For Node projects, add @openai/codex-sdk + tsx and package scripts review:agent / review:prepush to enable the default Codex SDK diff reviewer."
echo "  - Optional: enable .githooks with 'git config core.hooksPath .githooks' and prefer pre-push over pre-commit."
echo "  - Optional: run the Farplane install script so ~/.codex/skills/code-review/SKILL.md, reviewer agents, and review rubrics are linked."
echo "  - Optional: install coderabbit when an external heavyweight PR/pre-push review is useful."
echo "  - If the idea is still open-ended, start with brainstorm."
echo "  - For bootstrap ambiguity, run deep-interview in bootstrap mode and keep the answers in docs/bootstrap-brief.md."
echo "  - Then use prd + spec-to-ticket to author docs/specs and create tickets/*.md."
echo "  - For an existing repo, read ~/.codex/skills/deep-init-project/README.md and start with one ticket only."
