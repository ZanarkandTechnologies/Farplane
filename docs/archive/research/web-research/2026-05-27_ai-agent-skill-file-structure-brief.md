## Deep Research: Current Skill/Instruction File Structure Best Practices for Codex and Claude
**Project Context**: Codexter already separates source `SKILL.md` and `todos.md`, then embeds the checklist into installed `SKILL.md` for first-load reliability. `docs/progress.md` was not present, so local baseline came from `README.md`, [docs/skills/README.md](/Users/kenjipcx/coding-harness/Codexter/docs/skills/README.md), and `MEM-0114`.
**Date**: 2026-05-27

### Summary
- Official Anthropic and OpenAI guidance converges on progressive disclosure: skill metadata is always loaded first, full `SKILL.md` is loaded only when the skill is selected, and `references/` exists for conditional depth.
- Current official guidance also pushes small, focused skills with concise routing descriptions and a short main instruction file.
- Recent Codex practitioner evidence suggests the real loop may still partial-read long selected skill files in practice, often around a first chunk near 220 lines. This is not official behavior documentation, but it is a credible operational constraint.
- Result: the hypothesis is mostly supported. Put every-invocation logic and the required checklist in `SKILL.md`; keep references for conditional workflows, templates, long rubrics/model maps, delegated prompts, and rare-path recipes; if something must be read every run, promote it into `SKILL.md`. Refine this further by front-loading the critical path near the top of `SKILL.md`, not just somewhere in it.

### Dated Sources And What They Imply
- **2026-04 (search index), accessed 2026-05-27**: Anthropic PDF, *The Complete Guide to Building Skills for Claude*  
  https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf  
  Implies:
  - Skills use a three-level system: frontmatter always loaded, `SKILL.md` body loaded when relevant, linked files loaded only as needed.
  - `references/` is explicitly for documentation loaded on demand.
  - `SKILL.md` should stay focused on core instructions; detailed docs should move to `references/`.
  - Good skill content includes steps, examples, troubleshooting, and quality checks, but those should still respect progressive disclosure.

- **2025-10-16**: Anthropic engineering post, *Equipping agents for the real world with Agent Skills*  
  https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills  
  Implies:
  - `name` and `description` are the first routing layer.
  - As skills grow, additional files should be bundled only for specific scenarios.
  - Keeping the core skill lean is an explicit design goal; rare or mutually exclusive branches belong in linked files.
  - This directly supports promoting any always-needed logic back into the main file.

- **Accessed 2026-05-27**: Anthropic Claude Code best practices  
  https://code.claude.com/docs/en/best-practices  
  Implies:
  - Always-loaded instruction files should stay short and broad.
  - If a file is too long, rules get lost.
  - Domain knowledge or workflows that are only sometimes relevant should move out of the always-loaded file and into skills.
  - By analogy, selected skills should also keep their always-needed path concise.

- **2026-03-07 update (published 2026-02-25)**: OpenAI Academy, *Skills*  
  https://academy.openai.com/public/clubs/work-users-ynjqu/resources/skills  
  Implies:
  - Strong skills capture job-to-be-done, required inputs, numbered steps, required output format, and final quality checks.
  - Skills often work best as small building blocks instead of one massive end-to-end workflow.
  - `SKILL.md` is the workflow playbook; resources support it, but the main file owns the operational path.

- **Accessed 2026-05-27**: OpenAI Codex docs, *Agent Skills*  
  https://developers.openai.com/codex/skills  
  Implies:
  - Codex starts with only each skill's `name`, `description`, and path.
  - The initial skills list is capped to roughly 2% of context, or 8,000 characters when context size is unknown; descriptions are shortened first.
  - When selected, Codex reads the full `SKILL.md`.
  - Best practices: keep each skill focused on one job, prefer instructions over scripts unless determinism is needed, write explicit steps, and test trigger behavior.
  - `references/` is an official optional directory, which supports Codexter's split between core contract and long-tail references.

- **2026-03-09**: OpenAI Developers blog, *Using skills to accelerate OSS maintenance*  
  https://developers.openai.com/blog/skills-agents-sdk  
  Implies:
  - The `description` field is part of the routing contract, not decoration.
  - OpenAI states the same progressive-disclosure model as Anthropic: metadata first, full `SKILL.md` on activation, scripts/references later when needed.
  - This strengthens the case for small, trigger-rich frontmatter and a short first-load body.

- **Accessed 2026-05-27**: OpenAI Codex docs, *Custom instructions with AGENTS.md*  
  https://developers.openai.com/codex/guides/agents-md  
  Implies:
  - Repo-level always-on guidance is a separate layer from skills.
  - Instruction discovery has a byte cap (`project_doc_max_bytes`, 32 KiB by default), so even always-on files are bounded and should stay purposeful.
  - Separation of concerns matters: persistent repo rules belong in `AGENTS.md`; reusable conditional workflows belong in skills.

