#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path> [--with-helper] [--with-references] [--with-assets]

Examples:
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private --with-helper
"""

import sys
import argparse
from pathlib import Path

# Fallback template if the canonical docs-owned template is not found.
FALLBACK_SKILL_TEMPLATE = """---
name: {skill_name}
description: "[TODO: Verb input/context into output/artifact when call-condition; <=220 chars.]"
tier: [TODO: 1 | 2 | 3]
source: local
template_uses:
  skill-template: "0.3.2"
group: [TODO: required for Tier 3]
allowed-tools: {tools}
---

# {skill_title}

## Context

[TODO: Only context needed every time this skill loads: tier/system placement,
source-of-truth docs, ownership constraints, and assumptions.]

[TODO: Do not add a generic `## Job`; put ordered work in `## Todo List` and
use a specific contract section only when it adds non-duplicated durable shape.]

[TODO: Paths in this skill are relative to this skill package. Use
`scripts/foo.py` and `references/foo.md` for nearby files.]

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read required context and current artifacts.
- [ ] 2. Choose the branch.
   - [ ] 1. Default branch.
   - [ ] 2. Update/repair branch.
   - [ ] 3. Review branch.
- [ ] 3. Execute the workflow for the selected branch.
- [ ] 4. Produce or update the required artifact.
- [ ] 5. Verify with the named proof command or evidence surface.
- [ ] 6. Review against the gotchas before completion.
   - [ ] Repeatability from files alone.
   - [ ] No duplicated first-load logic.
   - [ ] Explicit proof command or blocker.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [TODO: Inline one short positive example, or link to `templates/*` /
  `prompts/*` when examples are too long.]

## Gotchas

- [TODO: Negative example or failure pattern.]
- [TODO: Negative example or failure pattern.]
- [TODO: Negative example or failure pattern.]

## Reference Map

- [TODO: `references/name.md` - read only when ...]

## Output

- [TODO: Expected artifact, type, path, or response shape.]
"""

EXAMPLE_HELPER_SCRIPT = '''#!/usr/bin/env python3
"""
Helper script for {skill_name}

This script was bootstrapped by skill-creator.
Replace with actual implementation or delete if not needed.
"""

def main():
    print("This is a helper script for {skill_name}")
    # TODO: Implement logic (e.g., data processing, API calls)

if __name__ == "__main__":
    main()
'''

ARCH_REF_CONTENT = """# Architectural Decisions for {skill_title}

This file documents the rationale behind the patterns used in this skill.

## Core Architecture
[TODO: Describe the high-level architecture]

## Design Decisions
- **Decision 1**: [Description and rationale]
- **Decision 2**: [Description and rationale]

## Trade-offs
- [Identify what was sacrificed for the chosen approach]
"""

WORKFLOW_REF_CONTENT = """# Implementation Workflows for {skill_title}

This file documents the detailed, step-by-step implementation logic.

## Primary Workflow: [Name]
1. **Step 1**: [Action]
2. **Step 2**: [Action]
...

## Conditional Paths
- **If X**: [Path A]
- **If Y**: [Path B]
"""

GOTCHAS_REF_CONTENT = """# Common Gotchas & Pitfalls for {skill_title}

Document known issues, edge cases, and patterns to avoid.

## Critical Gotchas
- **[Issue]**: [Description and how to avoid it]

## Edge Cases
- **[Scenario]**: [Expected behavior and handling]

