---
name: external-patterns
description: Workflows for finding code patterns across GitHub and exploring specific repositories. Use when searching for how others implement features or deep diving into libraries.
---

# External Patterns Skill

> **Purpose**: Workflows for finding code patterns across GitHub and exploring specific repositories.

## Tools Available

| Tool | Purpose | Use When |
|------|---------|----------|
| `mcp_grep_searchGitHub` | Broad search across 1M+ repos | "How do people typically do X?" |
| `mcp_deepwiki_*` | Deep dive into specific repo | "How does library X work internally?" |

---

## Mode 1: DISCOVER (Broad GitHub Search)

**Goal**: Find real-world code patterns across many repositories.

### Search Strategy

**Step 1: Define LITERAL code patterns**
- ✅ Good: `'import { useAction } from "convex/react"'`
- ✅ Good: `'async function handleAuth'`
- ❌ Bad: `"how to use convex auth"` (natural language)
- ❌ Bad: `"best react patterns"` (keywords)

**Step 2: Use searchGitHub with filters**
```javascript
searchGitHub({
  query: 'useQuery(',
  language: ['TypeScript', 'TSX'],
  useRegexp: true  // For patterns like (?s)try {.*await
})
```

**Step 3: Filter results for quality**
- Prioritize well-known orgs: `vercel/`, `microsoft/`, `facebook/`
- Check stars and last update date
- Look for repos updated in last 12 months

### Output Format

```markdown
## Remote Patterns for [Topic]
**Search Queries**: `[patterns used]`
**Date**: YYYY-MM-DD

### Implementation Approach 1: [Name]
- **Repository**: [org/repo] (Stars: Xk, Updated: YYYY-MM)
- **File**: [path]
- **Key Pattern**:
```javascript
// Full code with imports and context
```

### Implementation Approach 2: [Alternative]
...

### Comparison & Summary
[Compare the different approaches found]
```

---

## Mode 2: DEEP DIVE (Repository Exploration)

**Goal**: Understand architecture and design decisions of a specific repository.

### Workflow

**Step 1: Map the territory**
```javascript
mcp_deepwiki_read_wiki_structure({ repoName: "owner/repo" })
```

**Step 2: Ask targeted questions**
```javascript
mcp_deepwiki_ask_question({
  repoName: "owner/repo",
  question: "How is authentication handled?"
})
```

**Step 3: Read implementation details**
```javascript
mcp_deepwiki_read_wiki_contents({ repoName: "owner/repo" })
```

### Output Format

```markdown
## Repo Analysis: [Repo Name]
**URL**: [Link]
**Focus**: [Topic]
**Date**: YYYY-MM-DD

### Architectural Overview
[How the repo handles the specific topic]

### Key File Map
- `[Path]`: [Role in system]
- `[Path]`: [Logic description]

### Deep-Dive Analysis
[Detailed explanation with code snippets]

### Reusable Insights
[What we can apply to our work]
```

---

## Sequential Workflow: DISCOVER → DEEP DIVE

For comprehensive research:

1. **DISCOVER**: Search GitHub for patterns
   - Find which repos implement this well
   - Note: vercel/ai, t3-oss/create-t3-app, etc.

2. **DEEP DIVE**: Explore the best repo found
   - Understand their architecture
   - Extract design decisions

3. **SYNTHESIZE**: Combine findings
   - Compare approaches
   - Recommend "Best Version"

---

## Quality Guidelines

- **Literal over Keywords**: Search for actual code strings
- **Modern Standards**: Prioritize repos updated in last 12 months
- **Variety**: Show 3-5 different approaches
- **Context**: Include imports, setup, not just snippets
- **Source Attribution**: Always note repo URL and file path

## What NOT to Do

- Don't search for "how to" or "tutorial"
- Don't accept first result without evaluating quality
- Don't show examples from unmaintained repos
- Don't extract code without context
- Don't present only one pattern - show variety
- Don't skip noting star count and update date

