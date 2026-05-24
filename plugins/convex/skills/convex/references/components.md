# Convex Components

## When to Use
Use this reference when adding third-party integrations or reusable backend modules. Components are Convex's ecosystem of plug-and-play functionality.

## Official Docs
- [Components Overview](https://docs.convex.dev/components)
- [Components Marketplace](https://www.convex.dev/components)

---

## Finding Components

1. **Browse**: https://www.convex.dev/components
2. **Search**: `documentation-searcher` with "convex component [name]"
3. **GitHub**: Most components are open source, check implementation

---

## Component Bundles (Common Combinations)

### AI Apps Bundle
For LLM-powered applications:

| Component | Purpose | Link |
|-----------|---------|------|
| **@convex-dev/agent** | AI agent framework | [Docs](https://docs.convex.dev/agents) |
| **@convex-dev/rag** | Retrieval augmented generation | [Component](https://www.convex.dev/components/rag) |
| **@convex-dev/ratelimiter** | Protect against abuse | [Component](https://www.convex.dev/components/rate-limiter) |
| **@convex-dev/workflow** | Long-running orchestration | [Component](https://www.convex.dev/components/workflow) |

```bash
npm install @convex-dev/agent @convex-dev/rag @convex-dev/ratelimiter @convex-dev/workflow
```

### Enterprise Auth Bundle
For B2B/enterprise applications:

| Component | Purpose | Link |
|-----------|---------|------|
| **@workos-inc/authkit-convex** | Enterprise SSO, SCIM | [Component](https://www.convex.dev/components/authkit) |

> **Default Auth**: Use Clerk for standard apps (`@clerk/convex`)

### Expo/Mobile Bundle
For React Native apps:

| Component | Purpose | Link |
|-----------|---------|------|
| **@convex-dev/expo-push-notifications** | Push notifications | [Component](https://www.convex.dev/components/push-notifications) |

---

## Commonly Used Components

### Authentication

| Component | When to Use |
|-----------|-------------|
| **Clerk** (default) | Standard apps, quick setup |
| **WorkOS AuthKit** | Enterprise SSO, SCIM provisioning |
| **Auth0** | Complex auth requirements |

### Payments & Subscriptions

| Component | When to Use | Link |
|-----------|-------------|------|
| **Polar** ⭐ | MRR, subscriptions, easy setup | [Component](https://www.convex.dev/components/polar) |
| **Stripe** | Complex billing, marketplaces | [Component](https://www.convex.dev/components/stripe) |

> **Preference**: Use Polar for SaaS/subscriptions - much easier than Stripe.

### Storage

| Component | When to Use | Link |
|-----------|-------------|------|
| **Convex File Storage** | Default, small files | [Docs](https://docs.convex.dev/file-storage) |
| **Cloudflare R2** | Large files, persistent | [Component](https://www.convex.dev/components/cloudflare-r2) |
| **S3** | AWS ecosystem | [Component](https://www.convex.dev/components/s3) |

### Email

| Component | When to Use | Link |
|-----------|-------------|------|
| **Resend** | Transactional email | [Component](https://www.convex.dev/components/resend) |

### Scheduling

| Component | When to Use | Link |
|-----------|-------------|------|
| **Built-in scheduler** | Simple cron jobs | [Docs](https://docs.convex.dev/scheduling) |
| **Crons Component** | Dynamic cron configs | [Component](https://www.convex.dev/components/crons) |

### Geospatial

| Component | When to Use | Link |
|-----------|-------------|------|
| **Geospatial** | Location-based apps | [Component](https://www.convex.dev/components/geospatial) |

### AI & Search

| Component | When to Use | Link |
|-----------|-------------|------|
| **Agent** | AI chat, tools | [Docs](https://docs.convex.dev/agents) |
| **RAG** | Document Q&A | [Component](https://www.convex.dev/components/rag) |
| **Vector Search** | Similarity search | [Docs](https://docs.convex.dev/search/vector-search) |
| **Full Text Search** | Keyword search | [Docs](https://docs.convex.dev/search/text-search) |

---

## Installation Pattern

```typescript
// 1. Install
npm install @convex-dev/[component-name]

// 2. Add to convex.config.ts
import { defineApp } from "convex/server";
import agent from "@convex-dev/agent/convex.config";
import workflow from "@convex-dev/workflow/convex.config";

const app = defineApp();
app.use(agent);
app.use(workflow);
export default app;

// 3. Use in code
import { components } from "./_generated/api";
// Component-specific usage...
```

---

## My Default Stack

For new AI apps:
```
Auth:       Clerk (default) or WorkOS (enterprise)
AI:         @convex-dev/agent + @convex-dev/workflow
Search:     Built-in vector search
Rate Limit: @convex-dev/ratelimiter
Payments:   Polar (not Stripe)
Email:      Resend
Storage:    R2 (for large files)
```

---

## Component Checklist

When adding a component:
- [ ] Check compatibility with Convex version
- [ ] Read the component's README/docs
- [ ] Add to `convex.config.ts`
- [ ] Check if it needs environment variables
- [ ] Test in development before production

