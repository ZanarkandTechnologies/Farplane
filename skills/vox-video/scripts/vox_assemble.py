"""Assemble a Vox-style reel: retime silent clips to narration windows, slam
real-type paper labels on cue, mix the one narration track, render, and check.

Run (any directory): uv run --with pillow python <repo>/skills/vox-video/scripts/vox_assemble.py plan.json
Raw clip sheet:      ... vox_assemble.py --sheet c1.mp4 [fps]

Exit 0 only when the transcript check passes; 1 on a failed check, 2 when
whisper-cli or its model is missing (install whisper-cpp, never skip the check),
3 on an invalid plan.

plan.json (paths relative to the plan file):
{
  "size": [1080, 1920], "fps": 24, "out": "final.mp4",
  "vo": "vo.wav",
  "script": "script.txt",                       # required: the exact narration text
  "must_hear": ["$16,000", "-38 degrees"],       # required: figures with sign and unit, names
  "clips": [{"file": "c1.mp4", "start": 0.0, "end": 3.8}],
  "vo_segments": [{"from": 0.25, "to": 3.70, "at": 0.0}],
  "labels": [{"text": "$16,000", "start": 0.3, "end": 2.3, "y": 260,
              "x": "center", "style": "paper", "size": 150, "rot": 6}]
}
Clips play back to back from 0 with no gaps; each is retimed to fill its
[start, end) window, which must stay within 0.6x-1.7x of the clip's length.
Labels: "x" is "center" or the label's centre in pixels; "y" is its top edge.
Styles: "paper" (torn card, black type) or "stamp" (red outline).
"""

