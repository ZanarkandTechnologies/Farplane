---
kind: synthetic-research-evidence
captured_at: 2026-09-15
---

# Robotic Grasping Evidence Packet

Local boundary: one Franka arm, two RTX 4090 GPUs, 14 days, 120 real-object
trials, success rate plus collision rate, and an open geometric baseline.

- Approach A reports +12 points on Dataset X over a weak image-only baseline.
  Authors release code and weights but not the training split. Their lab demo and
  X thread share one provenance. An independent replication reports +3 points
  after matching the geometric baseline and identifies sensitivity to camera pose.
- Approach B reports +7 points on Dataset X over the geometric baseline, releases
  code, data splits, ablations, and a 24 GB training recipe. Two independent labs
  reproduce +5 and +6 points. Failures concentrate on transparent objects.
- Vendor C shows a strong hardware demo and founder paper, but provides no data,
  protocol, or independent replication. Its SDK requires proprietary grippers
  and sends telemetry to a hosted API.

Research trail: A's missing split triggers author-repo and replication searches;
the replication revises the expected gain and opens a camera-pose branch. B's
transparent-object ablation creates a local guard metric. Vendor C's missing
artifacts close the performance-ranking branch and backtrack to dependency and
reproducibility checks.
