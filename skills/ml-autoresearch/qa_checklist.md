---
title: ML Autoresearch QA Checklist
owner: ml-autoresearch
status: active
kind: qa-checklist
updated_at: 2026-07-31
---

# ML Autoresearch QA Checklist

Apply before campaign approval and again before completion.

- [ ] One campaign ticket owns a stable objective, evaluator, data/split
      boundary, mutable surface, metric, guards, budget, proof, and stop rules.
- [ ] The exact baseline ran before mutation, and smokes are never used for
      keep, kill, promotion, or scientific claims.
- [ ] The evaluator, metric direction, prohibited inputs, and data/split
      boundary remain frozen; drift stops and regenerates the packet.
- [ ] A bounded source stage extracts applicable techniques, mechanisms,
      variables, failure conditions, and source refs before the first mutation.
- [ ] `hypothesis-tree.json` is the only current research-state owner;
      `program.md` owns policy and `progress.md` owns chronological receipts.
- [ ] `program.md` requires Leverage Advisor to choose every next experiment
      from eligible pending tree leaves plus learnings, current receipts, and
      remaining budget using one ordinal judgment—never a tournament or stored
      rank.
- [ ] Every experiment preregisters one attributable change, hypothesis,
      expected observation, observation horizon, named confidence, falsifier,
      surprise trigger, cost, guards, and keep/kill rule before full metrics
      are read.
- [ ] Every valid, invalid, failed, kept, and discarded attempt has an
      append-only receipt with hashes, command/environment, metrics, guards,
      runtime/cost, learning, and tree mutation.
- [ ] Replanning changes the tree after positive, flat, negative,
      branch-specific, invalid, and budget evidence instead of replaying a
      fixed ladder or chasing novelty.
- [ ] Surprising, invalid, prerequisite-uncertain, or causally ambiguous
      results get only program-bounded diagnostic children before rejection;
      expected negatives may close directly and backtrack to a credible sibling.
- [ ] Final claims come from the frozen best candidate's complete evaluator and
      independent leakage/reproducibility/evidence review, not the executor's
      self-assessment.
- [ ] A material negative miss or implausibly strong positive result has an
      `agent-qa-test:experiment` diagnosis receipt before method rejection or
      candidate promotion.
