# Eval Viewer React

Shadcn + Vite viewer for local eval run artifacts.

## Run

```bash
pnpm install
pnpm dev --host 127.0.0.1
```

Open the printed local URL and use `Load latest`.

## What It Reads

- `../runs/index.json`
- `../runs/<job_id>/summary.json`
- `../runs/<job_id>/tasks/<task_id>.json`

The Vite config allows reads from the parent eval folder so the app can load
the local run artifacts during development.

## Quality

```bash
pnpm lint
pnpm build
```
