# User System Patterns

## When to Use
Use these patterns when implementing user authentication, profiles, and encrypted secrets storage. Based on production code from Zanarkand.

## Official Docs
- [Authentication](https://docs.convex.dev/auth) - Convex auth setup

## System Structure

```
convex/user_system/
├── schema.ts           # Validators, tables, type exports
├── auth_helpers.ts     # Reusable auth utilities
├── secrets.ts          # Internal mutations/queries for secrets
└── secrets_node.ts     # Node.js actions for encryption (uses "use node")
```

## Auth Helpers Pattern

Create reusable auth helper functions that can be imported across your backend:

```typescript
// convex/user_system/auth_helpers.ts
import { QueryCtx, MutationCtx, ActionCtx } from "../_generated/server";

/**
 * Get the current user's ID from authentication
 */
export async function getAuthUserId(
  ctx: QueryCtx | MutationCtx | ActionCtx
): Promise<string | null> {
  const identity = await ctx.auth.getUserIdentity();
  return identity?.subject ?? null;
}

/**
 * Get the current user's profile from the database
 */
export async function getAuthUser(ctx: QueryCtx | MutationCtx) {
  const userId = await getAuthUserId(ctx);
  if (!userId) return null;

  return await ctx.db
    .query("userProfiles")
    .withIndex("by_userId", (q) => q.eq("userId", userId))
    .first();
}

/**
 * Require authentication - throws if not authenticated
 */
export async function requireAuth(
  ctx: QueryCtx | MutationCtx | ActionCtx
): Promise<string> {
  const userId = await getAuthUserId(ctx);
  if (!userId) {
    throw new Error("Authentication required");
  }
  return userId;
}

/**
 * Check if user has admin role
 */
export async function isAdmin(ctx: QueryCtx | MutationCtx): Promise<boolean> {
  const user = await getAuthUser(ctx);
  return user?.type === "admin";
}

/**
 * Require admin role - throws if not admin
 */
export async function requireAdmin(ctx: QueryCtx | MutationCtx): Promise<void> {
  await requireAuth(ctx);
  if (!(await isAdmin(ctx))) {
    throw new Error("Admin role required");
  }
}
```

## User Profile Schema

```typescript
// convex/user_system/schema.ts
import { defineTable } from "convex/server";
import { v, Infer } from "convex/values";

export const userTypeSchema = v.union(
  v.literal("regular"),
  v.literal("pro"),
  v.literal("admin"),
);

export const userProfileSchema = v.object({
  userId: v.string(),           // Auth provider ID (e.g., Clerk subject)
  name: v.optional(v.string()),
  email: v.string(),
  type: userTypeSchema,
  onboardingCompleted: v.optional(v.boolean()),
});

export const userProfiles = defineTable(userProfileSchema)
  .index("by_userId", ["userId"]);

export const userSystemTables = {
  userProfiles,
};

export type UserType = Infer<typeof userTypeSchema>;
export type UserProfile = Infer<typeof userProfileSchema>;
```

## Get or Create User Pattern

For handling first-time logins:

```typescript
export async function getOrCreateUserProfile(
  ctx: MutationCtx,
  tokenIdentifier: string,
  email: string,
  name?: string
): Promise<Id<"userProfiles">> {
  // Check if user already exists
  const existingUser = await ctx.db
    .query("userProfiles")
    .withIndex("by_userId", (q) => q.eq("userId", tokenIdentifier))
    .first();

  if (existingUser) {
    return existingUser._id;
  }

  // Create new user with default role
  return await ctx.db.insert("userProfiles", {
    userId: tokenIdentifier,
    email,
    name,
    type: "regular",
  });
}
```

## Encrypted Secrets Pattern

For storing API keys, tokens, and other sensitive data:

### Schema
```typescript
export const secretTypeSchema = v.union(
  v.literal("github_pat"),
  v.literal("openai_api_key"),
  v.literal("anthropic_api_key"),
  v.literal("custom"),
);

export const userSecretsSchema = v.object({
  userId: v.string(),
  secretType: secretTypeSchema,
  label: v.optional(v.string()),      // User-friendly name
  encryptedValue: v.string(),         // AES-256-GCM encrypted
  createdAt: v.number(),
  updatedAt: v.number(),
});

export const userSecrets = defineTable(userSecretsSchema)
  .index("by_userId", ["userId"])
  .index("by_userId_and_type", ["userId", "secretType"]);
```

### Split Architecture
Secrets require splitting between Node.js (encryption) and V8 (mutations):

```typescript
// secrets.ts - Internal mutations (V8 runtime)
export const createSecretInternal = internalMutation({
  args: createSecretArgsSchema,
  returns: v.id("userSecrets"),
  handler: async (ctx, args) => {
    const now = Date.now();
    return await ctx.db.insert("userSecrets", {
      ...args,
      createdAt: now,
      updatedAt: now,
    });
  },
});

// secrets_node.ts - Actions with encryption (Node.js runtime)
"use node";
import { action } from "../_generated/server";
import { internal } from "../_generated/api";
import * as crypto from "crypto";

export const saveSecret = action({
  args: { secretType: secretTypeSchema, value: v.string() },
  handler: async (ctx, args) => {
    const userId = await requireAuth(ctx);
    const encrypted = encrypt(args.value); // Your encryption logic
    
    await ctx.runMutation(internal.user_system.secrets.createSecretInternal, {
      userId,
      secretType: args.secretType,
      encryptedValue: encrypted,
    });
  },
});
```

## Usage in Other Files

```typescript
// convex/some_system/some_file.ts
import { getAuthUserId, requireAuth } from "../user_system/auth_helpers";

export const myMutation = mutation({
  args: { data: v.string() },
  handler: async (ctx, args) => {
    const userId = await requireAuth(ctx); // Throws if not authenticated
    // ... rest of logic
  },
});
```

## Key Patterns Summary

| Pattern | Purpose |
|---------|---------|
| `getAuthUserId()` | Get current user ID (nullable) |
| `getAuthUser()` | Get full user profile (nullable) |
| `requireAuth()` | Get user ID or throw |
| `requireAdmin()` | Ensure admin role or throw |
| `getOrCreateUserProfile()` | Handle first-time login |
| Split secrets architecture | Encryption in Node.js, storage in V8 |

