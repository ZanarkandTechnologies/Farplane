## Deep Research: Terminal Industries parity target for a cinematic warehouse/computer-vision landing page
**Project Context**: Codexter frontend delegation QA for a cinematic enterprise landing page, using Terminal Industries as a parity target for production-grade motion, media, and proof surfaces. `docs/progress.md` is not present in this repo, so project context was taken from `README.md`.
**Date**: 2026-05-07

### Summary
The current `terminal-industries.com` homepage feels premium because it is not a single hero plus static cards. It is a paced narrative with:

- an immediate branded loader and transition system
- a high-contrast hero with oversized statement copy
- scroll-scrubbed sequence media and sticky section choreography
- repeatable section motifs instead of one-off components
- concrete proof modules: operator logos, named quote, Gartner badge, and explicit demo/ROI CTAs
- deliberate responsive fallbacks rather than shipping the exact desktop behavior to mobile

The strongest parity signals are observable in the shipped Nuxt bundles and CSS:

- `Lenis` smooth scrolling is wired into the app shell
- `GSAP` and `ScrollTrigger` drive section transitions, pinning, and parallax
- a canvas-based video-sequence component exists for scrubbed frame playback
- desktop/mobile media assets are intentionally split
- the site uses preload hints for `SuisseIntl` fonts and ships a custom loader / transition layer

### Detailed Findings
- **Site structure**: The homepage sequence is hero -> YOS positioning statement -> 3 fullscreen benefit modules -> industry credibility/logo section -> named testimonial quote -> operator logos -> "How it Works" transition section -> high-intent contact form. Source: `https://terminal-industries.com/`
- **Hero treatment**: The hero copy is oversized, multi-line, and concept-led rather than product-feature-led. It holds attention with statement copy first and defers detail until the next panels. Source: `https://terminal-industries.com/`
- **Scroll-scrubbed media**: The shipped `VideoSequence` component draws frames onto a canvas, lazy-loads frames through a worker, and updates the canvas from a progress value rather than relying only on native `<video>` playback. Source: `https://terminal-industries.com/_nuxt/BbytzNpB.js`
- **Sticky fullscreen section behavior**: The `FullscreenFeatures` module uses GSAP + ScrollTrigger with breakpoint-specific behavior. Desktop uses a scrubbed sticky layout with progress bar and staged text reveals; mobile switches to a simplified progress model. Source: `https://terminal-industries.com/_nuxt/BH53jP1Z.js`
- **Background motion system**: The background is not just gradient decoration. A canvas module renders a grid plus animated pulse/wave masks and moving blurred blobs, with theme variants for dark/green/white. Source: `https://terminal-industries.com/_nuxt/CJZnftco.js`
- **Motion rhythm**: Motion is staged in long beats, not constant ambient animation. Text lines reveal in sequence, parallax is reserved for large image blocks, and section progress is spatially explicit. Sources: `https://terminal-industries.com/_nuxt/BH53jP1Z.js`, `https://terminal-industries.com/_nuxt/Bq_xl9qZ.js`
- **Typography system**: The app preloads `SuisseIntl-Regular` and `SuisseIntl-Medium`; CSS shows a second mono system used for labels, counters, metadata, and buttons. This creates a clear editorial hierarchy between statement copy and operational labels. Source: `https://terminal-industries.com/_nuxt/hEtIiFtn.js`
- **Proof/data surfaces**: Credibility is carried by operator logos, a named quote with role/company attribution, a Gartner badge, and explicit ROI/demo contact options. The site uses real brands and operator-facing conversion paths instead of generic "contact sales". Source: `https://terminal-industries.com/`
- **Media asset strategy**: The homepage ships multiple prerendered MP4 assets plus separate wide/vertical variants, indicating that desktop and mobile framing are intentionally art-directed. Source: `https://terminal-industries.com/`
- **Responsive concerns**: CSS and JS show explicit desktop/mobile asset swaps and different interaction models under `1024px`; the most complex sticky/scrub behavior is reduced on smaller screens rather than forced unchanged. Sources: `https://terminal-industries.com/_nuxt/entry.HNda-aXC.css`, `https://terminal-industries.com/_nuxt/BH53jP1Z.js`

