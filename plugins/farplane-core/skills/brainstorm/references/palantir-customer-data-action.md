# Palantir Customer / Data / Action Lens

Use this lens when the problem is best understood as an operational workflow:

- a user or team needs to make a decision
- the decision depends on specific data or context
- the system should trigger or support a concrete action
- the action writes back into the operational system

## Core Questions

1. **Who is the actor?**
   - Which user, operator, or team is trying to act?
2. **What decision are they making?**
   - What call must they make in the moment?
3. **What data do they need?**
   - Which objects, signals, or facts are required?
4. **What action follows the decision?**
   - What workflow, intervention, or state change happens next?
5. **What writes back?**
   - What new state or evidence should the system capture after the action?

## Decomposition Output

- `Actor`
- `Decision`
- `Required data / objects`
- `Action / workflow`
- `Write-back / state update`
- `System boundary`

## Good Fit

- operational products
- internal tools
- alerting / triage / investigation loops
- systems where users need context to act and then persist the outcome

## Warning Sign

If the decomposition still reads like a list of components instead of:

`actor -> data -> decision -> action -> write-back`

then the lens is not being used correctly.
