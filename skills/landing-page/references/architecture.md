# Architecture

`landing-page` owns one-page story and section structure.

Inputs:

- offer,
- audience,
- product/place/person/object details,
- proof assets,
- taste brief or visual constraints.

Outputs:

- story arc,
- section map,
- visual scenes,
- asset plan,
- motion plan,
- QA plan,
- approved `LANDING_SPEC.md` or an exact blocked-spec report for the calling
  implementation planner.

It uses `visual-design` for visual-system decisions, `asset-advisor` for
missing/reference-led/rights-sensitive media, and official GreenSock skills or
docs for GSAP details. It does not implement, render, deploy, or create another
implementation plan.
