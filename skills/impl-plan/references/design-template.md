# Copy-Complete UI Design Baseline

Use this ticket-local `design.md` shape for every UI-bearing ticket. Keep the
compact journey in `ticket.md`; use this file for every screen, visible string,
and proofable expectation the builder must not invent.

```text
# <Ticket> Design Baseline

## <State ID — name>

Reader question: <the question this state must answer>

+--------------------------------------+
| <literal heading>                    |
| <literal body copy>                  |
| [<literal CTA>]                      |
+--------------------------------------+

Visible copy:
- Heading: <literal final text>
- Body: <literal final text>
- Labels/errors/empty states/CTA: <literal final text>

Proof shown: <source, evidence caption, or explicitly labelled hypothesis>
Intended takeaway: <what the reader concludes>
Action: <literal next step>
Assertion: <observable capture or behavior condition>
```

No placeholder, lorem ipsum, or “implementer decides” field may remain in a
required state. Unsupported product truth blocks approval; do not turn it into
invented copy.
