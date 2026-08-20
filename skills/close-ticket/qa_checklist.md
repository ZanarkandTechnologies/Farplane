---
template_id: skill-qa-checklist
template_version: "0.1.1"
feature_refs:
  - FEAT-0057
  - FEAT-0062
consumer_scope: skill
applies_to:
  - skills/close-ticket/qa_checklist.md
---

# Close Ticket QA Checklist

Read this checklist before remote mutation and apply it again before claiming
completion. Any unchecked item retains the local ticket packet.

## Checklist

- [ ] The exact project repository from `integrations.github.repo` is accessible
  and matches `gh repo view`; repository visibility is not a gate. Current
  GitHub attachment types/limits and every explicit media path/digest passed
  before issue creation.
- [ ] Exactly one issue body has the literal ticket marker and concise,
  non-empty `Before`, `After`, `Example`, `Key decisions`, and `Proof`
  sections derived from final ticket truth; the body does not dump the ticket
  plan or full test log, and title or fuzzy search was not used as identity.
- [ ] For a material feature ticket, a passing independently reviewed `$demo`
  `final.mp4` is the first selected media item and first marked comment.
  Maintenance-only tickets do not invent a demo.
- [ ] Authenticated `@Chrome` uploaded only missing media, one comment per
  SHA-256 marker, captured each canonical comment URL, and wrote no credential,
  cookie, token, browser state, or profile data into the repository.
- [ ] `gh` was used only for documented issue text/state operations. Browser
  authentication was checked separately from `gh auth`; every real binary was
  uploaded through GitHub's authenticated composer, produced a
  `github.com/user-attachments` URL, and was not replaced by a local path,
  repository commit, Release, or guessed upload API.
- [ ] Each new attachment comment was verified twice: `gh issue view` found one
  exact digest marker plus its user-attachment URL, and the authenticated issue
  fragment rendered the image or playable video. A material feature's `Proof`
  line links the first demo comment instead of retaining a pending placeholder.
- [ ] Core created or resumed exactly one ticket-marked issue, found exactly
  one marked attachment comment with a GitHub user-attachment URL per expected
  digest, and closed it only after verification.
- [ ] Core received the ticket ID and original selected media paths, then
  rendered, created or resumed, closed, mined, indexed, and deleted the exact
  packet. No caller-supplied issue URL was required. On any failure the
  packet remains and no Release, asset, tag, bundle, manifest, restore path,
  alternate-repository fallback, manual delete, or provider abstraction was
  introduced.

## Authentication Resume Check

- [ ] If the composer was signed out, the run stopped before upload/close/Core,
  retained the packet and open issue, recorded the next missing digest, asked
  the operator to sign in in that browser, and resumed the same issue after
  readiness without duplicating issue or media markers.