- **2026-05-02**: Reddit, *Codex may only read the first ~220 lines of a skill file*  
  https://www.reddit.com/r/codex/comments/1t1rbqt/codex_may_only_read_the_first_220_lines_of_a/  
  Implies:
  - In observed Codex traces, selected skills were often first-read with a `sed` chunk around 220 lines, and follow-up reads were inconsistent.
  - Several practitioners report better results from keeping skills short and pushing detail into references.
  - Confidence is lower than official docs, but this is the strongest recent practical signal that file shape matters operationally, not just conceptually.

- **Accessed 2026-05-27**: Peter Steinberger public repo instructions, `steipete/agent-scripts/AGENTS.MD`  
  https://github.com/steipete/agent-scripts/blob/main/AGENTS.MD  
  Implies:
  - Always-on repo instructions should stay hard-rule only.
  - Skills are treated as the canonical place for tool workflows.
  - Skill descriptions should be short trigger phrases, not long summaries.
  - I did not find a newer dedicated Steipete post specifically on skill file structure in accessible search results; this repo artifact is the closest recent public practitioner signal.

### Conflicts To Account For
- **Official model**: selected skills read the full `SKILL.md`, references only when needed.
- **Observed Codex behavior**: in some real sessions, the first read of a selected skill appears chunked and may stop early.
- **Practical inference**: design for both. Assume the platform intends to read the full file, but make the first 100-220 lines sufficient for correct core behavior if the rest is delayed or skipped.

### Evaluation Of The Hypothesis
**Verdict: supported, with one refinement.**

The hypothesis is directionally correct:
- `SKILL.md` should contain every-invocation logic.
- The required checklist should be visible from the main file on first load.
- `references/` should contain only conditional workflows, templates, examples, long rubrics, model maps, delegated prompts, and rare-path recipes.
- If a reference is needed on every run, its operational logic belongs in `SKILL.md`.

Refinement:
- Do not merely keep the required logic somewhere in `SKILL.md`; front-load it near the top of the body so the skill still works if the agent only reads an initial chunk.

### Concrete Recommendations For Codexter
1. **Keep the current source/install split.**  
   Codexter's current pattern already matches the strongest evidence: source `SKILL.md` plus source `todos.md`, with install-time embedding of the checklist into installed `SKILL.md` for first-load visibility.

2. **Standardize a short top-of-body critical path.**  
   Each local skill should put this near the top of `SKILL.md`, before long explanations:
   - purpose and trigger boundary
   - must-follow steps
   - required checklist
   - hard stop / never-do rules
   - only then conditional branches and reference links

3. **Treat `references/` as conditional depth only.**  
   Keep in references:
   - long rubrics
   - model maps
   - delegated prompts
   - rare-path troubleshooting
   - large examples
   - templates and schemas
   Do not keep core workflow steps there.

4. **Audit for partial-read resilience, not just correctness.**  
   A skill should still behave acceptably if the agent reads only frontmatter plus the top section of `SKILL.md`. This is an inference from the conflict between official docs and observed Reddit traces.

5. **Keep skills single-job and description-heavy.**  
   The description is the routing API. Make it short, explicit, trigger-rich, and front-loaded with the key use case and terms.

6. **Avoid duplicate narrative surfaces.**  
   Do not add skill-local `README.md` files just to restate the same workflow. Keep the workflow contract in `SKILL.md`, long-tail depth in references, and human-facing repo explanation elsewhere.

7. **Promote repeated reference reads upward.**  
   If a branch keeps forcing the agent to open the same reference on most invocations, that logic no longer belongs in a reference. Promote the operational part into `SKILL.md` and leave the bulky examples below.

8. **Use explicit invocation or policy when side effects are sensitive.**  
   For risky workflows, prefer metadata or policy that requires explicit invocation rather than relying on implicit routing.

### Action Items For Main Agent
1. Keep `MEM-0114` and the installed-skill embedded-checklist approach; it is the right default under current evidence.
2. Add a Codexter-wide `SKILL.md` top-section template: `First-Load Contract`, `Required Checklist`, `Conditional References`.
3. Audit local skills whose operational body exceeds roughly 200-250 lines or buries must-follow rules deep in the file.
4. Move any always-read reference logic into `SKILL.md`; leave only conditional or bulky material in `references/`.
5. Add a lightweight regression check for skill shape: description quality, first-load section presence, and whether the skill still makes sense if only the top chunk is read.
