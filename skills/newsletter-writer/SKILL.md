---
name: newsletter-writer
description: "Turn verified source material and voice examples into a ready-to-review recurring newsletter issue or sustainable newsletter blueprint."
tier: 3
group: marketing
source: local
template_uses:
  skill-template: "0.4.0"
  skill-surface-budget: "0.1.0"
allowed-tools: Read, Glob, Grep, Write
---

# Newsletter Writer

## Context

Use this skill to write one recurring newsletter issue, define a sustainable
format and cadence, or repair a stale newsletter. Match the reader's expected
shape: editorial issues teach one idea; release digests group high-impact change
units for fast scanning. Value comes first; promotion stays out of the body
unless the operator explicitly requests a promotional issue.

This adapts Sanket Dongre's MIT-licensed `newsletter` skill, adding Farplane
provenance, hypothesis-voice, and publication gates. See `UPSTREAM_LICENSE.txt`.

Do not use it for triggered email sequences. Evidence aggregators should pass
verified facts, exclusions, and source references here instead of drafting.

## Skill Signature

```text
newsletter_writer(audience, raw_material, goal,
                  voice_examples?, list_expectation?, cadence?, format?)
  -> newsletter_blueprint? + newsletter_issue + send_notes + source_receipt
state:
  reads(verified source material, prior issues or voice guide, audience/list
        expectation, the first-load Todo List guardrails)
  writes(draft artifacts only when the caller supplies an owned path)
owns: reader-facing newsletter structure and prose
gates:
  one_reader_bound; format_intent_bound; source_truth_preserved;
  subject_preview_limits; cta_limit; voice_mode_named;
  human_publication_approval_required
routes: social-content | seo-content-advisor | review | direct-answer
fails:
  format_mismatch; ungrouped activity dump; invented anecdote;
  generic_ai_voice; clickbait; promotion disguised as value;
  publishing or sending without explicit approval
```

## Phase Boundary

Draft one issue inline; use `review` when public-facing voice is material. Route
finished prose to `social-content` for adaptation or `seo-content-advisor` for
search articles. This skill never publishes or sends.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the reader, promise, evidence, voice, and issue goal.
  - [ ] Read the first-load Todo List guardrails before drafting.
  - [ ] Resolve who subscribes, what they expect, the verified raw material,
        the relationship or promotional goal, and any prior issues or voice
        examples. If voice evidence is absent, set `voice_mode: hypothesis` and
        do not invent personal stories, feelings, or quotations.
  - [ ] If the topic, audience, and goal are sufficient for a truthful draft,
        state minimal assumptions and draft now. Do not block on optional voice
        samples, sign-off name, links, price, or cadence. When a missing fact
        would force fabrication, ask only for that one blocking fact. A
        conservative non-statistical lesson may be framed as an editorial
        hypothesis; empirical or autobiographical claims may not.
  - [ ] If source truth still blocks drafting, return one candidate thesis
        labeled as a question or editorial hypothesis, request exactly one
        missing source input, name `voice_mode`, and keep
        `publication_status: approval_required` visible.
- [ ] 2. Select the format and information architecture.
  - [ ] When starting from zero, choose one flagship format by the decision
        rules below and set a cadence the writer can sustain.
  - [ ] For editorial formats, select one useful idea and bank the rest. For a
        requested weekly recap, changelog, or showcase, select `release-digest`
        and group verified changes into two to four reader-impact themes.
- [ ] 3. Draft the subject/preview pair and issue.
  - [ ] Write three honest subjects of 45 characters or fewer and one preview
        of 90 characters or fewer that extends rather than repeats the subject.
  - [ ] Editorial formats open with a grounded observation and address one
        reader as `you`. A release digest opens with one or two factual
        sentences, then renders each change as an indented block with
        `Changed`, `Impact`, and `Evidence`; do not add a personal story.
  - [ ] Use exactly one CTA for editorial formats and zero or one for a release
        digest; use a sign-off only when it fits. P.S. claims must be verified.