## "DO NOT" Patterns
- DO NOT [Anti-pattern 1]
- DO NOT [Anti-pattern 2]
"""

def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))

def strip_template_metadata(template_text):
    """Return the literal SKILL.md template body from a versioned template file."""
    if not template_text.startswith('---\n'):
        return template_text
    first_end = template_text.find('\n---\n', 4)
    if first_end == -1:
        return template_text
    body = template_text[first_end + len('\n---\n'):].lstrip('\n')
    return body if body.startswith('---\n') else template_text

def render_template(template: str, replacements: dict[str, str]) -> str:
    """Replace only supported placeholders without interpreting other braces."""
    rendered = template
    for key, value in replacements.items():
        rendered = rendered.replace("{" + key + "}", value)
    return rendered


def init_skill(
    skill_name,
    path,
    tools="Read, Write, Grep, LS",
    with_helper=False,
    with_references=False,
    with_assets=False,
):
    """
    Initialize a new skill directory with template SKILL.md and reference files.
    """
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"❌ Error: Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    # Read the canonical docs-owned skill template.
    template_path = Path(__file__).resolve().parents[3] / 'docs' / 'skills' / 'templates' / 'SKILL_TEMPLATE.md'
    if template_path.exists():
        skill_template = strip_template_metadata(template_path.read_text())
        print("📖 Loaded SKILL.md template from file")
    else:
        skill_template = FALLBACK_SKILL_TEMPLATE
        print("⚠️ SKILL_TEMPLATE.md not found, using fallback")

    skill_title = title_case_skill_name(skill_name)
    skill_content = render_template(
        skill_template,
        {
            "skill_name": skill_name,
            "skill_title": skill_title,
            "skill_function": skill_name.replace("-", "_"),
            "tools": tools,
        },
    )

    try:
        (skill_dir / 'SKILL.md').write_text(skill_content)
        print("✅ Created SKILL.md")

        if with_helper:
            scripts_dir = skill_dir / 'scripts'
            scripts_dir.mkdir(exist_ok=True)
            (scripts_dir / 'helper.py').write_text(EXAMPLE_HELPER_SCRIPT.format(skill_name=skill_name))
            (scripts_dir / 'helper.py').chmod(0o755)
            print("✅ Created scripts/helper.py")

        if with_references:
            references_dir = skill_dir / 'references'
            references_dir.mkdir(exist_ok=True)
            (references_dir / 'architecture.md').write_text(ARCH_REF_CONTENT.format(skill_title=skill_title))
            (references_dir / 'workflows.md').write_text(WORKFLOW_REF_CONTENT.format(skill_title=skill_title))
            (references_dir / 'gotchas.md').write_text(GOTCHAS_REF_CONTENT.format(skill_title=skill_title))
            print("✅ Created references/ (architecture.md, workflows.md, gotchas.md)")

        if with_assets:
            assets_dir = skill_dir / 'assets'
            assets_dir.mkdir(exist_ok=True)
            (assets_dir / '.gitkeep').touch()
            print("✅ Created assets/")

    except Exception as e:
        print(f"❌ Error creating resources: {e}")
        return None

    print(f"\n✅ Skill '{skill_name}' initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print("1. Replace TODOs in SKILL.md with the actual skill contract.")
    print("2. Add references, scripts, templates, or prompts only when the skill needs them.")
    print("3. Run quick_validate.py and the Farplane skill-maintenance validator.")

    return skill_dir

def main():
    parser = argparse.ArgumentParser(description="Skill Initializer")
    parser.add_argument("name", help="Name of the skill (hyphen-case)")
    parser.add_argument("--path", required=True, help="Path to create the skill in")
    parser.add_argument("--tools", default="Read, Write, Grep, LS", help="Comma-separated list of allowed-tools (default: Read, Write, Grep, LS)")
    parser.add_argument("--with-helper", action="store_true", help="Create scripts/helper.py")
    parser.add_argument("--with-references", action="store_true", help="Create placeholder references")
    parser.add_argument("--with-assets", action="store_true", help="Create assets/.gitkeep")

    args = parser.parse_args()

    # Validate skill name
    import re
    if not re.match(r'^[a-z0-9-]+$', args.name):
        print(f"❌ Error: Name '{args.name}' must be hyphen-case (lowercase, digits, hyphens)")
        sys.exit(1)

    result = init_skill(
        args.name,
        args.path,
        args.tools,
        args.with_helper,
        args.with_references,
        args.with_assets,
    )
    sys.exit(0 if result else 1)

if __name__ == "__main__":
    main()
