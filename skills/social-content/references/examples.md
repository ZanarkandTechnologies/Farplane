# Social Content Examples

Use this file when the output quality depends on voice, taste, explanation, or
visual structure. These examples are not fixed templates; they show the quality
bar and the reasoning pattern to adapt.

## Example: Harness Engineering Infographic Carousel

Input brief:

```text
Create a bite-sized LinkedIn carousel about a Farplane harness-engineering
concept. Audience: builders of agent workflows. Goal: make the concept feel
clear, useful, and postable without sounding like internal docs.
```

Output shape:

```text
Platform: LinkedIn
Format: 7-slide carousel, 1080 x 1350
Message job: explain one compact harness concept
Asset carrier: typographic infographic with small system-map motifs
Publish boundary: draft only; human approval required before posting
```

Slide sequence:

1. `Your agent does not need more memory. It needs a contract.`
   Subtitle: `The Farplane Goal Packet pattern in 60 seconds.`
2. `The failure mode`
   `Long tasks drift because the agent keeps optimizing the last message, not
   the original job.`
3. `The fix`
   `Put the job in files: ticket.md for the promise, program.md for the loop,
   progress.md for what actually happened.`
4. `Why it works`
   `The agent can resume from state, reviewers can inspect proof, and humans do
   not have to reconstruct intent from chat.`
5. `The tiny equation`
   `GoalPacket = ticket + program + progress + generated prompt + drift check`
6. `The rule of thumb`
   `If the work is ambitious, resuming, feedback-driven, or easy to
   self-approve, give it a Goal Packet.`
7. `Takeaway`
   `Do not make agents remember promises. Make the promise inspectable.`
   CTA: `Save this if you build long-running agent workflows.`

Why this works:

- It leads with a contrarian but accurate hook.
- It explains one concept, not the whole harness.
- Each slide has one job and stays under the text density limit.
- The equation gives builders a memorable handle.
- The CTA asks for saving, not premature publishing or sales behavior.

Visual direction:

```text
Base: warm off-white background, charcoal type, one electric accent.
Motif: three file cards connected by a thin progress line.
Avoid: purple-blue gradient SaaS sludge, giant abstract orbs, dense docs
screenshots, and decorative code blocks.
```
