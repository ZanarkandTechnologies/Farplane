---
title: Implementation Discovery
owner: implementation-research
status: active
kind: workflow-reference
---

# Implementation Discovery

Translate the feature question into literal source expressions: imports,
exported symbols, API calls, filenames, configuration keys, annotations, event
names, and exact error strings. Record every query, language/repository filter,
freshness bar, and empty result.

Build a candidate pool from maintained repositories, official examples, and
the caller's repository family before choosing finalists. Use official docs,
specifications, changelogs, and release notes to verify public contracts. Use
issues and discussions to find limitations and failed approaches. Use X posts
and YouTube demos as trails to authors, repos, talks, benchmarks, and newer
implementations; verify their claims against inspectable code or docs.

On X, open relevant threads and replies, distinguish author claims from
independent use, and follow linked repositories, issues, or demos. On YouTube,
inspect the video or transcript sections, chapters, description, and relevant
comments that address the implementation question. Record whether each
modality was actually inspected, partially available, or inaccessible; titles,
snippets, and metadata do not prove video or thread content.

For each finalist, inspect the tree or architecture before reading an isolated
file. Record the entrypoint, key file map, surrounding types/configuration,
data and state flow, lifecycle, tests, fixtures, error handling, retry,
cancellation, validation, migration, and operational constraints. Keep quoted
code minimal and preserve direct repository and file URLs.

Drive follow-up searches from the hypothesis tree. An unexplained lifecycle
edge creates a code/test query; a version caveat creates a changelog query; an
author demo creates a repository and publication trail; conflicting patterns
create a focused comparison. Stop branches once they cannot change the local
decision or the evidence budget is exhausted. Mark each branch open,
corroborated, contradicted, or exhausted; after contradiction or a dead end,
return to the highest-value unresolved sibling rather than repeating the query.
