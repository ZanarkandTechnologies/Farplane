#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");

let chromium;
let PNG;

try {
  ({ chromium } = require("playwright"));
  ({ PNG } = require("pngjs"));
} catch (error) {
  console.error(
    "Missing browser QA dependencies. Run with Codex bundled NODE_PATH or install playwright and pngjs.\n" +
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
    waitMs: 700,
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
    } else {
      throw new Error(`unknown argument: ${arg}`);
    }
  }
  if (!args.url) throw new Error("missing --url");
  if (!args.out) throw new Error("missing --out");
  return args;
}

function normalizeUrl(rawUrl) {
  if (/^https?:\/\//.test(rawUrl) || rawUrl.startsWith("file://")) {
    return rawUrl;
  }
  const resolved = path.resolve(rawUrl);
  if (!fs.existsSync(resolved)) throw new Error(`url path does not exist: ${rawUrl}`);
  return pathToFileURL(resolved).href;
}

function slug(value) {
  return String(value || "section")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 80);
}

function analyzePng(buffer) {
  const png = PNG.sync.read(buffer);
  const buckets = new Set();
  let nonDark = 0;
  let accent = 0;
  let alphaPixels = 0;
  let sum = 0;
  let sumSq = 0;
  let minLuma = 255;
  let maxLuma = 0;
  const total = png.width * png.height;

  for (let offset = 0; offset < png.data.length; offset += 4) {
    const r = png.data[offset];
    const g = png.data[offset + 1];
    const b = png.data[offset + 2];
    const a = png.data[offset + 3];
    if (a < 16) continue;
    alphaPixels += 1;
    const luma = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    sum += luma;
    sumSq += luma * luma;
    minLuma = Math.min(minLuma, luma);
    maxLuma = Math.max(maxLuma, luma);
    if (luma > 36) nonDark += 1;
    if (g > r * 1.25 && g > b * 1.25 && g > 80) accent += 1;
    buckets.add(`${r >> 4}:${g >> 4}:${b >> 4}`);
  }

  const mean = alphaPixels ? sum / alphaPixels : 0;
  const variance = alphaPixels ? sumSq / alphaPixels - mean * mean : 0;
  return {
    width: png.width,
    height: png.height,
    alphaRatio: alphaPixels / Math.max(1, total),
    nonDarkRatio: nonDark / Math.max(1, alphaPixels),
    accentRatio: accent / Math.max(1, alphaPixels),
    uniqueColorBuckets: buckets.size,
    lumaMean: Number(mean.toFixed(2)),
    lumaStdDev: Number(Math.sqrt(Math.max(0, variance)).toFixed(2)),
    lumaRange: Number((maxLuma - minLuma).toFixed(2)),
  };
}

function visualRichnessScore(metrics) {
  let score = 0;
  if (metrics.uniqueColorBuckets >= 18) score += 2;
  else if (metrics.uniqueColorBuckets >= 10) score += 1;
  if (metrics.nonDarkRatio >= 0.08) score += 2;
  else if (metrics.nonDarkRatio >= 0.025) score += 1;
  if (metrics.lumaStdDev >= 18) score += 2;
  else if (metrics.lumaStdDev >= 8) score += 1;
  if (metrics.lumaRange >= 80) score += 2;
  else if (metrics.lumaRange >= 35) score += 1;
  if (metrics.accentRatio >= 0.002) score += 1;
  return score;
}

function classifySection(section) {
  const key = `${section.id} ${section.className} ${section.label} ${section.heading}`.toLowerCase();
  const className = String(section.className || "").toLowerCase();
  const label = String(section.label || "").toLowerCase();
  if (key.includes("hero")) return "hero";
  if (key.includes("problem") || key.includes("rupture")) return "problem";
  if (className.includes("command") || label.includes("platform")) return "solution";
  if (className.includes("mission") || label.includes("capabilities")) return "capabilities";
  if (key.includes("platform") || key.includes("command")) return "solution";
  if (key.includes("capabilities") || key.includes("mission")) return "capabilities";
  if (key.includes("proof")) return "proof";
  if (key.includes("contact") || key.includes("cta")) return "cta";
  return "section";
}

function expectedFor(kind) {
  if (kind === "hero") return { minTextChars: 30, minHeadingCount: 1, minRichVisuals: 1 };
  if (kind === "proof") return { minTextChars: 90, minHeadingCount: 1, minRichVisuals: 0 };
  return { minTextChars: 80, minHeadingCount: 1, minRichVisuals: 1 };
}

