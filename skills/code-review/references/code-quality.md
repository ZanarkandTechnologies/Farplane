# Code Quality Review

> **When to use**: Always, for every code change. Ensures adherence to project guidelines with high precision to minimize false positives.

## Review Scope

By default, review unstaged changes from `git diff`. User may specify different files.

---

## Core Review Responsibilities

### 1. Project Guidelines Compliance

Verify adherence to explicit project rules (typically in CLAUDE.md):
- Import patterns and sorting
- Framework conventions
- Language-specific style
- Function declarations
- Error handling patterns
- Logging practices
- Testing practices
- Platform compatibility
- Naming conventions

### 2. Bug Detection

Identify actual bugs that will impact functionality:
- Logic errors
- Null/undefined handling
- Race conditions
- Memory leaks
- Security vulnerabilities
- Performance problems

### 3. Code Quality

Evaluate significant issues:
- Code duplication
- Missing critical error handling
- Accessibility problems
- Inadequate test coverage

---

## Confidence Scoring

Rate each issue from 0-100:

| Score | Meaning |
|-------|---------|
| 0-25 | Likely false positive or pre-existing issue |
| 26-50 | Minor nitpick not explicitly in guidelines |
| 51-75 | Valid but low-impact issue |
| 76-90 | Important issue requiring attention |
| 91-100 | Critical bug or explicit guideline violation |

**Only report issues with confidence ≥ 80**

---

## Output Format

Start by listing what you're reviewing. For each high-confidence issue:

```markdown
## Issue: [Description]
- **Confidence**: X/100
- **File**: `path/to/file.ts:123`
- **Rule**: [Specific guideline or bug explanation]
- **Fix**: [Concrete fix suggestion]
```

Group issues by severity:
- **Critical**: 90-100
- **Important**: 80-89

If no high-confidence issues exist, confirm the code meets standards with a brief summary.

---

## Common Patterns to Check

### TypeScript/JavaScript
- [ ] ES modules with proper import sorting
- [ ] Prefer `function` keyword over arrow functions (if project standard)
- [ ] Explicit return type annotations
- [ ] Proper React component patterns with Props types
- [ ] Consistent naming conventions

### Error Handling
- [ ] No empty catch blocks
- [ ] Errors logged appropriately
- [ ] User-facing error messages are helpful

### Testing
- [ ] Tests cover happy path
- [ ] Tests cover edge cases
- [ ] Tests are behavioral, not implementation-focused

---

## Review Checklist

```markdown
### Project Guidelines
- [ ] Import patterns correct
- [ ] Naming conventions followed
- [ ] File structure appropriate

### Bug Risk
- [ ] No null/undefined issues
- [ ] No race conditions
- [ ] No memory leaks

### Quality
- [ ] No code duplication
- [ ] Error handling present
- [ ] Tests adequate
```

---

## Gotchas

1. **Filter aggressively**: Quality over quantity. Focus on issues that truly matter.
2. **Be specific**: Include file paths and line numbers.
3. **Be actionable**: Provide concrete fix suggestions.
4. **Check context**: Ensure issues are in changed code, not pre-existing.

