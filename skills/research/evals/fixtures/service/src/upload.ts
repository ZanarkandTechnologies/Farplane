export async function upload(request: Request): Promise<Response> {
  const ownerId = requireAuthenticatedOwner(request);
  const body = await request.arrayBuffer();
  if (body.byteLength > 10_000_000) return new Response("too large", { status: 413 });
  const objectKey = await objectStore.put(ownerId, Buffer.from(body));
  return Response.json({ objectKey }, { status: 201 });
}
