# Evidence switch

- **Event:** `UserPromptSubmit` (five-second timeout).
- **Entrypoint:** `evidence.py --hook`; the same file is the `evidence` command.
- **Purpose:** tell every turn how much proof to gather. Awake: Kenji is at the
  Mac and tests by hand, so threads prove with the smallest check and record no
  video. Asleep: nobody is watching, so threads prove everything themselves.
  On 28 Oct 2026 threads waited 6.4 h on screenshots and recordings (4.5 h in
  hand-written recording scripts in 27 threads) while Kenji was testing by hand.

## Control

```sh
evidence              # show the mode and why
evidence asleep       # set by hand: maximum proof; holds until `evidence auto`
evidence awake        # set by hand: minimal proof
evidence auto         # follow the lid and the clock (the default)
evidence --mode       # print only awake or asleep, for scripts
```

Auto is asleep while the lid is closed, or from 01:00 to 09:00 Amsterdam time
when no operator message came in the last 30 minutes; otherwise awake. A hand
setting always wins. State lives in `~/.farplane/evidence/` (`mode`,
`last-prompt`). Any thread can flip it when Kenji asks ("evidence max").

## Who reads it

- This hook prints one `Evidence: <mode> (<why>). ...` line into each turn, so
  a flip applies on the next turn without restarting threads.
- The Stop gate's response-format check
  ([`response_format.py`](../shared/response_format.py)) asks for a video for
  a new visible feature only when asleep; awake, any cited proof is enough.
  When the switch cannot be read the gate stays strict (asleep).
- A repo's own done-check can call `evidence --mode` (Oures runs its full
  checks asleep and the quick ones awake).
- The policy text is in [`runtimes/AGENTS.md`](../../runtimes/AGENTS.md).

## Checks

```sh
python3 -m unittest bin/tests/test_evidence_mode.py bin/tests/test_stop_gate.py
```
