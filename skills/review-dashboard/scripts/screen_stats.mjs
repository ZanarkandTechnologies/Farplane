#!/usr/bin/env node
// What a dashboard's first screen shows, measured: words, controls, font sizes, colours and corner
// radii above the fold, plus graph node shapes. Feeds criteria D7 and D8 of references/rubric.md.
//
//   node scripts/screen_stats.mjs <url> [root-selector] [--size 1440x900] [--shot out.png] [--wait 3000]
//
// Needs Playwright: set PLAYWRIGHT_MODULE to a playwright or playwright-core entry file, or run where
// one of them resolves. Prints one JSON object.
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const flag = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args.splice(i, 2)[1] : fallback;
};
const size = flag('size', '1440x900');
const shot = flag('shot', null);
const wait = Number(flag('wait', '3000'));
const [url, root = 'body'] = args;
if (!url) {
  console.error('usage: screen_stats.mjs <url> [root-selector] [--size WxH] [--shot out.png] [--wait ms]');
  process.exit(2);
}

async function playwright() {
  if (process.env.PLAYWRIGHT_MODULE) return import(pathToFileURL(process.env.PLAYWRIGHT_MODULE).href);
  const require = createRequire(`${process.cwd()}/`);
  for (const name of ['playwright', 'playwright-core']) {
    try {
      return import(pathToFileURL(require.resolve(name)).href);
    } catch {}
  }
  throw new Error('Playwright not found: set PLAYWRIGHT_MODULE');
}

const { chromium } = await playwright();
const [width, height] = size.split('x').map(Number);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width, height } });
await page.goto(url, { waitUntil: 'networkidle' }).catch(() => {});
await page.waitForTimeout(wait);
if (shot) await page.screenshot({ path: shot });

const stats = await page.evaluate((sel) => {
  const scope = document.querySelector(sel) ?? document.body;
  const shown = [...scope.querySelectorAll('*')].filter((e) => {
    const r = e.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && r.top < innerHeight && r.bottom > 0 && getComputedStyle(e).visibility !== 'hidden';
  });
  const ownText = (e) => [...e.childNodes].filter((n) => n.nodeType === 3).map((n) => n.nodeValue.trim()).join(' ').trim();
  const texty = shown.filter((e) => ownText(e));
  const style = (e) => getComputedStyle(e);
  const count = (values) => Object.fromEntries(Object.entries(values.reduce((m, v) => ((m[v] = (m[v] ?? 0) + 1), m), {})).sort((a, b) => b[1] - a[1]));
  const words = texty.map(ownText).join(' ').split(/\s+/).filter(Boolean);
  const truncated = texty.filter((e) => /…|\.\.\.$/.test(ownText(e)) || (style(e).textOverflow === 'ellipsis' && e.scrollWidth > e.clientWidth));
  return {
    wordsAboveFold: words.length,
    controlsAboveFold: shown.filter((e) => e.matches('button, a[href], select, input, textarea, [role=button], [role=tab]')).length,
    fontSizes: count(texty.map((e) => style(e).fontSize)),
    fontFamilies: count(texty.map((e) => style(e).fontFamily.split(',')[0].replace(/["']/g, ''))),
    textColours: Object.keys(count(texty.map((e) => style(e).color))).length,
    cornerRadii: count(shown.map((e) => style(e).borderTopLeftRadius).filter((r) => r !== '0px')),
    isoDates: words.filter((w) => /^\d{4}-\d{2}-\d{2}T/.test(w)).length,
    truncatedLabels: truncated.map(ownText).slice(0, 20),
    graphNodes: { circles: scope.querySelectorAll('svg circle').length, rects: scope.querySelectorAll('svg rect').length, canvases: scope.querySelectorAll('canvas').length },
    headings: [...scope.querySelectorAll('h1, h2, h3, h4, [role=heading]')].map((e) => e.textContent.trim().slice(0, 60)).slice(0, 20),
  };
}, root);

await browser.close();
console.log(JSON.stringify({ url, root, size, ...stats }, null, 2));