async function main() {
  const args = parseArgs(process.argv);
  const outDir = path.resolve(args.out);
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: args.width, height: args.height },
    deviceScaleFactor: 1,
  });
  const consoleMessages = [];
  const pageErrors = [];
  page.on("console", (msg) => {
    consoleMessages.push({ type: msg.type(), text: msg.text() });
  });
  page.on("pageerror", (error) => {
    pageErrors.push({ message: error.message, stack: error.stack || "" });
  });

  await page.goto(normalizeUrl(args.url), { waitUntil: "load" });
  await page.waitForTimeout(args.waitMs);

  const sections = await page.evaluate(() => {
    return Array.from(document.querySelectorAll("section")).map((section, index) => {
      const rect = section.getBoundingClientRect();
      const heading = section.querySelector("h1,h2,h3")?.textContent?.trim() || "";
      const label = section.querySelector(".label,.mission__num,.hero__label")?.textContent?.trim() || "";
      const text = section.innerText || "";
      const media = Array.from(section.querySelectorAll("canvas,video,img,svg")).map((element, mediaIndex) => {
        const mediaRect = element.getBoundingClientRect();
        const style = getComputedStyle(element);
        return {
          index: mediaIndex,
          tag: element.tagName.toLowerCase(),
          id: element.id || "",
          className: element.className && String(element.className.baseVal || element.className) || "",
          width: mediaRect.width,
          height: mediaRect.height,
          area: mediaRect.width * mediaRect.height,
          opacity: Number(style.opacity || "1"),
          display: style.display,
          visibility: style.visibility,
        };
      });
      return {
        index,
        id: section.id || "",
        className: section.className && String(section.className.baseVal || section.className) || "",
        label,
        heading,
        textChars: text.replace(/\s+/g, " ").trim().length,
        rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
        media,
        linkCount: section.querySelectorAll("a,button").length,
      };
    });
  });

  const visualBlocks = await page.evaluate(() => {
    const selectors = [
      ".rupture__canvas-wrap",
      ".command__svg-wrap",
      ".mission__visual",
      ".cta__stage",
      "[data-visual-carrier]",
    ].join(",");
    return Array.from(document.querySelectorAll(selectors)).map((element, index) => {
      const rect = element.getBoundingClientRect();
      const section = element.closest("section");
      const heading = section?.querySelector("h1,h2,h3")?.textContent?.trim() || "";
      return {
        index,
        selector: element.className && String(element.className.baseVal || element.className) || element.id || element.tagName.toLowerCase(),
        sectionIndex: section ? Array.from(document.querySelectorAll("section")).indexOf(section) : -1,
        heading,
        mediaCount: element.querySelectorAll("canvas,video,img,svg").length,
        rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
      };
    });
  });

  const findings = [];
  const sectionResults = [];
  for (const section of sections) {
    const kind = classifySection(section);
    const expected = expectedFor(kind);
    const visualMetrics = [];
    const locators = await page.locator(`section`).nth(section.index).locator("canvas,video,img,svg").elementHandles();
    for (let mediaIndex = 0; mediaIndex < locators.length; mediaIndex += 1) {
      const media = section.media[mediaIndex];
      if (!media || media.area < 4000 || media.opacity < 0.05 || media.display === "none" || media.visibility === "hidden") {
        continue;
      }
      const fileName = `${String(section.index).padStart(2, "0")}-${kind}-${slug(media.id || media.className || media.tag)}-${mediaIndex}.png`;
      const screenshotPath = path.join(outDir, fileName);
      const buffer = await locators[mediaIndex].screenshot({ path: screenshotPath });
      const metrics = analyzePng(buffer);
      const richness = visualRichnessScore(metrics);
      visualMetrics.push({ ...media, screenshotPath, metrics, richness });
    }

    const richVisuals = visualMetrics.filter((item) => item.richness >= 4).length;
    const issues = [];
    if (section.textChars < expected.minTextChars) {
      issues.push(`thin section copy (${section.textChars} chars < ${expected.minTextChars})`);
    }
    if (!section.heading || expected.minHeadingCount > 0 && !section.heading) {
      issues.push("missing visible heading");
    }
    if (richVisuals < expected.minRichVisuals) {
      issues.push(`missing rich visual carrier (${richVisuals} < ${expected.minRichVisuals})`);
    }
    if (kind === "proof") {
      const text = `${section.heading} ${section.label}`.toLowerCase();
      void text;
    }

    const pass = issues.length === 0;
    if (!pass) {
      findings.push({
        section: section.index,
        kind,
        heading: section.heading,
        issues,
      });
    }
    sectionResults.push({
      ...section,
      kind,
      expected,
      richVisuals,
      visualMetrics,
      pass,
      issues,
    });
  }

  const visualBlockResults = [];
  const richBlockSections = new Map();
  const blockLocators = await page.locator(
    ".rupture__canvas-wrap,.command__svg-wrap,.mission__visual,.cta__stage,[data-visual-carrier]",
  ).elementHandles();
  for (let index = 0; index < blockLocators.length; index += 1) {
    const block = visualBlocks[index];
    if (!block || block.rect.width * block.rect.height < 6000) continue;
    await blockLocators[index].scrollIntoViewIfNeeded();
    await page.waitForTimeout(Math.min(500, Math.max(120, args.waitMs / 2)));
    const fileName = `visual-block-${String(index).padStart(2, "0")}-${slug(block.selector)}.png`;
    const screenshotPath = path.join(outDir, fileName);
    const buffer = await blockLocators[index].screenshot({ path: screenshotPath });
    const metrics = analyzePng(buffer);
    const richness = visualRichnessScore(metrics);
    const pass = richness >= 4;
    const result = { ...block, screenshotPath, metrics, richness, pass };
    visualBlockResults.push(result);
    if (pass && Number.isInteger(block.sectionIndex)) {
      richBlockSections.set(block.sectionIndex, (richBlockSections.get(block.sectionIndex) || 0) + 1);
    }
    if (!pass) {
      findings.push({
        section: block.sectionIndex,
        kind: "visual-block",
        heading: block.heading || block.selector,
        issues: [`blank or under-rendered visual block (${block.selector}, richness ${richness} < 4)`],
      });
    }
  }

  for (const section of sectionResults) {
    if (section.expected.minRichVisuals > 0 && section.richVisuals < section.expected.minRichVisuals) {
      const richBlocks = richBlockSections.get(section.index) || 0;
      if (richBlocks >= section.expected.minRichVisuals) {
        section.pass = section.issues.length === 1 && section.issues[0].startsWith("missing rich visual carrier")
          ? true
          : section.pass;
        section.richVisualBlocks = richBlocks;
        section.issues = section.issues.filter((issue) => !issue.startsWith("missing rich visual carrier"));
      }
    }
  }
  for (let index = findings.length - 1; index >= 0; index -= 1) {
    const finding = findings[index];
    if (
      Number.isInteger(finding.section) &&
      (richBlockSections.get(finding.section) || 0) > 0 &&
      finding.issues.every((issue) => issue.startsWith("missing rich visual carrier"))
    ) {
      findings.splice(index, 1);
    }
  }

  const proofSection = page.locator(".section--proof,#proof").first();
  if (await proofSection.count()) {
    await proofSection.scrollIntoViewIfNeeded();
    await page.waitForTimeout(args.waitMs);
  }
  const proofPlaceholders = await page.evaluate(() => {
    return Array.from(document.querySelectorAll(".metric__num,.proof__metric .metric__num"))
      .map((element) => element.textContent.trim())
      .filter((text) => /^0(?:M\+|×|%|$)/.test(text));
  });
  if (proofPlaceholders.length) {
    findings.push({
      section: "proof",
      kind: "proof",
      heading: "proof metrics",
      issues: [`placeholder proof metrics visible: ${proofPlaceholders.join(", ")}`],
    });
  }

  for (const error of pageErrors) {
    findings.push({
      section: "runtime",
      kind: "runtime",
      heading: "page error",
      issues: [error.message],
    });
  }

  const importantKinds = new Set(["hero", "problem", "solution", "capabilities", "proof", "cta"]);
  const presentKinds = new Set(sectionResults.map((section) => section.kind));
  for (const kind of importantKinds) {
    if (!presentKinds.has(kind)) {
      findings.push({
        section: "document",
        kind,
        heading: kind,
        issues: ["missing expected narrative section"],
      });
    }
  }

  const passedSections = sectionResults.filter((section) => section.pass).length;
  const sectionScore = sectionResults.length ? passedSections / sectionResults.length : 0;
  const visualScore = sectionResults.length
    ? (
        sectionResults.filter((section) => section.richVisuals >= section.expected.minRichVisuals).length +
        visualBlockResults.filter((block) => block.pass).length
      ) / (sectionResults.length + Math.max(1, visualBlockResults.length))
    : 0;
  const runtimeScore = pageErrors.length === 0 ? 1 : 0;
  const proofScore = proofPlaceholders.length === 0 ? 1 : 0;
  const percentScore = Math.round((sectionScore * 45 + visualScore * 35 + runtimeScore * 10 + proofScore * 10) * 100) / 100;

  const result = {
    verdict: findings.length === 0 ? "PASS" : "FAIL",
    threshold: 85,
    percentScore,
    scores: {
      sectionScore: Number((sectionScore * 100).toFixed(2)),
      visualCarrierScore: Number((visualScore * 100).toFixed(2)),
      runtimeScore: Number((runtimeScore * 100).toFixed(2)),
      proofCredibilityScore: Number((proofScore * 100).toFixed(2)),
    },
    sections: sectionResults,
    visualBlocks: visualBlockResults,
    consoleMessages,
    pageErrors,
    proofPlaceholders,
    findings,
  };

  const resultPath = path.join(outDir, "section-quality-qa.json");
  fs.writeFileSync(resultPath, JSON.stringify(result, null, 2));
  await browser.close();
  console.log(JSON.stringify({ verdict: result.verdict, percentScore, resultPath, findings }, null, 2));
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
