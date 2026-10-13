---
name: zernio
description: "Turn a social posting, metrics, comment, or DM request into a Zernio draft, a read, or a gated handoff for the project's bound Zernio profile."
department: marketing
source: local
capability:
  kind: integration
  consumes: [social-post-draft]
template_uses:
  skill-template: "0.6.3"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Grep, Glob, Bash
---

# Zernio

## Context

Zernio is the one source of a business's social accounts (TikTok, Instagram,
YouTube, X and more): posting, drafts, comments, DMs, comment-to-DM
automations and analytics. Use its hosted MCP (`https://mcp.zernio.com/mcp`);
signing in to it is the auth. Farplane connects no platform itself
(`docs/farplane-framework/cli.md`). `social-content` writes the
copy; this skill owns the account boundary.

## Skill Signature

```text
zernio(request, project_root) -> draft | read_result | gate | blocked_report
reads: farplane/bindings.yaml#zernio (profile, access), human_gates,
       .farplane/metrics/observations/zernio_content/
does: drafts only with is_draft: true; reads freely; stops every mutation at a gate
fails: a create call without is_draft; a profile guessed from login;
       a zero written for a number Zernio didn't return
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the profile and access.
  - [ ] Read `profile` and `access` from the project's `farplane/bindings.yaml`
        `zernio:` block. One login can hold several profiles; never pick one
        from `accounts_list` alone. No binding: return `blocked_report`.
  - [ ] No Zernio MCP tools in the session: return `blocked_report` naming
        `claude mcp add --transport http zernio https://mcp.zernio.com/mcp`
        and the sign-in as Kenji's step. Reads may instead run
        `farplane run --` GET requests against `https://zernio.com/api/v1`.
- [ ] 2. Numbers ("views last week", followers, posts out).
  - [ ] Read the `zernio_content` observations first; they are the numbers
        the office shows. Older than a day: run
        `farplane run -- farplane metrics refresh --project-root <root> --no-push`.
  - [ ] Detail the observations lack (per-post, retention, demographics):
        Zernio analytics tools, bounded to the asked window and the profile.
  - [ ] A missing platform is a gap, never a zero.
- [ ] 3. Drafts ("post this", "schedule this").
  - [ ] Only when `access` is `drafts`: call `posts_create` with
        `is_draft: true`, `profile_id`, and the exact `account_id`. Without
        `is_draft` the tool schedules the post 60 minutes out.
  - [ ] `access: read_only`: return the validated payload instead.
  - [ ] Either way end with a gate: publishing or scheduling waits for
        Kenji's OK naming the draft and account, after `qa` outbound passes
        on the platform preview.
- [ ] 4. Comments, DMs and automations.
  - [ ] Reading comments, conversations and automation logs is allowed.
  - [ ] Replies, DMs, likes, hides, deletes, automation changes and account
        changes are mutations: draft the text, return a gate, change nothing.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Mutations stay gated even when the MCP offers them (`posts_publish_now`,
  `posts_cross_post`, inbox replies); `human_gates` in the binding decides.
- `ZERNIO_API_KEY` in Doppler serves the headless `metrics refresh`; an agent
  in a session uses the MCP login.
- Posts published natively on a platform still appear in Zernio analytics;
  `farplane content add` is only for posts Zernio can't see.

## Output

- `draft`: Zernio draft ID, account, and the publish gate.
- `read_result`: numbers or threads with window, profile, source, and gaps.
- `gate`: the exact mutation proposed and what Kenji approves.
- `blocked_report`: missing binding, MCP, or access, with the next step.
