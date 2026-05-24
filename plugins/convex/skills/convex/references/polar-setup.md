# Polar Payments Setup

> **When to use**: Adding subscription billing to your Convex app. Polar is much simpler than Stripe for SaaS subscriptions.

## Official Docs
- [Polar Component](https://www.convex.dev/components/polar)
- [Polar Dashboard](https://polar.sh)

---

## Quick Setup

### 1. Install

```bash
npm install @convex-dev/polar
```

### 2. Add to `convex.config.ts`

```typescript
import { defineApp } from "convex/server";
import polar from "@convex-dev/polar/convex.config";

const app = defineApp();
app.use(polar);
export default app;
```

### 3. Environment Variables

In Convex dashboard or `.env.local`:

```bash
# From Polar dashboard → Settings → Developers → Access Tokens
POLAR_ACCESS_TOKEN=polar_at_...

# From Polar dashboard → Settings → Developers → Webhooks
POLAR_WEBHOOK_SECRET=whsec_...

# Your product IDs from Polar dashboard
POLAR_SIGNAL_MONTHLY_ID=prod_...
POLAR_SIGNAL_YEARLY_ID=prod_...
```

---

## Minimal Setup File

Create `convex/polar.ts`:

```typescript
import { Polar } from "@convex-dev/polar";
import { api, components } from "./_generated/api";
import { action, query } from "./_generated/server";
import { getAuthUser } from "./auth_helpers";
import type { Doc } from "./_generated/dataModel";

export const polar = new Polar(components.polar, {
  // Required: provide user info for subscription lookup
  getUserInfo: async (ctx): Promise<{ userId: string; email: string }> => {
    const user: Doc<"userProfiles"> | null = await ctx.runQuery(
      api.polar.getCurrentUserRecord,
    );
    if (!user) {
      throw new Error("User not authenticated");
    }
    return {
      userId: user._id,
      email: user.email,
    };
  },
  // Configure static keys for your products
  products: {
    proMonthly: process.env.POLAR_PRO_MONTHLY_ID || "replace_me",
    proYearly: process.env.POLAR_PRO_YEARLY_ID || "replace_me",
  },
  webhookSecret: process.env.POLAR_WEBHOOK_SECRET,
});

// Internal query for getUserInfo
export const getCurrentUserRecord = query({
  args: {},
  handler: async (ctx) => {
    return await getAuthUser(ctx);
  },
});

// Export API functions from the Polar client
const polarApi = polar.api();
export const {
  changeCurrentSubscription,
  cancelCurrentSubscription,
  getConfiguredProducts,
  listAllProducts,
  generateCheckoutLink,
  generateCustomerPortalUrl,
} = polarApi;

// Action to sync products from Polar
export const syncProducts = action({
  args: {},
  handler: async (ctx) => {
    await polar.syncProducts(ctx);
  },
});

/**
 * Get current user with subscription details.
 * Main source of truth for frontend.
 */
export const getCurrentUser = query({
  handler: async (ctx) => {
    const user = await getAuthUser(ctx);
    if (!user) return null;

    const subscription = await polar.getCurrentSubscription(ctx, {
      userId: user._id,
    });

    const productKey = subscription?.productKey;
    const isPro = productKey === "proMonthly" || productKey === "proYearly";

    return {
      ...user,
      subscription,
      isFree: !isPro,
      isPro,
      isAnnual: productKey === "proYearly",
    };
  },
});
```

---

## Frontend Usage

### Check Subscription Status

```typescript
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function PricingPage() {
  const user = useQuery(api.polar.getCurrentUser);
  
  if (user?.isPro) {
    return <div>You're on the Pro plan!</div>;
  }
  
  return <UpgradeButton />;
}
```

### Generate Checkout Link

```typescript
import { useAction } from "convex/react";
import { api } from "../convex/_generated/api";

function UpgradeButton() {
  const generateCheckout = useAction(api.polar.generateCheckoutLink);
  
  const handleUpgrade = async () => {
    const url = await generateCheckout({ productKey: "proMonthly" });
    window.location.href = url;
  };
  
  return <button onClick={handleUpgrade}>Upgrade to Pro</button>;
}
```

### Customer Portal (Manage Subscription)

```typescript
const generatePortal = useAction(api.polar.generateCustomerPortalUrl);

const handleManage = async () => {
  const url = await generatePortal({});
  window.location.href = url;
};
```

---

## Webhook Setup

1. Go to Polar Dashboard → Settings → Developers → Webhooks
2. Add webhook URL: `https://your-deployment.convex.site/polar/webhook`
3. Copy the webhook secret to `POLAR_WEBHOOK_SECRET`
4. Select events: `subscription.created`, `subscription.updated`, `subscription.canceled`

---

## Beta Mode Pattern

For early access / beta periods:

```typescript
const BETA_MODE = true; // Set to false when ready to charge

const isPro =
  BETA_MODE ||
  productKey === "proMonthly" ||
  productKey === "proYearly";
```

---

## Gotchas

1. **Run `syncProducts`**: After adding/changing products in Polar dashboard
2. **User must exist**: `getUserInfo` throws if user not authenticated
3. **Webhook required**: Subscription status won't update without webhook
4. **Test mode**: Polar has a sandbox mode for testing

---

## Checklist

- [ ] Install `@convex-dev/polar`
- [ ] Add to `convex.config.ts`
- [ ] Create `convex/polar.ts` with setup
- [ ] Add environment variables
- [ ] Set up webhook in Polar dashboard
- [ ] Run `syncProducts` action
- [ ] Test checkout flow

