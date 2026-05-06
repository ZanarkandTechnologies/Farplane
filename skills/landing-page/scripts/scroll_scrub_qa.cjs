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

  const pageInfo = await page.evaluate(() => ({
    title: document.title,
    scrollHeight: document.documentElement.scrollHeight,
    viewportHeight: window.innerHeight,
    viewportWidth: window.innerWidth,
    hasGsap: Boolean(window.gsap),
    hasScrollTrigger: Boolean(window.ScrollTrigger || (window.gsap && window.gsap.core)),
    scriptSignals: [...document.scripts].map((script) => script.src || script.textContent.slice(0, 240)),
    pinSpacers: document.querySelectorAll(".pin-spacer").length,
    scrubRoots: document.querySelectorAll("[data-scroll-scrub-root], [data-scroll-scrub], [data-scroll-progress]").length,
  }));

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
  const debugValues = samples.map((sample) => numericDebugProgress(sample.debug)).filter((value) => value !== null);
  const debugFrames = samples.map((sample) => debugFrame(sample.debug)).filter((value) => value !== null);
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
  const hasDebugInstrumentation = debugValues.length >= 2 || new Set(debugFrames).size >= 2;
  const hasDebugScrub = debugProgressSpan > 0.35 || new Set(debugFrames).size >= 3;
  const hasMediaScrub = videoTimeSpan > 0.35;
  const hasStyleScrub = candidateChangeCount >= 2;
  const hasLargeScroll = maxScroll >= pageInfo.viewportHeight * 2;
  const likelyScrollScrub =
    hasLargeScroll &&
    (hasDebugScrub || hasMediaScrub || (hasPinnedSurface && hasStyleScrub && (pageInfo.hasGsap || pageInfo.hasScrollTrigger)));

  const result = {
    url: targetUrl,
    outDir,
    viewport: { width: args.width, height: args.height },
    pageInfo,
    verdict: likelyScrollScrub ? "PASS" : "FAIL",
    score: {
      hasLargeScroll,
      hasDebugInstrumentation,
      hasDebugScrub,
      hasMediaScrub,
      hasStyleScrub,
      hasPinnedSurface,
      hasGsapOrScrollTrigger: pageInfo.hasGsap || pageInfo.hasScrollTrigger,
      candidateChangeCount,
      debugProgressSpan: Number(debugProgressSpan.toFixed(3)),
      videoTimeSpan: Number(videoTimeSpan.toFixed(3)),
    },
    checkpoints: samples,
    screenshotFiles,
    screenshotDiffs,
    consoleMessages,
    failureHints: likelyScrollScrub
      ? []
      : [
          "Expose window.__scrollScrubDebug with progress, phase, frame/mediaTime, active, and reducedMotion.",
          "Mark the pinned/scrubbed section with data-scroll-scrub-root.",
          "Use GSAP ScrollTrigger or an explicit scroll-to-frame/media-time mapper for the hero scene.",
          "Verify checkpoint screenshots at 0, 25, 50, 75, and 95 percent show intended narrative phases.",
        ],
  };

  const resultPath = path.join(outDir, "scroll-scrub-qa.json");
  fs.writeFileSync(resultPath, `${JSON.stringify(result, null, 2)}\n`, "utf-8");
  console.log(JSON.stringify({ verdict: result.verdict, resultPath, score: result.score }, null, 2));
  await browser.close();
}

main().catch(async (error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
