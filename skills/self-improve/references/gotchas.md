# Self Improve Gotchas

- Do not optimize before baseline evals exist.
- Do not leak expected answers into prompts.
- Do not trust evals with fewer than 3 representative cases.
- Do not use judge-only scoring as the primary metric.
- Do not promote experimental evals into the target skill until they catch a
  real failure or prevent a known regression.
- Do not make the skill longer just to satisfy one brittle eval.
- Do not store bulky raw traces, secrets, or local-only transcripts in a target
  skill's `self-improve/` directory.
- Do not treat `program.md` as a second `SKILL.md`; it is memory for improving
  the skill, not the live usage contract.
- Do not run overnight optimization on smoke evals. Smoke means 3-5 cases;
  durable optimization needs a diverse suite closer to 20-100 cases.
- Do not promote a prompt candidate just because it passed one category. Check
  boundary, negative, and out-of-original-story cases.
- Do not schedule a future check-in for feedback measurable in the current Goal.
- Do not create a second ticket, finding, or reward registry for delayed
  feedback; reuse the original ticket Reward and Goal Packet.
