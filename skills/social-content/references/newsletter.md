# Newsletter Mode

Owner: `social-content` mode `newsletter` ([SKILL.md](../SKILL.md)). Load this
in N2-N5 when the deliverable is a recurring newsletter issue, a newsletter
blueprint, or a repair of a stale newsletter.

Credit: adapted from Sanket Dongre's MIT-licensed `newsletter` skill, with
Farplane provenance, hypothesis-voice, and publication gates added. License
text: [newsletter-UPSTREAM_LICENSE.txt](newsletter-UPSTREAM_LICENSE.txt).

Not for triggered email sequences or search articles; route those to
[copywriting](../../copywriting/SKILL.md). Evidence aggregators pass verified
facts, exclusions, and source references here instead of drafting themselves.

## Bind before drafting

- Who subscribes, what they expect, the verified raw material, the
  relationship or promotional goal, and any prior issues or voice examples.
- No voice evidence: set `voice_mode: hypothesis` and invent no personal story,
  feeling, or quotation.
- Topic, audience, and goal sufficient for a truthful draft: state minimal
  assumptions and draft now. Do not block on optional voice samples, sign-off
  name, links, price, or cadence.
- A missing fact that would force fabrication: ask for that one fact only. A
  conservative non-statistical lesson may be framed as an editorial
  hypothesis; empirical or autobiographical claims may not.
- Still blocked: return one candidate thesis labelled as a question or
  editorial hypothesis, the one missing source input, `voice_mode`, and
  `publication_status: approval_required`.

## Format Decision Rules

The available material chooses the format, not the writer's preference.

| Available material | Flagship format | Recurring skeleton |
| --- | --- | --- |
| Wide reading, low writing capacity | Curated | Personal note -> 5-10 links with one or two sentences of original commentary -> sign-off |
| Rich personal or client experience | Story-driven | Hook -> story -> lesson -> reader application -> sign-off |
| Expertise to teach | Educational | Why it matters -> concept or framework -> two or three real examples -> application -> sign-off |
| Access to interesting people | Interview | Who and why -> five to ten Q&As -> key takeaway -> sign-off |
| Original data or research | Data-driven | Surprising finding -> evidence -> meaning -> action -> sign-off |
| Building in public or personal brand | Personal update | Working on -> learning -> thinking about -> one recommendation -> sign-off |
| Verified shipped changes or weekly recap | Release digest | Factual opener -> 2-4 impact themes -> indented Changed / Impact / Evidence units -> optional CTA |

- Editorial formats teach one useful idea; bank the rest as next-issue seeds.
- A release digest gets no editorial arc and no personal story: rank, group,
  and cut change units into two to four reader-impact themes.

Cadence: weekly only when useful material recurs weekly; otherwise default to
biweekly; monthly for heavyweight issues. A kept cadence beats a broken one.

## Drafting rules

- Three honest subject lines of 45 characters or fewer, and one preview of 90
  characters or fewer that extends rather than repeats the subject.
- Editorial formats open with a grounded observation and address one reader
  as `you`. A release digest opens with one or two factual sentences, then
  renders each change as an indented block with `Changed`, `Impact`, and
  `Evidence`.
- Exactly one CTA for editorial formats; zero or one for a release digest.
- Value first: promotion stays out of the body unless the operator asks for a
  promotional issue; a soft mention goes in an optional P.S. P.S. claims must
  be verified.
- Editorial issues normally run 300-800 words; release digests may be shorter.
  Never pad; keep every claim attributable and phone-scannable.
- Cut throat-clearing, unsupported claims, invented anecdotes, generic
  transitions, repeated ideas, and low-impact activity.
- Never open with "Welcome to another issue" or a weekly weather report.
- Keep internal proof references out of reader copy unless already public.

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

## Source receipt
- Verified facts:
- Public links:
- Editorial interpretation:
- Unsupported material cut:

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

Full worked example: [release digest](../examples/newsletter/example.md).
