---
title: Agent Skills eval comparison feature ledger
created_at: 2026-06-30
target: Farplane skill system compared with Agent Skills eval and authoring practices
status: draft
sources:
  - https://agentskills.io/skill-creation/evaluating-skills
  - https://agentskills.io/skill-creation/best-practices
  - https://agentskills.io/skill-creation/optimizing-descriptions
  - docs/skills/system.md
  - docs/skills/best-practices.md
  - docs/features/FEAT-0054-modular-skill-local-eval-tasks.md
---

# Feature Ledger: Farplane skill system compared with Agent Skills eval and authoring practices

| Feature | Source | Evidence | User job | Metric moved | Transferable principle | Risks |
| --- | --- | --- | --- | --- | --- | --- |
| With-skill versus baseline output evals | Agent Skills evaluating-skills | Runs each test with and without a skill or previous version, captures pass rate, timing, token deltas, and assertion evidence. | Prove a skill adds value instead of only feeling useful. | Skill value delta, token/time cost, assertion pass rate. | Compare skill-enabled output against a baseline before claiming skill improvement. | Needs clean-run isolation and can become expensive if applied globally. |
| Realistic eval cases with assertions | Agent Skills evaluating-skills; Farplane FEAT-0054 | External source uses prompt, expected output, optional files, assertions; Farplane already has skill-local `eval_task.json`. | Give each skill a small regression suite near the owning package. | Eval coverage quality and repeatability. | Extend Farplane eval rows with richer case metadata where needed, not a second eval format. | Overly brittle assertions can optimize the wrong behavior. |
| Description trigger-rate evals | Agent Skills optimizing-descriptions | Uses positive and negative query sets, repeated runs, trigger-rate threshold, train/validation split, and fresh-query sanity checks. | Make skills activate on the right tasks and stay quiet on near-misses. | True positive trigger rate, false trigger rate, validation pass rate. | Add a skill-selection eval surface to Farplane's eval/maintenance loop. | Trigger behavior depends on client observability and may be nondeterministic. |
| Train/validation discipline | Agent Skills optimizing-descriptions | Optimizes on train failures, selects by validation pass rate, then checks fresh queries. | Prevent description edits from overfitting to known prompts. | Generalization rate across unseen queries. | Use fixed held-out trigger/output cases for material skill-description rewrites. | Too much ceremony for tiny wording fixes. |
| Trace-based simplification | Agent Skills best-practices; Farplane best-practices | External source says read execution traces for wasted steps, false positives, misses, and irrelevant instructions; Farplane already emphasizes correction, QA, eval, review, and hardcases. | Convert real mistakes into shorter, sharper skill instructions. | Reduced wasted steps, maintenance burden, bloat. | Feed trace findings into `skill-maintenance.refine_skill` and `skill-signals` maintenance burden. | Requires good trace capture; final-output-only review misses this. |
| Real-expertise source material | Agent Skills best-practices; Farplane docs/memory/tickets | External source prefers hands-on tasks, corrections, project artifacts, specs, reviews, git history, incident reports. Farplane already treats tickets/docs/proof as durable truth. | Keep skills local, concrete, and non-generic. | Skill specificity and usefulness. | Explicitly score skill changes higher when sourced from tickets, corrections, proof artifacts, and repo conventions. | Could become artifact harvesting without enough selection pressure. |
| Context budget and progressive disclosure | Agent Skills best-practices; Farplane FEAT-0062 and docs/skills/best-practices.md | Both systems prefer small first-load content, reference routing, defaults, and examples over exhaustive docs. | Keep activated skills usable in context. | First-load token cost, surface budget pass, task success. | Already mostly adopted; keep Farplane's stricter first-load contract plus opt-in `10/5/5` budget. | Global caps too early could break useful legacy skills. |
| Description style | Agent Skills optimizing-descriptions; Farplane docs/skills/system.md | External source allows up to 1024 chars and recommends imperative, user-intent descriptions. Farplane caps at 220 chars with functional routing syntax. | Improve routing without bloating startup context. | Trigger precision and recall. | Adapt imperative/user-intent wording within Farplane's 220-char cap. | Expanding descriptions could fight Farplane's lean registry contract. |
| HTML live report for optimization | Agent Skills optimizing-descriptions | Mentions a skill-creator loop with parallel eval and live HTML report. | Make optimization inspectable while it runs. | Operator observability. | Defer until Farplane has enough trigger/output eval data to justify UI work. | Premature UI before stable data contracts. |
