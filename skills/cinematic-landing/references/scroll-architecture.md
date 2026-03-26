# Scroll Architecture: NARRATIVE Timeline + Video Scrubbing

> **When to use**: Setting up the scroll engine after you have your story and assets ready.

**Note**: This reference shows both **Framer Motion** and **GSAP** approaches. Choose based on your needs:
- **GSAP ScrollTrigger**: Best for complex timelines, video scrubbing, pinning
- **Framer Motion**: Best for simpler scroll-linked transforms, React integration

## Core Concept: Sticky Viewport Architecture

The entire page is a tall container (e.g., 2600vh) with a sticky viewport that:
1. Pins visual layers to the screen
2. Manipulates properties based on scroll progress
3. Creates the illusion of scene transitions without page navigation

```
┌─────────────────────────────────────┐
│         Tall Scroll Container       │  height: 2600vh
│  ┌───────────────────────────────┐  │
│  │     Sticky Viewport (100vh)   │  │  position: sticky
│  │  ┌─────────────────────────┐  │  │
│  │  │   Layer Stack (z-index) │  │  │
│  │  │   - Background Videos   │  │  │
│  │  │   - WebGL Effects       │  │  │
│  │  │   - Content Overlays    │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
│                                     │
│         (scroll area continues)     │
└─────────────────────────────────────┘
```

---

## NARRATIVE Timeline Configuration

Define your scroll timeline using START/PEAK/END percentages:

```typescript
/**
 * NARRATIVE TIMELINE
 * ------------------
 * Each section follows a [START, PEAK, END] lifecycle.
 * - START: Content begins to fade in
 * - PEAK: Content is at 100% opacity
 * - END: Content is completely faded out
 * 
 * ⚠️ CRITICAL: To prevent "blank" gaps, ensure the START of a section 
 * is equal to or less than the END of the previous section.
 */
const NARRATIVE = {
  // Phase 0: Hero / Opening Scene
  VISION: { START: 0.0, PEAK: 0.00, END: 0.025 },

  // Phase 1: Problem Statement
  FALLACY: { START: 0.025, PEAK: 0.075, END: 0.22 },

  // Phase 2: Solution Part 1
  CONCRETE: { START: 0.22, PEAK: 0.28, END: 0.35 },

  // Phase 3: Solution Part 2
  STANDARD: { START: 0.35, PEAK: 0.41, END: 0.50 },

  // Phase 4: Proof / Case Studies
  BENTO: { START: 0.50, PEAK: 0.57, END: 0.65 },

  // Phase 5: Social Proof
  PROOFS: { START: 0.65, PEAK: 0.70, END: 0.75 },

  // Phase 6: Pricing
  PRICING: { START: 0.75, PEAK: 0.80, END: 0.85 },

  // Phase 7: Final CTA (stays visible)
  CTA: { START: 0.85, PEAK: 0.90, END: 1.0 }
};

// Helper for layer visibility boundaries
const LAYERS = {
  BRIDGE: NARRATIVE.VISION.END,
  CRUMBLE: NARRATIVE.FALLACY.END,
  MECHANISM: NARRATIVE.STANDARD.END,
  PAPER: NARRATIVE.BENTO.END,
  CITY_START: NARRATIVE.BENTO.END,
};
```

---

## Basic Scroll Setup (Framer Motion)

```tsx
"use client";

import { useRef } from "react";
import { useScroll, useTransform, motion } from "framer-motion";

const TOTAL_VH = 2600; // Total scroll height

export function LandingScroll() {
  const containerRef = useRef<HTMLDivElement>(null);

  // Track scroll progress (0.0 to 1.0)
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"],
  });

  // Helper to generate opacity transforms from NARRATIVE config
  const useNarrativeOpacity = (config: { START: number, PEAK: number, END: number }) =>
    useTransform(
      scrollYProgress, 
      [config.START, config.PEAK, config.PEAK + (config.END - config.PEAK) * 0.8, config.END], 
      [0, 1, 1, 0]
    );

  return (
    <div
      ref={containerRef}
      className="relative bg-black"
      style={{ height: `${TOTAL_VH}vh` }}
    >
      <div className="sticky top-0 h-screen w-full overflow-hidden">
        {/* Layer stack goes here */}
      </div>
    </div>
  );
}
```

