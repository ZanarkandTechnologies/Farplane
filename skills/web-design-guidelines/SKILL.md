---
name: web-design-guidelines
version: 1.0.0
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
tier: 2
source: local
---

# Web Interface Guidelines

<!-- BEGIN CODEXTER_IMPORTANT_CHECKLIST -->
## Important Checklist

Source: `SKILL.md`

- [ ] Identify the UI source files, route, component, or diff being audited.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to keep the
  audit tied to the current source files and latest guideline source.
- [ ] Fetch or load the current Web Interface Guidelines before judging the
  code; do not rely on stale memory of the rules.
- [ ] Inspect the relevant source for accessibility, focus, forms, navigation,
  animation, responsive behavior, content semantics, and interface basics.
- [ ] Report findings in terse `file:line` format with severity and actionable
  correction.
- [ ] Keep raw guideline findings separate from any broader review rubric score.
- [ ] Use [review](../review/SKILL.md) when the audit feeds a material quality
  or completion claim.
<!-- END CODEXTER_IMPORTANT_CHECKLIST -->

Review files for compliance with Web Interface Guidelines.

This skill is the source-fresh standards audit lane for frontend work. It can be
called directly by the user, by `frontend-craft` after UI implementation, or by
`review/references/frontend-guidelines.md` when a frontend review needs a
separate measurable guideline score.

## How It Works

1. Fetch the latest guidelines from the source URL below
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format

## Guidelines Source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules. The fetched content contains all the rules and output format instructions.

## Usage

When a user provides a file or pattern argument:
1. Fetch guidelines from the source URL above
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format specified in the guidelines

If no files specified, ask the user which files to review.

## Review Integration

When used inside `review`, keep this skill's raw findings separate from the
anchored review score. The review lane converts findings into the
`frontend-guidelines` score while this skill stays focused on fetching and
applying the latest source rules.

## Reference Files

- [architecture.md](references/architecture.md) - source-fresh audit boundary.
- [workflows.md](references/workflows.md) - direct audit and review-metric paths.
- [gotchas.md](references/gotchas.md) - stale-rule and over-scoring failures.
