#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
reviews_root="$ROOT/.farplane/reviews"
review_dir="${FARPLANE_PRE_PUSH_REVIEW_DIR:-$reviews_root/pre-push-latest}"

case "$review_dir" in
  /*) ;;
  *) review_dir="$ROOT/$review_dir" ;;
esac

mkdir -p "$reviews_root" "$(dirname "$review_dir")"
reviews_root="$(cd "$reviews_root" && pwd -P)"
review_dir="$(cd "$(dirname "$review_dir")" && pwd -P)/$(basename "$review_dir")"

case "$review_dir/" in
  "$reviews_root"/*) ;;
  *)
    echo "Refuse unsafe FARPLANE_PRE_PUSH_REVIEW_DIR outside $reviews_root: $review_dir" >&2
    exit 2
    ;;
esac
if [ "$review_dir" = "$reviews_root" ]; then
  echo "Refuse unsafe FARPLANE_PRE_PUSH_REVIEW_DIR equal to reviews root: $review_dir" >&2
  exit 2
fi

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
