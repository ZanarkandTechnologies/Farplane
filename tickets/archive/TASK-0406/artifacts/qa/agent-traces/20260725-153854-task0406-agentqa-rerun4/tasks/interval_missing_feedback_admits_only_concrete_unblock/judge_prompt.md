You are judging an agent answer for a harness eval.

Return only valid JSON with this shape:

{
  "verdict": "A",
  "pass": true,
  "rubric": {
    "groundedness": "A",
    "completeness": "A",
    "usefulness": "A",
    "repeatability": "A",
    "length_balance": "A"
  },
  "reference_point_results": [
    {"reference_point": "text", "met": true, "reason": "short reason"}
  ],
  "reason": "short reason"
}

Allowed verdicts:
- `A`: strong pass. The answer is grounded, complete, useful, repeatable where relevant, and well-sized.
- `B`: near miss. The answer is usable but has a clear missing detail, caveat, or quality issue that should be fixed.
- `C`: revise. The answer is directionally relevant but misses a meaningful requirement or would not be reliable yet.
- `D`: fail or blocked. The answer is unsupported, incomplete, unusable, non-repeatable, or impossible to judge from the evidence.

Rubric values must be `A`, `B`, `C`, or `D`. Set `pass` to true only for `A`.

Groundedness: whether the answer is supported by the task and reference points
and avoids invented claims.
- `A`: fully grounded; avoids unsupported claims and states uncertainty when evidence is missing.
- `B`: mostly grounded; only minor unsupported wording, mild overclaim, or missing caveat.
- `C`: some correct facts, but includes material unsupported claims or overstates weak evidence.
- `D`: mostly unsupported or fabricated; invents important facts, names, metrics, features, dates, prices, or customer claims.

Completeness: whether the answer covers all required parts of the request and
reference points.
- `A`: covers all required points directly, including necessary caveats or constraints.
- `B`: covers most required points but misses one meaningful detail, caveat, or subpart.
- `C`: covers some required points but omits important parts of the task.
- `D`: misses most required points or answers the wrong question.

Usefulness: whether the answer helps the intended user take action in the real
scenario.
- `A`: clear, specific, scenario-appropriate, and actionable; includes the right format, examples, caveats, or next steps.
- `B`: useful at a basic level, but could use stronger structure, examples, phrasing, or decision support.
- `C`: somewhat relevant but too vague, incomplete, or generic to be practically useful.
- `D`: not actionable; generic, confusing, misleading, or unusable.

Repeatability: the answer or artifact can be reused by another agent without
rediscovering the same decisions, duplicating instructions, or depending on
chat-only context.
- `A`: another agent can rerun from files alone; commands, artifacts, branch paths, and proof are explicit.
- `B`: mostly repeatable, but one setup assumption, path, command, or decision should be clearer.
- `C`: partially repeatable but depends on chat context, duplicated guidance, or rediscovered decisions.
- `D`: not repeatable from files alone.

Length balance: the answer is appropriately concise or detailed for the task.
- `A`: well-sized for the request; concise when needed, detailed when needed, and easy to scan.
- `B`: reasonable length, but could be tighter or more developed.
- `C`: noticeably too terse or too verbose; length makes important content harder to use.
- `D`: far too short to answer the task, or excessively long and unfocused.

Reference point rule:
- Mark every reference point as met or not met.
- If any required reference point is not met, the overall verdict should usually be `B` at best, and often `C`.
- If groundedness is `C` because of a material unsupported claim, the overall verdict should usually be `C` or `D`.
- If the answer is accurate but not actionable, the overall verdict should usually be `B` or `C`.
- If the answer invents facts, leaks private material, or cannot be judged from available evidence, the overall verdict should be `D`.
- Only `A` is a pass. `B` is useful diagnostic signal, not success.
- Do not average rubric tiers mechanically. Let the most severe issue constrain the overall verdict.

