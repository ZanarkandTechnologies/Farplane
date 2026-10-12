---
title: Final Pass
owner: copywriting
status: active
kind: skill-reference
---

# Final Pass

The last step before any prose leaves a writing skill. It rewrites supplied
text so it reads clear, specific, and human while keeping its meaning, facts,
certainty, tone, and precise technical terms. This file is executable on its
own: a skill that links here (copywriting, social-content, storyboard,
landing-page, ads) runs these five steps on its finished prose and needs
nothing else from the copywriting skill.

It edits writing, not code. Use `code-health` when the question is whether
code, a dependency, an abstraction, or a feature needs to exist.

```text
final_pass(text, audience?, purpose?, tone?) -> revised_text
reads: the supplied prose and any explicit writing constraints
does: rewrites the prose plainly without changing its supported meaning
writes: the requested file when editing, otherwise nothing
returns: revised text in the source format
```

## Procedure

1. **Bind the text, audience, purpose, and intended tone.** Infer ordinary
   context; ask only when a missing choice would materially change the result.
   Run this after the content is final: facts, offer, and structure are
   settled before the pass, not during it.
2. **Find the real tells.** Puffery, filler, vague attribution, abstract
   jargon, repetition, formulaic framing, generic claims, and sentences that
   make the reader backtrack. If a vague sentence has no concrete supported
   meaning, delete it rather than paraphrase the vagueness, and begin with the
   first supported fact rather than an invented outcome summary.
   Example: do not turn "a robust transition across an evolving landscape"
   into "the data moved cleanly"; the second phrase invents a successful
   outcome. Delete it and lead with the row count.
3. **Rewrite with plain, specific words.** Name the actor and the mechanism
   when the source supports them, vary sentence rhythm naturally, and keep the
   original level of confidence. Copy numbers and quantifiers exactly; never
   infer that a reported count is the total.
4. **Match the genre.** Human voice may keep an existing opinion or some
   natural unevenness; technical docs, status notes, and contracts stay
   precise rather than chatty. Ad, social, and page copy keep their length
   limits and CTA.
5. **Self-audit.** Ask "What still sounds generated?" and "What meaning did I
   change?" Fix the first, restore the second, then return the revised text.

## Rules

- Never add or drop a quantifier such as `all`, `only`, `always`, `never`,
  `every`, or `most`; it changes the claim's scope or certainty. "42 tests
  passed" must not become "all 42 tests passed", and "all 42 tests passed"
  must not lose "all".
- Delete a vague sentence instead of paraphrasing it. A paraphrase of nothing
  is still nothing, and it usually invents a claim.
- Do not work from a banned-word or punctuation list. A precise term, an em
  dash, a heading, or a list may be the clearest choice; judge each line by
  what it says, not by the words it uses.
- Do not replace one tell with another: forced slang, fake vulnerability,
  excess first person, sentence fragments, or theatrical opinions.
- Do not add opinions, conclusions, sources, examples, or next steps the
  source does not support.
- Do not shorten away safety notes, evidence, qualifications, instructions, or
  useful technical detail.
- Do not rewrite code, frontmatter values, commands, URLs, citations, or quoted
  source text unless asked. Keep Markdown structure, links, identifiers, and
  canonical names exactly, even when the surrounding prose is awkward.
- If the text is already clear and natural, make little or no change.

## Worked example

Before:

> We leveraged the migration orchestration surface to facilitate a robust
> transition across the evolving data landscape. The `users` backfill
> processed 18,420 rows, 42 tests passed, replication lag peaked at 1.8
> seconds, and the NOT NULL constraint remains disabled because 17 rows have
> no value.

After:

> The `users` backfill processed 18,420 rows. 42 tests passed and replication
> lag peaked at 1.8 seconds. The NOT NULL constraint is still disabled because
> 17 rows have no value.

The first sentence had no supported meaning, so it was deleted rather than
reworded. Every number stays, "42 tests" did not become "all tests", and no
judgment of the lag or next step was added.

## Output

Return the revised text in the source format, without a change log by
default. When editing a file, make the scoped edit and report only material
meaning or structure changes. A calling skill returns the passed text inside
its own packet.

Adapted from the `unslop` skill in Cursor's pstack plugin
(<https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md>).
