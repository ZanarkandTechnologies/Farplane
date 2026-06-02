#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");

let chromium;
let sharp;
let pixelmatch;
let PNG;

try {
  ({ chromium } = require("playwright"));
  sharp = require("sharp");
  pixelmatch = require("pixelmatch");
  pixelmatch = pixelmatch.default || pixelmatch;
  ({ PNG } = require("pngjs"));
} catch (error) {
  console.error(
    "Missing browser QA dependencies. Run with Codex bundled NODE_PATH or install playwright, sharp, pixelmatch, and pngjs.\n" +
      String(error && error.message ? error.message : error),
  );
  process.exit(2);
}

function parseArgs(argv) {
  const args = {
    url: "",
    out: "",
    width: 1440,
    height: 960,
    waitMs: 450,
    label: "scroll-scrub",
    reducedMotion: "no-preference",
  };
  for (let index = 2; index < argv.length; index += 1) {
    const arg = argv[index];
    const next = argv[index + 1];
    if (arg === "--url") {
      args.url = next;
      index += 1;
    } else if (arg === "--out") {
      args.out = next;
      index += 1;
    } else if (arg === "--width") {
      args.width = Number(next);
      index += 1;
    } else if (arg === "--height") {
      args.height = Number(next);
      index += 1;
    } else if (arg === "--wait-ms") {
      args.waitMs = Number(next);
      index += 1;
    } else if (arg === "--label") {
      args.label = next;
      index += 1;
    } else if (arg === "--reduced-motion") {
      args.reducedMotion = "reduce";
    } else {
      throw new Error(`unknown argument: ${arg}`);
    }
  }
  if (!args.url) {
    throw new Error("missing --url");
  }
  if (!args.out) {
    throw new Error("missing --out");
  }
  return args;
}

function normalizeUrl(rawUrl) {
  if (/^https?:\/\//.test(rawUrl) || rawUrl.startsWith("file://")) {
    return rawUrl;
  }
  const resolved = path.resolve(rawUrl);
  if (!fs.existsSync(resolved)) {
    throw new Error(`url path does not exist: ${rawUrl}`);
  }
  return pathToFileURL(resolved).href;
}

function candidateSignature(candidate) {
  return [candidate.tag, candidate.id, candidate.className].filter(Boolean).join("|");
}

function changedCandidates(samples) {
  const firstBySignature = new Map();
  let changed = 0;
  for (const sample of samples) {
    for (const candidate of sample.candidates) {
      const signature = candidateSignature(candidate);
      if (!signature) continue;
      const previous = firstBySignature.get(signature);
      if (!previous) {
        firstBySignature.set(signature, candidate);
        continue;
      }
      const bboxMoved =
        Math.abs(previous.bbox.top - candidate.bbox.top) > 8 ||
        Math.abs(previous.bbox.left - candidate.bbox.left) > 8 ||
        Math.abs(previous.bbox.width - candidate.bbox.width) > 8 ||
        Math.abs(previous.bbox.height - candidate.bbox.height) > 8;
      const styleChanged =
        previous.transform !== candidate.transform ||
        previous.opacity !== candidate.opacity ||
        previous.filter !== candidate.filter ||
        previous.clipPath !== candidate.clipPath;
      if (bboxMoved || styleChanged) {
        changed += 1;
        firstBySignature.delete(signature);
      }
    }
  }
  return changed;
}

function numericDebugProgress(debug) {
  if (!debug || typeof debug !== "object") return null;
  for (const key of ["progress", "scrollProgress", "scrubProgress"]) {
    const value = Number(debug[key]);
    if (Number.isFinite(value)) return value;
  }
  return null;
}

function debugFrame(debug) {
  if (!debug || typeof debug !== "object") return null;
  for (const key of ["frame", "frameIndex", "currentFrame", "mediaTime", "phase"]) {
    const value = debug[key];
    if (value !== undefined && value !== null) return String(value);
  }
  return null;
}

function hasRequiredDebugFields(debug) {
  if (!debug || typeof debug !== "object") return false;
  const progress = numericDebugProgress(debug);
  const hasFrameOrMedia =
    Number.isFinite(Number(debug.frame)) ||
    Number.isFinite(Number(debug.frameIndex)) ||
    Number.isFinite(Number(debug.currentFrame)) ||
    Number.isFinite(Number(debug.mediaTime));
  return (
    Number.isFinite(progress) &&
    typeof debug.phase === "string" &&
    debug.phase.length > 0 &&
    hasFrameOrMedia &&
    typeof debug.active === "boolean" &&
    typeof debug.ready === "boolean" &&
    typeof debug.reducedMotion === "boolean"
  );
}

