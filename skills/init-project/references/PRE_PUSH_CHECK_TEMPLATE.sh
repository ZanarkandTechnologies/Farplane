#!/usr/bin/env bash
set -euo pipefail

echo "No project-specific pre-push checks configured yet."
echo "Edit scripts/pre_push_check.sh to add the validators for this repo."
echo ""
echo "Typical checks:"
echo "  Python: ruff check . && pyright && pytest -q"
echo "  TypeScript: pnpm lint && pnpm typecheck && pnpm test"

