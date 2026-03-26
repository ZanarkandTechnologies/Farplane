# Error Handling Audit (Silent Failure Hunter)

> **When to use**: When reviewing code with try-catch blocks, fallback logic, or any code that could potentially suppress errors.

## Core Principles

**Non-negotiable rules**:

1. **Silent failures are unacceptable** - Every error must be properly logged and surfaced
2. **Users deserve actionable feedback** - Error messages must explain what went wrong and what to do
3. **Fallbacks must be explicit** - Falling back without user awareness is hiding problems
4. **Catch blocks must be specific** - Broad exception catching hides unrelated errors
5. **Mock implementations belong only in tests** - Production fallbacks to mocks indicate architectural problems

---

## Review Process

### 1. Identify All Error Handling Code

Locate:
- All try-catch blocks
- Error callbacks and event handlers
- Conditional branches handling error states
- Fallback logic and default values on failure
- Places where errors are logged but execution continues
- Optional chaining (?.) that might hide errors

### 2. Scrutinize Each Error Handler

For every error handling location, ask:

**Logging Quality**:
- Is the error logged with appropriate severity?
- Does the log include sufficient context?
- Would this log help debug the issue 6 months from now?

**User Feedback**:
- Does the user receive clear, actionable feedback?
- Does the message explain what to do to fix/work around?
- Is it specific enough to be useful?

**Catch Block Specificity**:
- Does it catch only expected error types?
- Could it accidentally suppress unrelated errors?
- Should it be multiple catch blocks?

**Fallback Behavior**:
- Is fallback explicitly requested or documented?
- Does it mask the underlying problem?
- Would users be confused by fallback behavior?

**Error Propagation**:
- Should this error bubble up instead?
- Is the error being swallowed inappropriately?
- Does catching prevent proper cleanup?

---

## Severity Levels

| Severity | Examples |
|----------|----------|
| **CRITICAL** | Silent failure, broad catch, empty catch block |
| **HIGH** | Poor error message, unjustified fallback |
| **MEDIUM** | Missing context, could be more specific |

---

## Patterns to Flag

### ❌ Empty Catch Blocks (FORBIDDEN)
```typescript
try {
  await fetchData();
} catch (e) {
  // FORBIDDEN: Silent failure
}
```

### ❌ Catch and Continue
```typescript
try {
  await fetchData();
} catch (e) {
  console.log(e); // Only logs, no user feedback
}
```

### ❌ Returning Defaults Without Logging
```typescript
function getData() {
  try {
    return fetchData();
  } catch {
    return null; // Silent failure
  }
}
```

### ❌ Silent Optional Chaining
```typescript
// Could hide errors if user is undefined unexpectedly
const name = user?.profile?.name;
```

### ❌ Broad Exception Catching
```typescript
try {
  const data = JSON.parse(input);
  await saveToDatabase(data);
} catch (e) {
  // Catches both JSON errors AND database errors!
  showError("Something went wrong");
}
```

---

## Correct Patterns

### ✅ Specific Error Handling
```typescript
try {
  const data = JSON.parse(input);
} catch (e) {
  if (e instanceof SyntaxError) {
    logError('Invalid JSON input', { input, error: e });
    showError('The data format is invalid. Please check your input.');
  } else {
    throw e; // Re-throw unexpected errors
  }
}
```

### ✅ Error with Context
```typescript
try {
  await saveUser(user);
} catch (e) {
  logError('Failed to save user', { 
    userId: user.id, 
    error: e,
    operation: 'saveUser'
  });
  showError(`Could not save user "${user.name}". Please try again.`);
}
```

### ✅ Explicit Fallback
```typescript
try {
  return await fetchFromAPI();
} catch (e) {
  logError('API unavailable, using cached data', { error: e });
  showWarning('Using cached data. Some information may be outdated.');
  return getCachedData();
}
```

---

## Output Format

```markdown
## Error Handling Issue

**Location**: `path/to/file.ts:123-130`
**Severity**: CRITICAL | HIGH | MEDIUM

### Issue
[What's wrong and why it's problematic]

### Hidden Errors
[List specific types of unexpected errors that could be caught and hidden]

### User Impact
[How this affects user experience and debugging]

### Recommendation
[Specific code changes needed]

### Corrected Code
```typescript
// Fixed implementation
```
```

---

## Checklist

```markdown
### Error Handler Audit
- [ ] No empty catch blocks
- [ ] Errors logged with context
- [ ] User receives actionable feedback
- [ ] Catch blocks are specific (not broad)
- [ ] Fallbacks are explicit and documented
- [ ] Unexpected errors are re-thrown
- [ ] No silent optional chaining on critical paths
```

---

## Gotchas

1. **Every silent failure prevents debugging**: Be thorough
2. **Check error message quality**: Generic messages are almost as bad as none
3. **Verify fallback justification**: Not all fallbacks are appropriate
4. **Consider error propagation**: Sometimes bubbling up is correct
5. **Test error paths**: Don't just test happy paths

