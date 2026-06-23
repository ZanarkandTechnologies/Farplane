---
title: Deliberative Advice System Surface Decision Note
date: 2026-06-22
status: complete
owner: deliberative-advice
context_ref: experiments/decisions/2026-06-22-deliberative-advice-system-surface/context.md
review_route: council
---

# Decision

Should Farplane make council-style deliberative advice a first-class system
workflow surface beyond the existing `deliberative-advice` skill, or keep it as
an on-demand skill invoked only for costly decisions?

# Stakes

The decision affects operator trust, prompt/context cost, workflow ceremony,
and where future multi-agent reasoning patterns belong in Farplane.

# Grounding

Local grounding is sufficient for this test because the question is internal
harness placement. Evidence came from:

- `AGENTS.md`
- `docs/fundamentals/harness-engineering-doctrine.md`
- `docs/LESSONS.md`
- `skills/skill-maintenance/audits/2026-06-13-behavior-delta-compression.md`
- `/Users/kenjipcx/.codex/skills/deliberative-advice/SKILL.md`

The baseline is that Farplane already has `deliberative-advice` as a Tier 2
skill, already requires durable context packets for nontrivial subagent
handoffs, and prefers the smallest effective harness lever before root/global
prompt expansion or new orchestration.

# Perspectives

## Lane A

- Recommendation: option 2.
- Strongest reason: a lightweight routing note gives the operator council value
  at the right moment without making every serious decision ceremonial.
- Strongest opposing point: even a small policy note can become pressure to
  overuse councils.
- Evidence that would change its mind: repeated high-stakes misses or operator
  feedback that setup feels too manual.
- Next owner/proof: a short follow-up ticket or doc diff with trigger criteria
  and one example invocation.

## Lane B

- Recommendation: option 2.
- Strongest reason: option 2 fixes discoverability and routing with the
  smallest lever; option 3 risks stale templates and fragmented ownership.
- Strongest opposing point: the note can become prompt bloat if it repeats the
  skill contract.
- Evidence that would change its mind: repeated missed invocations despite a
  routing note, or recurring manual setup errors the skill cannot prevent.
- Next owner/proof: keep `deliberative-advice` as owner; prove with one
  behavior test using this decision packet.

## Lane C

- Recommendation: option 1.
- Strongest reason: the packet does not prove repeated need, usage frequency,
  or insufficiency of the existing skill.
- Strongest opposing point: a tiny routing note could prevent missed
  invocations for high-stakes decisions.
- Evidence that would change its mind: three or more recent high-stakes
  Farplane decisions where agents failed to invoke the skill and outcomes would
  likely have improved.
- Next owner/proof: collect this result first; create a usage-gap note or
  ticket before policy changes.

## Lane D

- Recommendation: option 2.
- Strongest reason: council mode is a routing/escalation rule, not a new
  runtime.
- Strongest opposing point: a routing note can add ceremony if agents overuse
  it for ordinary architecture or planning choices.
- Evidence that would change its mind: repeated council runs failing because
  the skill lacks templates, lane prompts, aggregation structure, or proof
  gates.
- Next owner/proof: repo-local `AGENTS.md` or harness doctrine routing note,
  plus one transcript replay showing correct invocation without prompt bloat.

# Critique / Ranking

## Option 1: Keep Council Skill-Only

This is the strongest evidence posture. It avoids adding policy based on one
successful test and respects the doctrine that root and local prompt expansion
need a real repeated failure mode.

Weakness: it leaves discoverability as a memory problem. The current test
worked because the operator explicitly named the skill; the system still lacks
a crisp cue for when agents should escalate from ordinary `advise` to council
mode.

## Option 2: Add A Lightweight Routing Note

This is the best local fit if the note is narrow and points to the existing
skill rather than copying its procedure. It improves invocation at the moment
of need while preserving `deliberative-advice` as the owner of ceremony,
artifacts, lane contracts, critique, and synthesis.

Weakness: without usage-gap evidence, even a small note is speculative. It can
also create over-triggering if it frames normal architecture choices as council
worthy.

## Option 3: Create A First-Class Council Workflow Package

This would help only if repeated council runs fail because the skill lacks
templates, aggregation scripts, lane prompts, or proof gates. It is premature
for this decision because the current skill already produced a durable context
packet, independent lanes, dissent, and a chair synthesis.

Weakness: it adds coordination cost, new maintenance surfaces, and likely stale
workflow machinery before proving the existing skill is insufficient.

# Recommendation

Choose option 2, but make it evidence-gated and minimal:

Add at most a compact Farplane-local routing note that says high-stakes,
expensive, disputed, cross-functional, or hard-to-reverse decisions should
consider `deliberative-advice`; the skill remains the primary owner of council
procedure and artifacts.

Do not create a new workflow package or script layer now.

# Dissent

The strongest dissent is Lane C's option 1 argument: this test proves the skill
can work when explicitly invoked, but it does not prove repeated missed
invocations or demand. That dissent should block any global-template change and
any first-class workflow package until a usage gap is documented.

# Tradeoff Accepted

Accept a small amount of routing guidance in exchange for better
discoverability, while rejecting broader council infrastructure until there is
evidence that the existing skill fails in repeated use.

# Confidence

Medium.

Confidence is higher on rejecting option 3 than on adopting option 2. The
evidence strongly supports avoiding new orchestration, but only moderately
supports adding a note before collecting usage-gap examples.

# Next Owner

Primary owner: `deliberative-advice` remains the skill owner.

Potential follow-up owner: `harness-advisor` or a small direct doc/ticket task
if the operator wants to add a routing note.

# Proof / Evidence Gap

Proof artifact for this test:

- `experiments/decisions/2026-06-22-deliberative-advice-system-surface/context.md`
- `experiments/decisions/2026-06-22-deliberative-advice-system-surface/decision-note.md`

Evidence gap before further promotion:

- Find at least three recent high-stakes Farplane decisions where agents failed
  to invoke `deliberative-advice`, or one transcript replay showing that a
  compact routing note changes behavior without noticeable prompt bloat.
