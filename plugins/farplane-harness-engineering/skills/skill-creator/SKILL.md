---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
tier: 3
group: skills
source: local
license: Complete terms in LICENSE.txt
allowed-tools: mcp__sequential-thinking__sequentialthinking, Read, Write, Grep, Glob
---

# Skill Creator

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] Read the requested capability, existing skills, registry, and nearby
  project docs before creating or updating a skill.
- [ ] Apply `docs/skills/best-practices.md` for checklist shape, reference
  placement, actor-prompt versus skill-contract boundaries, duplication
  control, and repeatability.
- [ ] Use [plan](../plan/SKILL.md) when tier, ownership, package boundary, or
  first-load contract is unclear.
- [ ] Use [research:parity](../research/SKILL.md#researchparity) or
  [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
  when external skill examples should inform the design.
- [ ] Define trigger conditions, job, direct `## Important Checklist`, decision
  branches, gotchas or hard gates, judgment questions, and outcome contract in
  `SKILL.md`.
- [ ] Keep actor identity, delegation routing, tool-use policy, and artifact
  writeback in the owning agent prompt or caller skill, not in a reusable skill
  contract.
- [ ] Keep every-invocation logic in `SKILL.md`; use references only for
  conditional branches, examples, templates, long rubric detail, model maps,
  delegated prompts, and rare-path recipes.
- [ ] Promote reference logic back into `SKILL.md` when it must be read every
  time.
- [ ] Add `tier`, `source`, Tier 3 `group`, optional `methods`, optional
  `common_chains`, and optional `upstream_url` frontmatter as appropriate.
- [ ] Put required first-load checklist items directly in `SKILL.md`; create a
  legacy `todos.md` only as temporary migration input when explicitly needed.
- [ ] Run the skill registry and tier validators after edits.
- [ ] Before completion, call the native `reviewer` subagent when available
  with a reviewer handoff using `skill-contract`, `integration-readiness`, and
  `evidence-quality` families; require `TAS-A` on repeatability, no duplicated
  first-load logic, actor-prompt versus skill-contract boundaries, and explicit
  proof commands.
- [ ] Use [execute](../execute/SKILL.md) for final proof/writeback after skill
  files change.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform Claude from a general-purpose agent into a specialized agent
equipped with procedural knowledge that no model can fully possess.

### The Correct Mental Model

*   **Tools (MCP/Search)** = Your library documentation on-demand. Use these for raw API references, fetching docs, and up-to-date tool specifications.
*   **Skills** = Your battle-tested **workflows** for solving problems. Use these to capture *how* you build things (e.g., "How I build streaming chat using Convex + AI SDK").

The VALUE of a skill is the **integration workflow** and **architectural decisions**, not the tool documentation. Claude should use Skills to follow your preferred patterns and use available tools to fill in the API details.

### What Skills Provide

1.  **Specialized workflows** - Multi-step procedures for specific domains (e.g., "Streaming AI Chat Implementation").
2.  **Integration patterns** - How different tools and technologies work together effectively.
3.  **Architectural decisions** - The "Why" behind a specific approach (e.g., "Why use Convex actions for AI?").
4.  **Bundled resources** - Scripts, references, and assets that support the workflow.

### What to Build vs. What Not to Build

| Build (Workflow-Driven) | Do Not Build (Tool-Centric) |
| :--- | :--- |
| `skill-streaming-ai-chat.md` | `skill-convex.md` (Use MCP/Docs) |
| `skill-multi-agent-coordination.md` | `skill-vercel-ai-sdk.md` (Use MCP/Docs) |
| `skill-realtime-dashboard.md` | `skill-react-patterns.md` (Too generic) |
| `skill-file-upload-processing.md` | `skill-python-basics.md` (Claude already knows this) |

### Tier 3 Pipeline Model

For complex Tier 3 domain skills, prefer a compact algebraic model plus
filesystem-visible method records over long prose recipes. Use
`references/tier3-pipeline-model.md` when a skill has planning/execution
phases, component matrices, method selection, and per-component proof.

```text
Tier3Pipeline := Model + MethodRegistry + TodoRecipe + Templates + Proof

Component := Job + Claim + Inputs + CandidateMethods + ChosenMethod + Output + Proof

MethodSelection(component, methods, constraints) :=
  candidates = filter(methods, component, constraints)
  chosen = advise(top3(candidates))
```

Do not add `README.md` files to skill packages just to explain this model.
`SKILL.md` remains the first-load entrypoint; put detailed notation in
`references/model.md` or another targeted reference.

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Claude needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.

**Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of Claude as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

### First-Load Contract (Non-Negotiable)

If an agent only reads `SKILL.md` once and skips all references, it should still execute correctly.

Farplane skills are stable local contracts. External skills, repos, blogs, and
command families are research inputs, not live dependencies. Do not create thin
wrappers that auto-sync upstream behavior; use `best-of-worlds` to import ideas
through explicit `adopt`, `adapt`, `reject`, or `defer` decisions. See
`MEM-0073`.

Every new skill must include this minimum contract directly in `SKILL.md`:

1. **Trigger conditions**: Explicit user/task signals that should activate the skill.
2. **Job**: The smallest statement of what the skill does.
3. **Important Checklist**: Required anti-forgetting steps under
   `## Important Checklist`.
4. **Core decision branches**: Primary conditional paths.
5. **Top gotchas / hard gates**: High-risk failure modes, stop conditions, and
   escalation points.
6. **Judgement questions**: Material choices that should use `advise` when the
   answer is not mechanically determined.
7. **Outcome contract**: Which files or outputs must exist or be updated.

Rule of thumb: **If skipping all references would make the skill fail, `SKILL.md` is too thin.**

### Main File vs References

Put logic in `SKILL.md` when it affects every invocation:

- trigger boundary
- required order
- checklist
- decision routing
- escalation and stop conditions
- hard gates
- output contract
- high-risk guardrails

Use `references/*` only for conditional content:

- examples
- templates
- variant-specific details
- long rubric or scoring detail
- model maps
- delegated prompts
- rare-path recipes

If a reference file must be read every time, promote the needed logic into
`SKILL.md`. Templates can stay as files because the agent uses them as
artifacts, not always-loaded reasoning.

### Repeatability Review Gate

Before calling a new or updated skill ready, review it with the same skepticism
as implementation work. Use `docs/skills/best-practices.md` as the standard.
The minimum pass bar:

- Another agent can use the skill from repo files alone without hidden chat
  context.
- The first-load checklist is short, operational, and branch-aware.
- Onboarding, examples, long rationale, and rare-path detail live in references
  instead of bloating the main checklist.
- The same instruction is not copied across `SKILL.md`, references, templates,
  and README-style docs unless each surface has a distinct job.
- Required scripts, commands, artifact paths, and validation steps are explicit.
- The review result names `repeatability` as a checked dimension, alongside
  integration and evidence readiness.

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    ├── prompts/          - Copy/paste operator prompts for repeated workflows
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

Every SKILL.md consists of:

- **Frontmatter** (YAML): Contains `name`, `description`, and `allowed-tools` fields. These are the only fields that Claude reads to determine when the skill gets used and which tools are available.
    - `name`: (required) hyphen-case identifier.
    - `description`: (required) clear and comprehensive explanation of what the skill does and when to trigger it.
    - `allowed-tools`: (required) A **comma-separated string** of tools this skill is allowed to use (e.g., `Read, Grep, Glob`).
- **Body** (Markdown): Instructions and guidance for using the skill. Only loaded AFTER the skill triggers. A well-structured workflow skill should include:
    - **Use when**: Specific scenarios for triggering this skill.
    - **Job**: What specific problem this skill solves.
    - **Important Checklist**: Required steps that affect every invocation.
    - **Decision branches**: The main conditional paths.
    - **Output / proof**: What must exist when done.
    - **Guardrails**: Mistakes to avoid, hard gates, and stop conditions.

#### Bundled Resources (optional)

##### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits**: Token efficient, deterministic, may be executed without loading into context
- **Note**: Scripts may still need to be read by Claude for patching or environment-specific adjustments

##### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform Claude's process and thinking.

- **When to include**: For documentation that Claude should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/mnda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when Claude determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both.
- **Absorption heuristic**:
  - Mission-critical + short (<~100 lines) -> absorb summary into SKILL.md.
  - Low-frequency + verbose -> keep in references.
  - Empty/thin files -> delete or merge inline.
- **Core workflow rule**: Keep the base workflow and top gotchas in SKILL.md. References should enrich, not define the minimum executable path.

##### Prompts (`prompts/`)

Copy/paste operational prompts that reduce session startup friction and enforce consistency.

- **When to include**: When users repeatedly run planning/build/review sessions with fixed instructions
- **Examples**: `prompts/plan.md`, `prompts/build.md`
- **Use cases**: Multi-session flows (PRD -> plan -> build), role handoff prompts, review prompts
- **Benefits**: Faster starts, fewer path mistakes, more consistent execution quality
- **Guideline**: Keep all prompt paths aligned to current canonical structure
  (for example `docs/*`, not retired `_ralph/*`)

##### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output Claude produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates, `assets/frontend-template/` for HTML/React boilerplate, `assets/font.ttf` for typography
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables Claude to use files without loading them into context

#### What to Not Include in a Skill

A skill should only contain essential files that directly support its functionality. Do NOT create extraneous documentation or auxiliary files, including:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

The skill should only contain the information needed for an AI agent to do the job at hand. It should not contain auxilary context about the process that went into creating it, setup and testing procedures, user-facing documentation, etc. Creating additional documentation files just adds clutter and confusion.

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (Unlimited because scripts can be executed without reading into context window)

#### Progressive Disclosure Patterns

Keep SKILL.md body to the essentials and under 500 lines to minimize context bloat. Split content into separate files when approaching this limit. When splitting out content into other files, it is very important to reference them from SKILL.md and describe clearly when to read them, to ensure the reader of the skill knows they exist and when to use them.

**Key principle:** When a skill supports multiple variations, frameworks, or options, keep only the core workflow and selection guidance in SKILL.md. Move variant-specific details (patterns, examples, configuration) into separate reference files.

**Pattern 1: High-level guide with references**

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

Claude loads FORMS.md, REFERENCE.md, or EXAMPLES.md only when needed.

**Pattern 2: Domain-specific organization**

For Skills with multiple domains, organize content by domain to avoid loading irrelevant context:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

When a user asks about sales metrics, Claude only reads sales.md.

Similarly, for skills supporting multiple frameworks or variants, organize by variant:

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

When the user chooses AWS, Claude only reads aws.md.

**Pattern 3: Conditional details**

Show basic content, link to advanced content:

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

Claude reads REDLINING.md or OOXML.md only when the user needs those features.

**Important guidelines:**

- **Avoid deeply nested references** - Keep references one level deep from SKILL.md. All reference files should link directly from SKILL.md.
- **Structure longer reference files** - For files longer than 100 lines, include a table of contents at the top so Claude can see the full scope when previewing.

## Skill Creation Process

Skill creation involves these steps:

1. **Understand & Diagnose**: Identify the problem and the core complexity.
2. **Architectural Reasoning**: Use `SequentialThinking` to define the "Meta-Brain" structure.
3. **Initialize & Bootstrap**: Run `init_skill.py` to create the directory structure.
4. **Implementation & Documentation**: Populate `SKILL.md` and reference files with your reasoning results.
5. **Package & Validate**: Run `package_skill.py` to ensure compliance.
6. **Iterate**: Refine based on real-world usage.

### Step 1: Understand & Diagnose

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

*   "What functionality should the image-editor skill support? Editing, rotating, anything else?"
*   "What would a user say that should trigger this skill?"

### Step 2: Architectural Reasoning (CRITICAL)

Before coding, you MUST use `mcp__sequential-thinking__sequentialthinking` to architect the skill. Do not skip this phase; it is the foundation of a high-quality skill.

**Reasoning Goals**:

*   **Identify the Source of Truth**: Where does the official documentation live?
*   **Define the Architecture**: Why is a certain approach chosen? Keep concise critical rationale in SKILL.md; use `references/architecture.md` only when tradeoff history is substantial.
*   **Map the Workflows**: What are the sequential and conditional steps? Keep the baseline workflow in SKILL.md; use `references/workflows.md` when variants/branches would bloat SKILL.md.
*   **Identify Gotchas**: What are the "DO NOT" patterns and edge cases? Keep top gotchas inline; use a reference file only for long-tail edge-case catalogs.

### Step 3: Initializing the Skill

Once you have a reasoned architecture, run the `init_skill.py` script.

Usage:

```bash
scripts/init_skill.py <skill-name> --path <output-directory> [--version <version>] [--tools <tool-list>]
```

The script will:

*   Load the master template from `references/SKILL_TEMPLATE.md`.
*   Create a full directory structure.
*   Generate core files and optional references based on selected pattern.
*   Create a `prompts/` directory for reusable operator prompts.
*   Bootstrap a `helper.py` script and `assets/` directory.
*   Populate the `allowed-tools` section in the frontmatter.

### Step 4: Implementation & Documentation

When editing the skill, move beyond placeholders. **Inject the results of your reasoning phase** directly into the generated files.

*   **Frontmatter**: Ensure `name`, `version`, `allowed-tools`, and `description` are accurate. **CRITICAL**: `allowed-tools` MUST be a **comma-separated string** (e.g., `Read, Grep, Glob`), NOT a YAML list.
*   **Body**: Link to the detailed reasoning in `references/`.

#### Populate Reference Files (Conditional)

Only create/populate these when they add value beyond SKILL.md:

*   **architecture.md**: Use when decision history or tradeoffs are substantial.
*   **workflows.md**: Use when variants/branches cannot be expressed clearly inline.
*   **gotchas.md**: Use for long-tail edge cases; keep the top 3 gotchas in SKILL.md.
*   **judgement-questions.md**: Use when the skill has reusable ambiguity,
    metric-selection, or adoption questions that would bloat `SKILL.md`.

Local references:

*   `references/architecture.md`
*   `references/workflows.md`
*   `references/gotchas.md`
*   `references/judgement-questions.md`

#### Populate Prompt Files (When Workflow Repeats)

For repeated operator workflows, include copy/paste prompts in `prompts/`:

*   **prompts/plan.md**: Planning session baseline.
*   **prompts/build.md**: Build session baseline.
*   Keep prompt paths canonical and current.

Added scripts in `scripts/` must be tested by actually running them.

### Step 5: Packaging a Skill

Once development of the skill is complete, it must be packaged into a distributable .skill file that gets shared with the user. The packaging process automatically validates the skill first to ensure it meets all requirements:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory specification:

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

The packaging script will:

1. **Validate** the skill automatically, checking:

   - YAML frontmatter format and required fields
   - Skill naming conventions and directory structure
   - Description completeness and quality
   - File organization and resource references
   - No dead links in `SKILL.md`
   - No orphan references never linked by `SKILL.md`
   - No empty guidance files
   - No stale path patterns in examples/prompts (for example retired `_ralph/` when `docs/` is canonical)
   - Command snippets are syntactically runnable

2. **Package** the skill if validation passes, creating a .skill file named after the skill (e.g., `my-skill.skill`) that includes all files and maintains the proper directory structure for distribution. The .skill file is a zip file with a .skill extension.

If validation fails, the script will report the errors and exit without creating a package. Fix any validation errors and run the packaging command again.

### Step 6: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again