### Recommended "Best Version"
For QA parity, the target should not be "looks sleek." The target should be:

1. A branded loader or first-impression transition exists and feels intentional.
2. The hero carries the story with oversized copy and a controlled background/media system.
3. At least one major section uses scroll-linked media or sequence behavior, not only fade-in cards.
4. Motion pacing alternates between dense visual sections and quiet proof/copy sections.
5. Proof is concrete: named customers, measurable claims, or industry artifacts.
6. Mobile has deliberate fallbacks for heavy motion and art direction, not broken desktop leftovers.

### QA Recipe / Checklist for a delegated Pi/Kimi build
- **Hero**: Above the fold should contain one dominant headline block, one supporting line, and one motion-capable visual surface. Reject if the first screen is just a nav, a small headline, and a centered mockup.
- **Hero media**: The main visual should either scrub with scroll or clearly run as a high-quality loop with no visible stutter, cropping bugs, or poster flash. Reject if the media behaves like a default autoplay embed.
- **Section progression**: The page should read as 6-8 distinct beats with clear changes in density: statement -> system explanation -> benefits -> proof -> workflow -> CTA. Reject if all sections are interchangeable card grids.
- **Scroll-linked section**: At least one section should pin or feel spatially anchored while copy or media progresses. Reject if every section only fades upward on intersection.
- **Motion rhythm**: Animations should arrive in groups with staggered line or block reveals, then settle. Reject if motion is constant everywhere or absent everywhere.
- **Typography**: Use one premium primary face for large statements and one technical/mono face for labels, counters, and metadata. Reject if all text uses one generic sans stack.
- **Proof**: Include at least two of: customer logos, named testimonial, recognizable analyst/press badge, concrete metric, demo artifact, ROI entrypoint. Reject if proof is only abstract claims.
- **Media art direction**: Mobile should have separate crops or alternate assets for key media moments. Reject if desktop videos simply shrink and crop unpredictably on phones.
- **Responsive behavior**: Sticky/scrub sections should degrade cleanly on mobile into shorter reveals or stepped progress. Reject if mobile traps scroll, causes jank, or leaves overlapping layers.
- **CTA quality**: Final CTA should be high-intent and specific, such as demo, ROI assessment, or proof-of-value. Reject if the only close is a generic email signup.
- **Implementation clue parity**: A premium build in this style should usually show evidence of a motion stack equivalent to Lenis + GSAP/ScrollTrigger or an equally deliberate alternative. Reject if the output uses only basic CSS transitions while claiming cinematic parity.

### Action Items for Main Agent
1. Use this checklist as the acceptance rubric for the delegated Pi/Kimi build, especially hero, one pinned/scrubbed section, proof surfaces, and mobile degradation.
2. Require the delegated build to declare its motion stack and fallback plan up front.
3. During visual QA, test desktop and mobile separately; do not accept desktop-first motion that collapses on small screens.

### Sources
- Homepage: https://terminal-industries.com/
- App shell and motion/font preload clues: https://terminal-industries.com/_nuxt/hEtIiFtn.js
- Video sequence canvas component: https://terminal-industries.com/_nuxt/BbytzNpB.js
- Fullscreen sticky features logic: https://terminal-industries.com/_nuxt/BH53jP1Z.js
- Background canvas system: https://terminal-industries.com/_nuxt/CJZnftco.js
- Quote/parallax section behavior: https://terminal-industries.com/_nuxt/Bq_xl9qZ.js
- Core CSS / responsive asset switching: https://terminal-industries.com/_nuxt/entry.HNda-aXC.css
- Video sequence CSS: https://terminal-industries.com/_nuxt/get-frames.BEFbNTY1.css
- Background canvas CSS: https://terminal-industries.com/_nuxt/BackgroundCanvas.BfIfKjEO.css
