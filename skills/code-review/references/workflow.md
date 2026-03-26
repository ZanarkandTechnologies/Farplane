# PR Review Workflow

> **When to use**: Comprehensive review before creating a PR or after completing a feature.

## Review Aspects

| Aspect | Focus | When Applicable |
|--------|-------|-----------------|
| **code** | Project guidelines, bugs, style | Always |
| **errors** | Silent failures, catch blocks | Code with error handling |
| **types** | Type design and invariants | New/modified types |
| **simplify** | Clarity and maintainability | After passing other reviews |

---

## Workflow Steps

### 1. Determine Review Scope

```bash
# Check changed files
git diff --name-only

# Or for staged changes
git diff --staged --name-only

# Check if PR exists
gh pr view
```

### 2. Identify Applicable Reviews

Based on changes:
- **Always**: Code quality review
- **If test files changed**: Test coverage review
- **If error handling changed**: Error handling audit
- **If types added/modified**: Type design analysis
- **After passing**: Simplification pass

### 3. Run Reviews Sequentially

**Order matters**:
1. Code quality (catch obvious issues first)
2. Error handling (security and reliability)
3. Type design (if applicable)
4. Simplification (polish after passing)

### 4. Aggregate Results

```markdown
# PR Review Summary

## Critical Issues (X found)
- **[Aspect]**: Issue description
  - File: `path/to/file.ts:123`
  - Fix: [Recommendation]

## Important Issues (X found)
- **[Aspect]**: Issue description
  - File: `path/to/file.ts:45`
  - Fix: [Recommendation]

## Suggestions (X found)
- **[Aspect]**: Suggestion [file:line]

## Strengths
- What's well-done in this PR

## Recommended Action
1. Fix critical issues first
2. Address important issues
3. Consider suggestions
4. Re-run review after fixes
```

---

## Workflow Integration

### Before Committing
```
1. Write code
2. Run: code-quality + error-handling
3. Fix any critical issues
4. Commit
```

### Before Creating PR
```
1. Stage all changes
2. Run: ALL reviews
3. Address all critical and important issues
4. Run specific reviews again to verify
5. Create PR
```

### After PR Feedback
```
1. Make requested changes
2. Run targeted reviews based on feedback
3. Verify issues are resolved
4. Push updates
```

---

## Quick Commands

### Full Review
```bash
# Review all changed files
git diff --name-only | head -20

# Then run each review aspect
```

### Specific Aspects
```bash
# Only error handling
# Focus on files with try-catch, error callbacks

# Only type design
# Focus on files with new type definitions
```

---

## Review Depth Guidelines

### Quick Review (5-10 min)
- Code quality check only
- Focus on obvious issues
- Good for small changes

### Standard Review (15-30 min)
- Code quality + error handling
- Good for most features

### Deep Review (30-60 min)
- All aspects including type design
- Good for critical features, new systems

---

## Tips

1. **Run early**: Before creating PR, not after
2. **Focus on changes**: Review git diff, not entire files
3. **Address critical first**: Fix high-priority before low
4. **Re-run after fixes**: Verify issues are resolved
5. **Use specific reviews**: Target aspects when you know the concern

---

## Integration with Base Loop

```
Plan → Execute → REVIEW → HITL
                   │
    ┌──────────────┼──────────────┐
    ↓              ↓              ↓
Code Quality  Error Handling  Type Design
    │              │              │
    └──────────────┴──────────────┘
                   ↓
            Simplification
                   ↓
               Summary
                   ↓
                 HITL
```

---

## Checklist

```markdown
### PR Review Checklist

#### Pre-Review
- [ ] Identified all changed files
- [ ] Determined applicable review aspects
- [ ] Read CLAUDE.md/project guidelines

#### Code Quality
- [ ] No style violations
- [ ] No obvious bugs
- [ ] Tests adequate

#### Error Handling
- [ ] No empty catch blocks
- [ ] Errors logged with context
- [ ] User feedback appropriate

#### Type Design (if applicable)
- [ ] Invariants enforced
- [ ] Encapsulation proper
- [ ] No anemic models

#### Simplification
- [ ] No unnecessary complexity
- [ ] No nested ternaries
- [ ] Names are descriptive

#### Post-Review
- [ ] Critical issues fixed
- [ ] Important issues addressed
- [ ] Re-verified after fixes
```