---

## Basic Scroll Setup (GSAP)

```tsx
"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

const TOTAL_VH = 2600;

export function LandingScrollGSAP() {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    // Create timeline with pin
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: containerRef.current,
        start: "top top",
        end: "bottom bottom",
        scrub: 1,
        pin: ".viewport", // Pin the viewport
      }
    });

    // Phase 1: Vision fades out
    tl.to(".vision-content", {
      opacity: 0,
      y: -50,
      duration: NARRATIVE.VISION.END - NARRATIVE.VISION.START,
    }, NARRATIVE.VISION.START);

    // Phase 2: Problem fades in then out
    tl.fromTo(".problem-content",
      { opacity: 0, y: 50 },
      { opacity: 1, y: 0, duration: 0.1 },
      NARRATIVE.PROBLEM.START
    ).to(".problem-content",
      { opacity: 0, duration: 0.05 },
      NARRATIVE.PROBLEM.END - 0.05
    );

    // Continue for other phases...

  }, { scope: containerRef });

  return (
    <div ref={containerRef} style={{ height: `${TOTAL_VH}vh` }}>
      <div className="viewport sticky top-0 h-screen w-full overflow-hidden">
        <div className="vision-content absolute inset-0">{/* Vision */}</div>
        <div className="problem-content absolute inset-0">{/* Problem */}</div>
        {/* More layers */}
      </div>
    </div>
  );
}
```

---

## Video Scrubbing with RAF Loop (Production-Proven)

**Problem**: Direct `video.currentTime` updates are janky.  
**Solution**: Use requestAnimationFrame with interpolation for smooth scrubbing.

> ✅ **This is the battle-tested approach from Zanarkand Landing.** It works reliably and requires no extra dependencies beyond Framer Motion.

```tsx
"use client";

import { useRef, useEffect } from "react";
import { useScroll, useMotionValueEvent } from "framer-motion";

export function VideoScrubber() {
  const containerRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  
  // Target time for smooth interpolation
  const targetTimeRef = useRef<number>(0);

  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"],
  });

  // Video initialization
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    
    video.preload = "auto";
    video.load();
    
    const handleReady = () => {
      video.pause();
      video.currentTime = 0;
    };
    
    video.addEventListener("loadedmetadata", handleReady);
    return () => video.removeEventListener("loadedmetadata", handleReady);
  }, []);

  // Smooth scrubbing RAF loop
  useEffect(() => {
    let animationFrameId: number;
    
    const updateVideo = () => {
      const video = videoRef.current;
      if (!video || !video.duration || isNaN(video.duration)) {
        animationFrameId = requestAnimationFrame(updateVideo);
        return;
      }

      const targetTime = targetTimeRef.current;
      const diff = targetTime - video.currentTime;
      
      // Smooth interpolation (0.1 = lerp factor)
      if (Math.abs(diff) > 0.001) {
        video.currentTime += diff * 0.1;
      } else if (video.currentTime !== targetTime) {
        video.currentTime = targetTime;
      }
      
      animationFrameId = requestAnimationFrame(updateVideo);
    };
    
    updateVideo();
    return () => cancelAnimationFrame(animationFrameId);
  }, []);

  // Update target time based on scroll
  useMotionValueEvent(scrollYProgress, "change", (latest) => {
    const video = videoRef.current;
    if (!video || !video.duration) return;

    const { START, END } = NARRATIVE.FALLACY; // Example phase
    
    if (latest < START) {
      video.style.opacity = "0";
      targetTimeRef.current = 0;
    } else if (latest < END) {
      video.style.opacity = "1";
      const progress = (latest - START) / (END - START);
      targetTimeRef.current = progress * video.duration;
    } else {
      video.style.opacity = "0";
    }
  });

  return (
    <video
      ref={videoRef}
      className="absolute inset-0 w-full h-full object-cover transition-opacity duration-500"
      src="/assets/scrub_video.mp4"
      muted
      playsInline
      preload="auto"
      style={{ zIndex: 10, opacity: 0 }}
    />
  );
}
```

