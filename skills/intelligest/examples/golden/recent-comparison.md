---
title: Recent comparable takes
status: active
owner: intelligest
---

# Recent Comparable Takes

Input: a new video analyzes the announced Atlas Control 3 release. The last
14 days contain one creator testing that same release, one warehouse-robotics
market roundup, and one six-week-old Atlas history video. The operator did not
ask to save anything for reuse.

Good receipt excerpt:

```yaml
relatedCoverage:
  - sourceRef: content:atlas-control-3-field-test
    relation: same_development
    take: The field-test creator questions the launch benchmark conditions.
    evidence: Both sources explicitly discuss the Atlas Control 3 release.
news:
  - title: Atlas Control 3 announced
    reference: https://example.com/atlas/control-3-announcement
resourceBank: skipped_no_reuse_intent
```

The market roundup is rejected because robotics is only a broad topic match.
The history video is rejected because it is outside the comparison window.
The original announcement URL is the News reference; the generated summary is
not presented as a source.