function screenshotDeltaStats(diffs) {
  const ratios = diffs.map((diff) => Number(diff.changedRatio || 0));
  const maxCheckpointChangedRatio = ratios.length ? Math.max(...ratios) : 0;
  const meaningfulCheckpointDeltaCount = ratios.filter((ratio) => ratio >= 0.04).length;
  const strongCheckpointDeltaCount = ratios.filter((ratio) => ratio >= 0.15).length;
  const midScrollDeltaCount = ratios.slice(1, -1).filter((ratio) => ratio >= 0.04).length;
  return {
    maxCheckpointChangedRatio: Number(maxCheckpointChangedRatio.toFixed(5)),
    meaningfulCheckpointDeltaCount,
    strongCheckpointDeltaCount,
    midScrollDeltaCount,
  };
}

async function diffScreenshots(files) {
  const diffs = [];
  for (let index = 1; index < files.length; index += 1) {
    const previous = PNG.sync.read(await sharp(files[index - 1]).png().toBuffer());
    const current = PNG.sync.read(await sharp(files[index]).png().toBuffer());
    const width = Math.min(previous.width, current.width);
    const height = Math.min(previous.height, current.height);
    const previousSized = PNG.sync.read(
      await sharp(PNG.sync.write(previous)).resize(width, height).png().toBuffer(),
    );
    const currentSized = PNG.sync.read(
      await sharp(PNG.sync.write(current)).resize(width, height).png().toBuffer(),
    );
    const diff = new PNG({ width, height });
    const diffPixels = pixelmatch(
      previousSized.data,
      currentSized.data,
      diff.data,
      width,
      height,
      { threshold: 0.12 },
    );
    diffs.push({
      from: path.basename(files[index - 1]),
      to: path.basename(files[index]),
      changedPixels: diffPixels,
      totalPixels: width * height,
      changedRatio: Number((diffPixels / (width * height)).toFixed(5)),
    });
  }
  return diffs;
}

async function collectVisualGeometry(page) {
  return page.evaluate(() => {
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const viewportArea = Math.max(1, viewportWidth * viewportHeight);

    function visibleRect(rect) {
      const left = Math.max(0, rect.left);
      const top = Math.max(0, rect.top);
      const right = Math.min(viewportWidth, rect.right);
      const bottom = Math.min(viewportHeight, rect.bottom);
      if (right <= left || bottom <= top) return null;
      return { left, top, right, bottom, width: right - left, height: bottom - top };
    }

    function rectArea(rect) {
      return rect ? rect.width * rect.height : 0;
    }

    const mediaSelector = [
      "[data-hero-object]",
      "[data-scroll-scrub-root] video",
      "[data-scroll-scrub-root] img",
      "video",
      "picture",
      "img",
      ".hero-media",
      ".media",
      ".visual",
      ".scene",
    ].join(",");
    const textSelector = [
      "header",
      "nav",
      "h1",
      "h2",
      "p",
      "a",
      "button",
      "[role='navigation']",
      "[data-scroll-scrub-root]",
      ".hero",
      ".hero-media",
    ].join(",");

    const mediaRects = [...document.querySelectorAll(mediaSelector)]
      .map((element) => visibleRect(element.getBoundingClientRect()))
      .filter(Boolean);
    const heroObjectFillRatio = mediaRects.length
      ? Math.max(...mediaRects.map((rect) => rectArea(rect) / viewportArea))
      : 0;

    const intervals = [...document.querySelectorAll(textSelector)]
      .map((element) => {
        const style = getComputedStyle(element);
        if (style.visibility === "hidden" || style.display === "none" || Number(style.opacity) === 0) {
          return null;
        }
        const rect = visibleRect(element.getBoundingClientRect());
        if (!rect || rect.height < 4 || rect.width < 4) return null;
        return [rect.top, rect.bottom];
      })
      .filter(Boolean)
      .sort((a, b) => a[0] - b[0]);

    let cursor = 0;
    let largestGap = intervals.length ? Math.max(0, intervals[0][0]) : viewportHeight;
    for (const [top, bottom] of intervals) {
      largestGap = Math.max(largestGap, Math.max(0, top - cursor));
      cursor = Math.max(cursor, bottom);
    }
    largestGap = Math.max(largestGap, Math.max(0, viewportHeight - cursor));

    const navOverflow = [...document.querySelectorAll("header, nav, [role='navigation'], button, a")]
      .some((element) => {
        const rect = element.getBoundingClientRect();
        if (rect.bottom < 0 || rect.top > viewportHeight) return false;
        return rect.left < -2 || rect.right > viewportWidth + 2;
      });
    const hasMedia = mediaRects.length > 0;
    const firstViewportBlankRatio = largestGap / Math.max(1, viewportHeight);
    const mobileCropIntent =
      viewportWidth > 768
        ? "deliberate"
        : !hasMedia
          ? "missing"
          : !navOverflow && heroObjectFillRatio >= 0.35 && firstViewportBlankRatio <= 0.28
            ? "deliberate"
            : "accidental";

    return {
      dom_hero_object_fill_ratio: Number(heroObjectFillRatio.toFixed(4)),
      dom_first_viewport_blank_ratio: Number(firstViewportBlankRatio.toFixed(4)),
      nav_overflow: navOverflow,
      mobile_crop_intent: mobileCropIntent,
      sampled_media_rects: mediaRects.length,
    };
  });
}

