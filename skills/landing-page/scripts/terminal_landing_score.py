#!/usr/bin/env python3
"""Score Terminal-style scroll landing pages with mechanical evidence checks."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TEXT_EXTENSIONS = {".html", ".css", ".js", ".md", ".json", ".txt"}
IGNORED_SITE_TEXT_NAMES = {
    "BRIEF.md",
}
PLACEHOLDER_HANDOFF_MARKERS = (
    "pending live external cli run",
    "- none reported yet",
    "status: pending",
    "observed output: pending",
)
HANDOFF_COMPLETION_SECTION_PATTERNS = {
    "changed_files": re.compile(
        r"^(?:Changed Files|Changed\s*/\s*Produced Files|Produced Files)$",
        re.I,
    ),
    "verification": re.compile(
        r"^(?:Verification(?:\s+Commands\s*&\s*Results)?|Self-Review Findings|Output Contract Compliance)$",
        re.I,
    ),
    "risks": re.compile(r"^(?:Risks(?:\s*/\s*Followups)?|Findings\s*/\s*Risks)$", re.I),
}


@dataclass
class Dimension:
    name: str
    score: int
    max_score: int
    findings: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", required=True)
    parser.add_argument("--desktop-qa", default="")
    parser.add_argument("--mobile-qa", default="")
    parser.add_argument("--delegate-run-dir", default="")
    parser.add_argument("--out", default="")
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def load_json(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def has_any(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return any(needle.lower() in lowered for needle in needles)


def markdown_sections(text: str) -> dict[str, str]:
    matched: dict[str, list[str]] = {}
    current_name = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            current_name = ""
            for name, pattern in HANDOFF_COMPLETION_SECTION_PATTERNS.items():
                if pattern.fullmatch(title):
                    current_name = name
                    matched.setdefault(name, [])
                    break
            continue
        if current_name:
            matched[current_name].append(raw_line)
    return {name: "\n".join(lines).strip() for name, lines in matched.items()}


def find_file(site_dir: Path, names: list[str]) -> Path | None:
    for name in names:
        candidate = site_dir / name
        if candidate.exists():
            return candidate
    for path in site_dir.rglob("*"):
        if path.is_file() and path.name in names:
            return path
    return None


def collect_site_text(site_dir: Path) -> str:
    chunks: list[str] = []
    for path in sorted(site_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if path.name in IGNORED_SITE_TEXT_NAMES:
            continue
        if path.name.startswith("terminal-score") and path.suffix.lower() == ".json":
            continue
        if any(part.startswith("qa-") for part in path.parts):
            continue
        if path.stat().st_size > 500_000:
            continue
        chunks.append(f"\n\n--- {path.relative_to(site_dir)} ---\n")
        chunks.append(read_text(path))
    return "".join(chunks)


def manifest_path(site_dir: Path) -> Path | None:
    return find_file(site_dir, ["asset-manifest.json"])


def asset_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    raw_assets = manifest.get("assets")
    if isinstance(raw_assets, list):
        return [item for item in raw_assets if isinstance(item, dict)]
    if isinstance(raw_assets, dict):
        return [item for item in raw_assets.values() if isinstance(item, dict)]
    return []


def asset_text(entry: dict[str, Any]) -> str:
    return " ".join(str(value) for value in entry.values()).lower()


def local_asset_exists(site_dir: Path, manifest_file: Path | None, entry: dict[str, Any]) -> bool:
    raw_path = str(entry.get("path") or entry.get("src") or "").strip()
    if not raw_path or re.match(r"^https?://", raw_path):
        return False
    candidates: list[Path] = []
    if manifest_file is not None:
        candidates.append(manifest_file.parent / raw_path)
    candidates.append(site_dir / raw_path)
    candidates.append(site_dir / raw_path.lstrip("/"))
    return any(candidate.exists() for candidate in candidates)


def score_strategy(site_dir: Path, text: str) -> Dimension:
    spec = find_file(site_dir, ["SPEC.md", "spec.md", "landing-brief.md"])
    spec_text = read_text(spec) if spec else ""
    combined = spec_text
    checks = [
        ("spec file exists", spec is not None),
        ("competitor or inspiration analysis", has_any(combined, ["competitor", "inspiration", "terminal industries", "primary reference", "gold reference"])),
        ("user story or buyer job", has_any(combined, ["user story", "buyer", "job", "audience"])),
        ("section-count or section map", has_any(combined, ["section map", "hero -> problem", "problem -> solution", "sections"])),
        ("ascii or low-fidelity flow", has_any(combined, ["ascii", "low-fidelity", "[hero", "beat 0"])),
        ("nested advise decisions", has_any(combined, ["nested advise", "advise", "rejected options", "tradeoff accepted"])),
        ("phase-aware handoff", has_any(combined, ["phase", "handoff", "spec", "assets", "implementation", "visual-review"])),
    ]
    points = [4, 3, 3, 3, 3, 3, 1]
    score = sum(point for (_, passed), point in zip(checks, points) if passed)
    findings = [name for name, passed in checks if not passed]
    return Dimension("strategy_and_spec", score, 20, findings)


def score_assets(site_dir: Path, text: str) -> Dimension:
    manifest_file = manifest_path(site_dir)
    manifest = load_json(manifest_file)
    assets = asset_entries(manifest)
    manifest_text = json.dumps(manifest, sort_keys=True).lower() if manifest else ""
    joined = "\n".join(asset_text(asset) for asset in assets) + "\n" + manifest_text
    existing_count = sum(1 for asset in assets if local_asset_exists(site_dir, manifest_file, asset))
    generated_media = manifest.get("generated_media") if isinstance(manifest.get("generated_media"), dict) else {}
    generated_count = int(generated_media.get("count") or 0) if isinstance(generated_media, dict) else 0
    if generated_count == 0:
        generated_count = sum(
            1
            for asset in assets
            if has_any(asset_text(asset), ["generated-", "rendered-", ".mp4", ".webp", "frame-sequence"])
        )
    code_native_only = generated_count == 0 and "code-native" in joined
    has_manifest = manifest_file is not None and bool(manifest)
    has_video_or_frames = generated_count > 0 or (
        has_any(joined, [".mp4", ".webp", "generated-frame", "rendered-video"])
        and not code_native_only
    )
    has_prompt = (
        any(asset.get("source_prompt") or asset.get("prompt") for asset in assets)
        or bool(generated_media.get("upgrade_prompts") if isinstance(generated_media, dict) else False)
    )
    has_mobile = bool(manifest.get("has_mobile_fallback")) or has_any(joined, ["mobile", "crop"])
    has_reduced = bool(manifest.get("has_reduced_motion_fallback")) or has_any(joined, ["reduced-motion", "reduced motion", "poster"])
    has_support = has_any(joined, ["support", "mission", "proof", "section still", "loop"])
    no_remote_refs = not any(re.match(r"^https?://", str(asset.get("path") or asset.get("src") or "")) for asset in assets)
    checks = [
        ("asset manifest exists and parses", has_manifest, 4),
        ("video or frame sequence planned", has_video_or_frames, 4),
        ("source prompts recorded", has_prompt, 3),
        ("mobile fallback or crop", has_mobile, 3),
        ("reduced-motion/poster fallback", has_reduced, 3),
        ("support assets beyond hero", has_support, 2),
        ("local existing asset refs", existing_count >= min(2, len(assets)) if assets and not code_native_only else False, 1),
        ("no remote manifest paths", no_remote_refs if assets else False, 0),
    ]
    score = sum(points for _, passed, points in checks if passed)
    findings = [name for name, passed, _ in checks if not passed]
    return Dimension("asset_pipeline", min(score, 20), 20, findings)


def qa_score(qa: dict[str, Any]) -> dict[str, Any]:
    score = qa.get("score")
    return score if isinstance(score, dict) else {}


def score_scroll(desktop_qa: dict[str, Any]) -> Dimension:
    qscore = qa_score(desktop_qa)
    checks = [
        ("terminal final readiness", desktop_qa.get("terminalVerdict") == "PASS" or bool(qscore.get("terminalFinalReady")), 7),
        ("required debug contract", bool(qscore.get("hasRequiredDebugContract")), 4),
        ("debug/media/style scrub", any(qscore.get(key) for key in ("hasDebugScrub", "hasMediaScrub", "hasStyleScrub")), 4),
        ("distributed checkpoint deltas", bool(qscore.get("hasDistributedScrubDeltas")), 4),
        ("pinned or GSAP/ScrollTrigger signal", bool(qscore.get("hasPinnedSurface") or qscore.get("hasGsapOrScrollTrigger")), 3),
        ("mid-scroll checkpoint movement", int(qscore.get("midScrollDeltaCount") or 0) >= 1, 2),
        ("low failure-hint count", len(desktop_qa.get("terminalFailureHints") or desktop_qa.get("failureHints") or []) == 0, 1),
    ]
    score = sum(points for _, passed, points in checks if passed)
    findings = [name for name, passed, _ in checks if not passed]
    return Dimension("scroll_scrub_mechanics", score, 25, findings)


def score_visual(desktop_qa: dict[str, Any], text: str) -> Dimension:
    qscore = qa_score(desktop_qa)
    geometry = desktop_qa.get("visualGeometry")
    geometry = geometry if isinstance(geometry, dict) else {}
    fill = float(geometry.get("hero_object_fill_ratio") or geometry.get("dom_hero_object_fill_ratio") or 0)
    blank = float(geometry.get("first_viewport_blank_ratio") or geometry.get("dom_first_viewport_blank_ratio") or 1)
    has_early_signal = has_any(text, ["computer vision", "warehouse", "yard", "dock", "gate", "terminal", "ai"])
    has_enterprise_copy = has_any(text, ["enterprise", "operations", "safety", "sla", "accuracy", "audit", "workflow", "deployment"])
    checks = [
        ("dominant hero media", bool(qscore.get("hasDominantHeroMedia")) or fill >= 0.35, 3),
        ("visible initial hero offer", bool(qscore.get("hasInitialHeroOfferVisible")), 3),
        ("low first viewport blank band", blank <= 0.25, 2),
        ("product/category signal early", has_early_signal, 2),
        ("enterprise proof language", has_enterprise_copy, 2),
        ("support video or section media", int(qscore.get("supportVideoCount") or 0) >= 2 or bool(qscore.get("hasSupportVideoDom")), 2),
        ("checkpoint visual delta is strong enough", float(qscore.get("maxCheckpointChangedRatio") or 0) >= 0.12, 1),
    ]
    score = sum(points for _, passed, points in checks if passed)
    findings = [name for name, passed, _ in checks if not passed]
    return Dimension("visual_craft_proxy", score, 15, findings)


def score_mobile(mobile_qa: dict[str, Any], desktop_qa: dict[str, Any]) -> Dimension:
    source = mobile_qa or desktop_qa
    qscore = qa_score(source)
    geometry = source.get("visualGeometry")
    geometry = geometry if isinstance(geometry, dict) else {}
    checks = [
        ("mobile QA supplied", bool(mobile_qa), 2),
        ("mobile hero phrase separation", bool(qscore.get("hasMobileHeroPhraseSeparation")), 2),
        ("mobile deliberate crop or no nav overflow", geometry.get("mobile_crop_intent") == "deliberate" or not geometry.get("nav_overflow", True), 2),
        ("reduced-motion debug field exists", "reducedMotion" in str(source), 2),
        ("terminal readiness holds on mobile/source", source.get("terminalVerdict") == "PASS" or bool(qscore.get("terminalFinalReady")), 2),
    ]
    score = sum(points for _, passed, points in checks if passed)
    findings = [name for name, passed, _ in checks if not passed]
    return Dimension("mobile_and_reduced_motion", score, 10, findings)


def handoff_complete(text: str) -> bool:
    if not text.strip():
        return False
    lowered = text.lower()
    if any(marker in lowered for marker in PLACEHOLDER_HANDOFF_MARKERS):
        return False
    sections = markdown_sections(text)
    return all(bool(sections.get(section)) for section in ("changed_files", "verification", "risks"))


def output_quality_ok(first_write: dict[str, Any]) -> bool:
    raw_quality = first_write.get("output_quality")
    if not isinstance(raw_quality, dict):
        return True
    return str(raw_quality.get("status", "")).lower() in {"pass", "not_configured"}


def score_delegation(run_dir_raw: str) -> Dimension:
    if not run_dir_raw:
        return Dimension("delegation_process_evidence", 0, 10, ["delegate run dir not supplied"])
    run_dir = Path(run_dir_raw)
    first_write = load_json(run_dir / "first_write.json")
    session_files = load_json(run_dir / "session_files.json")
    handoff = read_text(run_dir / "handoff.md")
    exit_code = read_text(run_dir / "exit_code.txt").strip()
    checks = [
        ("prompt captured", (run_dir / "prompt.md").exists(), 1),
        ("command captured", (run_dir / "command.json").exists(), 1),
        ("stdout/stderr logs captured", (run_dir / "stdout.log").exists() and (run_dir / "stderr.log").exists(), 1),
        ("first-write passed", first_write.get("status") == "pass", 1),
        ("output quality passed or not configured", output_quality_ok(first_write), 1),
        ("session files captured", bool(session_files.get("session_files") if isinstance(session_files, dict) else session_files), 1),
        ("handoff complete", handoff_complete(handoff), 2),
        ("run exited cleanly", exit_code == "0", 1),
        ("handoff mentions skills or loaded skills", has_any(handoff, ["loaded skills", "landing-page", "frontend-craft", "visual-qa", "review"]), 1),
    ]
    score = sum(points for _, passed, points in checks if passed)
    findings = [name for name, passed, _ in checks if not passed]
    return Dimension("delegation_process_evidence", score, 10, findings)


def anchored_score(percent: int) -> float:
    if percent < 40:
        return 1.0
    if percent < 60:
        return 2.0
    if percent < 75:
        return 3.0
    if percent < 90:
        return 4.0
    return 5.0


def hard_gates(dimensions: list[Dimension], desktop_qa: dict[str, Any], delegate_run_dir: str) -> list[str]:
    gates: list[str] = []
    by_name = {dimension.name: dimension for dimension in dimensions}
    if by_name["strategy_and_spec"].score < 10:
        gates.append("strategy/spec evidence too thin for Terminal final parity")
    if by_name["asset_pipeline"].score < 10:
        gates.append("asset pipeline lacks generated/rendered media proof")
    if by_name["scroll_scrub_mechanics"].score < 15:
        gates.append("scroll-scrub mechanics are not proven")
    if desktop_qa and desktop_qa.get("terminalVerdict") != "PASS":
        gates.append("desktop terminalVerdict is not PASS")
    if delegate_run_dir and by_name["delegation_process_evidence"].score < 6:
        gates.append("delegated run evidence is incomplete")
    return gates


def main() -> int:
    args = parse_args()
    site_dir = Path(args.site_dir).expanduser().resolve()
    desktop_qa = load_json(Path(args.desktop_qa).expanduser().resolve() if args.desktop_qa else None)
    mobile_qa = load_json(Path(args.mobile_qa).expanduser().resolve() if args.mobile_qa else None)
    text = collect_site_text(site_dir) if site_dir.exists() else ""
    dimensions = [
        score_strategy(site_dir, text),
        score_assets(site_dir, text),
        score_scroll(desktop_qa),
        score_visual(desktop_qa, text),
        score_mobile(mobile_qa, desktop_qa),
        score_delegation(args.delegate_run_dir),
    ]
    total = sum(dimension.score for dimension in dimensions)
    gates = hard_gates(dimensions, desktop_qa, args.delegate_run_dir)
    verdict = "pass" if total >= 80 and not gates else ("revise" if total >= 50 else "block")
    result = {
        "scored_at": datetime.now(timezone.utc).isoformat(),
        "site_dir": str(site_dir),
        "desktop_qa": args.desktop_qa,
        "mobile_qa": args.mobile_qa,
        "delegate_run_dir": args.delegate_run_dir,
        "percent_score": total,
        "threshold": 80,
        "anchored_score": anchored_score(total),
        "verdict": verdict,
        "hard_gates": gates,
        "dimensions": [asdict(dimension) for dimension in dimensions],
        "next_action": next((gate for gate in gates), "human visual review against gold reference"),
    }
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        out_path = Path(args.out).expanduser()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
