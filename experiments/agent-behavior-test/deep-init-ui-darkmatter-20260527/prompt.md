You are a fresh Codex behavior-test child agent. Your task is to test whether the
Codexter `deep-init-project` skill now makes UI-bearing project bootstrap carry
the shadcn/tweakcn darkmatter baseline.

Working directory: `/tmp/codexter-init-ui-probe`

Behavior under test:
- Target skill: `/Users/kenjipcx/coding-harness/Codexter/skills/deep-init-project/SKILL.md`
- Persona: agent using the init project skill on a new small frontend app.
- App to make: a tiny calculator UI.

Required actions:
1. Read the `deep-init-project` skill and the smallest needed references for generated project templates.
2. Run or manually follow the deep-init bootstrap into `/tmp/codexter-init-ui-probe`.
3. Create a minimal UI-bearing project artifact for a calculator. Keep it tiny.
   You may use plain HTML/CSS/JS if that is fastest, but you must still treat it
   as a frontend app for bootstrap documentation purposes.
4. Fill or update the generated bootstrap/project docs so they visibly answer:
   - whether UI applies,
   - component system,
   - shadcn/tweakcn status,
   - whether the darkmatter command was applied or skipped,
   - the exact skip reason if not applied,
   - tooltip-over-explainer rule,
   - initial visual QA evidence path.
5. Check whether the actual calculator UI has evidence of the darkmatter theme
   being applied. For this probe, acceptable evidence is either:
   - the command `pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/darkmatter.json`
     was run successfully and theme tokens landed in CSS, or
   - the project is non-shadcn/plain HTML and docs clearly record that darkmatter
     was skipped because there is no shadcn setup yet.
6. Produce visible artifacts in `/tmp/codexter-init-ui-probe`, including the app
   files and any docs you updated.

Forbidden shortcuts:
- Do not claim darkmatter was applied unless command output or files prove it.
- Do not skip reading the skill before bootstrapping.
- Do not return prose-only. Final output must be strict JSON.

Final response must be only this JSON object shape:
{
  "target": "deep-init-project-ui-darkmatter",
  "persona": "fresh skill caller",
  "checkpoints": [
    {
      "name": "loaded_required_context",
      "status": "done | skipped | blocked",
      "evidence": "path or command"
    },
    {
      "name": "bootstrapped_project",
      "status": "done | skipped | blocked",
      "evidence": "path or command"
    },
    {
      "name": "created_calculator_ui",
      "status": "done | skipped | blocked",
      "evidence": "path"
    },
    {
      "name": "recorded_ui_baseline",
      "status": "done | skipped | blocked",
      "evidence": "path and key line"
    },
    {
      "name": "theme_evidence_checked",
      "status": "done | skipped | blocked",
      "evidence": "command or file evidence"
    }
  ],
  "artifacts": ["absolute paths"],
  "deviations": [
    {
      "expected": "what should have happened",
      "observed": "what happened instead",
      "owner": "skill | prompt | instrumentation | environment | unknown"
    }
  ],
  "themeApplied": true,
  "themeSkippedWithReason": true,
  "themeSkipReason": "string or empty",
  "verdict": "pass | fail | blocked"
}
