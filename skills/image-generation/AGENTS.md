# Image Generation Skill Instructions

This module is the inference.sh image-generation category skill. Keep `SKILL.md` as the active root with the umbrella model map and Codexter gates.

The files under `references/tools/` are copied upstream inference.sh `SKILL.md` files for specific image tool branches. Refresh them from upstream instead of rewriting them by hand.

Treat copied upstream references as read-only usage docs. Do not run upstream `npx skills add ...` install commands from Related Skills sections unless the operator explicitly asks.

Do not turn each upstream image model into a public active Codexter skill. Route through `image-generation`, then load the specific reference.

Keep the built-in `imagegen` skill as the default for normal Codex-native bitmap generation/editing when inference.sh is not needed.

Route artifact-level social/photo requests through `product-photography` or the
appropriate `social-content:*` method before choosing image models.

Keep shared social/photo/image artifact routing in `references/domain-production.md` and link to it from domain skills instead of duplicating save/async/publish/upstream-safety rules.

Never publish to social platforms unless the operator explicitly asks to publish.

For long-running or batched media jobs, require saved `input.json`, `result.json`, task IDs, and `jobs.md` before continuing in parallel or handing polling to another lane permitted by the current harness policy.
