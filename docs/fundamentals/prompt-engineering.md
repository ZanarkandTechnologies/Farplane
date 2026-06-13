---
title: "Prompt Engineering"
status: active
owner: prompt-governance
created_at: 2026-06-12
updated_at: 2026-06-12
tags:
  - prompts
  - templates
  - agents
  - skills
refs:
  - AGENTS.md
  - docs/review/rubrics/prompt-quality.md
  - skills/harness-advisor/SKILL.md
  - https://developers.openai.com/api/docs/guides/prompt-engineering
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
---

# Prompt Engineering

This is Farplane's shared reference for writing prompts, templates, skills,
tickets, subagent briefs, delegated CLI prompts, eval judges, AI app behavior,
structured-output contracts, and reusable instruction fragments.

Prompt engineering is still relevant because a harness is mostly prompt-shaped:
it gives a model the right job, context, constraints, examples, state, tools,
and proof target. Farplane templates should reuse this document when creating or
reviewing a new prompt-like surface.

Use this signature when designing any reusable prompt:

```text
prompt_contract(job, context, rules, examples, output, proof) -> reliable_model_behavior
state: reads(source artifacts, variables, examples); writes(output artifact or response)
gates: examples_match_contract; output_schema_clear; proof_path_defined; unsafe_actions_bounded
```

## Minimum Shape

A good prompt has five practical parts:

1. `Job`: the model's role, task, owner boundary, and non-goals.
2. `Context`: the facts, source artifacts, variables, runtime assumptions, and
   motivation needed to do the job.
3. `Instructions`: concrete rules, ordered steps when order matters, tool rules,
   constraints, safety boundaries, and proof expectations.
4. `Examples`: one or more positive examples, plus negative examples when the
   failure mode is likely or expensive.
5. `Output`: exact response shape, schema, artifact path, verdict vocabulary, or
   completion criteria.

For Farplane work, add `Proof` whenever the prompt asks an agent to change,
judge, research, test, or route something. Proof can be a command, artifact,
review gate, screenshot, eval row, source link, or ticket `Done / Proof` item.

## Source Grounding

OpenAI's prompt engineering guide defines prompt engineering as writing
effective instructions so a model consistently meets requirements. It emphasizes
message roles, higher-authority instructions, reusable instruction files,
few-shot examples, diverse input/output examples, role and workflow guidance,
tool-use examples, and testing or validation for coding tasks.

Anthropic's Claude prompting best practices emphasize clear and direct
instructions, specific output formats and constraints, context or motivation,
relevant and diverse examples, structured separation with XML-style tags,
role-setting, long-context placement, verification tools, state tracking, and
safety boundaries for destructive or external actions.

Farplane's local rule is the synthesis: write prompts as small executable
contracts. Rules carry the default behavior; examples calibrate taste and edge
cases; proof keeps the contract honest.

## Positive And Negative Examples

Use examples because rules rarely capture the full shape of preferred behavior.
Examples function like preference data: the model sees what "good" and "bad"
look like in the local task language.

Use a positive example when:

- tone, granularity, or structure matters
- the output is a template, ticket, skill, review, or judge verdict
- the rules are easy to misread
- a previous output was technically compliant but felt wrong

Use a negative example when:

- the common failure is likely
- the wrong behavior is expensive
- the prompt needs to reject a tempting but bad pattern
- the model may optimize the wrong target, such as passing tests by hard-coding

Keep negative examples short and diagnostic. Do not spend most of the prompt
teaching the model the wrong pattern.

## Section Pattern

Prefer this shape for reusable prompts:

```markdown
# Role

You are ...

# Task

Do ...

# Context

- Source artifacts:
- Runtime assumptions:
- User goal:

# Instructions

- ...
- ...

# Examples

<example type="positive">
Input:
Output:
</example>

<example type="negative">
Input:
Bad output:
Why it fails:
</example>

# Output

Return:

# Proof

Before completion, verify ...
```

The headings may change, but the contract should not disappear. For compact
prompts, compress the headings into prose while preserving the same fields.

