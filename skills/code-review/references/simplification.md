# Code Simplification

> **When to use**: After code passes other reviews. Enhances clarity, consistency, and maintainability while preserving exact functionality.

## Core Principles

### 1. Preserve Functionality
Never change what the code does—only how it does it. All original features, outputs, and behaviors must remain intact.

### 2. Apply Project Standards
Follow established coding standards:
- ES modules with proper import sorting
- Prefer `function` keyword over arrow functions (if standard)
- Explicit return type annotations
- Proper React component patterns
- Consistent naming conventions

### 3. Enhance Clarity
Simplify code structure by:
- Reducing unnecessary complexity and nesting
- Eliminating redundant code and abstractions
- Improving variable and function names
- Consolidating related logic
- Removing obvious-code comments

**CRITICAL**: Avoid nested ternary operators—prefer switch statements or if/else chains.

### 4. Maintain Balance
Avoid over-simplification that could:
- Reduce clarity or maintainability
- Create overly clever solutions
- Combine too many concerns
- Remove helpful abstractions
- Prioritize "fewer lines" over readability
- Make code harder to debug

### 5. Focus Scope
Only refine recently modified code unless instructed otherwise.

---

## Refinement Process

1. **Identify** recently modified code sections
2. **Analyze** for opportunities to improve elegance
3. **Apply** project-specific best practices
4. **Ensure** all functionality remains unchanged
5. **Verify** refined code is simpler and more maintainable
6. **Document** only significant changes

---

## Simplification Patterns

### Remove Unnecessary Complexity

**Before**:
```typescript
const result = data ? (data.value ? data.value.toString() : '') : '';
```

**After**:
```typescript
const result = data?.value?.toString() ?? '';
```

### Consolidate Related Logic

**Before**:
```typescript
const firstName = user.firstName;
const lastName = user.lastName;
const fullName = firstName + ' ' + lastName;
```

**After**:
```typescript
const fullName = `${user.firstName} ${user.lastName}`;
```

### Replace Nested Ternaries

**Before**:
```typescript
const status = isLoading ? 'loading' : hasError ? 'error' : 'success';
```

**After**:
```typescript
function getStatus(isLoading: boolean, hasError: boolean): string {
  if (isLoading) return 'loading';
  if (hasError) return 'error';
  return 'success';
}
```

### Eliminate Redundant Abstractions

**Before**:
```typescript
function getUser() {
  return fetchUser();
}
const user = getUser();
```

**After**:
```typescript
const user = fetchUser();
```

---

## Anti-Patterns to Avoid

### ❌ Over-Compression
```typescript
// Too clever
const x = a ? b ? c : d : e ? f : g;
```

### ❌ Unnecessary Abstractions
```typescript
// One-use wrapper
const wrappedFetch = (url) => fetch(url);
```

### ❌ Combining Too Many Concerns
```typescript
// Does too much
function fetchAndParseAndValidateAndStore(url) { ... }
```

### ❌ Dense One-Liners
```typescript
// Hard to debug
return arr.filter(x => x.active).map(x => x.id).reduce((a, b) => a + b, 0);
```

---

## Clarity Guidelines

### Prefer Explicit Over Implicit
```typescript
// Good: Clear intent
const isAdmin = user.role === 'admin';

// Bad: Magic value
const isAdmin = user.role === 1;
```

### Use Descriptive Names
```typescript
// Good
const activeUserCount = users.filter(u => u.isActive).length;

// Bad
const n = users.filter(u => u.a).length;
```

### Break Up Long Chains
```typescript
// Good: Readable steps
const activeUsers = users.filter(u => u.isActive);
const userNames = activeUsers.map(u => u.name);
const sortedNames = userNames.sort();

// Bad: Wall of methods
const sortedNames = users.filter(u => u.isActive).map(u => u.name).sort();
```

---

## Output Format

```markdown
## Simplification: [File]

### Change 1: [Description]
**Reason**: [Why this improves clarity]

**Before**:
```typescript
// original code
```

**After**:
```typescript
// simplified code
```

### Change 2: ...
```

---

## Gotchas

1. **Don't change functionality**: Only HOW, not WHAT
2. **Preserve helpful abstractions**: Not all abstractions are bad
3. **Consider debugging**: Will this be harder to step through?
4. **Test after simplification**: Ensure nothing broke
5. **Know when to stop**: Perfect is the enemy of good

