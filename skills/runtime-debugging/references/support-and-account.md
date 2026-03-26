# Support And Account

Use when the issue comes from a support ticket, customer report, or account-specific context.

## Strategy

1. Translate the symptom into likely system boundaries: auth, permissions, sync, caching, exports, billing, feature flags.
2. Gather the identifying context: email, account ID, org ID, plan, environment, timestamps.
3. Find the relevant flow and enumerate likely failure points before editing code.
4. Check for stale tokens, stale caches, delayed sync, permissions mismatches, or account-data edge cases.
5. If logs exist, reconstruct the account-specific timeline.

## Useful Checks

- token claims vs database truth
- plan or role casing mismatches
- org membership propagation
- feature flag targeting
- export filters and date ranges
- account-specific data gaps

## Output

- symptom translated into candidate causes
- account-specific checks performed
- likely root cause
- short-term workaround and code fix if needed
