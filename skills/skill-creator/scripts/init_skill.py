#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path> [--version <version>]

Examples:
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private --version 1.1.0
"""

import sys
import argparse
from pathlib import Path

# Fallback template if file is not found
FALLBACK_SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Clear trigger/use description. This metadata decides when the skill loads.]
tier: [TODO: 1 | 2 | 3]
source: local
skill_template_version: "0.1.0"
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

1. [ ] Read required context and current artifacts.
2. [ ] Choose the branch.
   1. [ ] Default branch.
   2. [ ] Update/repair branch.
   3. [ ] Review branch.
3. [ ] Execute the workflow for the selected branch.
4. [ ] Produce or update the required artifact.
5. [ ] Verify with the named proof command or evidence surface.
6. [ ] Review against the gotchas before completion.
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

This file documents the "Why" behind the patterns used in this skill.
It should be populated based on the Sequential Thinking phase during skill creation.

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

def init_skill(skill_name, path, version="1.0.0", tools="Read, Write, Grep, LS"):
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

    # Try to read template from references/SKILL_TEMPLATE.md
    template_path = Path(__file__).parent.parent / 'references' / 'SKILL_TEMPLATE.md'
    if template_path.exists():
        skill_template = template_path.read_text()
        print("📖 Loaded SKILL.md template from file")
    else:
        skill_template = FALLBACK_SKILL_TEMPLATE
        print("⚠️ SKILL_TEMPLATE.md not found, using fallback")

    skill_title = title_case_skill_name(skill_name)
    skill_content = skill_template.format(
        skill_name=skill_name,
        skill_title=skill_title,
        version=version,
        tools=tools
    )

    try:
        (skill_dir / 'SKILL.md').write_text(skill_content)
        print("✅ Created SKILL.md")

        # Create resource directories
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        (scripts_dir / 'helper.py').write_text(EXAMPLE_HELPER_SCRIPT.format(skill_name=skill_name))
        (scripts_dir / 'helper.py').chmod(0o755)
        print("✅ Created scripts/helper.py")

        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        (references_dir / 'architecture.md').write_text(ARCH_REF_CONTENT.format(skill_title=skill_title))
        (references_dir / 'workflows.md').write_text(WORKFLOW_REF_CONTENT.format(skill_title=skill_title))
        (references_dir / 'gotchas.md').write_text(GOTCHAS_REF_CONTENT.format(skill_title=skill_title))
        print("✅ Created references/ (architecture.md, workflows.md, gotchas.md)")

        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        (assets_dir / '.gitkeep').touch()
        print("✅ Created assets/")

    except Exception as e:
        print(f"❌ Error creating resources: {e}")
        return None

    print(f"\n✅ Skill '{skill_name}' v{version} initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print("1. Populate architecture.md and workflows.md with your reasoning results.")
    print("2. Update SKILL.md to link to your findings.")
    print("3. Run quick_validate.py to ensure compliance.")

    return skill_dir

def main():
    parser = argparse.ArgumentParser(description="Skill Initializer")
    parser.add_argument("name", help="Name of the skill (hyphen-case)")
    parser.add_argument("--path", required=True, help="Path to create the skill in")
    parser.add_argument("--version", default="1.0.0", help="Initial version (default: 1.0.0)")
    parser.add_argument("--tools", default="Read, Write, Grep, LS", help="Comma-separated list of allowed-tools (default: Read, Write, Grep, LS)")

    args = parser.parse_args()

    # Validate skill name
    import re
    if not re.match(r'^[a-z0-9-]+$', args.name):
        print(f"❌ Error: Name '{args.name}' must be hyphen-case (lowercase, digits, hyphens)")
        sys.exit(1)

    result = init_skill(args.name, args.path, args.version, args.tools)
    sys.exit(0 if result else 1)

if __name__ == "__main__":
    main()
