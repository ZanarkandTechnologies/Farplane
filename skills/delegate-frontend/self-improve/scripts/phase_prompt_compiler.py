#!/usr/bin/env python3
"""Compile bounded delegate-frontend phase prompts for Pi/Kimi runs."""

from __future__ import annotations

import argparse
from pathlib import Path


PHASE_DEFAULTS: dict[str, dict[str, object]] = {
    "startup": {
        "objective": "prove the external CLI can start, write the probe file, and exit cleanly",
        "acceptance": [
            "do not analyze at length; immediately write the probe output",
            "create or modify the probe output as the first external tool call",
            "write a one-paragraph readiness note",
            "do not read skill references or inspect the repository after the probe write",
            "exit after the probe; do not start implementation",
        ],
    },
    "spec": {
        "objective": "produce a complete spec-first cinematic landing-page build plan",
        "acceptance": [
            "include offer, audience, carrier object/world, recipe ID, taste profile ID, and effect stack ID",
            "include at least 5 sections or beats and 5 motion checkpoints: 0%, 25%, 50%, 75%, and 95%",
            "include at least 4 asset prompts with source intent",
            "include QA plan for desktop, mobile, reduced motion, scroll-scrub, visual geometry, and review",
            "write only the spec and handoff; do not implement the page",
        ],
    },
    "assets": {
        "objective": "produce the media asset plan or generated/rendered asset manifest for the approved spec",
        "acceptance": [
            "write assets/asset-manifest.json as the first owned output with a valid JSON object stub before any reference reading",
            "record at least 4 generated/rendered frame, image, or video assets in assets/asset-manifest.json",
            "include a source_prompt for every generated/rendered asset",
            "include mobile and reduced-motion fallbacks",
            "broken refs must be zero",
            "include positive width and height for every generated/rendered image, frame, or video asset",
            "include at least one scroll-scrubbable frame/video/sequence asset",
            "make paths local workspace/public paths, not remote URLs",
            "verify with python3 skills/delegate-frontend/self-improve/scripts/asset_manifest_lint.py assets/asset-manifest.json",
            "code-native-canvas is prototype-only and cannot satisfy final Terminus-level quality",
        ],
    },
    "implementation": {
        "objective": "implement the bounded frontend files from the approved spec and asset manifest",
        "acceptance": [
            "use the supplied spec and asset manifest instead of rereading broad references",
            "expose window.__scrollScrubDebug with progress, phase, frame or mediaTime, active, ready, and reducedMotion",
            "mark the scrubbed stage with data-scroll-scrub-root",
            "wire generated/rendered media or frame assets from assets/asset-manifest.json",
            "for Terminal/Terminus-level final builds, report terminalVerdict and terminalFinalReady; basic verdict PASS is only mechanics proof",
            "report hasTerminalMediaPipeline, hasDominantHeroMedia, hasDistributedScrubDeltas, maxCheckpointChangedRatio, meaningfulCheckpointDeltaCount, strongCheckpointDeltaCount, and midScrollDeltaCount when scroll-scrub QA runs",
            "run syntax checks and scroll-scrub QA when runnable",
        ],
    },
    "repair": {
        "objective": "make one bounded repair patch to an existing frontend artifact until the named mechanical QA gate passes",
        "acceptance": [
            "after the first-write stub, inspect only the owned target file plus explicitly named artifact files",
            "do not read scroll_scrub_qa.cjs, broad skill bodies, screenshots, or unrelated references before the repair patch is complete",
            "do not read sibling prototype pages or previous failed outputs unless the prompt names them as allowed reference files",
            "make the patch before running QA; do not spend the run explaining the gap",
            "preserve the existing production surface, section count, and generated-media wiring; never replace a built page with a minimal dark text stub just to satisfy DOM metrics",
            "style scrub must change computed transform, opacity, filter, or clip-path on at least two elements matching the QA sampled selectors",
            "QA samples these selectors: [data-scroll-scrub-root], [data-scroll-scrub], [data-scroll-progress], [data-scroll-phase], canvas, video, .pin-spacer, .scroll-stage, .scrub-stage, .frame-sequence, .hero-media, .hero, .cinematic, .scene",
            "support video proof must use real video elements and should satisfy hasSupportVideoDom and hasMissionSupportVideos when mission support assets exist",
            "mobile typography proof should satisfy hasMobileHeroPhraseSeparation when the page has a multi-phrase hero title",
            "Terminal/Terminus-level final repair proof should satisfy terminalFinalReady, hasTerminalMediaPipeline, hasDominantHeroMedia, and hasDistributedScrubDeltas; basic verdict PASS is only mechanics proof",
            "report maxCheckpointChangedRatio, meaningfulCheckpointDeltaCount, strongCheckpointDeltaCount, and midScrollDeltaCount",
            "preserve window.__scrollScrubDebug with progress, phase, frame or mediaTime, active, ready, and reducedMotion",
            "run the named QA commands once after the patch; if they still fail, write the handoff with the failing scores instead of looping until timeout",
        ],
    },
    "visual-review": {
        "objective": "review screenshots and QA artifacts without rewriting the whole frontend",
        "acceptance": [
            "compare observed screenshots to the expected spec and Terminal-style bar",
            "report concrete gaps in geometry, motion, assets, typography, enterprise proof, and mobile behavior",
            "produce the smallest repair prompt with one owned file when repair is needed",
            "do not rewrite implementation unless the prompt explicitly grants a repair phase",
        ],
    },
}


