---
title: Vox video call recipes
status: active
owner: skills/vox-video
kind: reference
---

# Call Recipes

Load at N4 and N5. Checked live on 15 Oct 2026; confirm prices with
`catalog_get` before each paid call, since treg listings change.

Use the `treg` CLI with `--file body.json` so base64 audio never lands in the
conversation; keep every request body in `prompts/`.

## Narration: Gemini 3.8 Flash TTS

```bash
treg call google-ai.voice-gen.gemini-3-8-flash-tts --method POST \
  --query model=gemini-3.8-flash-tts --file prompts/tts.json > takes/tts1.json
```

```json
{"contents": [{"parts": [{"text": "<the plain script, nothing else>"}]}],
 "generationConfig": {"responseModalities": ["AUDIO"],
  "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Charon"}}}}}
```

- The WAV (24 kHz mono) is base64 at `body.candidates[0].content.parts[0].inlineData.data`.
- The catalog example puts a cue such as "Say cheerfully:" in the text. Do not:
  the cue is read aloud.
- About $0.003 a take. Charon reads near 2.8-3.0 words a second.
- Transcribe: `whisper-cli -m ~/.cache/whisper-cpp/ggml-small.en.bin -f vo16.wav -np`
  (convert first with `ffmpeg -i vo.wav -ar 16000 -ac 1 vo16.wav`).
- Sentence ends: `ffmpeg -i vo.wav -af silencedetect=noise=-35dB:d=0.25 -f null -`;
  a 0.25 s minimum skips most commas.

## Clips: Veo 3.1 Fast

```bash
treg call replicate.video-gen.veo-3.1-fast --method POST --file prompts/c1.json
```

```json
{"input": {"prompt": "<clip prompt>", "duration": 6, "resolution": "1080p",
  "aspect_ratio": "9:16", "generate_audio": false, "image": "<start frame URL, optional>"}}
```

- Durations 4, 6 or 8 only. The defaults are `generate_audio: true` ($0.15/s)
  and 16:9, so set both. Silent costs $0.10/s.
- Two submits within a second return HTTP 429 at no charge; wait 2 s between
  submits and retry a 429 once.
- Poll: `treg call replicate.predictions.get --query id=<prediction id>` every
  20-30 s until `succeeded` or `failed`; a clip takes 1-3 minutes. Record ids in
  `jobs.md`.
- Download `output` straight away (`curl -sL <url> -o c1.mp4`); Replicate
  deletes prediction files.
