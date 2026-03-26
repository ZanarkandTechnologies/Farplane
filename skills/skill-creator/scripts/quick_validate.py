#!/usr/bin/env python3
"""
Quick validation script for skills - Meta-Brain version
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

    # Define allowed properties (Added 'version')
    ALLOWED_PROPERTIES = {'name', 'description', 'version', 'license', 'allowed-tools', 'metadata'}

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

    # Validate core reference files (Meta-Brain requirement)
    references_dir = skill_path / 'references'
    if not references_dir.exists() or not references_dir.is_dir():
        return False, "Missing 'references/' directory"

    REQUIRED_REFS = ['architecture.md', 'workflows.md', 'gotchas.md']
    missing_refs = [ref for ref in REQUIRED_REFS if not (references_dir / ref).exists()]
    if missing_refs:
        return False, f"Missing required reference files: {', '.join(missing_refs)}"

    return True, "Skill is valid!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    
    valid, message = validate_skill(sys.argv[1])
    print(f"[{'PASSED' if valid else 'FAILED'}] {message}")
    sys.exit(0 if valid else 1)
