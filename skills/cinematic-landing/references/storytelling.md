# Storytelling: Pitch → Parable → Visuals

> **When to use**: Starting a new landing page. This is Phase 1 of the cinematic workflow.

## The Philosophy

Standard UI design starts with layout. **Cinematic design starts with story.**

By anchoring every visual decision in a narrative (the "parable"), we break the generic patterns that arise from component-first thinking. The story gives you:
- Natural scene breaks (scroll sections)
- Visual metaphors (hero elements)
- Emotional arc (problem → tension → resolution)
- Distinctive aesthetic (the story's "world")

---

## 5-Step Process

### Step 1: Write the Pitch (Problem → Solution → CTA)

Before any design, write a 3-part pitch:

```markdown
## Pitch Template

**Problem**: [What pain does your audience feel?]
**Solution**: [How do you solve it uniquely?]
**CTA**: [What action should they take?]
```

**Example (Zanarkand Technologies):**
```markdown
**Problem**: 95% of AI pilots fail. Enterprise AI is opaque—you can't fix what you can't observe.
**Solution**: Industrial-grade AI infrastructure with total traceability. Audited logic for mission-critical systems.
**CTA**: Initialize Partnership (book a consultation)
```

---

### Step 2: Create the Parable

Transform your pitch into a metaphorical story. The parable should:
- Mirror your customer's journey
- Have visual potential (can you see it?)
- Contain 3-4 distinct "scenes" or moments

**Parable Template:**
```markdown
## The Parable of [Metaphor Name]

[Opening scene - the promise/vision]
[Conflict scene - the hidden problem]
[Resolution scene - the method/proof]
[Finale scene - the transformed state]
```

**Example: The Broken Bridge**
```markdown
## The Parable of the Broken Bridge

SCENE 1: A beautiful oil painting of a grand bridge - the vision sold to stakeholders.
SCENE 2: Zoom in reveals cracks, stress points, structural debt - the reality beneath the vision.
SCENE 3: Engineers with blueprints, measurement tools, rigorous analysis - the method of observability.
SCENE 4: The bridge rebuilt, stronger, monitored - the proven infrastructure.
```

---

### Step 3: Extract Visual Elements

From your parable, identify:

| Element Type | Count | Purpose |
|--------------|-------|---------|
| **Backgrounds** | 4 (one per scene) | Set the atmosphere |
| **Hero Elements** | 2-3 | Eye-catching focal points |
| **Transitional Assets** | As needed | Connect scenes (e.g., zooming, revealing) |

**Example Visual Breakdown:**
```markdown
## Backgrounds
1. Oil painting of complete bridge (renaissance style)
2. Same bridge crumbling (video scrub reveal)
3. Engineering mechanism / blueprint aesthetic
4. City skyline - the infrastructure transformed

## Hero Elements
- ASCII overlay effect (structural analysis visualization)
- Diagnostic HUD markers (stress points)
- Animated mechanism (engineering precision)

## Transitions
- Mouse-reveal effect (beautiful → structural)
- Video scrub (bridge crumbling)
- Parallax city scroll
```

---

### Step 4: Choose Your Style

The style should emerge from the parable's world. Commit fully—timidity leads to genericism.

| Style | When to Use | Visual Characteristics |
|-------|-------------|------------------------|
| **Renaissance Oil** | Authority, trust, timelessness | Rich textures, impasto effects, dramatic chiaroscuro |
| **Pixel Art** | Tech/gaming, nostalgia, playfulness | Limited palette, crisp edges, 8-bit aesthetic |
| **Brutalist** | Disruption, bold statements, avant-garde | High contrast, monochrome, raw typography |
| **Cinematic** | Premium, storytelling, emotional | Film grain, letterbox, atmospheric lighting |
| **Technical** | B2B, engineering, precision | Grids, monospace fonts, diagnostic overlays |

**Style Commitment Rules:**
- ❌ Don't mix styles (no "a bit of brutalist, a bit of minimal")
- ❌ Don't use safe defaults (Inter, white backgrounds)
- ✅ Push the aesthetic to its extreme
- ✅ Let the parable dictate the style

---

### Step 5: Generate Assets

**Human-in-the-Loop Workflow** (default):
1. Agent provides prompts and visual concepts
2. 🛑 **Human generates assets** using:
   - **Images**: [NanoBanana](https://replicate.com/fofr/nanobanana), Midjourney, DALL-E
   - **Videos**: [Kling](https://klingai.com/), Runway
   - **Effects**: [Efecto](https://efecto.app/) (WebGL), [Tooooools](https://www.tooooools.app/) (static)
3. Human provides file paths to agent
4. Agent encodes with FFmpeg and integrates

**Automated Workflow** (if Replicate MCP available):
1. Agent generates via Replicate API automatically
2. No human pause required

**NanoBanana Prompts by Style:**

```markdown
## Renaissance Oil Painting
"[subject], renaissance oil painting style, dramatic chiaroscuro lighting, 
rich impasto texture, baroque composition, museum quality, 8k detail"

## Pixel Art
"[subject], pixel art style, 16-bit aesthetic, limited color palette, 
crisp edges, retro gaming, nostalgic atmosphere"

## Brutalist
"[subject], brutalist design, high contrast black and white, raw concrete 
textures, geometric shapes, bold shadows, industrial aesthetic"

## Cinematic
"[subject], cinematic movie still, anamorphic lens, film grain, 
letterbox composition, dramatic lighting, 35mm film aesthetic"
```

**Video Compression for Scroll Scrub:**
```bash
# Compress for web (target: <5MB per video)
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 -preset slow \
  -vf "scale=1920:-2" -an output_compressed.mp4
```

---

## Content Configuration Pattern

After defining your story, create a centralized content config for easy editing:

```typescript
/**
 * CONTENT CONFIGURATION
 * ---------------------
 * Centralized text content for the entire landing page.
 * Edit these values to refine the brand voice and core messaging.
 */
const CONTENT = {
  // Scene 1: The Vision
  VISION: {
    TITLE_PREFIX: "95% of AI Pilots",
    TITLE_ACCENT: "Fail.",
    SUBTITLE_1: "Most AI failures are invisible.",
    SUBTITLE_2: "We audit the fractures in mission-critical infrastructure.",
    SCROLL_LABEL: "Audit for Transparency"
  },
  
  // Scene 2: The Problem
  PROBLEM: {
    TITLE: "The Black Box Trap",
    QUOTE: "You can't fix what you can't observe.",
    STATUS: "[ SYSTEM STATUS: OPAQUE ]",
    DESCRIPTION: "Enterprise AI isn't for 'cool demos'—it's for critical infrastructure."
  },
  
  // Scene 3: The Solution
  SOLUTION: {
    OVERHEAD: "Our Standard",
    TITLE_PREFIX: "Engineering",
    TITLE_ACCENT: "Reliability.",
    FEATURES: [
      { icon: LayersIcon, text: "SYSTEM INTEGRATION", sub: "Connecting AI to your legacy infrastructure." },
      { icon: ShieldAlert, text: "BENCHMARKS > HYPE", sub: "Hard metrics on latency, drift, and accuracy." },
    ]
  },
  
  // Scene 4: The CTA
  CTA: {
    TITLE_PREFIX: "Engineer Your",
    TITLE_ACCENT: "Mission-Critical",
    TITLE_SUFFIX: "Enterprise.",
    BUTTON: "[ INITIALIZE PARTNERSHIP ]"
  }
};
```

---

## Checklist Before Moving to Implementation

- [ ] Pitch written (Problem → Solution → CTA)
- [ ] Parable created with 4 distinct scenes
- [ ] Visual elements identified (backgrounds, heroes, transitions)
- [ ] Style chosen and committed
- [ ] Asset prompts prepared for NanoBanana
- [ ] CONTENT config drafted

