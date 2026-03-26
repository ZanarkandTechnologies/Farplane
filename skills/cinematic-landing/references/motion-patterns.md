# Motion Patterns: GSAP & Framer Motion

> **When to use**: Adding animations to content overlays, transitions, and interactive elements.

## Library Decision Matrix

| Use Case | Recommended | Why |
|----------|-------------|-----|
| Scroll-scrubbed timelines | **GSAP ScrollTrigger** | Best scrub performance, timeline control |
| Multi-element sequences | **GSAP** | Timeline orchestration, labels |
| WebGL property animations | **GSAP** | Direct value manipulation |
| Simple hover/tap states | **Framer Motion** | Declarative, React-native |
| Layout animations | **Framer Motion** | `layout` prop magic |
| Enter/exit transitions | **Framer Motion** | AnimatePresence |

---

# GSAP Patterns

## Setup in React/Next.js

```bash
pnpm add gsap @gsap/react
```

```tsx
"use client";

import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

// Register plugin once
gsap.registerPlugin(ScrollTrigger);
```

## useGSAP Hook (Required for React)

**⚠️ CRITICAL**: Always use `useGSAP` or `gsap.context()` to prevent memory leaks.

```tsx
import { useGSAP } from "@gsap/react";
import { useRef } from "react";

function AnimatedComponent() {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    // All GSAP animations here are auto-cleaned up
    gsap.to(".box", { x: 100, duration: 1 });
  }, { scope: containerRef }); // Scope animations to container

  return (
    <div ref={containerRef}>
      <div className="box">Animated</div>
    </div>
  );
}
```

## ScrollTrigger: Basic Scrub Animation

```tsx
useGSAP(() => {
  gsap.to(".hero-text", {
    y: -100,
    opacity: 0,
    scrollTrigger: {
      trigger: ".hero-section",
      start: "top top",      // When top of trigger hits top of viewport
      end: "bottom top",     // When bottom of trigger hits top of viewport
      scrub: true,           // Link to scroll position
      markers: true,         // Debug markers (remove in production)
    }
  });
}, { scope: containerRef });
```

## ScrollTrigger: Pin + Scrub (Sticky Sections)

```tsx
useGSAP(() => {
  gsap.to(".content-panels", {
    xPercent: -100 * (panels.length - 1), // Horizontal scroll
    ease: "none",
    scrollTrigger: {
      trigger: ".panels-container",
      pin: true,              // Pin the container
      scrub: 1,               // Smooth scrubbing (1 = 1 second lag)
      snap: 1 / (panels.length - 1), // Snap to panels
      end: () => "+=" + document.querySelector(".panels-container")?.scrollWidth,
    }
  });
}, { scope: containerRef });
```

## Timeline with ScrollTrigger

```tsx
useGSAP(() => {
  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: ".sequence-container",
      start: "top top",
      end: "+=3000",          // 3000px of scroll
      scrub: 1,
      pin: true,
    }
  });

  // Phase 1: Hero fades out
  tl.to(".hero", { opacity: 0, duration: 1 }, "phase1")
    .to(".hero", { y: -50, duration: 1 }, "phase1");

  // Phase 2: Problem statement appears
  tl.from(".problem", { opacity: 0, y: 50, duration: 1 }, "phase2")
    .to(".problem-bg", { scale: 1.1, duration: 1 }, "phase2");

  // Phase 3: Solution reveals
  tl.to(".problem", { opacity: 0, duration: 0.5 }, "phase3")
    .from(".solution", { opacity: 0, scale: 0.9, duration: 1 }, "phase3");

}, { scope: containerRef });
```

## NARRATIVE Timeline with GSAP

```tsx
const NARRATIVE = {
  VISION: { START: 0, END: 0.15 },
  PROBLEM: { START: 0.10, END: 0.35 },
  SOLUTION: { START: 0.30, END: 0.60 },
  CTA: { START: 0.85, END: 1.0 },
};

useGSAP(() => {
  const totalScroll = 3000; // Total scroll distance

  // Vision phase
  gsap.timeline({
    scrollTrigger: {
      trigger: ".scroll-container",
      start: `top+=${totalScroll * NARRATIVE.VISION.START} top`,
      end: `top+=${totalScroll * NARRATIVE.VISION.END} top`,
      scrub: true,
    }
  })
  .fromTo(".vision", 
    { opacity: 1 }, 
    { opacity: 0 }
  );

  // Problem phase
  gsap.timeline({
    scrollTrigger: {
      trigger: ".scroll-container",
      start: `top+=${totalScroll * NARRATIVE.PROBLEM.START} top`,
      end: `top+=${totalScroll * NARRATIVE.PROBLEM.END} top`,
      scrub: true,
    }
  })
  .fromTo(".problem", 
    { opacity: 0, y: 50 }, 
    { opacity: 1, y: 0, duration: 0.3 }
  )
  .to(".problem", 
    { opacity: 0, duration: 0.2 }, 
    0.8 // Start at 80% of this timeline
  );

}, { scope: containerRef });
```

