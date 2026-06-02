# Transcription Notes

Use the smallest reliable transcription path available for the source.

## Preferred Order

1. `summarize <source> --extract-only` when the source or platform already
   exposes usable transcript text.
2. Local Whisper when the operator has configured a local CLI/model.
3. Provider API transcription only when the operator has intentionally exposed a
   key in the shell environment for this task.

## Local Whisper

Record the command and model in the ingest bundle. For a beefy laptop, prefer a
large local model when accuracy matters more than speed; use a smaller model
only for quick triage.

## Failure Handling

If the transcript cannot be produced, continue only when frames provide enough
evidence for the downstream task. Mark the bundle `visual-only` or `partial`
and lower confidence on any spoken claims.
