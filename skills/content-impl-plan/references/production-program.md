---
title: Content production program contract
status: active
owner: content-impl-plan
updated_at: 2026-08-04
---

# Content production program contract

Visual production plans persist a versioned JSON program and validate it with
`scripts/validate_production_program.py` before execution.

```json
{
  "schema_version": "1.0",
  "content_kind": "reel",
  "creative_input_bundle": {
    "brand_kit_snapshot": {},
    "tasty_pack_ref": null,
    "selected_element_ids": [],
    "conflict_decisions": [],
    "icp": "",
    "platform": "instagram",
    "proof": {},
    "proof_limits": [],
    "production_policy": {}
  },
  "advisor_actions": [
    {
      "owner": "storyboard",
      "accepted_inputs": ["ticket://brief"],
      "authored_output": "ticket://storyboard",
      "acceptance_or_blocker": {
        "state": "accepted",
        "evidence_refs": ["ticket://storyboard-review"],
        "reason": "reviewed against the frozen brief"
      },
      "next_handoff": "asset-advisor"
    }
  ]
}
```

For a visual program, `storyboard`, `asset-advisor`, `editing-advisor`,
`remotion`, and `review` are distinct required owners. An owner string cannot
group lanes. `remotion` cannot be accepted until the three upstream production
owners are accepted with evidence and its `accepted_inputs` names each
upstream authored output. The Creative Input Bundle is immutable for
the program: Brand Kit is the stable visual authority and an optional computed
Tasty Pack supplies selected references. `style_profile` is invalid on this
composed path; standalone `video-production` may still use one when no Brand
Kit/Tasty composition is being compiled.
