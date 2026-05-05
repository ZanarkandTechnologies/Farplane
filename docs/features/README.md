# Feature Registry

Codexter's feature registry is the structured system of record for harness
techniques.

Use it when a source, video, blog, repo, or ticket proposes a feature and the
agent needs to answer:

- does Codexter already have this?
- where does it live?
- what source or ticket introduced it?
- what evidence proves it works?
- what limits or metrics should future work consider?

`docs/specs/harness-techniques.md` remains the skimmable human inventory.
`docs/features/registry.jsonl` is the queryable feature record for technique
dedupe, provenance, and benchmark history. `docs/sources/registry.jsonl` is the
source provenance registry; use `SRC-*` there to dedupe blogs, specs, videos,
docs, and repos before deciding whether they introduce or update `FEAT-*`
records.

## Record Shape

Each line in `registry.jsonl` is one JSON object:

```json
{
  "id": "FEAT-0001",
  "name": "Metric-driven autoresearch sessions",
  "status": "implemented",
  "category": "improvement-loop",
  "surfaces": ["skills/autoresearch-plan", "skills/autoresearch-exec"],
  "source_refs": ["docs/specs/autoresearch-skill-suite.md"],
  "external_refs": [],
  "evidence_refs": ["tickets/archive/TASK-0100/ticket.md"],
  "known_limits": "Skill-and-script based, not a hosted benchmark lab.",
  "metrics": [],
  "last_verified": "2026-05-04"
}
```

## Field Contract

- `id`: stable `FEAT-####` identifier; never reuse an ID for a different
  technique.
- `name`: short, unique technique name.
- `status`: `implemented`, `partial`, `proposed`, `deferred`, or `retired`.
- `category`: broad grouping such as `planning`, `proof`, `memory`,
  `source-ingestion`, or `improvement-loop`.
- `surfaces`: repo paths that own the live behavior.
- `source_refs`: `SRC-*` records, local docs, tickets, memories, or specs that
  explain why the feature exists.
- `external_refs`: outside URLs, repos, videos, or standards that influenced the
  feature.
- `evidence_refs`: tickets, artifacts, commands, or experiment outputs that
  support the current status.
- `known_limits`: one concise caveat agents should preserve when comparing
  source ideas.
- `metrics`: metric names or scorecards associated with the feature. Leave empty
  when the feature is not benchmarked yet.
- `last_verified`: date when the record was last checked against live surfaces.

## Update Rules

1. Add or update the registry when a shipped or planned harness technique needs
   dedupe, provenance, or benchmark tracking.
2. Keep raw transcripts, bulky summaries, and one-off logs in `experiments/`,
   not in the registry.
3. Link to ticket evidence instead of copying proof into the record.
4. Keep `harness-techniques.md` synchronized at the category/status level, but
   do not duplicate every registry field there.
5. When a source proposes a feature, use `harness-scout` to search
   `docs/sources/registry.jsonl` first for source dedupe, then this registry
   for feature dedupe before creating a new ticket.

## ID Allocation

1. Read all existing `id` values before adding a record.
2. Pick the next unused numeric ID in `FEAT-####` form.
3. Do not fill gaps without checking archived branches or tickets that may
   already reference the missing ID.
4. Do not rename or reuse an ID after another doc, ticket, scorecard, or source
   run references it.

## Verification Rules

- Refresh `last_verified` when the record's status, surfaces, evidence, known
  limits, or metrics are checked against live repo files.
- Do not refresh `last_verified` for pure wording edits that do not inspect the
  live surfaces.
- If a feature moves from `proposed` to `implemented`, link the ticket or
  artifact that proves the change in `evidence_refs`.
- If a feature is retired, set `status` to `retired`, keep the record, and add
  the removal evidence instead of deleting the row.
- Prefer specific ticket or artifact paths over broad refs such as
  `docs/HISTORY.md` when proof exists.

## Validation

Run this before claiming registry edits are safe:

```bash
python3 - <<'PY'
import json
import re
from pathlib import Path

root = Path(".")
registry = Path("docs/features/registry.jsonl")
required = {
    "id",
    "name",
    "status",
    "category",
    "surfaces",
    "source_refs",
    "external_refs",
    "evidence_refs",
    "known_limits",
    "metrics",
    "last_verified",
}
allowed_statuses = {"implemented", "partial", "proposed", "deferred", "retired"}
id_re = re.compile(r"^FEAT-\d{4}$")
date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ids = set()
errors = []

def is_url(value):
    return value.startswith(("http://", "https://"))

def local_path(value):
    return value.split("#", 1)[0]

def require_string_list(record, field, line_no):
    value = record.get(field)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"line {line_no}: {field} must be a list of strings")
        return []
    return value

for line_no, line in enumerate(registry.read_text().splitlines(), 1):
    if not line.strip():
        continue
    try:
        record = json.loads(line)
    except json.JSONDecodeError as exc:
        errors.append(f"line {line_no}: invalid JSON: {exc}")
        continue
    missing = required - record.keys()
    extra = record.keys() - required
    if missing:
        errors.append(f"line {line_no}: missing fields: {sorted(missing)}")
    if extra:
        errors.append(f"line {line_no}: unknown fields: {sorted(extra)}")
    feature_id = record.get("id")
    if not isinstance(feature_id, str) or not id_re.match(feature_id):
        errors.append(f"line {line_no}: id must match FEAT-####")
        feature_id = f"line-{line_no}"
    if feature_id in ids:
        errors.append(f"line {line_no}: duplicate id {feature_id}")
    ids.add(feature_id)
    if record.get("status") not in allowed_statuses:
        errors.append(f"{feature_id}: invalid status {record.get('status')!r}")
    for field in ("name", "category", "known_limits", "last_verified"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            errors.append(f"{feature_id}: {field} must be a non-empty string")
    if isinstance(record.get("last_verified"), str) and not date_re.match(record["last_verified"]):
        errors.append(f"{feature_id}: last_verified must use YYYY-MM-DD")
    for field in ("surfaces", "source_refs", "external_refs", "evidence_refs", "metrics"):
        require_string_list(record, field, line_no)
    if record.get("status") == "implemented" and not record.get("surfaces"):
        errors.append(f"{feature_id}: implemented records need at least one surface")
    if record.get("status") == "implemented" and not record.get("evidence_refs"):
        errors.append(f"{feature_id}: implemented records need evidence refs")
    for field in ("surfaces", "source_refs", "evidence_refs"):
        for ref in record.get(field, []):
            if is_url(ref):
                continue
            path = local_path(ref)
            if path and not (root / path).exists():
                errors.append(f"{feature_id}: {field} local ref does not exist: {ref}")
if errors:
    raise SystemExit("\n".join(errors))
print(f"feature registry contract OK ({len(ids)} records)")
PY
```
