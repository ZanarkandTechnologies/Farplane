---
skill: ad-advisor
example: meta-lead-campaign
---

# Meta Lead Campaign Example

Ad goal: Test whether owner-operators will book a review call for an onboarding
workflow diagnostic.

Platform: Meta

Account binding: `farplane/bindings.yaml#ads.meta.primary` if present; otherwise
blocked until configured.

Offer: 20-minute review of current onboarding handoffs and time-to-value
bottlenecks.

Audience: founders and operators of B2B service/software companies. Exclude
existing customers and internal test accounts when the platform supports it.

Objective / event: lead or landing-page conversion, depending on pixel/event
readiness.

Creative variants:

- Variant A: operational pain hook.
- Variant B: before/after workflow proof.
- Variant C: founder-specific diagnostic offer.

Policy risks: avoid implying the viewer personally has a problem. Say "teams
with manual onboarding handoffs" rather than "your team is failing onboarding."

Measurement:

- Primary: qualified lead submissions or booked calls.
- Guard: spend per qualified lead, landing-page conversion rate, rejection
  reasons from follow-up.
- Anti-metric: cheap unqualified leads.

Dry-run / CLI plan:

- Confirm Ads CLI installed and authenticated through private runtime.
- Resolve campaign/ad account alias from bindings.
- Generate a redacted dry-run command or JSON config.
- Prefer paused campaign creation before active delivery.

Launch gate: explicit approval naming account, budget cap, creative bundle,
landing page, and launch window.

Stop / iterate rule: stop if spend reaches the cap with no qualified lead or if
lead quality is clearly wrong after the first review batch.
