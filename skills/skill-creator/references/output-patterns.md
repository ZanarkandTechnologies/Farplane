# Output Patterns

Use these patterns when skills need to produce consistent, high-quality output.

## Prompt Template Pattern

When workflows repeat across sessions, include copy/paste prompts in `prompts/`.

```markdown
## Prompt Templates

- [prompts/plan.md](prompts/plan.md) - Planning baseline prompt
- [prompts/build.md](prompts/build.md) - Build baseline prompt
```

Each prompt should include:

- canonical paths (for example `docs/*`)
- mode constraints (plan-only vs build-only)
- required updates/output artifacts

Avoid retired paths unless the project still uses them.

## Template Pattern

Provide templates for output format. Match the level of strictness to your needs.

**For strict requirements (like API responses or data formats):**

```markdown
## Report structure

ALWAYS use this exact template structure:

# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

**For flexible guidance (when adaptation is useful):**

```markdown
## Report structure

Here is a sensible default format, but use your best judgment:

# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]

Adjust sections as needed for the specific analysis type.
```

## Examples Pattern

For skills where output quality depends on seeing examples, provide input/output pairs:

````markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Follow this style: type(scope): brief description, then detailed explanation.
````

Examples help Claude understand the desired style and level of detail more clearly than descriptions alone.

## Validation Checklist Pattern

For deterministic outputs, include a preflight checklist in the skill:

```markdown
## Pre-Package Checks

- [ ] No dead links in SKILL.md
- [ ] No orphan references (every reference is linked from SKILL.md)
- [ ] No empty guidance files
- [ ] No stale path conventions (for example `_ralph/*` if canonical is `docs/*`)
- [ ] Command snippets are syntactically runnable
```
