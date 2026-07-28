---
artifact: source-output-eval
fixture: animated-data-story
status: frozen
frozen_before_candidate_generation: true
rights: synthetic-eval-fixture
---

# Animated Data Story Frozen Eval

```yaml
frozen_before_candidate_review: true
must_match:
  - four horizontal bars share a visible zero baseline and finish on declared numeric labels
  - exactly 36 categorical records become a semicircular fixed-position dot lattice
  - lattice entrance order progresses left to right without shifting revealed dots
  - three chronological lines draw and hold direct endpoint labels together
  - line endpoints and text remain sharp while only interior points receive restrained seeded displacement
  - the terminal state visibly contains bar, lattice, and line outputs together
may_vary:
  - clean-room subject, category names, counts used by the bar scene, palette, typography, audio, copy, duration, and layout
reject:
  - source data, wording, branding, frames, voice, music, fonts, assets, exact layout, or affiliation
  - paper texture, visual polish, or render success presented as workflow proof
  - a sequential chart montage without the terminal three-output state
source_anchor_checks:
  - AD-01: 00:12–00:28 and frame 00:20 prove the zero-baseline bar state
  - AD-02: 00:42–01:04 and frame 00:58 prove 36-record lattice cardinality, topology, reveal order, and fixed positions
  - AD-03: 01:18–01:38 and frame 01:32 prove chronological line draw, direct labels, sharp endpoints, and interior-only variation
  - AD-04: 01:52–02:03 and frame 01:59 prove the terminal bar+lattice+line composition
```

Pass only when every source-anchor check has an observable candidate result and
rights/render integrity are reported separately from reconstruction fidelity.
