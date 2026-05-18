# Todos

- [ ] Clarify the domain, task, and whether an installable skill is likely to
  help more than existing local skills.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to compare the
  requested capability against currently installed skills and trusted sources.
- [ ] Search for external skills only when local skills do not already cover the
  need.
- [ ] Present the strongest candidates with install command, source, and why
  they fit.
- [ ] Use [advise](../advise/SKILL.md) when multiple candidate skills fit.
- [ ] Do not install, update, or run external code unless the user explicitly
  asks and the environment policy allows it.
- [ ] Use [review](../review/SKILL.md) before adding a discovered skill to
  Codexter-owned docs or registry guidance.
