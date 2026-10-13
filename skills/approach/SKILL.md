---
name: approach
description: "Use for \"how should I approach them\", \"what should we offer\", \"write the outreach\" or \"shape a solution for them\": pick one approach and contribution or offer, return an unsent message."
source: local
department: sales
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash, web_search
---

# Approach

## Context

Use this once a target is known (a `prospect` OpportunityCase or supplied
research naming one person and one dated professional signal) and the operator
asks how to approach them, what to offer, or what to send. It compares the
approaches the evidence supports, picks one, builds the contribution or offer
behind it, and drafts one unsent message. One pass returns one approach packet.

It does not find or research targets (`prospect`), price a proposal
(`proposal-pricing`), polish final copy (`copywriting`), or send
anything. It uses an existing problem frame when the operator supplies one.

## Skill Signature

```text
approach(target_ref, signal_ref, relationship_class?, accepted_usecase_or_proof?, channel?, budget?)
  -> approach_packet { approach frontier + chosen approach + contribution | offer + unsent message + learning contract } + next_owner
reads: the OpportunityCase or research, entity bodies, proof packages, frame output, supplied relationship context
does: frames the problem when an offer needs it, compares approaches on four axes, builds the contribution or offer, drafts the message
writes: the caller's artifact, else .farplane/approach/reports/YYYY-MM-DD-<person>-<slug>.md; inline for answer-only requests
returns: the approach packet, readiness send | revise | stop, the approval still needed, and the next owner
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind one target and one signal, or stop.**
  `request -> person + dated signal + relationship class + budget | prospect handoff`

  Rule: Resolve one person, one dated professional signal (something they
  said, published, built, hired for, or own), the relationship class
  (`sell_to`, `partner_or_jv`, `channel`, `data_or_delivery`, `learn_from`),
  the channel, and the effort cap. Default to micro effort, a five-minute
  recipient budget, and zero spend. With no research or no traceable signal,
  stop with a `prospect` handoff naming the missing inputs; draft no
  placeholder message.

  Assert:
  - Career prestige never stands in for a signal or a problem.
- [ ] **N2 — Frame the problem and shape the solution when an offer needs one.**
  `signal + use case -> problem frame + solution boundary + walkthrough | skip`

  Rule: Skip this node for a contribution that needs no product proof. For an
  offer, use the supplied problem frame if there is one; otherwise name the
  actor, job, stakes, constraints and the smallest rung (manual service ->
  tool -> product -> platform) inline. An ERP-adjacent tool is a decision layer beside
  the system of record, not a replacement. When several problems share one
  planning or allocation decision, shape one loop, not one module each; load
  [Mine-to-Margin](references/mine-to-margin-reference-standard.md). Name V1,
  deferred V2, non-goals, risks, and, for system-heavy work, decision rights
  and permissions. An operational MVP gets a walkthrough (inputs, steps,
  mechanism, outputs, how actuals feed the next run) covering an ordinary
  case, a binding constraint, and changed demand.

  Example: `three mining problems -> one lot-allocation loop beside ERP and
  mine planning; cases: ordinary quarter, labour shortage, premium spike`

  Assert:
  - The requested artifact is evidence, not automatically the V1.
  - A small tool stays the V1 when the facts make it sufficient.
- [ ] **N3 — Compare the approaches the evidence supports.**
  `case + resources -> approach frontier + one selected approach`

  Rule: Build options only from the accepted proof, research, entity bodies,
  and supplied relationship context; never invent an intro, favour, asset, or
  shared interest. Show three options only when three are viable. Judge each
  on four axes, `low | medium | high | unknown`: commercial movement,
  relationship value, ask burden, relationship risk. Never sum them. Prefer
  the option that preserves trust over a costly ask, and say why each
  alternative lost. Render the comparison even when one short DM is asked for.

  Example: `pilot ask (high movement, high burden) vs annotated sample first
  (medium, low) vs ask an advisor who never offered an intro (unknown risk)
  -> sample first`

  Assert:
  - No numeric total or relationship-points score.
- [ ] **N4 — Build the contribution or the offer.**
  `selected approach -> contribution brief | offer`

  Rule: A contribution is one artifact (workflow map, teardown, benchmark,
  checklist, calculator, field note, or proof-sized demo) that stays useful
  if they never reply, within a recipient-effort budget of 2, 5, or 10
  minutes. Reject free-help offers and disguised discovery homework. A demo
  needs a reason a static artifact cannot test the uncertainty, one workflow
  and one decision, and a route receipt: boundary accepted, `prd` realism mode
  needed or not, build owner (project owner or `impl-plan`), inspection
  surface. An offer names the target outcome, smallest engagement,
  deliverables, proof and its limit, reason-now hypothesis, and non-goals; the
  proof must match every claim.

  Assert:
  - The contribution does not depend on booking a call to be useful.
  - No production, ROI, or company-specific claim the proof does not support.
- [ ] **N5 — Draft one message and keep it unsent.**
  `contribution | offer -> unsent message + approval gate`

  Rule: Lead with the artifact and the signal that made it relevant, state its
  limit, and ask one easy correction question; make no reply comfortable.
  Every personalisation claim carries its evidence and a correction question.
  Use `copywriting` when wording quality matters, and draft only the
  channels asked for. Name the exact approval needed before contact.

  Assert:
  - Nothing private, sensitive, or manipulative is used to personalise.
- [ ] **N6 — Return the packet, readiness, and next owner.**
  `packet -> readiness + learning contract + next_owner`

  Rule: Render [the template](templates/approach-packet.md). Set readiness
  `send`, `revise`, or `stop`, the learning objective, the stop condition, and
  the maximum follow-ups. Route a confirmed problem after a call to
  `proposal-pricing`, an accepted build to `prd` or `impl-plan`, research gaps
  to `prospect`, and durable facts to `manage-wiki`. Use `review` before a
  material customer-facing packet is called ready.

  Assert:
  - The packet names what reply would move it to a proposal.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- A personalised offer is not a mail merge; career history explains relevance
  but does not prove current pain.
- "Let me know if you need free AI help" hands all the problem definition to
  the recipient and is not first value.
- A thoughtful gesture must be relevant, supported, and carry no quid pro quo.
- Copy quality can hide a weak solution or a proof that does not match.
- A polished demo can still fail when it guesses the workflow or costs more
  than what it can teach.
- CRM is not the campaign queue: send stages live in this packet or its
  ticket; CRM holds durable people and validated opportunities only.
- Approving the plan does not approve sending; each send needs its own yes.
- Posting about a person's public idea needs their separate permission.

## Reference Map

- [approach packet template](templates/approach-packet.md) - load in N6.
- [Mine-to-Margin](references/mine-to-margin-reference-standard.md) - load in
  N2 for an operational decision system or a client demo.
- [offer example](examples/offer/example.md) - calibrates the four-axis
  frontier and a restrained offer.
- [contribution example](examples/contribution/example.md) - calibrates
  standalone value and a correction-first message.

## Output

```yaml
target: <person, company, relationship class, dated signal>
frame: <frame ref or skipped; V1 / V2 / non-goals / walkthrough when shaped>
frontier: <option -> movement, relationship value, ask burden, risk; why each lost>
chosen: <approach>
contribution_or_offer: <artifact brief + effort caps | offer + proof and limit>
message: <unsent draft per requested channel, correction question>
readiness: send | revise | stop
learning: <objective, stop condition, max follow-ups>
approval_needed: <exact send, CRM, spend, or publish approval>
next_owner: proposal-pricing | prd | impl-plan | prospect | manage-wiki | none
```
