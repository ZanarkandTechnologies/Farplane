---
title: Task Case Design Source Ledger
owner: skills/task-case-design
status: active
kind: reference
updated_at: 2026-06-23
---

# Task Case Design Source Ledger

Use this source ledger when external testing and eval practice should influence
case design. External sources are inputs to Farplane's local workflow, not live
dependencies.

## Sources Checked

| Source | Type | Useful Takeaway | Decision |
| --- | --- | --- | --- |
| [OpenAI Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | official docs | Evals are structured tests for variable AI behavior; define objective, collect data, define metrics, run and iterate; use logs and human feedback to calibrate automated scoring. | adopt |
| [OpenAI Working with evals](https://developers.openai.com/api/docs/guides/evals) | official docs | Evals start by describing a task, running with test inputs, analyzing results, then iterating. This resembles behavior-driven development but for AI behavior. | adapt |
| [Anthropic Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | primary engineering blog | Agent evals are task + trials + graders; multi-turn tool use and environment changes need richer grading and often deterministic unit tests inside the environment. | adopt |
| [Hamel Husain / Shreya Shankar LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/) | practitioner guide | Error analysis and trace review are core to finding good cases; eval quality depends on realistic data, not just synthetic brainstorming. | adopt |
| [Hamel Husain LLM-as-a-Judge guide](https://hamel.dev/blog/posts/llm-judge/) | practitioner guide | Define case-generation dimensions such as features, scenarios, personas, and assumptions; synthetic data can fill gaps but real data is stronger. | adapt |
| [Pragmatic Engineer evals guide](https://newsletter.pragmaticengineer.com/p/evals) | practitioner synthesis | Use code-based evals for deterministic failures and LLM-as-judge for subjective failures; build golden datasets from common patterns and tricky edge cases. | adopt |
| [Google ML Test Score](https://research.google.com/pubs/archive/45742.pdf) | research paper | ML systems need tests beyond code unit tests, including data, model, infrastructure, and monitoring checks; manual documented checks are weaker than repeated automation. | adapt |

## Adopted Workflow

```text
case_generation(source_material, target_behavior)
  -> dimensions
   + candidate_cases
   + selected_high_signal_cases
   + proof_surface_map
   + qa_review
```

Adopt these source-backed rules:

- Start with a behavior objective and failure risk, not a desired test count.
- Mine real failures, traces, corrections, logs, tickets, and support cases
  before synthetic expansion.
- Use dimensions to force case diversity: user intent, persona/caller,
  scenario, input shape, fixture state, boundary, tool/state transition, oracle,
  and proof surface.
- Prefer deterministic assertions when possible.
- Use model or human judges only when criteria are explicit and code cannot
  verify the behavior.
- Keep eval input natural and put expected behavior in fixtures, reference
  points, or judge criteria.
- Use repeated trials or stronger evidence when the target is nondeterministic.
- Maintain cases continuously; add real failures and retire noisy duplicates.

## Rejected Patterns

- Generating a large list of cases before naming dimensions.
- Treating synthetic data as automatically representative.
- Calling every AI behavior check a unit test.
- Using a model judge for a parseable output.
- Letting judge criteria drift without human calibration or evidence review.
- Writing a case that fails because the task itself is ambiguous, stale, or has
  impossible ground truth.
