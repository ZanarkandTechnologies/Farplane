# Human-Feedback Preset

Load when Kenji's judgment is the fastest honest quality signal for an
optimization loop (content, skills, creative artifacts, offers, demos, UI,
taste) before a benchmark or market test exists. One-off approval goes to chat,
`review`, or `telegram-message`; correctness goes to QA. The [metric card](metrics.md)
already lists `human_feedback` as a signal class; this file owns only the loop
protocol.

## Program binding

```text
loop_shape: optimization | skill_improvement
metric_provider: human_feedback
feedback_channel: telegram          # fallback: local feedback-request.md
feedback_policy: ask_when_artifact_ready
phase: planning | execution
approved_plan_ref: <required for execution unless a tiny planning test>
worker_thread_ref: <thread that receives replies, when replies resume work>
founder_lens: true for product, content, distribution, or offer bets
state_surfaces: ticket.md + program.md + progress.md + hypothesis-tree.json?
```

When a worker packet already exists, bind this inside its `program.md`; do not
create a second packet. Add `hypothesis-tree.json` only for a multi-turn
experiment-backed campaign; a one-off request omits it.

## Rules

- **Reply path.** When Telegram replies should resume the job, send from the
  dedicated worker thread or a named `worker_thread_ref`, never from a parent
  heartbeat. With no worker thread, return that handoff requirement instead of
  sending.
- **Phase-appropriate artifacts.** Planning feedback needs a proposal Kenji can
  judge: audience or buyer, insight, artifact shape, core angle, execution
  beats, why it could win, what would make it cringe, references, the
  question, and next step if approved. A hook alone is valid only when the hook
  is what is being judged. Execution feedback implements an approved plan.
- **Founder lens.** For bets, name customer, problem, wedge, offer or artifact,
  distribution angle, validation question, and what feedback would change the
  next bet. Ask "would this make you want to build, sell, or test this?", not
  "is this good?".
- **One small question.** Ask for the fastest judgment that suffices: `score`
  (small bounded scale), `decision` (keep/revise/reject/approve),
  `observation`, or `ranking`. Never make Kenji write the next prompt.
- **Ranking is a signal, not the selector.** The next hypothesis is chosen by
  `choose_next` ([choose-next](choose-next.md)); human ranking scores the
  selected experiment.
- **Harden slowly.** A first rejection perturbs the local attempt. Use
  `promotion_decision: keep_local | rerun | harden_skill | discard`, and
  reserve `harden_skill` for repeated same-phase failure or a reusable approved
  pattern.
- **No authority from feedback.** Feedback never authorizes publishing,
  spending, contacting people, or external promises.

## Turn exit gate

Before every stop, exactly one holds:

```text
waiting_for_feedback: Telegram send proven | fallback request path shown | blocker
feedback_processed_non_terminal: next artifact + next request sent | blocker
terminal: keep | approve | convergence | budget | blocker, recorded in progress.md
```

A `revise` or `reject` reply needs the corrected understanding and the next
operator-facing action, not only "feedback recorded".

## Writeback

Before the request, append to `progress.md`: phase, current hypothesis,
planned attempt, artifact refs, question, expected signal, and any
`skill_delta_candidate`. After the reply, update the tree node first (when
present), then append the human signal, learning, next hypothesis, and
promotion decision.

## Templates

```json
{
  "artifact_id": "run-1",
  "score": 8,
  "verdict": "keep | revise | reject | approve",
  "feedback": "Short reason.",
  "labels": [],
  "next_instruction": "What the next Goal turn should do."
}
```

Use `score: null` for qualitative feedback. The request (`feedback-request.md`
under the ticket artifacts, also sent via `telegram-message`) carries: target,
objective, worker thread, artifact refs, proposal summary, one question, the
`feedback.json` path, and this schema.
