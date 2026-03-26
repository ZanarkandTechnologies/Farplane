---
name: code-review
version: 1.0.0
description: Comprehensive code review skill covering quality checks, simplification, error handling analysis, and type design. Use after completing a feature or before creating a PR.
allowed-tools: Bash, Glob, Grep, Read, Write, Edit, Task
---

# Code Review Skill

> **Purpose**: Ensure code quality through systematic review of adherence to project guidelines, error handling, type design, and simplification before merging.

## What Reference Do I Need?

| I'm doing... | Load this |
|--------------|-----------|
| General code quality check | [code-quality.md](references/code-quality.md) |
| Simplifying complex code | [simplification.md](references/simplification.md) |
| Auditing error handling | [error-handling.md](references/error-handling.md) |
| Reviewing type design | [type-design.md](references/type-design.md) |
| Full PR review workflow | [workflow.md](references/workflow.md) |

---

## Quick Start

### Before Committing
```bash
# Review code quality and error handling
git diff --name-only  # See changed files
# Then run code-quality and error-handling checks
```

### Before Creating PR
```bash
# Full review: all aspects
# 1. code-quality
# 2. error-handling
# 3. type-design (if new types added)
# 4. simplification (polish after passing review)
```

---

## Review Aspects

| Aspect | Focus | When to Use |
|--------|-------|-------------|
| **Code Quality** | Project guidelines, bugs, style | Always |
| **Error Handling** | Silent failures, catch blocks | Code with try/catch, fallbacks |
| **Type Design** | Invariants, encapsulation | New or modified types |
| **Simplification** | Clarity, maintainability | After passing other reviews |

---

## Confidence Scoring

Rate each issue from 0-100:

| Score | Meaning |
|-------|---------|
| 0-25 | Likely false positive or pre-existing |
| 26-50 | Minor nitpick not in guidelines |
| 51-75 | Valid but low-impact |
| 76-90 | Important issue requiring attention |
| 91-100 | Critical bug or explicit guideline violation |

**Only report issues with confidence ≥ 80**

---

## Issue Severity

| Severity | Score | Action |
|----------|-------|--------|
| **Critical** | 90-100 | Must fix before merge |
| **Important** | 80-89 | Should fix |
| **Suggestion** | 50-79 | Nice to have |

---

## Output Format

```markdown
# Code Review Summary

## Critical Issues (X found)
- **[Aspect]**: Issue description
  - File: `path/to/file.ts:123`
  - Confidence: 95
  - Fix: [Specific recommendation]

## Important Issues (X found)
- **[Aspect]**: Issue description
  - File: `path/to/file.ts:45`
  - Confidence: 85
  - Fix: [Specific recommendation]

## Suggestions (X found)
- **[Aspect]**: Suggestion [file:line]

## Strengths
- What's well-done in this code

## Recommended Action
1. Fix critical issues first
2. Address important issues
3. Consider suggestions
4. Re-run review after fixes
```

---

## Integration with Base Loop

The code review step fits into the base workflow:

```
Plan → Execute → REVIEW → HITL
                   ↑
            You are here
```

**Review Phase**:
1. Run code-quality check
2. Run error-handling audit
3. Run type-design analysis (if applicable)
4. Run simplification pass
5. Summarize findings
6. Fix critical/important issues
7. Re-run until clean

---

## Reference Files

- [code-quality.md](references/code-quality.md) - Project guideline compliance, bug detection
- [simplification.md](references/simplification.md) - Code clarity and maintainability
- [error-handling.md](references/error-handling.md) - Silent failure detection
- [type-design.md](references/type-design.md) - Type invariants and encapsulation
- [workflow.md](references/workflow.md) - Full PR review orchestration

---

## Anti-Patterns to Flag

### Code Quality
- Style violations (imports, naming, declarations)
- Logic errors, null handling, race conditions
- Missing error handling, accessibility issues

### Error Handling
- Empty catch blocks (FORBIDDEN)
- Catch blocks that only log and continue
- Silent failures without user feedback
- Broad exception catching

### Type Design
- Anemic domain models
- Types exposing mutable internals
- Invariants enforced only by documentation
- Missing validation at construction

### Code Complexity
- Nested ternary operators
- Overly clever one-liners
- Too many concerns in one function
- Unnecessary abstractions

