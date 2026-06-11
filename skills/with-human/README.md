# with-human

`with-human` is the human feedback provider for Goal Packet loops.

It creates a compact feedback request and `feedback.json` contract so a Goal can
pause for Kenji's judgment, then resume from the result.

It replaces the old mental model of "human feedback owns the loop." Native
Goal mode owns continuation; `with-human` owns human feedback.
