# Video Generation Skill Instructions

This module is the model/app execution skill for inference.sh video. Keep the first-load `SKILL.md` focused on routing, capability gates, output handling, and proof.

The files under `references/tools/` are copied upstream inference.sh tool `SKILL.md` files. Refresh them from the upstream source instead of rewriting them by hand.

Keep domain video workflow planning in `video-production` method addresses.
This module remains the model/app execution skill.

Do not create a standalone public `video-prompting-guide` skill. Prompting guidance should live inside the artifact/domain skill that owns the output.

Keep the copied upstream video prompting guide at `references/prompting/video-prompting-guide.md`; load it from `video-generation` or artifact skills when video prompt quality needs shot/camera/lighting/model-specific guidance.

Keep shared artifact production workflow in `references/domain-production.md` and link to it from domain skills instead of duplicating routing/save/async/upstream-safety rules.

Treat copied upstream references as read-only usage docs. Do not run upstream `npx skills add ...` install commands from Related Skills sections unless the operator explicitly asks.

Use the `SKILL.md` Important Checklist for selecting references.

For long-running or batched media jobs, require saved `input.json`,
`result.json`, task IDs, and `jobs.md` before continuing in parallel or handing
polling to another lane permitted by the current harness policy. Use adaptive
backoff from `docs/specs/adaptive-backoff.md` for next-check timing.

Keep `remotion` and `remotion-render` separate. Model-native generation, Remotion authoring, and code-to-video rendering have different inputs, failure modes, and QA expectations.
