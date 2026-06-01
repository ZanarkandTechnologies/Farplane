---
name: video-understanding
version: 0.1.0
description: Use after media ingest when transcript evidence and representative frames need to be turned into a storyboard, visible workflow reconstruction, extracted source todos, skill-to-skill comparison, copied-skill candidate, and proof requirements.
tier: 2
source: local
allowed-tools: Read, Glob, Grep, Bash
---

# Video Understanding

<!-- BEGIN CODEXTER_IMPORTANT_CHECKLIST -->
## Important Checklist

Source: `SKILL.md`

- [ ] Read the media ingest bundle, transcript status, retention note, contact
  sheet, and selected frames.
- [ ] Separate transcript-backed evidence, frame-backed evidence, source
  claims, and inferred steps.
- [ ] Build the storyboard and source-todo comparison using
  [reconstruction-brief.md](./templates/reconstruction-brief.md).
- [ ] For smoke testing without native video, replay
  [replay-log.md](./references/replay-log.md).
- [ ] Prefer augmenting an existing owner skill; use harness placement advice
  when ownership remains ambiguous.
- [ ] Write a copied-skill candidate with source anchors, likely owner,
  supporting skills, acceptance criteria, and proof requirements.
- [ ] State confidence limits clearly when transcript, frames, or external links
  are missing.
<!-- END CODEXTER_IMPORTANT_CHECKLIST -->

Turn an ingested video bundle into a grounded reconstruction of what the video
teaches or demonstrates.

This skill is for understanding source evidence. It should not implement the
copied skill itself unless the caller explicitly routes to an implementation
owner such as `frontend-craft`.

## Trigger Conditions

Use this skill when:

- [media-ingest](../media-ingest/SKILL.md) produced a transcript, selected
  frames, contact sheet, or visual-only bundle
- a video shows someone explaining a workflow, skill, prompt, UI, app, coding
  process, design process, or generated artifact
- `harness-scout` needs source todos before comparing the source against
  existing Codexter skills
- the operator wants to copy a skill from a video with frame-grounded evidence

Do not use this skill when the source is text-only or the caller only needs a
plain summary.

## Workflow

1. **Read transcript status first:** identify whether the video has transcript,
   partial transcript, or visual-only evidence.
2. **Inspect selected frames:** use the contact sheet and selected frames to
   identify source states, UI states, visible prompts, timeline labels,
   generated assets, final outputs, and proof cues.
3. **Build a storyboard:** align timestamp or frame order with visible action,
   spoken or on-screen claim, confidence, and downstream implication.
4. **Extract source todos:** write the operational checklist the creator appears
   to be teaching. Keep claims, inferred actions, and visibly proven steps
   separate.
5. **Compare to local skills:** map each source todo to existing Codexter
   skills/todos as `covered`, `augment`, `missing`, `reject`, or `defer`.
6. **Name the copied-skill candidate:** describe the reusable capability, likely
   owner skill, supporting skills, evidence anchors, and proof requirements.
7. **Route handoff:** return a reconstruction brief to the caller; use
   `harness-advisor` only when ownership is ambiguous.

## Output Contract

A complete pass produces a `VideoReconstructionBrief`:

- `source_id` and ingest bundle path
- transcript status and confidence limits
- storyboard table with frame/timestamp anchors
- source todos extracted from the video
- source-todo-to-Codexter-skill comparison
- copied-skill candidate with likely owner and supporting skills
- acceptance criteria and proof requirements for reimplementation
- gaps that require more transcript, frames, external links, or user input

## Core Decision Branches

- **Transcript plus frames agree:** treat the step as high-confidence evidence.
- **Frames show a step but transcript is missing:** mark it visual evidence and
  avoid asserting spoken details.
- **Transcript claims a step but frames do not show it:** mark it as a source
  claim and require proof before copying.
- **Todos map cleanly to an existing skill:** recommend augmenting that skill,
  not creating a wrapper.
- **Todos cross multiple owners:** produce a short owner comparison and call
  [harness-advisor](../harness-advisor/SKILL.md) when the primary surface is
  not obvious.

## Judgement Questions

Use [advise](../advise/SKILL.md) when the answer is not mechanical:

- Is the source teaching a reusable skill or just showing a one-off artifact?
- Is the right output a new skill, an existing skill method, a reference file,
  an eval, or a one-off ticket?
- Are the frames and transcript strong enough to justify reimplementation?

## Top Gotchas

1. Do not collapse “what the video shows” and “what the agent should do” into
   one unchecked prompt.
2. Do not create a new skill when existing skill todos can be augmented.
3. Do not claim an accurate reimplementation without frame or screenshot proof.

## References

- [media-ingest](../media-ingest/SKILL.md) for source metadata, transcripts,
  frames, and retention notes
- [harness-scout](../harness-scout/SKILL.md) for source registry, dedupe,
  scoring, owner handoff, and copied-skill ticketing
- `templates/reconstruction-brief.md` for a compact output shape
- `references/replay-log.md` for a text-only smoke fixture that tests the
  route without native video playback or model video understanding
