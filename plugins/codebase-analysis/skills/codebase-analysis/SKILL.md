---
name: codebase-analysis
description: Patterns for exploring local codebases - finding files, understanding implementations, and extracting reusable patterns. Use when exploring WHERE, HOW, or SHOW ME questions about local code.
tier: 2
source: local
---

# Codebase Analysis Skill

> **Purpose**: Patterns and workflows for exploring local codebases - finding files, understanding implementations, and extracting reusable patterns.

## Modes of Operation

### Mode 1: LOCATE (Where is X?)

**Goal**: Find files and directories relevant to a feature or topic.

**Strategy**:
1. Start with grep for keywords
2. Use glob for file patterns
3. List directories to understand structure

**Search Patterns**:
```bash
# By feature keywords
grep -r "authentication" --include="*.ts"

# By file patterns
*service*, *handler*, *controller* → Business logic
*test*, *spec* → Test files
*.config.*, *rc* → Configuration
*.d.ts, *.types.* → Type definitions
```

**Output Format**:
```markdown
## File Locations for [Topic]

### Implementation Files
- `src/services/feature.js` - Main service logic
- `src/handlers/feature-handler.js` - Request handling

### Test Files
- `tests/feature.test.js` - Unit tests

### Configuration
- `config/feature.json` - Feature config

### Related Directories
- `src/services/feature/` - Contains X related files
```

---

### Mode 2: ANALYZE (How does X work?)

**Goal**: Understand implementation details, trace data flow, explain technical workings.

**Strategy**:
1. Read entry points first (exports, public methods, route handlers)
2. Follow the code path step by step
3. Document key logic with file:line references

**Focus Areas**:
- Entry points and surface area
- Data transformations
- State changes and side effects
- Error handling patterns
- Configuration and feature flags

**Output Format**:
```markdown
## Analysis: [Component Name]

### Overview
[2-3 sentence summary]

### Entry Points
- `api/routes.js:45` - POST /endpoint
- `handlers/feature.js:12` - handleFeature()

### Core Implementation

#### 1. Request Validation (`handlers/feature.js:15-32`)
- Validates input using X
- Returns 400 if validation fails

#### 2. Data Processing (`services/processor.js:8-45`)
- Transforms data at line 23
- Queues for async processing at line 40

### Data Flow
1. Request → `api/routes.js:45`
2. Handler → `handlers/feature.js:12`
3. Service → `services/processor.js:8`

### Key Patterns
- **Pattern Name**: Description at `file:line`
```

---

### Mode 3: PATTERNS (Show me examples)

**Goal**: Find similar implementations that can serve as templates for new work.

**Strategy**:
1. Identify what type of pattern (API, data, component, testing)
2. Search for comparable features
3. Extract reusable code with context

**Pattern Categories**:
- **API Patterns**: Route structure, middleware, error handling, validation, pagination
- **Data Patterns**: Database queries, caching, transformations, migrations
- **Component Patterns**: File organization, state management, event handling
- **Testing Patterns**: Unit test structure, integration setup, mock strategies

**Output Format**:
```markdown
## Pattern Examples: [Pattern Type]

### Pattern 1: [Name]
**Found in**: `src/api/users.js:45-67`
**Used for**: [Description]

```javascript
// Code snippet with full context
```

**Key aspects**:
- Point 1
- Point 2

### Pattern 2: [Alternative]
**Found in**: `src/api/products.js:89-120`
...

### Pattern Usage in Codebase
- Pattern A: Found in X, Y, Z
- Pattern B: Found in A, B, C
```

---

## Quality Guidelines

- **Always include file:line references** for claims
- **Read files thoroughly** before making statements
- **Trace actual code paths** - don't assume
- **Show working code** - not just snippets
- **Include context** - imports, setup, usage
- **Multiple examples** - show variations that exist

## What NOT to Do

- Don't guess about implementation
- Don't skip error handling or edge cases
- Don't make architectural recommendations (unless asked)
- Don't critique code quality (unless asked)
- Don't suggest improvements (unless asked)
- Document what EXISTS, not what SHOULD exist

