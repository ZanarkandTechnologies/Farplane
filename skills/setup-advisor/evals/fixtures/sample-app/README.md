# AGI Toy Shop App

This is a Farplane-managed Next.js project. Runtime secrets are injected from
Doppler project `agi-toy-shop`, config `dev`. GitHub Actions owns CI secrets.
Do not commit `.env` files.

Repository: `agi-toy-shop/storefront`.

Requested integrations:

- Stripe for checkout and webhooks
- Vercel for deployment
- Supabase for database and authentication

Current tool state is recorded in `ops/setup-state.md`. Provider account login,
MFA, secret revelation, billing acceptance, deploys, DNS changes, and production
cutovers require an operator gate. Other safe setup steps may be performed by
the agent when tools and authorization are available.
