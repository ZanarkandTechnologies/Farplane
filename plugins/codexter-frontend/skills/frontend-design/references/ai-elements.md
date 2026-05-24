# AI Elements: Building AI App Interfaces

> **When to use**: Building chatbots, v0-style code generators, or workflow visualization UIs.

## Overview

[AI Elements](https://ai-sdk.dev/elements) are pre-built React components for AI applications, designed to work with the Vercel AI SDK.

**Three main patterns**:
1. **Chatbot** - Conversational AI with reasoning and sources
2. **v0 Clone** - Code generation with live preview
3. **Workflow** - Process/pipeline visualization

---

## Installation

### 1. Install AI Elements

```bash
npx ai-elements@latest
```

This installs the base components to `components/ai-elements/`.

### 2. Install AI SDK Dependencies

```bash
npm i ai @ai-sdk/react zod
```

### 3. Configure API Key

Create `.env.local`:
```env
# For AI Gateway (recommended)
AI_GATEWAY_API_KEY=your_key_here

# Or direct provider keys
OPENAI_API_KEY=your_key_here
```

Get your AI Gateway key: [vercel.com/account/ai-gateway](https://vercel.com/account/ai-gateway)

---

## Pattern 1: Chatbot

**Example**: [ai-sdk.dev/elements/examples/chatbot](https://ai-sdk.dev/elements/examples/chatbot)

### Components Used

| Component | Purpose |
|-----------|---------|
| `Conversation` | Container with scroll management |
| `Message` | Message bubble with role styling |
| `PromptInput` | Rich input with attachments, model picker |
| `Reasoning` | Expandable thinking display |
| `Sources` | Citation links |
| `Loader` | Thinking indicator |

### Client Setup (app/page.tsx)

```tsx
'use client';

import {
  Conversation,
  ConversationContent,
  ConversationScrollButton,
} from '@/components/ai-elements/conversation';
import {
  Message,
  MessageContent,
  MessageResponse,
  MessageActions,
  MessageAction,
} from '@/components/ai-elements/message';
import {
  PromptInput,
  PromptInputTextarea,
  PromptInputSubmit,
  PromptInputSelect,
  PromptInputSelectContent,
  PromptInputSelectItem,
  PromptInputSelectTrigger,
  PromptInputSelectValue,
  PromptInputFooter,
  PromptInputTools,
  PromptInputButton,
  type PromptInputMessage,
} from '@/components/ai-elements/prompt-input';
import { Reasoning, ReasoningContent, ReasoningTrigger } from '@/components/ai-elements/reasoning';
import { Sources, Source, SourcesContent, SourcesTrigger } from '@/components/ai-elements/sources';
import { Loader } from '@/components/ai-elements/loader';
import { useChat } from '@ai-sdk/react';
import { useState } from 'react';
import { CopyIcon, RefreshCcwIcon, GlobeIcon } from 'lucide-react';

const models = [
  { name: 'GPT 4o', value: 'openai/gpt-4o' },
  { name: 'Deepseek R1', value: 'deepseek/deepseek-r1' },
];

export default function ChatPage() {
  const [input, setInput] = useState('');
  const [model, setModel] = useState(models[0].value);
  const [webSearch, setWebSearch] = useState(false);
  const { messages, sendMessage, status, regenerate } = useChat();

  const handleSubmit = (message: PromptInputMessage) => {
    if (!message.text && !message.files?.length) return;
    
    sendMessage(
      { text: message.text || 'Sent with attachments', files: message.files },
      { body: { model, webSearch } }
    );
    setInput('');
  };

  return (
    <div className="max-w-4xl mx-auto p-6 h-screen flex flex-col">
      <Conversation className="flex-1">
        <ConversationContent>
          {messages.map((message) => (
            <div key={message.id}>
              {/* Sources */}
              {message.role === 'assistant' && 
                message.parts.filter(p => p.type === 'source-url').length > 0 && (
                <Sources>
                  <SourcesTrigger count={message.parts.filter(p => p.type === 'source-url').length} />
                  {message.parts.filter(p => p.type === 'source-url').map((part, i) => (
                    <SourcesContent key={i}>
                      <Source href={part.url} title={part.url} />
                    </SourcesContent>
                  ))}
                </Sources>
              )}
              
              {/* Message Parts */}
              {message.parts.map((part, i) => {
                if (part.type === 'text') {
                  return (
                    <Message key={i} from={message.role}>
                      <MessageContent>
                        <MessageResponse>{part.text}</MessageResponse>
                      </MessageContent>
                      {message.role === 'assistant' && (
                        <MessageActions>
                          <MessageAction onClick={regenerate} label="Retry">
                            <RefreshCcwIcon className="size-3" />
                          </MessageAction>
                          <MessageAction 
                            onClick={() => navigator.clipboard.writeText(part.text)} 
                            label="Copy"
                          >
                            <CopyIcon className="size-3" />
                          </MessageAction>
                        </MessageActions>
                      )}
                    </Message>
                  );
                }
                if (part.type === 'reasoning') {
                  return (
                    <Reasoning key={i} isStreaming={status === 'streaming'}>
                      <ReasoningTrigger />
                      <ReasoningContent>{part.text}</ReasoningContent>
                    </Reasoning>
                  );
                }
                return null;
              })}
            </div>
          ))}
          {status === 'submitted' && <Loader />}
        </ConversationContent>
        <ConversationScrollButton />
      </Conversation>

      <PromptInput onSubmit={handleSubmit} className="mt-4" globalDrop multiple>
        <PromptInputTextarea value={input} onChange={(e) => setInput(e.target.value)} />
        <PromptInputFooter>
          <PromptInputTools>
            <PromptInputButton 
              variant={webSearch ? 'default' : 'ghost'} 
              onClick={() => setWebSearch(!webSearch)}
            >
              <GlobeIcon size={16} />
              <span>Search</span>
            </PromptInputButton>
            <PromptInputSelect value={model} onValueChange={setModel}>
              <PromptInputSelectTrigger>
                <PromptInputSelectValue />
              </PromptInputSelectTrigger>
              <PromptInputSelectContent>
                {models.map((m) => (
                  <PromptInputSelectItem key={m.value} value={m.value}>
                    {m.name}
                  </PromptInputSelectItem>
                ))}
              </PromptInputSelectContent>
            </PromptInputSelect>
          </PromptInputTools>
          <PromptInputSubmit disabled={!input} status={status} />
        </PromptInputFooter>
      </PromptInput>
    </div>
  );
}
```

### Server Setup (app/api/chat/route.ts)

```typescript
import { streamText, UIMessage, convertToModelMessages } from 'ai';

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages, model, webSearch }: { 
    messages: UIMessage[]; 
    model: string; 
    webSearch: boolean;
  } = await req.json();

  const result = streamText({
    model: webSearch ? 'perplexity/sonar' : model,
    messages: convertToModelMessages(messages),
    system: 'You are a helpful assistant.',
  });

  return result.toUIMessageStreamResponse({
    sendSources: true,
    sendReasoning: true,
  });
}
```

---

## Pattern 2: v0 Clone (Code Generator)

**Example**: [ai-sdk.dev/elements/examples/v0](https://ai-sdk.dev/elements/examples/v0)

### Components Used

| Component | Purpose |
|-----------|---------|
| `WebPreview` | Iframe container for live preview |
| `WebPreviewNavigation` | URL bar |
| `WebPreviewBody` | Iframe content |
| `Conversation` | Chat history |
| `Suggestion` | Quick action chips |

### Key Pattern: Split View

```tsx
<div className="flex h-screen">
  {/* Left: Chat */}
  <div className="w-1/2 flex flex-col">
    <Conversation>...</Conversation>
    <PromptInput>...</PromptInput>
  </div>
  
  {/* Right: Preview */}
  <div className="w-1/2">
    <WebPreview>
      <WebPreviewNavigation>
        <WebPreviewUrl value={previewUrl} readOnly />
      </WebPreviewNavigation>
      <WebPreviewBody src={previewUrl} />
    </WebPreview>
  </div>
</div>
```

### Server: v0 SDK Integration

```bash
npm i v0-sdk
```

```typescript
// app/api/chat/route.ts
import { v0 } from 'v0-sdk';

export async function POST(request: Request) {
  const { message, chatId } = await request.json();

  let chat;
  if (chatId) {
    chat = await v0.chats.sendMessage({ chatId, message });
  } else {
    chat = await v0.chats.create({ message });
  }

  return Response.json({ id: chat.id, demo: chat.demo });
}
```

---

## Pattern 3: Workflow Visualization

**Example**: [ai-sdk.dev/elements/examples/workflow](https://ai-sdk.dev/elements/examples/workflow)

For complex workflow visualization, consider using the **react-flow skill** instead.

### Basic Workflow Components

| Component | Purpose |
|-----------|---------|
| `Task` | Step/progress indicator |
| `Loader` | Processing state |

---

## Customization Tips

### Theming AI Elements

AI Elements use shadcn styling. Customize via:

1. **CSS Variables**: Edit `globals.css`
2. **Component Source**: Modify files in `components/ai-elements/`
3. **Tailwind**: Override classes directly

### Common Customizations

```tsx
// Custom message styling
<Message from="assistant" className="bg-muted/50">

// Custom prompt input
<PromptInput className="border-primary">

// Adjust conversation height
<Conversation className="h-[calc(100vh-200px)]">
```

---

## Gotchas

1. **Streaming requires edge runtime**: Use `export const runtime = 'edge'` in route handlers for best performance
2. **File attachments**: Use `globalDrop multiple` props on `PromptInput`
3. **Model switching**: Pass `model` in the `body` option of `sendMessage`
4. **Reasoning display**: Only works with models that support reasoning (e.g., Deepseek R1)
5. **Sources**: Only returned by search-enabled models (e.g., Perplexity)

---

## Quick Start Checklist

- [ ] Run `npx ai-elements@latest`
- [ ] Install `ai @ai-sdk/react zod`
- [ ] Configure API key in `.env.local`
- [ ] Create `/api/chat/route.ts`
- [ ] Import components from `@/components/ai-elements/`
- [ ] Use `useChat` hook from `@ai-sdk/react`

