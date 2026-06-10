#!/usr/bin/env python3
"""
Quick validation script for skills.
"""

import sys
import re
import yaml
from pathlib import Path


def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    try:
        content = skill_md.read_text()
    except Exception as e:
        return False, f"Error reading SKILL.md: {e}"

    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format (ensure it starts and ends with ---)"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    ALLOWED_PROPERTIES = {
        'name',
        'description',
        'version',
        'skill_template_version',
        'feature_refs',
        'license',
        'allowed-tools',
        'metadata',
        'tier',
        'source',
        'group',
        'methods',
        'common_chains',
        'upstream_url',
    }

    # Check for unexpected properties
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Validate name
    name = frontmatter.get('name', '')
    if not re.match(r'^[a-z0-9-]+$', str(name)):
        return False, f"Name '{name}' should be hyphen-case"

    # Validate the reference surface without enforcing a fixed file taxonomy.
    references_dir = skill_path / 'references'
    if not references_dir.exists() or not references_dir.is_dir():
        return False, "Missing 'references/' directory"

    reference_files = [
        p for p in references_dir.rglob('*.md')
        if p.is_file()
    ]
    if not reference_files:
        return False, "Missing reference markdown files under 'references/'"

    return True, "Skill is valid!"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        return 1

    valid, message = validate_skill(sys.argv[1])
    print(f"[{'PASSED' if valid else 'FAILED'}] {message}")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
