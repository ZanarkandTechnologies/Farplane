from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_production_program.py")
SPEC = importlib.util.spec_from_file_location("validate_production_program", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def valid_program() -> dict:
    actions = []
    outputs = {owner: f"ticket://{owner}-output" for owner in ("storyboard", "asset-advisor", "editing-advisor", "remotion", "review")}
    for owner, next_owner in (
        ("storyboard", "asset-advisor"),
        ("asset-advisor", "editing-advisor"),
        ("editing-advisor", "remotion"),
        ("remotion", "review"),
        ("review", "distribution_handoff"),
    ):
        accepted_inputs = [f"ticket://{owner}-input"]
        if owner == "remotion":
            accepted_inputs = [outputs[name] for name in ("storyboard", "asset-advisor", "editing-advisor")]
        actions.append({
            "owner": owner,
            "accepted_inputs": accepted_inputs,
            "authored_output": outputs[owner],
            "acceptance_or_blocker": {
                "state": "accepted",
                "evidence_refs": [f"ticket://{owner}-receipt"],
                "reason": "accepted by the owning lane",
            },
            "next_handoff": next_owner,
        })
    return {
        "schema_version": "1.0",
        "content_kind": "reel",
        "creative_input_bundle": {
            "brand_kit_snapshot": {"id": "gagazet", "kit_revision": 1, "prompt_revision": 1, "prompt": "clean explainer", "elements": ["halftone"], "resolution_state": "resolved"},
            "tasty_pack_ref": None,
            "selected_element_ids": ["brand:halftone"],
            "conflict_decisions": [],
            "icp": "people tracking AI infrastructure risk",
            "platform": "instagram",
            "proof": {"evidence_ref": "ticket://evidence"},
            "proof_limits": ["do not claim delivered capacity"],
            "production_policy": {"publish_gate": "human"},
        },
        "advisor_actions": actions,
    }


class ProductionProgramTests(unittest.TestCase):
    def test_owner_separated_program_passes(self) -> None:
        self.assertEqual(validator.validate(valid_program()), [])

    def test_grouped_owner_and_missing_sibling_fail(self) -> None:
        program = valid_program()
        program["advisor_actions"][0]["owner"] = "storyboard / asset-advisor"
        program["advisor_actions"] = [row for row in program["advisor_actions"] if row["owner"] != "asset-advisor"]
        errors = validator.validate(program)
        self.assertTrue(any("exactly one owner" in error for error in errors))
        self.assertTrue(any("missing required visual owners" in error for error in errors))

    def test_remotion_cannot_pass_before_assets_and_editing(self) -> None:
        program = valid_program()
        for row in program["advisor_actions"]:
            if row["owner"] == "editing-advisor":
                row["acceptance_or_blocker"] = {"state": "blocked", "evidence_refs": [], "reason": "timing recipe missing"}
        errors = validator.validate(program)
        self.assertTrue(any("remotion cannot be accepted" in error for error in errors))

    def test_style_profile_is_not_a_third_authority(self) -> None:
        program = copy.deepcopy(valid_program())
        program["creative_input_bundle"]["style_profile"] = {"look": "newspaper"}
        errors = validator.validate(program)
        self.assertTrue(any("style_profile" in error for error in errors))

    def test_remotion_must_consume_each_upstream_output(self) -> None:
        program = valid_program()
        remotion = next(row for row in program["advisor_actions"] if row["owner"] == "remotion")
        remotion["accepted_inputs"].remove("ticket://editing-advisor-output")
        errors = validator.validate(program)
        self.assertTrue(any("accepted_inputs missing upstream outputs" in error for error in errors))

    def test_blank_or_unversioned_brand_snapshot_fails(self) -> None:
        program = valid_program()
        program["creative_input_bundle"]["brand_kit_snapshot"].update({
            "id": " ",
            "prompt": "",
            "kit_revision": None,
            "prompt_revision": 0,
            "elements": [""],
        })
        program["creative_input_bundle"]["selected_element_ids"] = []
        errors = validator.validate(program)
        self.assertTrue(any(".id must be a non-empty string" in error for error in errors))
        self.assertTrue(any(".prompt must be a non-empty string" in error for error in errors))
        self.assertTrue(any("kit_revision must be a positive integer" in error for error in errors))
        self.assertTrue(any("prompt_revision must be a positive integer" in error for error in errors))
        self.assertTrue(any("elements must be a non-empty list of IDs" in error for error in errors))
        self.assertTrue(any("selected_element_ids must not be empty" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