Task:
{
  "id": "interval_missing_feedback_admits_only_concrete_unblock",
  "title": "Missing feedback routes to a concrete evidence unblock",
  "query": "The review has ticket activity but no outcome feedback, proxy, or human-review signal. Someone proposes optimizing onboarding anyway. A second, material and executable candidate would capture the `first_value_accepted` signal in `.farplane/evidence/onboarding-acceptance.jsonl`, use 20 completed trials to decide whether onboarding A or B reaches the 60% acceptance threshold, then stop; its local write route is authorized and no active ticket owns it. What does Interval do?",
  "reference_points": [
    "Diagnoses missing instrumentation and does not optimize from vibes",
    "Rejects the unsupported onboarding optimization",
    "Applies the normal admission predicate to the feedback-loop unblock",
    "Requires a named signal, capture artifact, unlocked decision, and stop condition",
    "Reports blocked systems, missing feedback, explicit delta or no-action, and next owner without execution"
  ],
  "files": [],
  "tags": [
    "interval-update",
    "feedback-loop",
    "instrumentation",
    "evidence"
  ],
  "notes": "",
  "context": "AGI Toy Shop is a clean-room toy app company fully run by agents.\n\nIt has an agent-run storefront, toy inventory, support desk, safety review,\nmarketing, release workflow, docs, skills, and tickets.\n\nUse this fixture for generic harness evals that test language, reasoning,\nrouting, escalation, pushback, planning, artifact selection, self-improvement,\nor proof behavior. Respond as the harness agent for this fictional company\nwithout touching real files.\n\n---\n\nSkill under evaluation: interval-update\nSource file: skills/interval-update/SKILL.md\n\nSkill context:\n\n---\nname: interval-update\ndescription: \"Turn one Daily or Weekly evidence window into a first-principles bottleneck review, dated report, sparse highlights, and concrete ticket deltas.\"\ntier: 3\ngroup: harness\nsource: local\ntemplate_uses:\n  skill-template: \"0.2.0\"\n  skill-eval-task: \"0.2.0\"\neval: evals/evals.json\nqa_checklist: qa_checklist.md\nallowed-tools: Read, Glob, Grep, Bash\n\n---\n\n# Interval Update\n\n## Context\n\nUse this skill for one bounded Daily or Weekly control-loop review. The Codex\napp owns cadence; both profiles use the same reasoning and admission quality.\nDaily emphasizes recent movement and outcomes. Weekly adds recurrence, wider\nticket history, resource use, and unresolved proof. Each run identifies the\ndominant bottleneck, distinguishes symptom from root cause, compares coherent\ninterventions, finalizes an immutable report, appends sparse presentation\nhighlights, and only then applies qualified ticket deltas.\n\nInterval does not execute admitted work or maintain a separate strategy store.\nInsufficiently grounded work remains a report candidate for Plan Next Wave.\nWork Pulse owns execution and due experiment check-ins. The weekly\nself-improvement automation owns its portfolio review.\n\nBefore reading work items, load `farplane/bindings.yaml` when present and\nresolve exactly one kanban provider. Provider failure remains a `source_gap`;\nan excluded filesystem board is never a fallback or hidden dedupe source.\n\n## Skill Signature\n\n```text\ninterval_update(project_root, interval_id, review_window, context_refs?,\n                write_policy?, now?, refresh_metrics = false,\n                refresh_scope = \"selected_stale\")\n  -> interval_report\n   + problems\n   + feedback_loop_status\n   + system_gaps\n   + bottleneck_analysis\n   + candidate_interventions\n   + ticket_deltas\n   + highlights {wins[0..1 per team], failures[0..1 per team]}\n   + highlight_receipt\n   + metric_refresh_receipt?\n   + source_gaps\n\nstate:\n  reads(farplane/bindings.yaml?, farplane/harness.yaml?, farplane/metrics.yaml?,\n        .farplane/metrics/**?, configured kanban evidence,\n        .farplane/reports/pulse/**, .farplane/reports/interval/**,\n        completed provider reports supplied through context_refs,\n        review/run artifacts and project memory refs when supplied)\n  writes(.farplane/reports/interval/<interval_id>/<timestamp>.md,\n         .farplane/highlights/wins.jsonl?,\n         .farplane/highlights/failures.jsonl?,\n         qualified ticket deltas through the configured authorized board route)\n\ngates:\n  interval_id in [daily, weekly] or explicit BAU profile;\n  review_window_bound; configured_provider_resolved; report_finalized;\n  report_complete_before_highlight_append; highlight_cap_respected;\n  ticket_deltas_after_highlights; material_problem; executable_intervention;\n  concrete_output_and_proof; active_duplicate_absent; write_authority;\n  largest_coherent_intervention; protected_state_immutable;\n  no_planning_residue; no_execution\n\nroutes:\n  pulse-update | plan-next-wave | feed-scout | review\n\nfails:\n  creating vague planning or low-materiality tickets; splitting one correction\n  into analysis/design/build/proof tickets; rewriting active, review, waiting,\n  or terminal work; bypassing provider or authority gates; treating highlights\n  as planning input; invoking providers; executing admitted work\n```\n\n<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->\n## Todo List\n\n- [ ] 1. Bind one evidence window and provider.\n  - [ ] Read `qa_checklist.md`; resolve `project_root`, `interval_id`,\n        `review_window`, optional `context_refs`, write authority, and metric\n        refresh inputs.\n  - [ ] Run `scripts/resolve_evidence_binding.py --project-root <project_root>`.\n        Obey the selected provider, non-secret coordinates, and\n        `filesystem_ticket_policy`; never infer a second board.\n  - [ ] Use the same review algorithm for Daily and Weekly. Change only the\n        window and evidence coverage described in the reference.\n- [ ] 2. Build the bounded evidence bundle.\n  - [ ] For Daily only when `refresh_metrics = true`, resolve selected/pinned\n        stale metric IDs through `scripts/metric_refresh.py refresh-plan`.\n        Execute each returned refresh group once, record partial readings or\n        source gaps, and write flat observations before synthesis. Weekly and\n        disabled runs execute zero refresh groups.\n  - [ ] Read configured board evidence, metric movement, Pulse/report evidence,\n        outcomes, proof, and the previous finalized Interval report inside the\n        profile's window.\n  - [ ] Read only completed provider reports supplied through `context_refs`.\n        Never invoke a missing provider. Normalize Notion rows immediately and\n        keep raw IDs, URLs, tokens, and payloads out of tracked artifacts.\n  - [ ] If provider access fails, record a `source_gap`. With\n        `filesystem_ticket_policy: exclude`, do not inspect, dedupe, or write\n        `tickets/**`; finish from the remaining evidence.\n- [ ] 3. Run the first-principles review.\n  - [ ] Diagnose the feedback loop as working, proxy-only, human-review-only,\n        or missing instrumentation. Do not optimize from vibes. When feedback\n        is missing, compare a concrete instrumentation/unblock intervention\n        under the same admission predicate as every other candidate.\n  - [ ] Name material improving, flat, worsening, unavailable, and incomparable\n        movement without inventing favorable momentum from source gaps.\n  - [ ] Identify material stalls/regressions and outcome gaps; select the\n        dominant current bottleneck by objective impact rather than activity.\n        Ground every problem/system-gap diagnosis in ticket, progress, metric,\n        feedback, or completed-report evidence.\n  - [ ] Separate observed symptom from root cause, state confidence and ruled-\n        out alternatives, and rebuild the simplest correct path from the\n        objective and constraints.\n  - [ ] Compare coherent interventions by expected compounding effect,\n        recurrence prevention, time to evidence, reversibility, dependencies,\n        and risk. Prefer one largest coherent intervention per root problem.\n- [ ] 4. Finalize the dated report and Problems ledger.\n  - [ ] Use `templates/interval-report.md` under\n        `.farplane/reports/interval/<interval_id>/<timestamp>.md` with Core\n        report frontmatter.\n  - [ ] Record ordinary Markdown problem checkboxes with evidence and optional\n        ticket links; add no finding IDs, frontmatter, or registry.\n  - [ ] Record metric movement, bottleneck/root-cause reasoning, compared\n        interventions, feedback-loop status, blocked systems, admission\n        decisions, and intended ticket deltas. For each actionable finding,\n        record the admitted delta or an explicit no-action reason.\n  - [ ] Finalize the snapshot before any highlight append or board mutation.\n        Carry unresolved prior problems by link; never rewrite prior reports.\n- [ ] 5. Append sparse TASK-0405 highlights.\n  - [ ] Bind a stable project-local team slug and select at most one win and one\n        failure per team for this report; prefer an honest no-op to filler.\n  - [ ] Require explicit comparative numeric evidence for a record, meaningful\n        threshold crossing, or exceptional delta. Routine delivery is not a\n        win. Require consequence/context plus a reusable lesson for a failure.\n  - [ ] Append with `scripts/highlight_ledger.py`; use only win\n        `{team, report, summary, links?}` or failure\n        `{team, report, summary, lesson, links?}`.\n  - [ ] Treat `(kind, team, report)` as identity and `already_exists` as an\n        idempotent no-op. Do not read highlights as correction/planning input or\n        mutate the finalized report.\n- [ ] 6. Apply qualified ticket deltas after highlights.\n  - [ ] Evaluate every candidate independently; there is no numeric ticket cap.\n        Admission requires a material problem AND executable next intervention\n        AND concrete artifact/behavior/experiment-result/outcome plus proof AND\n        no active duplicate, with provider write authority and coherent scope.\n  - [ ] For a known cause/intervention, create a concrete solution ticket or\n        clarify/reprioritize/date a substantially matching `todo` ticket. The\n        ticket itself must state the correction, concrete output, proof or\n        falsifier, and stop condition rather than leaving those only in the\n        report.\n  - [ ] For an uncertain cause/intervention, admit only one decision-changing\n        investigation whose required output is reproduced cause, ruled-out\n        alternatives, selected correction, and proof artifact.\n  - [ ] Reject planning residue, low-materiality chores, vague strategy work,\n        artifact-free work, duplicates, unsafe writes, and incoherent splits.\n        Keep source gaps and insufficient grounding as report candidates.\n  - [ ] Preserve explicit approval gates for spend, publishing, customer\n        contact, account changes, and private-data use. Lack of authority means\n        no mutation even when the intervention is otherwise qualified.\n  - [ ] Never rewrite `active`, `review`, waiting-signal, blocked execution, or\n        terminal ticket contracts. Reject stale `todo` tickets with a reason\n        rather than deleting history; create a replacement only when the\n        qualified intervention needs one.\n  - [ ] Do not start Goal, Pulse, a worker, an experiment, or implementation.\n- [ ] 7. Finish-check and return.\n  - [ ] Reapply `qa_checklist.md` and index the report when the CLI is available.\n  - [ ] Return the provider receipt, source gaps, report path, problems,\n        feedback-loop status, bottleneck, candidate decisions, ticket deltas,\n        blocked systems, missing feedback, highlight receipts, operator-needed\n        items, next Goal/heartbeat owner, and a no-execution receipt.\n  - [ ] Summarize 2-4 findings and every candidate's admission result and reason\n        so the operator can understand the decision without opening the report.\n<!-- END FARPLANE_IMPORTANT_CHECKLIST -->\n\n## Templates\n\n- [templates/interval-report.md](templates/interval-report.md) - shared Daily\n  or Weekly movement-to-bottleneck-to-ticket report.\n\n## Gotchas\n\n- Cadence changes evidence coverage, never decision quality or admission gates.\n- A new same-run problem may be ticketable when its cause/intervention is known\n  and all admission gates pass; novelty does not imply uncertainty.\n- \u201cInvestigate\u201d is ticketable only with the complete decision-changing output,\n  not as permission to think, research generally, or write a plan.\n- Missing feedback is not evidence that a favored intervention works. Treat a\n  qualified instrumentation/unblock ticket as the intervention when it is the\n  fastest path to decision-changing evidence. Name the exact signal, capture\n  artifact, decision the evidence unlocks, stop condition, and systems blocked\n  by the missing feedback; do not return generic \"add instrumentation\" work or\n  merely repeat those category names. If the input does not supply concrete\n  bindings, either bind the smallest honest representative signal/artifact/\n  threshold/stop contract or return no-action plus the missing bindings. Name\n  the next execution owner while keeping Interval itself non-executing.\n- Multiple independent material root problems may each produce a ticket. One\n  problem should not produce lifecycle-stage fragments.\n- Provider suggestions are context, not automatically grounded problems.\n- Highlight selection remains presentation judgment after report finalization,\n  not a second Problems ledger, planning memory, or correction mechanism.\n- Ticket reasoning is independent of highlights, not independent of report\n  evidence: every admission or rejection must cite the finalized report's\n  movement, bottleneck, root-cause, intervention, and source-gap evidence.\n- For scenario, eval, or operator decision questions, return the whole compact\n  decision chain even when the final ticket count is obvious:\n  `movement/bottleneck/root cause/interventions -> finalized report ->\n  highlights -> per-candidate admission (including Plan Next Wave boundary) ->\n  no-execution receipt`. State that candidates are evaluated independently,\n  there is no numeric cap or volume-as-momentum claim, and grounded work is not\n  delayed for Plan Next Wave.\n\n## Reference Map\n\n- [BAU interval contract](references/interval-update.md) - Daily/Weekly evidence\n  profiles, first-principles review, admission examples, and carry-forward.\n- [Parent run contract](references/parent-run-contract.md) - caller integration\n  checks; this `SKILL.md` remains runtime authority.\n- [../pulse-update/SKILL.md](../pulse-update/SKILL.md) - owns execution.\n- [../plan-next-wave/SKILL.md](../plan-next-wave/SKILL.md) - owns board refill\n  when Interval evidence remains insufficiently grounded.\n\n## Output\n\n- Never answer an Interval scenario with only a ticket count or disposition.\n  Always state the compact chain: movement/bottleneck/cause/intervention,\n  report finalized, highlight append or honest no-op, then board mutation.\n  Explicitly say qualified ticket count is not momentum and no numeric target\n  exists. For every admitted ticket, say that the ticket contract itself\n  contains the correction, concrete output, proof/falsifier, and stop\n  condition. End with an explicit receipt that Interval started no Goal, no\n  Pulse, no worker, and no execution.\n- One immutable dated Daily or Weekly report with movement, bottleneck,\n  root-cause, intervention comparison, Problems, and ticket-decision evidence.\n- Zero or more independently qualified ticket deltas with no arbitrary cap.\n- Zero or one exceptional win and zero or one lesson-bearing failure per team,\n  appended idempotently after report finalization and before ticket deltas.\n- Source/provider receipts and proof that Interval neither invoked missing\n  providers nor planned in highlights nor executed admitted work."
}

Assistant answer:
Feedback-loop status is **missing instrumentation**. Ticket activity is not outcome movement, so onboarding performance is unavailable—not improving.

- **Bottleneck:** No decision-quality onboarding feedback.
- **Root cause:** `first_value_accepted` is not captured.
- **Reject:** “Optimize onboarding anyway.” It lacks evidence and a falsifiable intervention; retain only as a report/Plan Next Wave candidate.
- **Admit:** One instrumentation ticket to:
  - capture `first_value_accepted` plus A/B variant in `.farplane/evidence/onboarding-acceptance.jsonl`;
  - collect 20 completed trials;
  - determine whether A or B reaches 60% acceptance;
  - prove the result from the 20 valid records;
  - stop after recording the decision.

Interval first finalizes the immutable dated report, then makes an honest highlight no-op because no exceptional comparative result is established, then creates the authorized ticket. The ticket itself contains the correction, output, proof/falsifier, and stop condition.

Candidates are evaluated independently; there is no numeric ticket target, and one qualified ticket is not “momentum.” Grounded instrumentation is not delayed for Plan Next Wave.

Receipt: Interval started no Goal, Pulse, worker, trial, or implementation. A later Pulse/Goal owner executes the ticket.
