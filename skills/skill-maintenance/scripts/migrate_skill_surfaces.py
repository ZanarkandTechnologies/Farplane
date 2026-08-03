#!/usr/bin/env python3
"""Migrate skill frontmatter from per-skill feature refs to local surface fields."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT = REPO_ROOT / "skills"
UI_SKILLS = {
    "skill-maintenance": "skills/skill-maintenance/graph/index.html",
    "harness-advisor": "skills/harness-advisor",
}


def split_frontmatter(text: str, path: Path) -> tuple[list[str], str]:
    if not text.startswith("---\n"):
        raise RuntimeError(f"{path}: missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise RuntimeError(f"{path}: unterminated frontmatter")
    return text[4:end].splitlines(), text[end + len("\n---\n") :]


def remove_block(lines: list[str], key: str) -> list[str]:
    output: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith(f"{key}:"):
            index += 1
            while index < len(lines) and (lines[index].startswith(" ") or not lines[index].strip()):
                index += 1
            continue
        output.append(line)
        index += 1
    return output


def has_key(lines: list[str], key: str) -> bool:
    return any(line.startswith(f"{key}:") for line in lines)


def insertion_index(lines: list[str]) -> int:
    preferred_after = ("skill_template_version", "source", "group")
    for key in preferred_after:
        for index, line in enumerate(lines):
            if line.startswith(f"{key}:"):
                return index + 1
    return len(lines)


def migrate_skill(skill_dir: Path) -> bool:
    skill_path = skill_dir / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    lines, body = split_frontmatter(text, skill_path)
    original = list(lines)

    lines = remove_block(lines, "feature_refs")

    surface_lines: list[str] = []
    if (skill_dir / "evals/evals.json").exists() and not has_key(lines, "eval"):
        surface_lines.append("eval: evals/evals.json")
    if (skill_dir / "qa_checklist.md").exists() and not has_key(lines, "qa_checklist"):
        surface_lines.append("qa_checklist: qa_checklist.md")
    ui_path = UI_SKILLS.get(skill_dir.name)
    if ui_path and not has_key(lines, "skill_ui"):
        surface_lines.append(f"skill_ui: {ui_path}")

    if surface_lines:
        index = insertion_index(lines)
        lines[index:index] = surface_lines

    if lines == original:
        return False

    skill_path.write_text("---\n" + "\n".join(lines).rstrip() + "\n---\n" + body, encoding="utf-8")
    return True


def main() -> int:
    changed: list[str] = []
    for skill_dir in sorted(path for path in SKILLS_ROOT.iterdir() if (path / "SKILL.md").exists()):
        if migrate_skill(skill_dir):
            changed.append(skill_dir.name)
    print(f"migrated {len(changed)} skill frontmatter rows")
    for name in changed:
        print(f"- {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
