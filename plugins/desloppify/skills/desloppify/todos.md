# Desloppify Todo Template

- [ ] Decide the mode first: main-agent coordinator or delegated worker.
- [ ] Read [SKILL.md](./SKILL.md) and confirm whether the task is cleanup work
      or review-only work.
- [ ] If you are the main agent, inspect obvious exclude candidates and spawn
      one worker using the phrase `use the desloppify skill in worker mode`.
- [ ] If you are the worker, verify Python 3.11+ and run
      `pip install --upgrade "desloppify[full]"`.
- [ ] Run `desloppify update-skill codex`.
- [ ] Ensure `.desloppify/` is ignored and exclude only obvious
      generated/vendor/runtime paths.
- [ ] Stop and ask before excluding any path that might contain hand-edited
      source, docs, tests, or config.
- [ ] Run `desloppify scan --path <target>`.
- [ ] Run `desloppify next`, fix the current issue, then run the exact resolve
      command that `next` prints.
- [ ] If the worker hits nested `desloppify review --run-batches --runner
      codex`, stop and return that blocker to the main agent instead of
      recursing.
- [ ] Repeat `desloppify next` until the queue is empty or a real blocker
      appears.
- [ ] Rescan after meaningful batches and write the latest score, exclusions,
      and blocker state back to the visible task artifact.
