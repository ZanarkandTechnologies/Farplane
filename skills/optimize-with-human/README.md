# optimize-with-human

`optimize-with-human` is the Goal Advisor preset for optimization loops that use
Kenji's feedback as the metric.

It binds the target, objective, Telegram-first feedback policy, and
`feedback.json` contract, then routes loop architecture and native `/goal`
prompt compilation through `goal-advisor`.

Goal mode owns continuation. `goal-advisor` owns the Goal Packet.
`optimize-with-human` owns the human feedback protocol.