## Video Scrubbing with GSAP

```tsx
useGSAP(() => {
  const video = videoRef.current;
  if (!video) return;

  // Wait for video metadata
  video.addEventListener("loadedmetadata", () => {
    gsap.to(video, {
      currentTime: video.duration,
      ease: "none",
      scrollTrigger: {
        trigger: ".video-section",
        start: "top top",
        end: "bottom bottom",
        scrub: true,
      }
    });
  });
}, { scope: containerRef, dependencies: [videoRef] });
```

## Parallax with GSAP

```tsx
useGSAP(() => {
  // Background moves slower
  gsap.to(".parallax-bg", {
    yPercent: -30,
    ease: "none",
    scrollTrigger: {
      trigger: ".parallax-container",
      start: "top bottom",
      end: "bottom top",
      scrub: true,
    }
  });

  // Foreground moves faster
  gsap.to(".parallax-fg", {
    yPercent: -60,
    ease: "none",
    scrollTrigger: {
      trigger: ".parallax-container",
      start: "top bottom",
      end: "bottom top",
      scrub: true,
    }
  });
}, { scope: containerRef });
```

## Staggered Reveal on Scroll

```tsx
useGSAP(() => {
  gsap.from(".card", {
    y: 100,
    opacity: 0,
    stagger: 0.2,           // 200ms between each
    duration: 0.8,
    ease: "power2.out",
    scrollTrigger: {
      trigger: ".cards-grid",
      start: "top 80%",     // Start when top is 80% down viewport
      toggleActions: "play none none reverse", // Play on enter, reverse on leave
    }
  });
}, { scope: containerRef });
```

## Motion Path Animation

```tsx
useGSAP(() => {
  gsap.to(".floating-element", {
    motionPath: {
      path: "#curve-path",   // SVG path element
      align: "#curve-path",
      alignOrigin: [0.5, 0.5],
      autoRotate: true,
    },
    scrollTrigger: {
      trigger: ".path-container",
      start: "top center",
      end: "bottom center",
      scrub: 1,
    }
  });
}, { scope: containerRef });
```

---

# Framer Motion Patterns

## Core Concepts

### Motion Values vs. State

```tsx
// ❌ Don't use React state for scroll-driven animations
const [opacity, setOpacity] = useState(1);

// ✅ Use Motion values - they don't trigger re-renders
const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);
```

### useTransform for Scroll-Linked Animations

```tsx
import { useScroll, useTransform, motion } from "framer-motion";

function ScrollAnimatedElement() {
  const { scrollYProgress } = useScroll();
  
  // Map scroll progress [0, 1] to opacity [0, 1]
  const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [0, 1, 0]);
  
  // Map scroll progress to Y position
  const y = useTransform(scrollYProgress, [0, 1], [100, -100]);
  
  // Map scroll progress to scale
  const scale = useTransform(scrollYProgress, [0, 0.5], [0.8, 1]);
  
  return (
    <motion.div style={{ opacity, y, scale }}>
      Content
    </motion.div>
  );
}
```

---

## NARRATIVE Opacity Pattern

Helper function to generate opacity from NARRATIVE config:

```tsx
const NARRATIVE = {
  VISION: { START: 0.0, PEAK: 0.05, END: 0.15 },
  PROBLEM: { START: 0.10, PEAK: 0.20, END: 0.35 },
  // ... more phases
};

/**
 * Generate opacity transform for a narrative phase.
 * Creates: fade in → hold at peak → fade out
 */
const useNarrativeOpacity = (
  scrollProgress: MotionValue<number>,
  config: { START: number; PEAK: number; END: number }
) => {
  return useTransform(
    scrollProgress,
    [
      config.START,                              // Begin fade in
      config.PEAK,                               // Reach full opacity
      config.PEAK + (config.END - config.PEAK) * 0.8, // Hold
      config.END                                 // Fade out complete
    ],
    [0, 1, 1, 0]
  );
};

// Usage
const visionOpacity = useNarrativeOpacity(scrollYProgress, NARRATIVE.VISION);
const problemOpacity = useNarrativeOpacity(scrollYProgress, NARRATIVE.PROBLEM);
```

