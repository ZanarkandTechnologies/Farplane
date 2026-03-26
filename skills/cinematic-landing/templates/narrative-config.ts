/**
 * NARRATIVE CONFIGURATION TEMPLATE
 * ================================
 * 
 * This template provides the core configuration for a cinematic scroll landing page.
 * Copy and customize for your project.
 * 
 * @usage
 * 1. Define your NARRATIVE timeline (scroll phases)
 * 2. Configure LAYERS for background transitions
 * 3. Set TOTAL_VH for total scroll length
 * 4. Customize CONTENT with your copy
 */

// ============================================================================
// NARRATIVE TIMELINE
// ============================================================================
// Each section follows a [START, PEAK, END] lifecycle:
// - START: Content begins to fade in
// - PEAK: Content is at 100% opacity
// - END: Content is completely faded out
//
// ⚠️ IMPORTANT: To prevent "blank" gaps, ensure the START of each section
// is equal to or less than the END of the previous section.
// ============================================================================

export const NARRATIVE = {
    // Phase 0: Hero / Opening Scene
    VISION: { START: 0.0, PEAK: 0.00, END: 0.025 },

    // Phase 1: Problem Statement
    PROBLEM: { START: 0.025, PEAK: 0.075, END: 0.22 },

    // Phase 2: Solution Part 1
    SOLUTION_1: { START: 0.22, PEAK: 0.28, END: 0.35 },

    // Phase 3: Solution Part 2
    SOLUTION_2: { START: 0.35, PEAK: 0.41, END: 0.50 },

    // Phase 4: Proof / Features
    PROOF: { START: 0.50, PEAK: 0.57, END: 0.65 },

    // Phase 5: Social Proof / Testimonials
    TESTIMONIALS: { START: 0.65, PEAK: 0.70, END: 0.75 },

    // Phase 6: Pricing (optional)
    PRICING: { START: 0.75, PEAK: 0.80, END: 0.85 },

    // Phase 7: Final CTA (stays visible at end)
    CTA: { START: 0.85, PEAK: 0.90, END: 1.0 }
} as const;

// ============================================================================
// LAYER BOUNDARIES
// ============================================================================
// Define when each visual background layer should be active.
// Used for z-index management and video playback control.
// ============================================================================

export const LAYERS = {
    // Hero layer (image/component) fades out at:
    HERO: NARRATIVE.VISION.END,

    // First scrub video plays until:
    VIDEO_1: NARRATIVE.PROBLEM.END,

    // Second scrub video plays until:
    VIDEO_2: NARRATIVE.SOLUTION_2.END,

    // WebGL / special effect layer until:
    WEBGL: NARRATIVE.PROOF.END,

    // Final background starts at:
    FINAL_BG_START: NARRATIVE.PROOF.END,
} as const;

// ============================================================================
// PAGE CONFIGURATION
// ============================================================================

export const PAGE_CONFIG = {
    // Total scroll height in vh units
    // Higher = slower scroll, more "breathing room" between sections
    TOTAL_VH: 2600,

    // Maximum content width
    MAX_WIDTH: '1920px',

    // Base z-index for content overlays
    CONTENT_Z_INDEX: 100,

    // Navbar z-index
    NAVBAR_Z_INDEX: 200,
} as const;

// ============================================================================
// CONTENT CONFIGURATION
// ============================================================================
// Centralized text content for easy editing.
// Edit these values to refine brand voice and messaging.
// ============================================================================

