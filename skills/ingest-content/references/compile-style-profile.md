---
template_uses:
  skill-method-reference: "0.1.0"
---

# Compile Style Profile

Use this reference when `ingest-content:compile-style-profile` turns an
existing saved capture into a reusable, creator-neutral visual-direction
profile.

```text
compile_style_profile(saved_capture, profile_id, destination, replace=false)
  -> collocated_profile_package + evidence | blocked_report
state: reads(saved ingest-content capture and rights metadata); writes(profile.md, prompts.md, example.md)
gates: capture_exists; profile_id_safe; collision_clear; provenance_preserved; rights_safe; package_complete
fails: re-ingests source media; overwrites silently; copies protected media; imitates a named creator; stores examples elsewhere
```

## Use When

- The operator wants a saved reference converted from task inspiration into a
  reusable visual grammar for future video plans.

## Inputs

```text
input_packet:
  required: saved_capture, profile_id
  optional: destination, compatible_methods, replace_authority
  source_refs: retrieval_handle, source URL/ref, operator note, creative elements
```

## Workflow

1. **Validate the capture.** Resolve the `ingest-content` retrieval handle and
   use its analysis and creative elements; do not fetch, transcribe, or store
   the source again. Separate observed evidence, operator taste, and inference.
2. **Protect identity and rights.** Convert creator-specific descriptions into
   creator-neutral visual, narrative, motion, typography, and audio grammar.
   Preserve attribution in provenance. Copy only small text/example assets
   whose reuse is explicitly rights-safe; otherwise store a source reference.
3. **Compile atomically.** Normalize `profile_id` to lowercase kebab case and
   target `references/style-profiles/<profile_id>/`. If it already exists,
   return a collision blocker unless explicit replace authority is recorded.
   Before replacement, preserve a reviewable diff and do not delete unrelated
   assets.
4. **Verify the package.** Require `profile.md`, `prompts.md`, and a collocated
   `example.md`; verify compatible methods, prompt variables, negative
   constraints, provenance, and concrete QA assertions before indexing it.

## Output Shape

```text
method_output:
  result: profile directory + index candidate
  evidence: capture handle + source ref + observation/inference map + rights decision + completeness checks
  blockers: missing capture | invalid id | collision | insufficient evidence | rights ambiguity | incomplete package
```

## Quality Gates

- Every reusable claim traces to saved evidence or is labeled inference.
- The package is creator-neutral, collocated, compatible with named methods,
  and safe to load without the original media.

## Bad Output

- A prompt-only profile, a directory named after a creator, an unreviewed
  overwrite, copied source footage, or a second Resource Bank capture.
