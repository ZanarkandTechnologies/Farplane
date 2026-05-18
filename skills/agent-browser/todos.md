# Todos

- [ ] State the browser goal: navigation, interaction, screenshot, extraction,
  console check, or QA proof.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to anchor the
  expected page, route, state, selector, or artifact before driving the browser.
- [ ] Open the target page or session and capture the current URL/title before
  changing state.
- [ ] Take an interactive snapshot before choosing refs; re-snapshot after
  navigation, form submits, modals, or major DOM changes.
- [ ] Prefer stable semantic actions (`role`, `text`, `label`) when refs are
  stale or the UI rerenders.
- [ ] Capture the proof artifact the caller needs: screenshot, full-page
  screenshot, snapshot, text/value, URL, console/page error, or saved state.
- [ ] Record command outputs and artifact paths in the owning ticket or handoff
  surface.
- [ ] Use [review](../review/SKILL.md) when browser evidence is being used to
  support a completion or quality claim.