def extract_heading_section(markdown: str, heading_name: str) -> str:
    lines = markdown.splitlines()
    start_index: int | None = None
    start_level = 0
    target = heading_name.strip().lower()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        hashes = len(stripped) - len(stripped.lstrip("#"))
        title = stripped.lstrip("#").strip().lower()
        if title == target:
            start_index = index
            start_level = hashes
            break
    if start_index is None:
        return ""
    end_index = len(lines)
    for index in range(start_index + 1, len(lines)):
        stripped = lines[index].strip()
        if not stripped.startswith("#"):
            continue
        hashes = len(stripped) - len(stripped.lstrip("#"))
        if hashes <= start_level:
            end_index = index
            break
    return "\n".join(lines[start_index:end_index]).strip()


def extract_asset_brief(markdown: str, max_chars: int = 9000) -> str:
    chunks: list[str] = []
    title = markdown.splitlines()[0].strip() if markdown.splitlines() else ""
    if title.startswith("#"):
        chunks.append(title)
    for heading in (
        "Route",
        "Offer",
        "Carrier Object / World",
        "Asset Plan",
        "Motion Plan",
        "Gold-Reference Comparison Checklist",
    ):
        section = extract_heading_section(markdown, heading)
        if section:
            chunks.append(section)
    brief = "\n\n".join(chunks).strip()
    if not brief:
        return markdown[:max_chars].strip()
    if len(brief) > max_chars:
        return brief[:max_chars].rstrip() + "\n\n[asset brief truncated for phase focus]"
    return brief


def read_brief(args: argparse.Namespace, phase: str) -> str:
    parts: list[str] = []
    if args.brief:
        parts.append(args.brief.strip())
    if args.brief_file:
        path = Path(args.brief_file).expanduser()
        text = path.read_text(encoding="utf-8").strip()
        if phase == "assets":
            text = extract_asset_brief(text)
        parts.append(text)
    return "\n\n".join(part for part in parts if part)


