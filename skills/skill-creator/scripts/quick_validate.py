#!/usr/bin/env python3
"""
Quick validation script for skills.
"""

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core.skill_contract import (
    FrontmatterError,
    normalize_capability_contract,
    normalize_method_contracts,
    parse_skill_frontmatter,
)

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

    # Parse through the same safe, duplicate-rejecting source used by registry
    # generation so authoring feedback cannot accept a contract the registry
    # would later reject.
    try:
        frontmatter = parse_skill_frontmatter(skill_md)
    except FrontmatterError as exc:
        return False, str(exc)

    ALLOWED_PROPERTIES = {
        'name',
        'description',
        'version',
        'skill_template_version',
        'template_uses',
        'skill_ui',
        'license',
        'allowed-tools',
        'metadata',
        'tier',
        'source',
        'group',
        'methods',
        'capability',
        'common_chains',
        'workflow',
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

    template_uses = frontmatter.get('template_uses')
    if template_uses is not None and not isinstance(template_uses, dict):
        return False, "'template_uses' must be a mapping"

    if 'skill_template_version' in frontmatter and template_uses:
        return False, "Use either legacy 'skill_template_version' or 'template_uses', not both"

    try:
        normalize_method_contracts(frontmatter.get('methods'), str(name), skill_md)
        normalize_capability_contract(frontmatter.get('capability'), skill_md)
    except FrontmatterError as exc:
        return False, str(exc)

    for dirname in ['references', 'templates', 'prompts']:
        support_dir = skill_path / dirname
        if not support_dir.exists() or not support_dir.is_dir():
            continue
        empty = [p for p in support_dir.rglob('*.md') if p.is_file() and not p.read_text().strip()]
        if empty:
            return False, f"Empty markdown support file(s): {', '.join(str(p) for p in empty)}"

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
