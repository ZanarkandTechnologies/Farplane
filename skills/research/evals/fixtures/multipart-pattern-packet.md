---
captured_at: 2026-08-15
kind: synthetic-repository-evidence-fixture
topic: resumable-multipart-upload
---

# Multipart Upload Repository Evidence

This is a deterministic eval fixture, not a claim about live repositories.
Treat its URLs, paths, snippets, maintenance signals, and search results as the
captured evidence available for this exercise.

## Broad search snapshot

| Repository | Updated | Query hit | File | Disposition signal |
| --- | --- | --- | --- | --- |
| https://github.com/northstar-labs/upload-service | 2026-08-02 | `createMultipartUpload(` | `src/uploads/multipart.ts` | active service, matching lifecycle |
| https://github.com/cedar-cloud/tus-gateway | 2026-07-19 | `Upload-Offset` | `src/routes/patch-upload.ts` | active protocol implementation |
| https://github.com/cloudkit-js/storage-examples | 2026-06-30 | `completeMultipartUpload(` | `examples/resumable-upload.ts` | maintained official examples |
| https://github.com/archivebox/upload-demo | 2021-03-04 | `uploadPart(` | `server.js` | stale demo, no tests |

Broad queries captured by the source collector:

- `createMultipartUpload(` filtered to TypeScript
- `completeMultipartUpload(` filtered to TypeScript
- `Upload-Offset` filtered to TypeScript
- `abortMultipartUpload(` filtered to TypeScript

## northstar-labs/upload-service

- Repository: https://github.com/northstar-labs/upload-service
- Source: https://github.com/northstar-labs/upload-service/blob/main/src/uploads/multipart.ts
- Tests: https://github.com/northstar-labs/upload-service/blob/main/tests/uploads/multipart.test.ts
- File map:
  - `src/uploads/routes.ts`: HTTP create, status, part, complete, abort routes
  - `src/uploads/multipart.ts`: session lifecycle and object-store adapter
  - `src/uploads/store.ts`: durable session and part metadata
  - `tests/uploads/multipart.test.ts`: retry, ordering, expiry, and abort cases

```ts
export async function putPart(sessionId: string, part: number, body: Buffer) {
  const session = await sessions.requireActive(sessionId);
  const result = await objects.uploadPart(session.objectKey, part, body);
  await sessions.recordPart(sessionId, part, result.etag, body.length);
  return result;
}

export async function complete(sessionId: string) {
  const session = await sessions.requireActive(sessionId);
  const parts = await sessions.orderedParts(sessionId);
  if (!parts.length) throw new EmptyUploadError(sessionId);
  await objects.completeMultipart(session.objectKey, parts);
  await sessions.markCompleted(sessionId);
}
```

Tests cover idempotent replacement of one part, rejection after completion,
missing-part ordering, expired sessions, object-store failure without marking
completion, and explicit abort cleanup. The session record owns `ownerId`,
`objectKey`, expected size, part ETags, `expiresAt`, and terminal state.

## cedar-cloud/tus-gateway

- Repository: https://github.com/cedar-cloud/tus-gateway
- Source: https://github.com/cedar-cloud/tus-gateway/blob/main/src/routes/patch-upload.ts
- Tests: https://github.com/cedar-cloud/tus-gateway/blob/main/test/offset-conflict.test.ts
- File map:
  - `src/routes/create-upload.ts`: session creation and declared length
  - `src/routes/head-upload.ts`: authoritative offset response
  - `src/routes/patch-upload.ts`: append guarded by expected offset
  - `test/offset-conflict.test.ts`: retry and offset-conflict behavior

```ts
if (requestOffset !== upload.offset) {
  throw new OffsetConflict(upload.offset, requestOffset);
}
const nextOffset = await chunks.append(upload.id, request.body);
await uploads.compareAndSetOffset(upload.id, requestOffset, nextOffset);
```

Tests cover stale offsets, duplicated patches, concurrent writers, length
overflow, checksum failure, expired uploads, and cleanup after termination.
This design is sequential-offset based rather than independently numbered
parts.

## cloudkit-js/storage-examples

- Repository: https://github.com/cloudkit-js/storage-examples
- Source: https://github.com/cloudkit-js/storage-examples/blob/main/examples/resumable-upload.ts
- Tests: none in the captured example folder
- Shape: initiate, upload numbered parts concurrently, retain ETags, complete
  with ordered parts, abort on user cancellation.
- Limitation: example code leaves durable session ownership, expiry, and retry
  reconciliation to the caller.

## Local baseline

The exercise workspace contains `service/src/upload.ts`, a single-request
handler with authentication and size validation but no durable session,
per-part retry, completion validation, expiry, or abort cleanup.
