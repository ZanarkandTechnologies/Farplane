---
title: ML Autoresearch QA Checklist
owner: ml-autoresearch
status: active
kind: qa-checklist
updated_at: 2026-07-22
---

# ML Autoresearch QA Checklist

Apply before campaign approval and again before completion.

- [ ] One campaign ticket owns a stable objective, evaluator, data/split
      boundary, mutable surface, metric, guards, budget, proof, and stop rules.
- [ ] The exact baseline ran before mutation, and smokes are never used for
      keep, kill, promotion, or scientific claims.
- [ ] The evaluator, metric direction, prohibited inputs, and data/split
      boundary remain frozen; drift stops and regenerates the packet.
- [ ] `program.md` requires Leverage Advisor to choose every next experiment
      from its roadmap plus `progress.md` learnings, current receipts, and
      remaining budget.
- [ ] Every experiment preregisters one attributable change, hypothesis,
      falsifier, cost, guards, and keep/kill rule before full metrics are read.
- [ ] Every valid, invalid, failed, kept, and discarded attempt has an
      append-only receipt with hashes, command/environment, metrics, guards,
      runtime/cost, learning, and frontier update.
- [ ] Replanning changes the frontier after positive, flat, negative,
      branch-specific, invalid, and budget evidence instead of replaying a
      fixed ladder or chasing novelty.
- [ ] Final claims come from the frozen best candidate's complete evaluator and
      independent leakage/reproducibility/evidence review, not the executor's
      self-assessment.