async function collectImageGeometry(screenshotPath) {
  const { data, info } = await sharp(screenshotPath)
    .resize({ width: 180, withoutEnlargement: true })
    .ensureAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });
  const width = info.width;
  const height = info.height;
  const cornerSamples = [
    [0, 0],
    [width - 1, 0],
    [0, height - 1],
    [width - 1, height - 1],
  ];
  const background = [0, 0, 0];
  for (const [x, y] of cornerSamples) {
    const index = (y * width + x) * 4;
    background[0] += data[index];
    background[1] += data[index + 1];
    background[2] += data[index + 2];
  }
  background[0] /= cornerSamples.length;
  background[1] /= cornerSamples.length;
  background[2] /= cornerSamples.length;

  const rowForeground = Array.from({ length: height }, () => 0);
  let foregroundPixels = 0;
  let minX = width;
  let minY = height;
  let maxX = -1;
  let maxY = -1;
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const index = (y * width + x) * 4;
      const alpha = data[index + 3];
      const dr = data[index] - background[0];
      const dg = data[index + 1] - background[1];
      const db = data[index + 2] - background[2];
      const distance = Math.sqrt(dr * dr + dg * dg + db * db);
      if (alpha > 20 && distance > 42) {
        foregroundPixels += 1;
        rowForeground[y] += 1;
        minX = Math.min(minX, x);
        minY = Math.min(minY, y);
        maxX = Math.max(maxX, x);
        maxY = Math.max(maxY, y);
      }
    }
  }

  let largestSparseRun = 0;
  let currentSparseRun = 0;
  for (const count of rowForeground) {
    if (count / Math.max(1, width) < 0.015) {
      currentSparseRun += 1;
      largestSparseRun = Math.max(largestSparseRun, currentSparseRun);
    } else {
      currentSparseRun = 0;
    }
  }

  const boxArea =
    maxX >= minX && maxY >= minY
      ? ((maxX - minX + 1) * (maxY - minY + 1)) / Math.max(1, width * height)
      : 0;
  return {
    image_foreground_fill_ratio: Number((foregroundPixels / Math.max(1, width * height)).toFixed(4)),
    image_foreground_box_ratio: Number(boxArea.toFixed(4)),
    image_blank_ratio: Number((largestSparseRun / Math.max(1, height)).toFixed(4)),
  };
}

