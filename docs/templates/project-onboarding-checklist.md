# Project onboarding checklist

Every new project gets a GitHub repo (private by default) and, with it, one pinned issue titled
`Onboarding: <name>` with the `onboarding` label and this checklist as its body. Add the project to
`~/.farplane/company.json` with its `kind`, `business`, `githubUrl`, and local checkout as its
`trackingContext`. Fetch Context reads the issue like any other; Progress Updater lists its
unchecked items under `Onboarding`. A dated follow-up is its own issue with the `check-in` label
and a `Due: YYYY-MM-DD` line.

```markdown
# <Project name>

- [ ] Kind: business, product, deployment, tooling or experiment
- [ ] Business it belongs to (a business belongs to itself)
- [ ] Goal: what it's for, and what done looks like
- [ ] Who it's for: the buyer, client or user
- [ ] Repo visibility: private (default, anything confidential) or public (engineering only)
- [ ] Whop company, for businesses only: `whop: company:` in the repo's `farplane/bindings.yaml`
- [ ] Where its metrics come from
- [ ] First setup on the heist board: the critical path to the goal
```

Kinds:

- **business:** sells something and can bind a Whop company.
- **product:** something a business makes and sells.
- **deployment:** service delivery for one client, paid by contract.
- **tooling:** internal, not sold.
- **experiment:** not a product yet. It belongs to the media business, whose floor lists it, and gets
  its own floor once it sells.
- **company:** the registered company itself, which owns every floor.
