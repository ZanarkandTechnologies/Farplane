---
skill: "customer-research"
change: "operator-authorized-browser-session"
target: "Mohamed Mo Tarek El-Fatatry"
created_at: "2026-07-14"
verdict: "pass_with_bounded-access_repair"
---

# Operator-Authorized Browser Trial

## Claim Under Test

The deep ICP route can use an explicitly operator-authorized browser session to
inspect professional LinkedIn material read-only without handling credentials,
extracting auth state, performing social actions, or overstating one activity
sample as a complete behavioral profile.

## Observed Behavior

- Brave exposed a loopback-only CDP endpoint on port 9222 using an isolated user
  data directory; process inspection confirmed the endpoint belonged to Brave.
- The operator authenticated directly in that browser. The agent never received
  credentials or cookie values.
- LinkedIn's localized `my.linkedin.com` URL rendered the guest shell, while the
  canonical `www.linkedin.com/in/dixrupt/` URL rendered the authenticated member
  view.
- A bounded read-only profile and activity inspection surfaced concrete company
  signals: partner campaign outcomes, circular-electronics positioning,
  regional founder interest, AI/operating content, Malaysian enterprise sales,
  and an explicit strategic-finance/internationalization hiring need.
- No message, connection, follow, reaction, publication, contact-detail overlay,
  cookie export, or account-setting action occurred.

## Skill Repair

- Added `operator_authorized_session` as a distinct source-access label.
- Allowed explicitly attached sessions only for bounded read-only inspection.
- Kept login, credential handling, cookie extraction, access-control evasion,
  social actions, bulk extraction, and ongoing monitoring prohibited.
- Required isolated interactions to remain weak evidence and visible activity to
  be described as a sample rather than a complete engagement history.

## Proof

- CDP `/json/version` responded and process inspection resolved the listener to
  `/Applications/Brave Browser.app`.
- `agent-browser --cdp 9222` returned the authenticated LinkedIn navigation and
  target profile activity.
- The project report now distinguishes the original public auth-wall trial from
  the later operator-authorized session and labels remaining unknowns.
