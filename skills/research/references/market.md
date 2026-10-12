---
title: Market Research
owner: research
status: active
kind: workflow-reference
---

# Market Research

Load for the `market` branch in N2-N3.

## Query families

Search each relevant surface with a family of explicit queries. Start broad,
then revise the ledger as claims, communities, authors, and failure modes emerge.

| Surface | Discovery queries | Deep-read behaviour |
| --- | --- | --- |
| Review sites and marketplaces | `<product> reviews`, `<product> alternative`, `<product> pricing`, `<product> <failure>` | Read recent positive, negative, and middling reviews; group by source lineage, version, segment, and use case. |
| Reddit | `site:reddit.com <product>`, `<product> vs`, `<product> switched`, `<product> problem` | Open several threads, read substantive comment branches, search them for price, setup, support, failure, migration, and named alternatives. |
| X | product, exact feature names, complaint terms, author handles, demo links | Read threads and replies, follow linked demos or repos, separate first-hand use from reposts and promotion. |
| YouTube | `<product> review`, `<product> tutorial`, `<product> vs`, `<product> problems` | Inspect transcripts, chapters, descriptions, and useful comments; record upload date and product version. |
| Official sources | product + feature, docs, changelog, pricing, status, migration | Verify claimed capability and current availability on the vendor's maintained surface. |

Capability claims lead to official verification; pain themes lead to review and
community searches; switching claims lead to alternative and migration
searches. Stop a branch when it is corroborated, falsified, or cannot affect the
decision, and report unsearched branches.

## Qualification ledger

Open and operate each candidate's official site before promotion. Keep one row
per candidate and field with `pass`, `fail`, or `unknown`, the source URL, and
the observation date:

- target geography served and actual market availability;
- current product availability and production status;
- relevant offering breadth and depth (more than an incidental SKU);
- operating recency and website freshness;
- social activity and engagement;
- estimated traffic or a defensible demand proxy;
- customer or review evidence;
- organizational credibility;
- same-customer-job fit.

Classify each candidate with exactly one primary class: `direct competitor`,
`adjacent competitor`, `supplier`, `inactive/noise`, or `unverified`, with
confidence. Record secondary relationships separately.

## Threat threshold

A competitive-threat claim needs all four mandatory gates (same customer job,
target geography served, currently obtainable and meaningfully in production,
more than an incidental relevant SKU) plus a current official observation and
at least two independent demand, customer, operating, or organizational
evidence lineages. Missing or conflicting mandatory evidence means `unverified`
or rejection, never assumed passage.

The qualification ledger is required even when every candidate is rejected;
the rejection ledger names the failed or unknown gates for each candidate that
was not promoted.