- [ ] 4. Cut until the reader value is obvious.
  - [ ] Remove throat-clearing, unsupported claims, invented anecdotes, generic
        transitions, repeated ideas, and low-impact activity.
  - [ ] Editorial issues normally use 300–800 words; release digests may be
        shorter. Never pad, and keep every claim attributable and phone-scannable.
- [ ] 5. Return the issue, receipt, and approval gate.
  - [ ] Apply the first-load Todo List guardrails, report the selected format, voice mode, source
        gaps, CTA count, promotion placement, and next-issue seeds.
  - [ ] Keep internal proof references out of reader copy unless already
        public. Require human fact, privacy, voice, link, media, and publication
        approval before any send or publish action.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Format Decision Rules

| Available material | Flagship format | Recurring skeleton |
| --- | --- | --- |
| Wide reading, low writing capacity | Curated | Personal note -> 5–10 links with one or two sentences of original commentary -> sign-off |
| Rich personal or client experience | Story-driven | Hook -> story -> lesson -> reader application -> sign-off |
| Expertise to teach | Educational | Why it matters -> concept or framework -> two or three real examples -> application -> sign-off |
| Access to interesting people | Interview | Who and why -> five to ten Q&As -> key takeaway -> sign-off |
| Original data or research | Data-driven | Surprising finding -> evidence -> meaning -> action -> sign-off |
| Building in public or personal brand | Personal update | Working on -> learning -> thinking about -> one recommendation -> sign-off |
| Verified shipped changes or weekly recap | Release digest | Factual opener -> 2–4 impact themes -> indented Changed / Impact / Evidence units -> optional CTA |

Choose weekly only when useful material recurs weekly. Otherwise default to
biweekly; use monthly for heavyweight issues. A kept cadence beats a broken one.

## Templates

```text
# Newsletter Issue — [working title]

## Subject line options
1. "..." ([n] chars)
2. "..." ([n] chars)
3. "..." ([n] chars)
Recommended: #[n] — [why it best earns the open and matches the body]

## Preview text
"..." ([n] chars)

## Body
[opening -> chosen format -> zero or one CTA -> sign-off? -> optional P.S.]

## Send notes
- Format:
- Voice mode: evidence_matched | hypothesis
- CTA:
- Promotion: none | P.S. only | promotional issue
- Source gaps:
- Publication status: approval_required

## Next-issue seeds
- [two or three banked ideas]
```

When establishing a newsletter, precede the issue with:

```text
# Newsletter Blueprint — [name]
- Audience and promise:
- Flagship format and reason:
- Cadence and send slot:
- Section template:
- Voice evidence:
- Metrics: open-rate trend, replies, and issue-level unsubscribe spikes
```

Short positive shape:

```text
Raw material: four product changes across two projects.
Bad: a founder story that buries the shipped changes.
Good: three impact themes, each with indented Changed / Impact / Evidence units.
```

See the [weekly office showcase example](examples/weekly-office-showcase/example.md).

## Gotchas

- Never open with "Welcome to another issue" or a weekly weather report.
- Never fabricate a founder anecdote; use a sourced observation or hypothesis.
- Never force an editorial arc onto a release-digest request. Rank, group, and
  cut change units instead of narrating them.

## Reference Map

- the first-load Todo List guardrails — read before drafting and apply
  again before returning an issue.
- [Weekly office showcase example](examples/weekly-office-showcase/example.md)
  — read when turning project Executive Updates into a release digest.
- [Upstream MIT license](UPSTREAM_LICENSE.txt) — source attribution and reuse
  terms for the adapted workflow.
- [Review](../review/SKILL.md) — use for public-facing voice and readiness
  judgment.

## Output

- `newsletter_blueprint` when the recurring promise, format, or cadence is new.
- `newsletter_issue` with three subjects, preview text, format-correct body,
  zero or one CTA, optional sign-off/P.S., and approval status.
- `send_notes` with format, voice mode, source gaps, promotion placement, and
  next-issue seeds.
- `source_receipt` that distinguishes verified facts, public links, editorial
  interpretation, and unsupported material that was cut.
- `blocked_report` with one candidate editorial hypothesis, the single missing
  source input, voice mode, and unchanged human publication gate.