import difflib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONTS = [
    "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf",
    "/System/Library/Fonts/Supplemental/Impact.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
PAPER, INK, RED = (244, 239, 228, 255), (20, 20, 20, 255), (178, 34, 34, 255)
WHISPER_MODEL = os.path.expanduser("~/.cache/whisper-cpp/ggml-small.en.bin")


def probe_duration(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out)


def torn_outline(w, h, jag, rnd, step=14):
    pts = [(x, rnd.uniform(0, jag)) for x in range(0, w + 1, step)]
    pts += [(w - rnd.uniform(0, jag), y) for y in range(0, h + 1, step)]
    pts += [(x, h - rnd.uniform(0, jag)) for x in range(w, -1, -step)]
    pts += [(rnd.uniform(0, jag), y) for y in range(h, -1, -step)]
    return pts


def render_label(spec, font_path, seed):
    rnd = random.Random(seed)
    size, text, stamp = spec.get("size", 160), spec["text"], spec.get("style") == "stamp"
    font = ImageFont.truetype(font_path, size)
    left, top, right, bottom = font.getbbox(text)
    tw, th = right - left, bottom - top
    pw, ph = tw + size // 2, th + size // 2
    card = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)
    origin = ((pw - tw) / 2 - left, (ph - th) / 2 - top)
    if stamp:
        draw.rectangle([6, 6, pw - 7, ph - 7], outline=RED, width=max(6, size // 14))
        draw.text(origin, text, font=font, fill=RED)
        for _ in range(pw * ph // 900):  # ink wear
            x, y = rnd.randrange(pw), rnd.randrange(ph)
            draw.ellipse([x, y, x + rnd.randint(1, 4), y + rnd.randint(1, 4)], fill=(0, 0, 0, 0))
    else:
        draw.polygon(torn_outline(pw, ph, size * 0.08, rnd), fill=PAPER)
        draw.text((origin[0], origin[1] + size * 0.04), text, font=font, fill=INK)
    card = card.rotate(spec.get("rot", 0), resample=Image.BICUBIC, expand=True)
    pad = 40
    canvas = Image.new("RGBA", (card.width + 2 * pad, card.height + 2 * pad), (0, 0, 0, 0))
    if not stamp:
        shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        shadow.paste((0, 0, 0, 110), (pad + 10, pad + 14), card)
        canvas = Image.alpha_composite(canvas, shadow.filter(ImageFilter.GaussianBlur(12)))
    canvas.alpha_composite(card, (pad, pad))
    return canvas


def validate(plan, base):
    errors = []
    if not plan.get("script") or not plan.get("must_hear"):
        errors.append("plan needs 'script' and a non-empty 'must_hear' list")
    if not plan.get("clips") or not plan.get("vo"):
        errors.append("plan needs 'clips' and 'vo'")
    paths = [plan.get("vo"), plan.get("script")] + [c.get("file") for c in plan.get("clips", [])]
    errors += [f"missing file: {p}" for p in paths if p and not os.path.exists(os.path.join(base, p))]
    if errors:
        fail_plan(errors)
    cursor = 0.0
    for clip in plan["clips"]:
        if abs(clip["start"] - cursor) > 0.01:
            errors.append(f"{clip['file']}: starts at {clip['start']}, expected {cursor:.2f} (no gaps)")
        cursor = clip["end"]
        factor = (clip["end"] - clip["start"]) / probe_duration(os.path.join(base, clip["file"]))
        if not 0.6 <= 1 / factor <= 1.7:
            errors.append(f"{clip['file']}: speed {1 / factor:.2f}x is outside 0.6-1.7x; regenerate at a fitting length")
    for seg in plan.get("vo_segments", []):
        if seg["at"] + seg["to"] - seg["from"] > cursor + 0.01:
            errors.append(f"narration segment at {seg['at']} runs past the last clip end {cursor}")
    if errors:
        fail_plan(errors)


def fail_plan(errors):
    print("plan errors:\n- " + "\n- ".join(errors), file=sys.stderr)
    sys.exit(3)


def contact_sheet(video, out, fps=1):
    frames = max(1, round(probe_duration(video) * fps))
    cols = min(8, frames)
    rows = -(-frames // cols)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf",
                    f"fps={fps},scale=270:-1,tile={cols}x{rows}", "-frames:v", "1", out], check=True)


def build_command(plan, base, work):
    width, height = plan.get("size", [1080, 1920])
    fps = plan.get("fps", 24)
    total = plan["clips"][-1]["end"]
    font = next((f for f in [plan.get("font")] + FONTS if f and os.path.exists(f)), None)
    if not font:
        fail_plan(["no usable font: set 'font' to a .ttf path"])

    cmd = ["ffmpeg", "-v", "error", "-y"]
    for clip in plan["clips"]:
        cmd += ["-i", os.path.join(base, clip["file"])]
    vo_index = len(plan["clips"])
    cmd += ["-i", os.path.join(base, plan["vo"])]
    label_index = vo_index + 1
    for i, spec in enumerate(plan.get("labels", [])):
        png = os.path.join(work, f"label{i}.png")
        render_label(spec, font, seed=i + 1).save(png)
        # A looped still must be bounded, or ffmpeg never finishes.
        cmd += ["-framerate", str(fps), "-loop", "1", "-t", f"{total:.3f}", "-i", png]

    parts = []
    for i, clip in enumerate(plan["clips"]):
        factor = (clip["end"] - clip["start"]) / probe_duration(os.path.join(base, clip["file"]))
        parts.append(
            f"[{i}:v]setpts=PTS*{factor:.5f},fps={fps},scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},format=yuv420p,settb=1/{fps}[v{i}]")
    n = len(plan["clips"])
    parts.append("".join(f"[v{i}]" for i in range(n))
                 + f"concat=n={n}:v=1:a=0,trim=0:{total:.3f},setpts=PTS-STARTPTS[base]")
    last = "base"
    for i, spec in enumerate(plan.get("labels", [])):
        x = spec.get("x", "center")
        x_expr = "(W-w)/2" if x == "center" else f"{x}-w/2"
        start, end, y = spec["start"], spec["end"], spec.get("y", 260)
        out = f"o{i}"
        parts.append(
            f"[{last}][{label_index + i}:v]overlay=x={x_expr}:"
            f"y={y}-max(0\\,0.15-(t-{start}))*400:enable='between(t,{start},{end})'[{out}]")
        last = out
    segs = plan.get("vo_segments") or [{"from": 0, "to": probe_duration(os.path.join(base, plan["vo"])), "at": 0}]
    for i, seg in enumerate(segs):
        parts.append(f"[{vo_index}:a]atrim={seg['from']}:{seg['to']},asetpts=PTS-STARTPTS,"
                     f"adelay={int(seg['at'] * 1000)}:all=1[a{i}]")
    parts.append("".join(f"[a{i}]" for i in range(len(segs)))
                 + f"amix=inputs={len(segs)}:normalize=0:duration=longest,aresample=48000[aout]")
    out_path = os.path.join(base, plan.get("out", "final.mp4"))
    cmd += ["-filter_complex", ";".join(parts), "-map", f"[{last}]", "-map", "[aout]",
            "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-c:a", "aac", "-b:a", "192k",
            "-t", f"{total:.3f}", out_path]
    return cmd, out_path


def words(text):
    # Whisper writes "minus 38" and "-38" interchangeably; keep the sign.
    text = text.lower().replace("\u2212", "-")  # Unicode minus sign
    text = re.sub(r"\bminus\s+(?=\d)", "-", text).replace(",", "")
    text = text.replace("°", " degrees ")
    return re.findall(r"-?[a-z0-9$]+", text)


def transcript_check(video, script_path, must_hear, work):
    if not shutil.which("whisper-cli") or not os.path.exists(WHISPER_MODEL):
        return {"status": "skipped", "reason": "whisper-cli or its model is missing; install whisper-cpp"}
    wav = os.path.join(work, "check.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-ar", "16000", "-ac", "1", wav], check=True)
    heard = subprocess.run(["whisper-cli", "-m", WHISPER_MODEL, "-f", wav, "-np", "-nt"],
                           capture_output=True, text=True).stdout.strip()
    expected = open(script_path).read()
    ratio = difflib.SequenceMatcher(None, words(expected), words(heard)).ratio()
    heard_words = f" {' '.join(words(heard))} "
    missing = [fact for fact in must_hear if f" {' '.join(words(fact))} " not in heard_words]
    status = "pass" if ratio >= 0.85 and not missing else "fail"
    return {"status": status, "similarity": round(ratio, 2), "missing_facts": missing, "heard": heard}


def main():
    if sys.argv[1] == "--sheet":
        video = os.path.abspath(sys.argv[2])
        fps = float(sys.argv[3]) if len(sys.argv) > 3 else 2
        out = os.path.splitext(video)[0] + "_sheet.png"
        contact_sheet(video, out, fps)
        print(out)
        return
    plan_path = os.path.abspath(sys.argv[1])
    base = os.path.dirname(plan_path)
    plan = json.load(open(plan_path))
    validate(plan, base)
    work = tempfile.mkdtemp(prefix="vox_")
    try:
        cmd, out_path = build_command(plan, base, work)
        subprocess.run(cmd, check=True)
        sheet = os.path.splitext(out_path)[0] + "_sheet.png"
        contact_sheet(out_path, sheet)
        check = transcript_check(
            out_path, os.path.join(base, plan["script"]), plan["must_hear"], work)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(json.dumps({"final": out_path, "duration": round(probe_duration(out_path), 2),
                      "contact_sheet": sheet, "transcript": check}, indent=2))
    sys.exit({"pass": 0, "fail": 1}.get(check["status"], 2))


if __name__ == "__main__":
    main()
