# Feed Scout Configure Intake

Minimum useful project YAML:

```yaml
feed_scout:
  entities:
    example-founder:
      name: Example Founder
      kind: person
      instructions: >-
        Track concrete product and operating-model changes. Propose valuable
        product features as planner candidates.
      owned_sources:
        x:
          url: https://x.com/example
          instructions: Prefer original announcements and demonstrations.
        podcast:
          url: https://example.fm/feed.xml
          instructions: >-
            For new episodes, nominate at most three verified first-party
            sources for high-value guests. Do not follow nominees recursively.
```

The source key carries source identity/type, so do not repeat it with `kind`.
Entity instructions are inherited and source instructions refine them. Exact
item dedupe remains canonical-URL-key based; source-level semantic redundancy
is a separate evidence-bearing judgment.

Keep the destination local unless live Notion routing is explicitly configured
and readback can verify required `Project` and `Areas` relations.
