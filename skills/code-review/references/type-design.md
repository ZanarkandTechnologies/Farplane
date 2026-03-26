# Type Design Analysis

> **When to use**: When introducing new types, during PR review, or when refactoring existing types.

## Core Mission

Evaluate type designs for:
- **Invariant strength**: Are constraints properly enforced?
- **Encapsulation quality**: Are internals properly hidden?
- **Practical usefulness**: Do types prevent real bugs?

Well-designed types are the foundation of maintainable, bug-resistant software.

---

## Analysis Framework

### 1. Identify Invariants

Examine the type for all implicit and explicit invariants:
- Data consistency requirements
- Valid state transitions
- Relationship constraints between fields
- Business logic rules encoded in the type
- Preconditions and postconditions

### 2. Evaluate Encapsulation (Rate 1-10)
- Are internal implementation details properly hidden?
- Can invariants be violated from outside?
- Are there appropriate access modifiers?
- Is the interface minimal and complete?

### 3. Assess Invariant Expression (Rate 1-10)
- How clearly are invariants communicated through structure?
- Are invariants enforced at compile-time where possible?
- Is the type self-documenting?
- Are edge cases obvious from the type definition?

### 4. Judge Invariant Usefulness (Rate 1-10)
- Do invariants prevent real bugs?
- Are they aligned with business requirements?
- Do they make the code easier to reason about?
- Are they neither too restrictive nor too permissive?

### 5. Examine Invariant Enforcement (Rate 1-10)
- Are invariants checked at construction time?
- Are all mutation points guarded?
- Is it impossible to create invalid instances?
- Are runtime checks appropriate and comprehensive?

---

## Output Format

```markdown
## Type: [TypeName]

### Invariants Identified
- [List each invariant with brief description]

### Ratings
- **Encapsulation**: X/10
  [Brief justification]
  
- **Invariant Expression**: X/10
  [Brief justification]
  
- **Invariant Usefulness**: X/10
  [Brief justification]
  
- **Invariant Enforcement**: X/10
  [Brief justification]

### Strengths
[What the type does well]

### Concerns
[Specific issues that need attention]

### Recommended Improvements
[Concrete, actionable suggestions]
```

---

## Key Principles

- **Prefer compile-time guarantees** over runtime checks
- **Value clarity** over cleverness
- **Consider maintenance burden** of improvements
- **Types should make illegal states unrepresentable**
- **Constructor validation** is crucial
- **Immutability** simplifies invariant maintenance

---

## Common Anti-Patterns

### ❌ Anemic Domain Models
```typescript
// No behavior, just data
type User = {
  id: string;
  name: string;
  email: string;
}

// All logic lives outside the type
function validateUser(user: User) { ... }
function formatUserName(user: User) { ... }
```

### ❌ Exposed Mutable Internals
```typescript
class UserList {
  public users: User[] = []; // Can be mutated directly!
}
```

### ❌ Documentation-Only Invariants
```typescript
// Email must be valid format (not enforced!)
type User = {
  email: string; // Just a string, no validation
}
```

### ❌ Missing Construction Validation
```typescript
class User {
  constructor(public email: string) {
    // No validation! Invalid emails allowed
  }
}
```

### ❌ Too Many Responsibilities
```typescript
class UserService {
  // Does authentication, validation, storage, formatting...
}
```

---

## Good Patterns

### ✅ Branded Types (Compile-Time Safety)
```typescript
type Email = string & { __brand: 'Email' };

function createEmail(value: string): Email {
  if (!isValidEmail(value)) {
    throw new Error('Invalid email format');
  }
  return value as Email;
}
```

### ✅ Constructor Validation
```typescript
class User {
  readonly email: Email;
  
  constructor(email: string) {
    this.email = createEmail(email); // Validates at construction
  }
}
```

### ✅ Immutable Data
```typescript
type User = Readonly<{
  id: string;
  email: Email;
  createdAt: Date;
}>;
```

### ✅ Encapsulated Collections
```typescript
class UserList {
  private readonly users: User[] = [];
  
  add(user: User): void { ... }
  get(id: string): User | undefined { ... }
  
  // No direct array access
}
```

### ✅ State Machines
```typescript
type OrderState = 
  | { status: 'pending' }
  | { status: 'paid'; paidAt: Date }
  | { status: 'shipped'; paidAt: Date; shippedAt: Date };

// Impossible to have shippedAt without paidAt
```

---

## Improvement Considerations

When suggesting improvements, consider:
- Complexity cost of the suggestion
- Whether improvement justifies breaking changes
- Skill level and conventions of existing codebase
- Performance implications
- Balance between safety and usability

---

## Checklist

```markdown
### Type Design Review
- [ ] Invariants clearly identified
- [ ] Encapsulation appropriate
- [ ] Invariants expressed in type structure
- [ ] Construction validates all invariants
- [ ] Mutation points guarded
- [ ] Type isn't doing too much
- [ ] Illegal states are unrepresentable
```

