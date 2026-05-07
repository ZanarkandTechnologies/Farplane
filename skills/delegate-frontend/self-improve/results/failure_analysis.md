# Failure Analysis

- No unexpected case failures.

## Unexpected Accept-Case Assertion Failures

- None.

## Expected Reject-Case Gate Failures

- warehouse-visual-delta:min_max_changed_ratio: 1
- warehouse-assets:asset_strategy_not: 1
- warehouse-assets:min_assets: 1
- spec-stub:status_in: 1
- spec-stub:nonempty:offer: 1
- spec-stub:nonempty:audience: 1
- spec-stub:nonempty:carrier_world: 1
- spec-stub:nonempty:recipe_id: 1
- spec-stub:nonempty:taste_profile_id: 1
- spec-stub:nonempty:effect_stack_id: 1
- spec-stub:nonempty:qa_plan: 1
- spec-stub:min_field:asset_prompts: 1
- spec-stub:min_field:sections: 1
- spec-stub:min_field:motion_checkpoints: 1
- spec-phase:status_in: 1
- spec-phase:handoff_present: 1
- spec-phase:handoff_section:risks: 1
- spec-phase:handoff_section:first_write_evidence: 1
- asset-manifest-missing-media:asset_strategy_not: 1
- asset-manifest-missing-media:min_assets: 1
- asset-manifest-missing-media:min_generated_or_rendered_count: 1
- asset-manifest-missing-media:require_true:has_mobile_fallback: 1
- asset-manifest-missing-media:require_true:has_reduced_motion_fallback: 1
- asset-manifest-missing-media:source_prompts_present: 1
- warehouse-geometry-bad:min_field:hero_object_fill_ratio: 1
- warehouse-geometry-bad:max_field:first_viewport_blank_ratio: 1
- warehouse-geometry-bad:require_false:nav_overflow: 1
- warehouse-geometry-bad:field_in:mobile_crop_intent: 1
- pi-startup:status_in: 1
- pi-startup:min_session_files: 1
- warehouse-produced-geometry:max_field:first_viewport_blank_ratio: 1
- compiled-spec-phase:status_in: 1
- compiled-assets-phase:status_in: 1
- asset-manifest-unsafe-ref:max_unsafe_refs: 1
- repair-timeout-desktop:score_true:hasStyleScrub: 1
- repair-timeout-desktop:score_true:hasMissionSupportVideos: 1
- repair-timeout-desktop:min_score:supportVideoCount: 1
- repair-timeout-mobile:score_true:hasStyleScrub: 1
- repair-timeout-mobile:score_true:hasMissionSupportVideos: 1
- repair-timeout-mobile:min_score:supportVideoCount: 1
- repair-timeout-phase:status_in: 1
- repair-timeout-phase:handoff_present: 1
- repair-live3-desktop:min_max_changed_ratio: 1
- repair-live3-mobile:min_max_changed_ratio: 1
- repair-live3-geometry:max_field:first_viewport_blank_ratio: 1
- implementation-live4-phase:status_in: 1
- implementation-live4-phase:handoff_present: 1
- implementation-v5-phase:status_in: 1
- implementation-v5-phase:handoff_present: 1
- repair-v4-timeout-phase:status_in: 1
- repair-v4-timeout-phase:handoff_present: 1
- repair-v4-timeout-phase:first_write_status_in: 1
- repair-v4-timeout-first-write:status_in: 1

## Next Hypothesis

- Add a harder captured-output case before optimizing further.
