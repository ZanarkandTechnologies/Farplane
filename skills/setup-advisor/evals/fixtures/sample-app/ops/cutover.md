# Sanitized Production Cutover

## Current state

- DNS provider: Cloudflare.
- `api.toys.example` CNAME points to `old-host.example` with TTL 300.
- Stripe production webhook points to `https://old-host.example/webhooks/stripe`.
- The old host must remain available for rollback.

## Target state

- New host: `new-host.example`.
- Health endpoint: `https://new-host.example/healthz` must return HTTP 200.
- Available read-only health probe:
  `curl -fsS -o /dev/null -w '%{http_code}\n' https://new-host.example/healthz`.
- New webhook endpoint: `https://new-host.example/webhooks/stripe`.
- Application logs must show a successful signed test webhook before traffic
  change and successful production delivery after the approved change.

## Safety boundary

- Safe preparation, snapshots, TTL reduction, new-host probes, and a Stripe
  test event may be prepared before approval when authorization exists.
- Changing the production DNS record or production webhook endpoint requires a
  narrow operator approval immediately before each mutation.
- Roll back when health fails twice, signed webhook delivery fails, or the new
  host error rate exceeds the old-host baseline.
- Store redacted preparation and verification evidence under
  `.farplane/setup/cutovers/api-toys-example/`.
