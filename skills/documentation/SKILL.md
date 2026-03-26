---
name: documentation
description: Workflows for fetching and synthesizing official documentation using Ref tools. Use when you need official docs for a library or framework.
---

# Documentation Skill

> **Purpose**: Workflows for fetching and synthesizing official documentation using Ref tools.

## Tools Available

| Tool | Purpose |
|------|---------|
| `mcp_Ref_ref_search_documentation` | Search for documentation pages |
| `mcp_Ref_ref_read_url` | Fetch and read specific documentation URL |

---

## Workflow: FETCH → SYNTHESIZE

### Step 1: Fetch Documentation

```javascript
// Search for relevant docs
mcp_Ref_ref_search_documentation({
  query: "convex react useQuery"
})

// Read specific URL (use EXACT url from search, including #hash)
mcp_Ref_ref_read_url({
  url: "https://docs.convex.dev/client/react#usequery"
})
```

### Step 2: Extract Key Information

Focus on:
- **Tech Stack**: Required libraries and versions
- **Core Logic**: How the feature works
- **API Reference**: Function names, parameters, return types
- **Examples**: Official code snippets
- **Gotchas**: Common pitfalls, deprecations, breaking changes

### Step 3: Synthesize into Implementation Guide

Convert verbose documentation into actionable steps:
1. Schema/Types
2. Functions/APIs
3. UI Integration
4. Error Handling

---

## Output Format

```markdown
## Documentation Research: [Library/Feature]
**Source URL**: [Link]
**Version**: [Version #]
**Date Retrieved**: YYYY-MM-DD

### Summary
[Brief overview of what this covers]

### Installation
```bash
npm install package@version
```

### Implementation Guide

#### 1. Setup
```typescript
// Configuration code
```

#### 2. Core Usage
```typescript
// Main implementation
```

#### 3. Error Handling
```typescript
// Error patterns
```

### API Reference

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `func()` | `arg: Type` | `Type` | What it does |

### Gotchas & Warnings
- ⚠️ [Breaking change in v2]
- ⚠️ [Common pitfall to avoid]

### Related Documentation
- [Link to related topic]
```

---

## Version Awareness

**Always note**:
- Documentation version
- Library version requirements
- Breaking changes between versions
- Deprecation warnings

**Example**:
```markdown
> **Note**: This is for Convex v1.x. The API changed significantly in v2.
> See migration guide: [link]
```

---

## Quality Guidelines

- **Links over Content**: Keep guide actionable, link to full source
- **Clean Snippets**: Only include necessary code
- **No Hypotheses**: Only document what official source says
- **Preserve Source**: Always include original URL
- **Note Version**: Documentation can become stale

## What NOT to Do

- Don't fetch from unofficial sources when official docs exist
- Don't skip noting version number
- Don't paraphrase in ways that change meaning
- Don't add "best practices" beyond what docs recommend
- Don't ignore warnings or caveats
- Don't present incomplete examples
- Don't add your own code - only use official examples

