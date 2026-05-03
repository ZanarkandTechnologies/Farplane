# Workflow Patterns

## First-Load vs Reference Rubric

Use this decision table when deciding whether content lives in `SKILL.md` or `references/`.

| Content Type | Where It Goes | Why |
| :--- | :--- | :--- |
| Mission-critical and short (<~100 lines) | `SKILL.md` | Must survive first load |
| Baseline execution path | `SKILL.md` | Agents need this immediately |
| Short judgement questions | `SKILL.md` | Agents need to know when to use `advise` |
| Long judgement rubric | `references/` | Keeps decision nuance out of first load |
| Variant-heavy branches | `references/` | Reduces SKILL.md bloat |
| Verbose domain docs and schemas | `references/` | Loaded on demand |
| Copy/paste session instructions | `prompts/` | Operator speed and consistency |
| Empty or thin guidance files | Delete or merge inline | Avoid dead indirection |

## Thin-File Policy

Before creating a reference file, ask:

1. Is this required to execute the default path?
   - If yes, keep it in `SKILL.md`.
2. Is this mostly repeated templates or prompts?
   - If yes, use `prompts/` or compact references.
3. Is this file currently empty/thin?
   - If yes, delete it or absorb into `SKILL.md`.

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. It is often helpful to give Claude an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

## Outcome Contract Pattern

Close workflow sections with an explicit output contract so completion is deterministic:

```markdown
## Outcome Contract

After this skill executes:
- `path/to/file-a` is created or updated
- `path/to/file-b` is created or updated
- Validation evidence exists at `path/to/evidence`
```

## Judgement Questions Pattern

Use this when a skill has choices that cannot be solved by a command or static
rule:

```markdown
## Judgement Questions

Use `advise` when these cannot be answered mechanically:

- What user or artifact is this skill optimizing for?
- What primary metric or success signal should decide keep/discard?
- What guard prevents the chosen metric from being gamed?
- What should be rejected or deferred even if it looks attractive?
```

Keep 3-7 questions in `SKILL.md`. Move longer scoring detail into
`references/judgement-questions.md`.
