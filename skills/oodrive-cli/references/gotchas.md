# OODrive Gotchas

- CARLA may be running but unresponsive. Smoke-test `client.get_world()` before long runs.
- CARLA on Kasm pods should run as `kasm-user`, not root.
- Town/map loading can time out; use the currently loaded map for snapshot proof when deadline is tight.
- Fail2Drive evaluator can create checkpoints without RGB frames. Treat missing RGB folder as a blocker, not success.
- Generated XML validation proves structure, not drivable scenario quality.
- Stock CARLA props are proxy assets unless custom asset import/spawn is proved.
- Do not send secrets through proxy SSH heredocs.
