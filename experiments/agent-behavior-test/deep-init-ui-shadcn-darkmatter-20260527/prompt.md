You are a fresh Codex behavior-test child agent. Test whether the updated
Codexter `deep-init-project` skill now defaults UI-bearing app bootstrap to
shadcn plus tweakcn darkmatter instead of accepting plain HTML.

Working directory: `/tmp/codexter-init-shadcn-probe`

Behavior under test:
- Target skill: `/Users/kenjipcx/coding-harness/Codexter/skills/deep-init-project/SKILL.md`
- Persona: agent using the init project skill on a new small frontend app.
- App to make: a tiny calculator UI.

Required actions:
1. Read the target `deep-init-project` skill and the smallest generated-template
   references needed for the UI baseline.
2. Bootstrap the project docs into `/tmp/codexter-init-shadcn-probe`.
3. Create a real UI-bearing app foundation with Next/Tailwind/shadcn. Plain
   HTML/CSS/JS is forbidden for this test unless a command failure blocks you;
   if blocked, report `blocked`, not `pass`.
4. Apply the default theme command:
   `pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/darkmatter.json`
5. Build a tiny calculator UI using the app stack.
6. Fill or update generated docs so they visibly answer:
   - UI applies: yes
   - component system: shadcn/ui
   - shadcn/tweakcn status
   - darkmatter command result
   - tooltip-over-explainer rule
   - initial visual QA evidence path
7. Prove whether the actual spawned UI has darkmatter evidence. Acceptable
   evidence must include command output or CSS/token files showing darkmatter
   landed. Merely saying it should be themed is not enough.

Suggested noninteractive commands if useful:
```bash
pnpm create next-app@latest . --ts --tailwind --eslint --app --src-dir --use-pnpm --yes
pnpm dlx shadcn@latest init -y
pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/darkmatter.json -y
```

Forbidden shortcuts:
- Do not use plain HTML/CSS/JS for the calculator and call it a pass.
- Do not claim darkmatter was applied unless command output or files prove it.
- Do not skip reading the skill before bootstrapping.
- Do not return prose-only. Final output must be strict JSON.

Final response must be only this JSON object shape:
{
  "target": "deep-init-project-ui-shadcn-darkmatter",
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
      "name": "created_shadcn_app",
      "status": "done | skipped | blocked",
      "evidence": "path or command"
    },
    {
      "name": "applied_darkmatter",
      "status": "done | skipped | blocked",
      "evidence": "command and file evidence"
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
  "themeEvidence": "string",
  "usedPlainHtml": false,
  "verdict": "pass | fail | blocked"
}