export const CONTENT = {
    // Scene 1: The Vision / Hero
    VISION: {
        TITLE_PREFIX: "Your",
        TITLE_ACCENT: "Headline.",
        SUBTITLE_1: "First subtitle line.",
        SUBTITLE_2: "Second subtitle line with more detail.",
        SCROLL_LABEL: "Scroll to explore"
    },

    // Scene 2: The Problem
    PROBLEM: {
        TITLE: "The Problem",
        QUOTE: "A powerful quote that resonates with your audience.",
        STATUS: "[ SYSTEM STATUS: OPAQUE ]",
        DESCRIPTION: "Expanded description of the problem your audience faces. Make it specific and relatable."
    },

    // Scene 3: The Solution (Part 1)
    SOLUTION_1: {
        TITLE_PREFIX: "Your",
        TITLE_ACCENT: "Solution.",
        CARDS: [
            { title: "Feature One", icon: "Terminal", text: "Description of feature one." },
            { title: "Feature Two", icon: "Activity", text: "Description of feature two." },
            { title: "Feature Three", icon: "Eye", text: "Description of feature three." },
        ]
    },

    // Scene 4: The Solution (Part 2 / Methodology)
    SOLUTION_2: {
        OVERHEAD: "Our Method",
        TITLE_PREFIX: "How We",
        TITLE_ACCENT: "Deliver.",
        DESCRIPTION: "Explanation of your methodology or approach.",
        FEATURES: [
            { icon: "Layers", text: "STEP ONE", sub: "Description of step one." },
            { icon: "Shield", text: "STEP TWO", sub: "Description of step two." },
            { icon: "Terminal", text: "STEP THREE", sub: "Description of step three." },
        ]
    },

    // Scene 5: The Proof
    PROOF: {
        TITLE_PREFIX: "Rigorous",
        TITLE_ACCENT: "Results.",
        SUBTITLE: "[ ESTABLISHING GROUND TRUTH ]",
        CARDS: [
            { name: "Metric One", icon: "Activity", desc: "Description of metric.", stats: "42ms AVG" },
            { name: "Metric Two", icon: "TrendingDown", desc: "Description.", stats: "99.2% UPTIME" },
            { name: "Metric Three", icon: "ShieldCheck", desc: "Description.", stats: "PASSED" },
        ]
    },

    // Scene 6: Social Proof / Case Studies
    TESTIMONIALS: {
        OVERHEAD: "// Track Record",
        TITLE_PREFIX: "Proven",
        TITLE_ACCENT: "Results.",
        ITEMS: [
            { project: "Project 01", text: "Description of project outcome.", highlight: true },
            { project: "Project 02", text: "Description of project outcome.", highlight: false },
            { project: "Project 03", text: "Description of project outcome.", highlight: false },
        ]
    },

    // Scene 7: Pricing (optional)
    PRICING: {
        TITLE_PREFIX: "Investment",
        TITLE_ACCENT: "Options.",
        SUBTITLE: "[ CHOOSE YOUR PATH ]",
        PLANS: [
            {
                name: "STARTER",
                price: "$X",
                icon: "Zap",
                features: ["Feature 1", "Feature 2"],
                desc: "For individuals."
            },
            {
                name: "PRO",
                price: "$XX",
                icon: "Database",
                features: ["All Starter", "Feature 3", "Feature 4"],
                desc: "For teams.",
                popular: true
            },
            {
                name: "ENTERPRISE",
                price: "Custom",
                icon: "Globe",
                features: ["All Pro", "Feature 5", "Feature 6"],
                desc: "For organizations."
            },
        ]
    },

    // Scene 8: Final CTA
    CTA: {
        TITLE_PREFIX: "Ready to",
        TITLE_ACCENT: "Start?",
        TITLE_SUFFIX: "",
        SUBTITLE: "Clear value proposition recap.",
        BUTTON: "[ GET STARTED ]",
        BUTTON_HREF: "/contact"
    }
} as const;

// ============================================================================
// ASSET CONFIGURATION
// ============================================================================
// Define assets for preloading and reference.
// ============================================================================

export const ASSETS = {
    critical: {
        images: [
            "/assets/hero.jpeg",
            "/assets/background.png",
        ],
        videos: [
            "/assets/scrub_video_1.mp4",
        ],
    },
    background: {
        images: [
            "/assets/secondary.jpeg",
        ],
        videos: [
            "/assets/scrub_video_2.mp4",
            "/assets/loop_video.mp4",
        ],
    }
} as const;

// ============================================================================
// TYPE EXPORTS
// ============================================================================

export type NarrativePhase = keyof typeof NARRATIVE;
export type LayerKey = keyof typeof LAYERS;
export type ContentSection = keyof typeof CONTENT;