---

## Video Scrubbing with GSAP (Alternative)

> ⚠️ **Alternative approach** - Use this if you're already using GSAP for other animations. The RAF loop above is proven to work.

GSAP provides cleaner video scrubbing with less boilerplate:

```tsx
"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function GSAPVideoScrubber() {
  const containerRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  useGSAP(() => {
    const video = videoRef.current;
    if (!video) return;

    // Wait for video to be ready
    const setupScrub = () => {
      gsap.to(video, {
        currentTime: video.duration,
        ease: "none",
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top top",
          end: "bottom bottom",
          scrub: 0.5,  // Smooth scrubbing with 0.5s lag
        }
      });
    };

    if (video.readyState >= 1) {
      setupScrub();
    } else {
      video.addEventListener("loadedmetadata", setupScrub, { once: true });
    }
  }, { scope: containerRef });

  return (
    <div ref={containerRef} style={{ height: "300vh" }}>
      <div className="sticky top-0 h-screen">
        <video
          ref={videoRef}
          className="absolute inset-0 w-full h-full object-cover"
          src="/assets/scrub_video.mp4"
          muted
          playsInline
          preload="auto"
        />
      </div>
    </div>
  );
}
```

### GSAP with NARRATIVE Phases

```tsx
useGSAP(() => {
  const video = videoRef.current;
  if (!video) return;

  const setupScrub = () => {
    const totalScroll = containerRef.current?.scrollHeight || 3000;
    
    // Only play video during PROBLEM phase
    ScrollTrigger.create({
      trigger: containerRef.current,
      start: `top+=${totalScroll * NARRATIVE.PROBLEM.START} top`,
      end: `top+=${totalScroll * NARRATIVE.PROBLEM.END} top`,
      onUpdate: (self) => {
        // Map phase progress to video time
        video.currentTime = self.progress * video.duration;
      },
      onEnter: () => { video.style.opacity = "1"; },
      onLeave: () => { video.style.opacity = "0"; },
      onEnterBack: () => { video.style.opacity = "1"; },
      onLeaveBack: () => { video.style.opacity = "0"; },
    });
  };

  video.addEventListener("loadedmetadata", setupScrub, { once: true });
}, { scope: containerRef });
```

---

## Layer Z-Index Management

Manage which visual layer is "active" based on scroll position:

```tsx
// Dynamic z-index based on scroll progress
const getLayerZ = (latest: number) => {
  if (latest < LAYERS.BRIDGE) return 50;    // Hero layer on top
  if (latest < LAYERS.CRUMBLE) return 10;   // Crumble video
  if (latest < LAYERS.MECHANISM) return 20; // Mechanism video
  if (latest < LAYERS.PAPER) return 30;     // Paper/WebGL
  return 40;                                 // Final city
};

// In component:
<motion.div
  className="absolute inset-0 w-full h-full"
  style={{
    zIndex: useTransform(scrollYProgress, [0, NARRATIVE.VISION.END, NARRATIVE.VISION.END + 0.01], [50, 50, 0]),
    pointerEvents: useTransform(scrollYProgress, [0, NARRATIVE.VISION.END], ["auto", "none"])
  }}
>
  {/* Layer content */}
</motion.div>
```

---

## Preloader Pattern

Load critical assets before showing the page:

```tsx
"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const ASSETS = {
  critical: {
    images: ["/assets/hero.jpeg", "/assets/background.png"],
    videos: ["/assets/scrub_video.mp4"],
  },
  background: {
    images: ["/assets/secondary.jpeg"],
    videos: ["/assets/city_loop.mp4"],
  }
};

export function Preloader({ onComplete }: { onComplete: () => void }) {
  const [progress, setProgress] = useState(0);
  const [isLoaded, setIsLoaded] = useState(false);
  const [loadingText, setLoadingText] = useState("INITIALIZING_SYSTEM");

  useEffect(() => {
    let loadedCount = 0;
    const criticalAssets = [...ASSETS.critical.images, ...ASSETS.critical.videos];
    const totalCritical = criticalAssets.length;

    const updateProgress = () => {
      loadedCount++;
      const newProgress = Math.round((loadedCount / totalCritical) * 100);
      setProgress(newProgress);

      // Update loading text based on progress
      if (newProgress < 30) setLoadingText("LOADING_CORE_ASSETS");
      else if (newProgress < 60) setLoadingText("CALIBRATING_ENGINE");
      else if (newProgress < 90) setLoadingText("READYING_NARRATIVE");
      else setLoadingText("SYSTEM_OPTIMIZED");

      if (loadedCount === totalCritical) {
        setTimeout(() => {
          setIsLoaded(true);
          setTimeout(onComplete, 1000);
        }, 500);
      }
    };

    // Load critical images
    ASSETS.critical.images.forEach((src) => {
      const img = new Image();
      img.src = src;
      img.onload = updateProgress;
      img.onerror = updateProgress;
    });

    // Load critical videos
    ASSETS.critical.videos.forEach((src) => {
      const video = document.createElement("video");
      video.src = src;
      video.preload = "auto";
      video.addEventListener("canplaythrough", updateProgress, { once: true });
      video.load();
    });

    // Background load non-critical assets (don't block)
    ASSETS.background.images.forEach((src) => {
      const img = new Image();
      img.src = src;
    });

    ASSETS.background.videos.forEach((src) => {
      const video = document.createElement("video");
      video.src = src;
      video.preload = "auto";
      video.load();
    });

    // Fallback timeout
    const timer = setTimeout(() => {
      if (!isLoaded) {
        setProgress(100);
        setIsLoaded(true);
        onComplete();
      }
    }, 15000); // 15s max wait

    return () => clearTimeout(timer);
  }, [onComplete, isLoaded]);

  return (
    <AnimatePresence>
      {!isLoaded && (
        <motion.div
          initial={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.8, ease: "easeInOut" }}
          className="fixed inset-0 z-[1000] flex flex-col items-center justify-center bg-black font-mono"
        >
          <div className="w-full max-w-md px-10 space-y-8">
            <div className="space-y-2">
              <div className="flex justify-between text-[10px] tracking-[0.3em] text-primary mb-2">
                <span>{loadingText}</span>
                <span>{progress}%</span>
              </div>
              <div className="h-[2px] w-full bg-white/10 relative overflow-hidden">
                <motion.div
                  className="absolute top-0 left-0 h-full bg-primary"
                  initial={{ width: "0%" }}
                  animate={{ width: `${progress}%` }}
                  transition={{ duration: 0.3 }}
                />
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

---

## Complete Component Structure

```tsx
export function LandingScroll() {
  return (
    <div className="bg-black text-white">
      <div ref={containerRef} style={{ height: `${TOTAL_VH}vh` }}>
        
        {/* Fixed Navbar */}
        <motion.div className="fixed top-0 left-0 w-full z-[200]">
          <Navbar />
        </motion.div>

        {/* Sticky Viewport */}
        <div className="sticky top-0 h-screen w-full overflow-hidden">
          <div className="relative w-full h-full max-w-[1920px] mx-auto">
            
            {/* === VISUAL LAYERS === */}
            
            {/* Layer 1: Hero Image/Component */}
            <motion.div style={{ zIndex: 50 }}>
              <HeroComponent scrollProgress={scrollYProgress} />
            </motion.div>

            {/* Layer 2: Scrub Video 1 */}
            <video ref={video1Ref} style={{ zIndex: 10, opacity: 0 }} />

            {/* Layer 3: Scrub Video 2 */}
            <video ref={video2Ref} style={{ zIndex: 20, opacity: 0 }} />

            {/* Layer 4: WebGL Effect */}
            <motion.div style={{ zIndex: 30 }}>
              <WebGLScene />
            </motion.div>

            {/* Layer 5: Final Background */}
            <motion.div style={{ zIndex: 40 }}>
              <video ref={finalVideoRef} loop />
            </motion.div>

            {/* === CONTENT OVERLAYS === */}
            <div className="relative z-[100]">
              <motion.div style={{ opacity: opacities.vision }}>
                {/* Vision content */}
              </motion.div>
              
              <motion.div style={{ opacity: opacities.problem }}>
                {/* Problem content */}
              </motion.div>
              
              {/* ... more overlays */}
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## Video Encoding for Scrubbing

**⚠️ CRITICAL**: Videos must be encoded with frequent keyframes for smooth scrubbing!

Without frequent keyframes (I-frames), the browser must decode from the previous keyframe when seeking, causing lag and jank during scroll scrubbing.

### FFmpeg Command for Scrub-Ready Videos

```bash
# Encode with keyframe every 1 frame (best for scrubbing, larger file)
ffmpeg -i input.mp4 \
  -vcodec libx264 \
  -x264-params keyint=1:scenecut=0 \
  -crf 23 \
  -preset slow \
  -vf "scale=1920:-2" \
  -an \
  output_scrub.mp4

# Balanced: keyframe every 10 frames (good compromise)
ffmpeg -i input.mp4 \
  -vcodec libx264 \
  -g 10 \
  -keyint_min 10 \
  -crf 25 \
  -preset slow \
  -vf "scale=1920:-2" \
  -an \
  output_scrub.mp4
```

### Key Parameters Explained

| Parameter | Purpose |
|-----------|---------|
| `-x264-params keyint=1` | Keyframe every N frames (1 = every frame) |
| `-g 10` | GOP (Group of Pictures) size - keyframe interval |
| `-keyint_min 10` | Minimum keyframe interval |
| `-scenecut=0` | Disable scene detection (consistent keyframes) |
| `-crf 23-28` | Quality (lower = better, larger file) |
| `-an` | Remove audio (not needed for scrub videos) |
| `-vf "scale=1920:-2"` | Scale to 1920px width, maintain aspect |

### Recommended Settings by Use Case

```bash
# Hero scrub video (needs smoothest scrubbing)
# Keyframe every frame, higher quality
ffmpeg -i hero.mp4 \
  -vcodec libx264 \
  -x264-params keyint=1:scenecut=0 \
  -crf 20 \
  -preset veryslow \
  -vf "scale=1920:-2" \
  -an \
  hero_scrub.mp4

# Background scrub video (can tolerate slight lag)
# Keyframe every 5 frames, smaller file
ffmpeg -i background.mp4 \
  -vcodec libx264 \
  -g 5 \
  -keyint_min 5 \
  -crf 26 \
  -preset slow \
  -vf "scale=1280:-2" \
  -an \
  background_scrub.mp4

# Loop video (not scrubbed, normal encoding is fine)
ffmpeg -i loop.mp4 \
  -vcodec libx264 \
  -crf 26 \
  -preset slow \
  -vf "scale=1920:-2" \
  -an \
  loop_compressed.mp4
```

### Verifying Keyframe Placement

```bash
# Check keyframe positions in a video
ffprobe -select_streams v -show_frames \
  -show_entries frame=pict_type \
  -of csv output_scrub.mp4 | grep -n "I"
```

---

## Gotchas

1. **Video Keyframes**: Encode with frequent keyframes for scrubbing (see above)
2. **Video Format**: Use H.264 MP4 for best browser support
3. **Video Size**: Keep scrub videos under 5MB after compression
4. **RAF Loop**: Always cleanup with `cancelAnimationFrame`
5. **Scroll Progress**: Ensure no "dead zones" between sections
6. **Mobile**: Test touch scrolling—momentum can cause jank
7. **Preload**: Mark videos as `preload="auto"` and `playsInline` for mobile
8. **Canvas Rendering**: For WebGL video textures, ensure video is CORS-enabled if hosted externally

