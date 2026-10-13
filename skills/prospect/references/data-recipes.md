---
title: Prospect Data Recipes
owner: prospect
status: active
kind: skill-reference
---

# Prospect Data Recipes

Load in N2 when a candidate pool, a contact or a signal needs a paid data
call. Each recipe is adapted from a published treg or Monid workflow; the
gateway named per step is the one that won that job on price and reliability
(see the tool loadout note in `~/.farplane/memory/`). Re-read live prices with
treg `catalog_get` or `monid inspect` before a run; listed prices drift.

## Rules For Every Recipe

- Set a dollar cap for the run before the first call and stop at it.
- Count before you pull: use a free or cheap `*.count` call, then fetch a
  10-row sample before a full list.
- Quote first (`catalog_get` / `monid inspect`), then call.
- Finding and verifying an email are separate steps; only `deliverable`
  addresses enter a case. Keep `catch_all` and `unknown` in their own column.
- Prefer routed endpoints (`treg.<capability>`) that try the cheapest provider
  first and bill misses at zero, unless a step needs one provider's fields.
- Nothing is sent, called, connected or followed. Recipes end at a shortlist
  or a draft; outreach is `approach`.
- End with an actual-spend line and log it in the operator's spend log.

## 1. ICP To Filters And A Free Market Count

Use before any list pull, when the market size is unknown.

1. Turn the ICP into provider filter objects (industry, headcount, country,
   funding stage, technologies).
2. Count on two or more providers (`companies.search.count`,
   `people.search.count`); flag counts more than 3x apart.
3. Pull 10 sample rows per provider and check them against the ICP by hand.

Out: market count, filter object, sample verdict. Cost: free to about $0.01.

## 2. Verified Lead List

Use for `industry` intake: "find me leads at X kind of company".

1. Company list from the filters (`apollo.companies.search`, about $0.026 a
   page of 50).
2. Judge fit per company against the signal ladder; keep rows that pass.
3. Find the person by role (VP or Head of the buying function).
4. Find the work email (`treg.people.email.find`, routed).
5. Verify it (`treg.people.email.verify`).
6. Pull the 3 latest dated news events per company for a `why now` line.

Out: company, person, role, fit reason, email status, news line. Published
receipt: $2.33 for 50 companies, about $0.12 per deliverable lead.

## 3. Local Leads With An Observable Gap

Use when the offer fixes something visible on a local business's site (no
online booking, no reviews reply, slow site).

1. Search map listings for the service and city
   (Apify `damilo/google-maps-scraper` via Monid, or the maps winner).
2. Open each website and check for the named gap.
3. Rank by gap severity and public contact availability.

Out: 10 businesses with the gap, public contact, source and spend. Cap: $2.

## 4. Lookalikes Of Best Customers

Use when 3-5 closed or ideal accounts exist.

1. Seed the accounts into `companies.similar` (or a lookalike finder).
2. Enrich once (`treg.companies.enrich`).
3. Apply the same ICP check as recipe 1; most will fail.

Published receipt: 71 found, 8 passed, $0.20.

## 5. Buying Committee, Then Waterfall Find And Verify

Use for `company` intake when more than one person decides.

1. Map the committee functions (buyer, user, budget, blocker).
2. Search people by function per account (`treg.people.search`).
3. Reveal only the chosen people; find email cheapest-first; verify as its
   own step; keep only deliverable addresses.

## 6. Dated Signals, Then Fit x Timing Tiers

Use to answer `why now`, or for a recurring signal watch.

1. Pull only dated, linkable signals: open roles
   (`treg.companies.jobs.search`), funding (`financing.discover`), job
   changes (`people.job-change`), LinkedIn engagers on topic posts
   (`linkedin.post.search` then reactions and comments), and Reddit or X
   complaints about a competitor.
2. Write one `why now` line per company from the signal.
3. Score fit and timing separately; tier A (both high), B, C.
4. Re-score weekly; report only people new since the last run.

Published receipt: 4,710 signals for $0.52. A recurring watch is set up
through `automation-advisor`, not run by hand.

## 7. One-Page Company Brief Before A Meeting

Use for `call` or `company` intake.

1. Resolve the company (domain first).
2. Enrich firmographics; pull funding and deals.
3. Pull 6 months of news; check each claim at its source.
4. Write: summary, dated developments, 3 partnership angles, 5 questions.

## 8. Creator Screening (Partnership Or Influencer)

Use when the relationship class is `channel` or `partner_or_jv` and the
targets are creators.

1. Discover creators by bio keyword, follower range, engagement floor and
   country (`influencersclub.creators.search` or `exa.creators.search`).
2. Pull each profile and the last 12 posts; compute engagement and views per
   follower; flag outliers (a post at 10x+ the creator's median).
3. Verify an exposed business email before it enters the case.

Published receipts: 20 creators screened for $0.036; 25 discovered for $0.20.

Source workflows: treg `/workflows`, `/gtm-engineering` ch.1-10, `/leads-signals`,
`/jev`; Monid docs examples (local leads, verified contacts, company brief) and
blog (influencer marketing). Mapped in the 2026-10-12 treg and Monid workflow
notes under `~/.farplane/memory/projects/farplane/`.
