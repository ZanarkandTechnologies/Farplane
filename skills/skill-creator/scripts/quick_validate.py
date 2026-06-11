#!/usr/bin/env python3
"""
Quick validation script for skills.
"""

import sys
import re
import yaml
from pathlib import Path

DESCRIPTION_MAX_CHARS = 220


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
    description = frontmatter.get('description')
    if not isinstance(description, str) or not description.strip():
        return False, "'description' must be a non-empty string"
    if 'TODO' in description:
        return False, "'description' still contains TODO text"
    if len(description) > DESCRIPTION_MAX_CHARS:
        return False, (
            f"'description' is {len(description)} chars; keep it at or below "
            f"{DESCRIPTION_MAX_CHARS} chars"
        )

    # Validate name
    name = frontmatter.get('name', '')
    if not re.match(r'^[a-z0-9-]+$', str(name)):
        return False, f"Name '{name}' should be hyphen-case"

    # Validate reusable support surfaces without enforcing a fixed taxonomy.
    support_dirs = ['references', 'templates', 'prompts']
    support_files = []
    for dirname in support_dirs:
        support_dir = skill_path / dirname
        if support_dir.exists() and support_dir.is_dir():
            support_files.extend(p for p in support_dir.rglob('*.md') if p.is_file())
    if not support_files:
        return False, "Missing markdown support files under references/, templates/, or prompts/"

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