---

## Content Overlay Template

Standard structure for scroll-reveal content sections:

```tsx
{/* Content Overlays Container */}
<div className="relative z-[100] h-full w-full pointer-events-none flex items-center justify-center">
  <div className="max-w-7xl w-full px-6 text-center">
    
    {/* Phase 1: Vision */}
    <motion.div 
      style={{ opacity: opacities.vision }} 
      className="absolute inset-0 flex flex-col items-center justify-end pb-24 px-6"
    >
      <h1 className="text-9xl font-mono font-black tracking-tighter uppercase">
        {CONTENT.VISION.TITLE_PREFIX}
        <span className="text-primary">{CONTENT.VISION.TITLE_ACCENT}</span>
      </h1>
      <p className="text-3xl font-mono uppercase tracking-widest">
        {CONTENT.VISION.SUBTITLE}
      </p>
    </motion.div>

    {/* Phase 2: Problem */}
    <motion.div 
      style={{ opacity: opacities.problem }} 
      className="absolute inset-0 flex flex-col items-center justify-center"
    >
      <div className="max-w-4xl text-left space-y-8">
        <div className="inline-block bg-primary border-4 border-black p-4 shadow-brutal">
          <h2 className="text-5xl font-black text-black uppercase">
            {CONTENT.PROBLEM.TITLE}
          </h2>
        </div>
        <blockquote className="text-4xl font-black border-l-8 border-secondary pl-8">
          {CONTENT.PROBLEM.QUOTE}
        </blockquote>
      </div>
    </motion.div>

    {/* Phase N: CTA (stays visible at end) */}
    <motion.div 
      style={{ 
        opacity: useTransform(scrollYProgress, [0.85, 0.95], [0, 1]) 
      }} 
      className="absolute inset-0 flex flex-col items-center justify-center"
    >
      <h2 className="text-8xl font-black">
        {CONTENT.CTA.TITLE}
      </h2>
      <motion.a
        href="/contact"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="pointer-events-auto px-12 py-6 bg-primary text-black font-black"
      >
        {CONTENT.CTA.BUTTON}
      </motion.a>
    </motion.div>

  </div>
</div>
```

---

## Parallax Backgrounds

Move backgrounds at different rates for depth:

```tsx
function ParallaxLayers() {
  const { scrollYProgress } = useScroll();
  
  // Background moves slower (parallax)
  const backgroundY = useTransform(scrollYProgress, [0, 1], ["0%", "-20%"]);
  
  // Midground moves at medium speed
  const midgroundY = useTransform(scrollYProgress, [0, 1], ["0%", "-35%"]);
  
  // Foreground moves fastest
  const foregroundY = useTransform(scrollYProgress, [0, 1], ["0%", "-50%"]);
  
  return (
    <>
      <motion.div style={{ y: backgroundY }} className="absolute inset-0 z-10">
        <Image src="/bg.jpg" fill className="object-cover" />
      </motion.div>
      
      <motion.div style={{ y: midgroundY }} className="absolute inset-0 z-20">
        <Image src="/midground.png" fill className="object-cover" />
      </motion.div>
      
      <motion.div style={{ y: foregroundY }} className="absolute inset-0 z-30">
        <Image src="/foreground.png" fill className="object-cover" />
      </motion.div>
    </>
  );
}
```

---

## Interactive Elements with Pointer Events

Content in scroll animations is pointer-events-none by default. Re-enable for interactive elements:

```tsx
<motion.div className="absolute inset-0 pointer-events-none">
  {/* Non-interactive content */}
  <h1>Title</h1>
  
  {/* Interactive button - re-enable pointer events */}
  <motion.a
    href="/contact"
    className="pointer-events-auto"  // ← Key!
    whileHover={{ scale: 1.05, x: 4, y: 4, boxShadow: "none" }}
    whileTap={{ scale: 0.95 }}
  >
    Click Me
  </motion.a>
</motion.div>
```

---

## AnimatePresence for Transitions

Animate elements entering and exiting:

