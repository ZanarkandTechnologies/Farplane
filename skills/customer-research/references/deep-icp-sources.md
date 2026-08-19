---
title: Deep ICP Source Protocol
owner: customer-research
status: active
kind: skill-reference
---

# Deep ICP Source Protocol

Load only when `mode=deep_icp`, a read-only authorized session is needed, or an
identifiable company requires a hiring-footprint scan.

## Professional Signal Sources

- Inspect public or supplied LinkedIn activity, company writing, podcasts,
  talks, newsletters, GitHub, X, YouTube, launches, project history, and
  language the target repeats.
- Use the Codex in-app Browser for a supplied rendered profile before declaring
  it inaccessible. Never log in, enter credentials, export cookies, or assume
  access to a private session.
- An explicitly operator-authorized session is read-only: do not message,
  connect, follow, react, publish, change settings, reveal auth state, perform
  bulk extraction, or create ongoing monitoring.
- If a profile is blocked, record `auth_walled` and continue with public company
  pages, indexed material, talks, interviews, and operator-supplied exports.
- Refuse or narrow bypass requests, login-only scraping, private-community
  access, sensitive-trait inference, private-life research, or social actions.

## Hiring-Footprint Scan

When the target company is identifiable, inspect the official careers/ATS
surface, company LinkedIn jobs, company/founder/recruiter hiring posts, and
relevant indexed job listings. Record `not_applicable` only when company binding
is missing; otherwise record coverage even when no role surfaces.

For each signal, preserve `active`, `closed_or_stale`, or `status_unknown`;
use `none_surfaced` only for an inspected source with no visible role. Extract
function, seniority, location, responsibilities, systems, metrics, and repeated
capability themes. Hiring reveals investment intent, not dysfunction.

## Evidence Promotion

Promote repeated, professionally relevant patterns over isolated reactions or
snippets. Keep access class, observation date, confidence, alternative
explanation, and falsifier. Deep evidence may raise confidence without making
the main Signal Card longer.