def bullet_lines(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def compile_prompt(args: argparse.Namespace) -> str:
    phase = args.phase
    phase_defaults = PHASE_DEFAULTS[phase]
    owned_outputs = args.owned_output or (["PROBE.md"] if phase == "startup" else [])
    acceptance = [str(item) for item in phase_defaults["acceptance"]]
    if phase == "assets" and owned_outputs:
        acceptance = [item.replace("assets/asset-manifest.json", owned_outputs[0]) for item in acceptance]
    acceptance.extend(args.acceptance or [])
    brief = read_brief(args, phase) or "No extra brief supplied. Use the selected route and acceptance criteria below."

    handoff_path = args.handoff_path or "handoff.md"
    if owned_outputs:
        first_write_section = [
            "## First-Write Contract",
            (
                f"Your first external tool call must create or modify `{owned_outputs[0]}` "
                "with a small valid stub before reading skill bodies, broad references, "
                "screenshots, or unrelated files."
            ),
            "The wrapper pre-creates parent directories for owned outputs; do not use `mkdir` as the first tool call.",
            "",
            "After the first-write proof exists, finish the owned artifact from the constraints in this prompt before optional reference reading.",
        ]
    else:
        first_write_section = [
            "## First-Write Contract",
            "No owned output was supplied for this handoff-only phase. Do not claim first-write evidence.",
            "",
            "Use the constraints in this prompt and write only the requested handoff.",
        ]
    lines = [
        f"# Delegate Frontend Phase Prompt: {phase}",
        "",
        "## Mission",
        str(phase_defaults["objective"]),
        "",
        *first_write_section,
        "",
        "## Selected Route",
        f"- recipe_id: {args.recipe_id}",
        f"- taste_profile_id: {args.taste_profile_id}",
        f"- effect_stack_id: {args.effect_stack_id}",
        "",
        "## Owned Outputs",
        bullet_lines(owned_outputs) if owned_outputs else "- none; this phase should only write the handoff",
        "",
        "## Brief",
        brief,
        "",
        "## Acceptance Criteria",
        bullet_lines(acceptance),
        "",
        "## Phase Boundaries",
        "- Preserve unrelated changes.",
        "- Do not push, deploy, publish, or perform destructive actions.",
        "- Do not claim final Codexter completion.",
        "- Do not build outside this phase.",
        "- Do not spend on generated media unless this is an approved asset phase and the asset skill gates pass.",
        "",
        "## Handoff",
        f"Write the delegated handoff to `{handoff_path}`.",
        "Include changed files, verification commands/results, loaded skills, risks, and next phase recommendation.",
    ]
    if phase == "assets":
        lines.extend(
            [
                "",
                "## Required Asset Manifest Shape",
                "Use this schema shape, adding fields only when useful:",
                "",
                "```json",
                "{",
                '  "asset_strategy": "generated-frame-sequence",',
                '  "has_mobile_fallback": true,',
                '  "has_reduced_motion_fallback": true,',
                '  "assets": [',
                "    {",
                '      "path": "frames/hero-desktop-0001.webp",',
                '      "kind": "generated-frame",',
                '      "role": "desktop hero frame sequence",',
                '      "width": 1920,',
                '      "height": 1080,',
                '      "source_prompt": "..."',
                "    }",
                "  ]",
                "}",
                "```",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def summarize_prompt(
    *,
    prompt: str,
    phase: str,
    owned_outputs: list[str],
    recipe_id: str,
    taste_profile_id: str,
    effect_stack_id: str,
) -> dict[str, object]:
    lowered = prompt.lower()
    summary: dict[str, object] = {
        "phase": phase,
        "owned_outputs": owned_outputs,
        "contains_first_write": "first external tool call must create or modify" in lowered,
        "contains_selected_route": all(
            value in prompt
            for value in (recipe_id, taste_profile_id, effect_stack_id)
        ),
        "contains_phase_boundary": "Do not build outside this phase." in prompt,
        "forbids_broad_reference_before_first_write": "before reading skill bodies, broad references" in prompt,
        "forbids_full_page_build": "do not implement the page" in lowered if phase == "spec" else True,
    }
    if phase == "repair":
        summary.update(
            {
                "contains_repair_micro_patch": "make one bounded repair patch" in lowered,
                "forbids_qa_script_read": "do not read scroll_scrub_qa.cjs" in lowered,
                "forbids_sibling_prototype_read": "do not read sibling prototype pages" in lowered,
                "requires_style_scrub": "style scrub must change computed transform" in lowered,
                "requires_support_video_metric": "hasmissionsupportvideos" in lowered,
                "requires_mobile_phrase_separation": "hasmobileherophraseseparation" in lowered,
                "requires_terminal_final_ready": "terminalfinalready" in lowered,
                "requires_distributed_scrub_deltas": "hasdistributedscrubdeltas" in lowered,
                "preserves_existing_surface": "never replace a built page with a minimal dark text stub" in lowered,
            }
        )
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--phase",
        choices=sorted(PHASE_DEFAULTS),
        required=True,
    )
    parser.add_argument("--brief", default="")
    parser.add_argument("--brief-file", default="")
    parser.add_argument("--owned-output", action="append", default=[])
    parser.add_argument("--handoff-path", default="")
    parser.add_argument("--recipe-id", default="cinematic-industrial-scroll")
    parser.add_argument("--taste-profile-id", default="terminal-mission-control")
    parser.add_argument("--effect-stack-id", default="video-frame-sequence-scroll-scrub")
    parser.add_argument("--acceptance", action="append", default=[])
    parser.add_argument("--output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prompt = compile_prompt(args)
    if args.output:
        output = Path(args.output).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(prompt, encoding="utf-8")
    else:
        print(prompt, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
