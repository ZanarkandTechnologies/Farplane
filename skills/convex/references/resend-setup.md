# Resend Email Setup

> **When to use**: Adding transactional email (newsletters, notifications, receipts) to your Convex app using React Email templates.

## Official Docs
- [Resend Component](https://www.convex.dev/components/resend)
- [React Email](https://react.email)
- [Resend Dashboard](https://resend.com)

---

## Quick Setup

### 1. Install

```bash
npm install @convex-dev/resend @react-email/components
```

### 2. Add to `convex.config.ts`

```typescript
import { defineApp } from "convex/server";
import resend from "@convex-dev/resend/convex.config";

const app = defineApp();
app.use(resend);
export default app;
```

### 3. Environment Variables

In Convex dashboard or `.env.local`:

```bash
# From Resend dashboard → API Keys
RESEND_API_KEY=re_...
```

---

## Minimal Setup File

Create `convex/emails.tsx` (note the `.tsx` extension for JSX):

```typescript
/**
 * EMAIL DELIVERY SYSTEM (Convex Node Action)
 * Uses React Email for templates and Resend for delivery.
 */

// IMPORTANT: This must be a Node action for React Email rendering
"use node";

import { internalAction } from "./_generated/server";
import { render } from "@react-email/render";
import {
  Html,
  Body,
  Head,
  Heading,
  Hr,
  Container,
  Preview,
  Section,
  Text,
  Link,
  Markdown,
  Tailwind,
} from "@react-email/components";
import { components, internal } from "./_generated/api";
import { Resend } from "@convex-dev/resend";
import { v } from "convex/values";

export const resend: Resend = new Resend(components.resend, {
  // Set to false for production, true for development testing
  testMode: false,
  // Optional: handle email events (delivered, bounced, etc.)
  onEmailEvent: internal.emails.handleEmailEvent,
});

// Send a newsletter email
export const sendNewsletterEmail = internalAction({
  args: {
    userId: v.string(),
    email: v.string(),
    title: v.string(),
    content: v.string(),
  },
  handler: async (ctx, args) => {
    const { email, title, content } = args;

    const html = await render(
      <NewsletterEmail title={title} content={content} />,
    );

    await resend.sendEmail(ctx, {
      from: "Your App <hello@yourdomain.com>", // Must be verified domain
      to: email,
      subject: title,
      html,
    });
  },
});

// Optional: Handle email events
export const handleEmailEvent = internalAction({
  args: { event: v.any() },
  handler: async (ctx, { event }) => {
    console.log("Email event:", event.type, event);
    // Handle: delivered, bounced, complained, etc.
  },
});

// =====================
// EMAIL TEMPLATES
// =====================

function NewsletterEmail({
  title,
  content,
}: {
  title: string;
  content: string;
}) {
  return (
    <Html>
      <Head />
      <Preview>{title}</Preview>
      <Tailwind>
        <Body className="bg-white font-sans">
          <Container className="mx-auto py-8 px-4 max-w-2xl">
            <Section>
              <Heading className="text-2xl font-bold text-gray-900 mb-4">
                {title}
              </Heading>
              <Hr className="border-gray-200 my-4" />
              <Markdown
                markdownCustomStyles={{
                  h1: { fontSize: "24px", fontWeight: "bold", margin: "24px 0 12px" },
                  h2: { fontSize: "20px", fontWeight: "bold", margin: "20px 0 10px" },
                  h3: { fontSize: "18px", fontWeight: "bold", margin: "18px 0 8px" },
                  p: { margin: "16px 0", lineHeight: "1.6", color: "#374151" },
                  li: { margin: "10px 0", lineHeight: "1.6", color: "#374151" },
                  link: { color: "#2563eb", textDecoration: "underline" },
                }}
              >
                {content}
              </Markdown>
              <Hr className="border-gray-200 my-8" />
              <Text className="text-xs text-gray-400 text-center">
                © {new Date().getFullYear()} Your Company. All rights reserved.
              </Text>
            </Section>
          </Container>
        </Body>
      </Tailwind>
    </Html>
  );
}
```

---

## Calling from Other Functions

```typescript
// From a mutation or action
import { internal } from "./_generated/api";

// In a mutation
await ctx.scheduler.runAfter(0, internal.emails.sendNewsletterEmail, {
  userId: user._id,
  email: user.email,
  title: "Welcome to Our App!",
  content: "# Hello!\n\nThanks for signing up.",
});

// From an action
await ctx.runAction(internal.emails.sendNewsletterEmail, {
  userId: user._id,
  email: user.email,
  title: "Your Report is Ready",
  content: reportMarkdown,
});
```

---

## Common Email Templates

### Simple Notification

```typescript
function NotificationEmail({ message }: { message: string }) {
  return (
    <Html>
      <Head />
      <Preview>{message}</Preview>
      <Body className="bg-gray-100 font-sans">
        <Container className="mx-auto py-8 px-4 max-w-xl">
          <Section className="bg-white rounded-lg p-6 shadow">
            <Text className="text-gray-700">{message}</Text>
          </Section>
        </Container>
      </Body>
    </Html>
  );
}
```

### Welcome Email with CTA

```typescript
function WelcomeEmail({ name, ctaUrl }: { name: string; ctaUrl: string }) {
  return (
    <Html>
      <Head />
      <Preview>Welcome to Our App, {name}!</Preview>
      <Tailwind>
        <Body className="bg-white font-sans">
          <Container className="mx-auto py-8 px-4 max-w-xl">
            <Heading className="text-2xl font-bold">Welcome, {name}!</Heading>
            <Text>We're excited to have you on board.</Text>
            <Section className="text-center my-8">
              <Link
                href={ctaUrl}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg"
              >
                Get Started
              </Link>
            </Section>
          </Container>
        </Body>
      </Tailwind>
    </Html>
  );
}
```

---

## Webhook Setup (Optional)

For tracking email delivery status:

1. Go to Resend Dashboard → Webhooks
2. Add webhook URL: `https://your-deployment.convex.site/resend/webhook`
3. Select events: `email.delivered`, `email.bounced`, `email.complained`

---

## Gotchas

1. **`"use node"`**: Required at top of file for React Email rendering
2. **File extension**: Use `.tsx` for JSX templates
3. **Verified domain**: Must verify domain in Resend for production
4. **Test mode**: Set `testMode: true` during development
5. **Internal action**: Use `internalAction` to prevent direct API calls

---

## Checklist

- [ ] Install `@convex-dev/resend` and `@react-email/components`
- [ ] Add to `convex.config.ts`
- [ ] Create `convex/emails.tsx` with `"use node"` directive
- [ ] Add `RESEND_API_KEY` environment variable
- [ ] Verify sending domain in Resend dashboard
- [ ] Test with `testMode: true` first
- [ ] Set up webhooks for delivery tracking (optional)