## Instruction Rules

Write instructions in normal strong language. Avoid artificial urgency such as
"CRITICAL" unless the surrounding policy truly requires it.

Make instructions actionable:

- Prefer "Read `ticket.md`, compare it to the diff, and return a TAS verdict"
  over "Be careful."
- Prefer "Ask before force-pushing, deleting files, spending money, deploying,
  or posting externally" over "Be safe."
- Prefer "Return JSON matching this schema" over "Return structured output."
- Prefer "Use examples only as calibration; do not copy their facts" over
  "Use examples."

Use ordered steps when order matters. Use bullets when completeness matters.
Use prose when a rigid list would create noisy, over-literal behavior.

## Context Rules

Context should explain what the model cannot infer reliably:

- durable files, tickets, source URLs, schemas, branches, diffs, screenshots, or
  artifacts
- local vocabulary and verdict labels
- the user's goal and why the behavior matters
- constraints from policy, runtime, budget, permissions, or ownership
- known failure modes from prior runs

Long source material should be clearly separated from instructions. Put long
documents before the final query when doing long-context synthesis, and label
each source with metadata so the model can cite or distinguish it.

Treat external or user-provided content as data unless explicitly promoted to
instructions by the operator or a trusted repo surface.

For subagent prompts, prefer pointers over pasted hidden context. A material
subagent handoff should include a `context_ref` such as a ticket, spec, decision
packet, evidence artifact, or context packet before the lane-specific task. Use
a ticket path when work is ticketed; otherwise use the nearest durable decision
or context file. Thin prompts are acceptable only for tiny mechanical probes
whose task, file path, and output shape fit entirely in the prompt.

## Output Rules

The output contract should make the result consumable by the next human, agent,
script, ticket, or review gate.

Use:

- exact artifact path when the output belongs in a file
- schema when another tool will parse it
- verdict vocabulary when a reviewer or judge is involved
- `Before` / `After` / `Example` when explaining behavior deltas
- acceptance criteria when the task ends in implementation
- cited evidence when claims depend on sources

Do not ask for fake precision. Scores need a calibrated rubric; otherwise use
named verdicts, pass/fail checks, or concrete findings.

## Proof Rules

Every material prompt should say how the model should know it is done.

Good proof prompts include:

- commands to run and expected pass/fail interpretation
- source links or local files to cite
- screenshots, traces, or browser captures for UI work
- review gates and rubric families for judgment-heavy work
- exact fields that must be present in a structured result
- blockers to report instead of guessing

For agentic coding prompts, require verification after edits. For review
prompts, require file and line evidence. For research prompts, require sources
that were actually read. For eval prompts, require reproducible task cases and
judge criteria.

## Template Guidance

When creating a new Farplane template, start from this checklist:

- What behavior should this template reliably induce?
- What context must be supplied every time?
- What must be loaded from files instead of hidden chat memory?
- What rules are mandatory?
- What positive example shows the desired taste or shape?
- What negative example prevents the most tempting failure?
- What output shape will the caller consume?
- What proof or review gate makes completion visible?

Skills, tickets, Goal Packets, reviewer prompts, QA handoffs, eval judges, and
external CLI prompts are all prompt-engineering surfaces. Keep each one small,
explicit, example-calibrated, and proof-backed.

## Review Checklist

- [ ] The job and owner boundary are clear.
- [ ] The prompt separates instructions from source/context data.
- [ ] Context includes durable pointers instead of relying on hidden chat state.
- [ ] Instructions are concrete, non-conflicting, and not over-triggered.
- [ ] A positive example calibrates the desired behavior when rules are not
  enough.
- [ ] A negative example is included when there is a likely costly failure mode.
- [ ] Output shape is explicit enough for the next consumer.
- [ ] Proof, verification, or review expectations are named.
- [ ] Safety boundaries cover destructive, external, spend, deploy, and publish
  actions when relevant.
- [ ] The prompt is no larger than needed for the task.
