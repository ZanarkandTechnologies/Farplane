#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
ticket_id="${FARPLANE_REVIEW_TICKET_ID:-}"
case "$ticket_id" in
  TASK-[0-9][0-9][0-9][0-9]) ;;
  *) echo "Set FARPLANE_REVIEW_TICKET_ID=TASK-XXXX so review evidence has a ticket owner." >&2; exit 2 ;;
esac
review_root="$ROOT/tickets/$ticket_id/artifacts/review"
review_dir="${FARPLANE_PRE_PUSH_REVIEW_DIR:-$review_root/pre-push-latest}"

case "$review_dir" in
  /*) ;;
  *) review_dir="$ROOT/$review_dir" ;;
esac

mkdir -p "$review_root" "$(dirname "$review_dir")"
review_root="$(cd "$review_root" && pwd -P)"
review_dir="$(cd "$(dirname "$review_dir")" && pwd -P)/$(basename "$review_dir")"

case "$review_dir/" in
  "$review_root"/*) ;;
  *)
    echo "Refuse review artifacts outside $review_root: $review_dir" >&2
    exit 2
    ;;
esac

mkdir -p "$review_dir/checks"

cd "$ROOT"
bash scripts/collect_review_context.sh "$review_dir/context.md" "$review_dir/checks"

if [ -n "${CODEX_REVIEW_CMD:-}" ]; then
  bash -lc "$CODEX_REVIEW_CMD \"${review_dir}/context.md\" \"${review_dir}/review.json\""
elif [ -f package.json ] && command -v npm >/dev/null 2>&1 && npm run 2>/dev/null | grep -q "review:agent"; then
  npm run review:agent -- "$review_dir/context.md" "$review_dir/review.json"
else
  echo "Skip Codex SDK review: configure npm script review:agent or set CODEX_REVIEW_CMD."
  echo "For Node projects, add @openai/codex-sdk and tsx, then add:"
  echo '  "review:agent": "tsx scripts/codex_review_agent.ts"'
fi