```tsx
import { AnimatePresence, motion } from "framer-motion";

function TransitionExample({ showContent }: { showContent: boolean }) {
  return (
    <AnimatePresence>
      {showContent && (
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -50 }}
          transition={{ duration: 0.5, ease: "easeInOut" }}
        >
          Content that fades in/out
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

---

## Staggered Animations

Animate children with delays:

```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,  // 100ms between each child
      delayChildren: 0.2,    // Wait 200ms before starting
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

function StaggeredList({ items }: { items: string[] }) {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map((item, i) => (
        <motion.li key={i} variants={itemVariants}>
          {item}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

---

## Scroll-Triggered Reveal Animation

Animate when element enters viewport:

```tsx
import { motion } from "framer-motion";

function RevealOnScroll({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
```

---

## Navbar Fade on Scroll

Fade/hide navbar as user scrolls:

```tsx
function ScrollFadeNavbar() {
  const { scrollYProgress } = useScroll();
  
  const headerY = useTransform(scrollYProgress, [0, 0.02], [0, -100]);
  const headerOpacity = useTransform(scrollYProgress, [0, 0.02], [1, 0]);
  
  return (
    <motion.nav
      style={{ y: headerY, opacity: headerOpacity }}
      className="fixed top-0 left-0 w-full z-[200]"
    >
      <Navbar />
    </motion.nav>
  );
}
```

---

## Bounce/Pulse Animations

For attention-grabbing elements:

```tsx
{/* Bouncing scroll indicator */}
<motion.div 
  animate={{ y: [0, 10, 0] }} 
  transition={{ repeat: Infinity, duration: 2 }}
  className="flex flex-col items-center"
>
  <span className="text-xs uppercase tracking-widest">Scroll</span>
  <ArrowDown className="w-5 h-5" />
</motion.div>

{/* Pulsing marker */}
<div className="relative">
  <div className="w-4 h-4 bg-primary rounded-full" />
  <div className="absolute inset-0 w-4 h-4 border-2 border-primary rounded-full animate-ping" />
</div>
```

---

## Hover Effects with Brutalist Style

```tsx
<motion.button
  whileHover={{ 
    scale: 1.02, 
    x: 4, 
    y: 4, 
    boxShadow: "none"  // Remove shadow on hover
  }}
  whileTap={{ scale: 0.98 }}
  className="
    px-8 py-4 
    bg-primary text-black font-black uppercase
    border-4 border-black 
    shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]
    transition-all
  "
>
  Click Me
</motion.button>
```

---

## Grid Card Hover

```tsx
<motion.div
  whileHover={{ scale: 1.02 }}
  className="
    p-8 
    bg-black border-4 border-white 
    shadow-[8px_8px_0px_0px_rgba(255,95,31,1)]
    hover:translate-x-1 hover:translate-y-1 
    hover:shadow-none 
    transition-all duration-300
  "
>
  <h3>Card Title</h3>
  <p>Card content</p>
</motion.div>
```

---

## Performance Tips

1. **Use Motion Values**: Avoid React state for animations
2. **Memoize Transforms**: `useTransform` returns stable references
3. **GPU Acceleration**: Use `transform` and `opacity` (not `top`, `left`)
4. **will-change**: Add `will-change: transform` for heavy animations
5. **Debounce**: For window resize handlers, debounce updates

---

## Gotchas

### GSAP-Specific
1. **useGSAP Required**: Always use `useGSAP` hook in React to prevent memory leaks
2. **Plugin Registration**: Register ScrollTrigger once at app level: `gsap.registerPlugin(ScrollTrigger)`
3. **Scope**: Pass `{ scope: containerRef }` to limit selector scope
4. **SSR**: GSAP runs on client only—wrap in `useEffect` or dynamic import
5. **Markers**: Remove `markers: true` in production

### Framer Motion-Specific
1. **pointer-events-none**: Don't forget to re-enable for interactive elements
2. **z-index Wars**: Use clear layering system (100+ for content)
3. **Mobile Performance**: Test on real devices—animations can be janky
4. **Initial Flash**: Use `initial={{ opacity: 0 }}` to prevent FOUC
5. **Exit Animations**: Wrap in `AnimatePresence` for exit animations to work

### General
1. **GPU Acceleration**: Use `transform` and `opacity` (not `top`, `left`)
2. **will-change**: Add `will-change: transform` for heavy animations
3. **Debounce**: For window resize handlers, debounce updates

