# Progress

2026-08-08 09:10 +0800 | Customer asked: “Can we tell the Monday shift that a
reopened handover will no longer lose the incident acknowledgement?”

2026-08-08 09:35 +0800 | Symptom reproduced: reopening a shift replaced the
handover record and omitted `acknowledgement_id` from the detail response.

2026-08-08 10:05 +0800 | Attempt rejected: a support-runbook reminder to copy
the acknowledgement manually. It reduces neither the data-loss path nor the
customer’s reliability requirement.

2026-08-08 11:20 +0800 | Implementation attempt: preserve
`acknowledgement_id` during the reopen merge and return it from the detail
response. Targeted unit coverage passed.

2026-08-08 15:40 +0800 | Operated check did not complete: the staffed test
window ended before the dispatcher reopen step. No dispatch-to-handover receipt
exists. Do not confirm the customer workflow yet.
