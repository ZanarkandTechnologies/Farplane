# Run Notes

## Before

`asset_evidence_lint.py` accepted `generated-video` when the only video work was
local `ffmpeg` packaging from Seedream/generated still frames.

## After

`generated-video` now requires video-generation provenance such as `videoModel`,
`videoProvider`, `sourceVideo`, `sourceVideoPath`, `sourceVideoModel`, or a
recognized video-generation app/model. `ffmpeg` still-frame assembly must be
declared as `frame-sequence` or downgraded to prototype.

## Example

The current XR site now fails the asset evidence gate until the hero media is
regenerated through the mounted `video-generation` skill or relabeled as a
frame-sequence prototype.

## Remaining Risk

The gate verifies provenance, not subjective video quality. A future eval should
score generated video motion quality after a real video-generation provider is
used.