async function main() {
  const args = parseArgs(process.argv);
  const outDir = path.resolve(args.out);
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: args.width, height: args.height },
    deviceScaleFactor: 1,
    reducedMotion: args.reducedMotion,
  });
  const page = await context.newPage();
  const targetUrl = normalizeUrl(args.url);
  const consoleMessages = [];
  page.on("console", (message) => {
    consoleMessages.push({ type: message.type(), text: message.text() });
  });
  await page.goto(targetUrl, { waitUntil: "networkidle", timeout: 60000 });
  await page.waitForTimeout(args.waitMs);
  const domVisualGeometry = await collectVisualGeometry(page);

  const pageInfo = await page.evaluate(() => {
    const videoInfos = [...document.querySelectorAll("video")].map((video) => {
      const sources = [
        video.currentSrc || "",
        video.getAttribute("src") || "",
        ...[...video.querySelectorAll("source")].map((source) => source.getAttribute("src") || ""),
      ].filter(Boolean);
      return { sources: [...new Set(sources)] };
    });
    const videoSources = videoInfos.flatMap((video) => video.sources);
    const missionSupportVideoCount = videoInfos.filter((video) =>
      video.sources.some((source) => /mission-(?:01|03)|manifest|safety/i.test(source)),
    ).length;
    const heroTitle = document.querySelector(".hero__title, .hero-title, [data-hero-title], h1");
    const heroBreaks = heroTitle ? [...heroTitle.querySelectorAll("br")] : [];
    const heroTitleText = heroTitle ? String(heroTitle.textContent || "").trim() : "";
    const heroTitleGluedPhrases = /[a-z0-9][.!?][A-Z]/.test(heroTitleText);
    const heroVisibleBreakCount = heroBreaks.filter((br) => {
      const style = getComputedStyle(br);
      return style.display !== "none" && style.visibility !== "hidden";
    }).length;

    function visibleHeroCopyElement(element) {
      if (!element) return false;
      const style = getComputedStyle(element);
      if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity) <= 0.05) {
        return false;
      }
      const rect = element.getBoundingClientRect();
      const visibleWidth = Math.max(0, Math.min(window.innerWidth, rect.right) - Math.max(0, rect.left));
      const visibleHeight = Math.max(0, Math.min(window.innerHeight, rect.bottom) - Math.max(0, rect.top));
      const visibleArea = visibleWidth * visibleHeight;
      const text = String(element.textContent || "").replace(/\s+/g, " ").trim();
      return text.length >= 12 && visibleArea >= Math.min(2600, window.innerWidth * window.innerHeight * 0.01);
    }

    const heroOfferCandidates = [
      ".hero__title",
      ".hero__dek",
      ".hero-title",
      "[data-hero-title]",
      "[data-hero-offer]",
      "h1",
    ];
    const visibleHeroCopy = [...document.querySelectorAll(heroOfferCandidates.join(","))]
      .filter(visibleHeroCopyElement)
      .map((element) => String(element.textContent || "").replace(/\s+/g, " ").trim());
    const visibleHeroCopyText = visibleHeroCopy.join(" ");
    const titleVisible = visibleHeroCopyElement(heroTitle);
    const initialHeroOffer = {
      visible: (titleVisible && heroTitleText.length >= 12) || visibleHeroCopyText.length >= 32,
      titleVisible,
      textLength: visibleHeroCopyText.length,
      candidateCount: visibleHeroCopy.length,
      textSample: visibleHeroCopyText.slice(0, 180),
    };
    return {
      title: document.title,
      scrollHeight: document.documentElement.scrollHeight,
      viewportHeight: window.innerHeight,
      viewportWidth: window.innerWidth,
      hasGsap: Boolean(window.gsap),
      hasScrollTrigger: Boolean(window.ScrollTrigger || (window.gsap && window.gsap.core)),
      scriptSignals: [...document.scripts].map((script) =>
        script.src || `[inline script ${script.textContent.length} chars]`,
      ),
      pinSpacers: document.querySelectorAll(".pin-spacer").length,
      scrubRoots: document.querySelectorAll("[data-scroll-scrub-root], [data-scroll-scrub], [data-scroll-progress]").length,
      videoSources,
      videoElementCount: videoInfos.length,
      supportVideoCount: videoInfos.length,
      missionSupportVideoCount,
      heroTitle: {
        text: heroTitleText,
        breakCount: heroBreaks.length,
        visibleBreakCount: heroVisibleBreakCount,
        gluedPhrases: heroTitleGluedPhrases,
      },
      initialHeroOffer,
    };
  });

  const checkpoints = [0, 0.25, 0.5, 0.75, 0.95];
  const maxScroll = Math.max(0, pageInfo.scrollHeight - pageInfo.viewportHeight);
  const samples = [];
  const screenshotFiles = [];

  for (const progress of checkpoints) {
    const y = Math.round(maxScroll * progress);
    await page.evaluate((scrollY) => window.scrollTo(0, scrollY), y);
    await page.waitForTimeout(args.waitMs);
    const screenshotPath = path.join(outDir, `${args.label}-${String(Math.round(progress * 100)).padStart(3, "0")}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: false });
    screenshotFiles.push(screenshotPath);
    const sample = await page.evaluate((currentProgress) => {
      const selector = [
        "[data-scroll-scrub-root]",
        "[data-scroll-scrub]",
        "[data-scroll-progress]",
        "[data-scroll-phase]",
        "canvas",
        "video",
        ".pin-spacer",
        ".scroll-stage",
        ".scrub-stage",
        ".frame-sequence",
        ".hero-media",
        ".hero",
        ".cinematic",
        ".scene",
      ].join(",");
      const candidates = [...document.querySelectorAll(selector)].slice(0, 40).map((element) => {
        const style = getComputedStyle(element);
        const bbox = element.getBoundingClientRect();
        return {
          tag: element.tagName.toLowerCase(),
          id: element.id || "",
          className: String(element.className || ""),
          dataset: { ...element.dataset },
          position: style.position,
          transform: style.transform,
          opacity: style.opacity,
          filter: style.filter,
          clipPath: style.clipPath,
          bbox: {
            top: Math.round(bbox.top),
            left: Math.round(bbox.left),
            width: Math.round(bbox.width),
            height: Math.round(bbox.height),
          },
        };
      });
      const videos = [...document.querySelectorAll("video")].map((video) => ({
        currentTime: Number(video.currentTime.toFixed(3)),
        duration: Number.isFinite(video.duration) ? Number(video.duration.toFixed(3)) : null,
        readyState: video.readyState,
        paused: video.paused,
      }));
      return {
        checkpoint: currentProgress,
        scrollY: Math.round(window.scrollY),
        debug: window.__scrollScrubDebug ? JSON.parse(JSON.stringify(window.__scrollScrubDebug)) : null,
        candidates,
        videos,
      };
    }, progress);
    samples.push(sample);
  }

  const screenshotDiffs = await diffScreenshots(screenshotFiles);
  const deltaStats = screenshotDeltaStats(screenshotDiffs);
  const imageVisualGeometry = await collectImageGeometry(screenshotFiles[0]);
  const visualGeometry = {
    ...domVisualGeometry,
    ...imageVisualGeometry,
    hero_object_fill_ratio: Number(
      Math.max(domVisualGeometry.dom_hero_object_fill_ratio, imageVisualGeometry.image_foreground_box_ratio).toFixed(4),
    ),
    first_viewport_blank_ratio: Number(
      Math.max(domVisualGeometry.dom_first_viewport_blank_ratio, imageVisualGeometry.image_blank_ratio).toFixed(4),
    ),
  };
  const debugValues = samples.map((sample) => numericDebugProgress(sample.debug)).filter((value) => value !== null);
  const debugFrames = samples.map((sample) => debugFrame(sample.debug)).filter((value) => value !== null);
  const validDebugSamples = samples.filter((sample) => hasRequiredDebugFields(sample.debug));
  const debugProgressSpan =
    debugValues.length > 1 ? Math.max(...debugValues) - Math.min(...debugValues) : 0;
  const videoTimes = samples.flatMap((sample) => sample.videos.map((video) => video.currentTime));
  const videoTimeSpan = videoTimes.length > 1 ? Math.max(...videoTimes) - Math.min(...videoTimes) : 0;
  const candidateChangeCount = changedCandidates(samples);
  const hasPinnedSurface =
    pageInfo.pinSpacers > 0 ||
    samples.some((sample) =>
      sample.candidates.some((candidate) => candidate.position === "sticky" || candidate.position === "fixed"),
    );
  const hasRequiredDebugContract = validDebugSamples.length >= 2;
  const hasDebugInstrumentation = hasRequiredDebugContract;
  const hasDebugScrub = hasRequiredDebugContract && (debugProgressSpan > 0.35 || new Set(debugFrames).size >= 3);
  const hasMediaScrub = videoTimeSpan > 0.35;
  const hasStyleScrub = candidateChangeCount >= 2;
  const hasSupportVideoDom = pageInfo.supportVideoCount > 0;
  const hasMissionSupportVideos = pageInfo.missionSupportVideoCount >= 2;
  const hasMobileHeroPhraseSeparation =
    pageInfo.viewportWidth > 768 ||
    !pageInfo.heroTitle.gluedPhrases ||
    pageInfo.heroTitle.visibleBreakCount > 0;
  const hasLargeScroll = maxScroll >= pageInfo.viewportHeight * 2;
  const hasRequiredDebugForScrubRoot = pageInfo.scrubRoots === 0 || hasRequiredDebugContract;
  const isReducedMotionRun = args.reducedMotion === "reduce";
  const hasDominantHeroMedia =
    visualGeometry.sampled_media_rects > 0 &&
    visualGeometry.hero_object_fill_ratio >= 0.55 &&
    visualGeometry.first_viewport_blank_ratio <= 0.18;
  const hasInitialHeroOfferVisible = Boolean(pageInfo.initialHeroOffer && pageInfo.initialHeroOffer.visible);
  const hasDistributedScrubDeltas =
    deltaStats.maxCheckpointChangedRatio >= 0.15 &&
    deltaStats.meaningfulCheckpointDeltaCount >= 2 &&
    (deltaStats.midScrollDeltaCount >= 1 || deltaStats.strongCheckpointDeltaCount >= 2);
  const hasTerminalMediaPipeline = hasMediaScrub && hasSupportVideoDom && hasMissionSupportVideos;
  const likelyScrollScrub =
    hasLargeScroll &&
    hasRequiredDebugForScrubRoot &&
    (hasDebugScrub ||
      hasMediaScrub ||
      (isReducedMotionRun && hasRequiredDebugContract && hasPinnedSurface) ||
      (pageInfo.scrubRoots === 0 && hasPinnedSurface && hasStyleScrub && (pageInfo.hasGsap || pageInfo.hasScrollTrigger)));
  const terminalFinalReady =
    likelyScrollScrub &&
    hasRequiredDebugContract &&
    hasPinnedSurface &&
    hasStyleScrub &&
    hasTerminalMediaPipeline &&
    hasDominantHeroMedia &&
    hasInitialHeroOfferVisible &&
    hasDistributedScrubDeltas &&
    hasMobileHeroPhraseSeparation;

  const result = {
    url: targetUrl,
    outDir,
    viewport: { width: args.width, height: args.height },
    pageInfo,
    verdict: likelyScrollScrub ? "PASS" : "FAIL",
    terminalVerdict: terminalFinalReady ? "PASS" : "FAIL",
    score: {
      hasLargeScroll,
      hasDebugInstrumentation,
      hasRequiredDebugContract,
      hasDebugScrub,
      hasMediaScrub,
      hasStyleScrub,
      hasSupportVideoDom,
      hasMissionSupportVideos,
      hasMobileHeroPhraseSeparation,
      hasDominantHeroMedia,
      hasInitialHeroOfferVisible,
      hasDistributedScrubDeltas,
      hasTerminalMediaPipeline,
      terminalFinalReady,
      hasPinnedSurface,
      hasGsapOrScrollTrigger: pageInfo.hasGsap || pageInfo.hasScrollTrigger,
      candidateChangeCount,
      supportVideoCount: pageInfo.supportVideoCount,
      missionSupportVideoCount: pageInfo.missionSupportVideoCount,
      debugProgressSpan: Number(debugProgressSpan.toFixed(3)),
      videoTimeSpan: Number(videoTimeSpan.toFixed(3)),
      ...deltaStats,
    },
    checkpoints: samples,
    visualGeometry,
    screenshotFiles,
    screenshotDiffs,
    consoleMessages,
    terminalFailureHints: terminalFinalReady
      ? []
      : [
          "Terminal-level pages need generated/rendered media or a frame/video asset pipeline, not just code-native canvas or HUD overlays.",
          "Require a dominant first-viewport media/object surface and low blank-band geometry.",
          "Require visible first-viewport offer copy so the visitor understands the product before scrolling.",
          "Require distributed checkpoint screenshot deltas so scroll changes the main visual across the narrative, not only at one transition.",
          "Require support-video or section media proof when the recipe calls for mission cards or feature sections.",
        ],
    failureHints: likelyScrollScrub
      ? []
      : [
          "Expose window.__scrollScrubDebug with progress, phase, frame/mediaTime, active, ready, and reducedMotion.",
          "Mark the pinned/scrubbed section with data-scroll-scrub-root.",
          "Use GSAP ScrollTrigger or an explicit scroll-to-frame/media-time mapper for the hero scene.",
          "Verify checkpoint screenshots at 0, 25, 50, 75, and 95 percent show intended narrative phases.",
        ],
  };

  const resultPath = path.join(outDir, "scroll-scrub-qa.json");
  fs.writeFileSync(resultPath, `${JSON.stringify(result, null, 2)}\n`, "utf-8");
  console.log(JSON.stringify({ verdict: result.verdict, terminalVerdict: result.terminalVerdict, resultPath, score: result.score }, null, 2));
  await browser.close();
}

main().catch(async (error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
