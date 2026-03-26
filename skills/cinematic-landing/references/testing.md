# Testing: Playwright Scroll Testing Workflow

> **When to use**: QA for scroll-scrubbed landing pages. Testing visual regressions and scroll behavior.

## The Challenge

Scroll-based landing pages are hard to test because:

1. Content changes based on scroll position
2. Video scrubbing creates intermediate states
3. Animations may not complete instantly
4. Visual differences are subtle

**Solution**: Snapshot at specific scroll percentages and compare.

---

## Testing Workflow Overview

```text
1. Define scroll checkpoints (0%, 10%, 25%, 50%, 75%, 100%)
2. For each checkpoint:
   a. Scroll to position
   b. Wait for animations to settle
   c. Take screenshot
   d. Compare to baseline
3. Report visual differences
```

---

## agent-browser workflow (fast iteration + artifacts)

This section is intentionally **cinematic-specific**: it focuses on *scroll checkpoint* screenshots for scroll-scrubbed / animation-heavy landings.

For general visual QA + debugging bundles (snapshots, console/errors/network, traces), use:

- `.claude/skills/visual-qa/references/workflows.md`
- `.claude/skills/visual-qa/references/debugging.md`
- `.claude/skills/agent-browser/references/qa-workflows.md`

```bash
mkdir -p test-results
agent-browser open http://localhost:3000
agent-browser wait --load networkidle

# 0%
agent-browser eval "window.scrollTo({ top: 0, behavior: 'instant' });"
agent-browser wait 500
agent-browser screenshot test-results/scroll-0.png

# 25%
agent-browser eval "window.scrollTo({ top: (document.body.scrollHeight - window.innerHeight) * 0.25, behavior: 'instant' });"
agent-browser wait 500
agent-browser screenshot test-results/scroll-25.png

# 50%
agent-browser eval "window.scrollTo({ top: (document.body.scrollHeight - window.innerHeight) * 0.50, behavior: 'instant' });"
agent-browser wait 500
agent-browser screenshot test-results/scroll-50.png

# 75%
agent-browser eval "window.scrollTo({ top: (document.body.scrollHeight - window.innerHeight) * 0.75, behavior: 'instant' });"
agent-browser wait 500
agent-browser screenshot test-results/scroll-75.png

# 100%
agent-browser eval "window.scrollTo({ top: (document.body.scrollHeight - window.innerHeight) * 1.00, behavior: 'instant' });"
agent-browser wait 500
agent-browser screenshot test-results/scroll-100.png

agent-browser close
```

Notes:

- If the page has video scrubbing or heavy animations, increase the settle wait to `1000`+ ms.
- For *baseline diffing* (true visual regression), prefer the Playwright `toHaveScreenshot` workflow below.

---

## Playwright Setup

```bash
# Install Playwright
pnpm add -D @playwright/test

# Install browsers
npx playwright install
```

**playwright.config.ts:**

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    video: 'on-first-retry',
  },

  projects: [
    {
      name: 'Desktop Chrome',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'Desktop Firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 13'] },
    },
  ],

  webServer: {
    command: 'pnpm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## Scroll Checkpoint Test

**tests/scroll-snapshots.spec.ts:**

```typescript
import { test, expect } from '@playwright/test';

// Define scroll checkpoints based on your NARRATIVE config
const SCROLL_CHECKPOINTS = [
  { name: 'hero', percentage: 0 },
  { name: 'vision-end', percentage: 2.5 },
  { name: 'problem-peak', percentage: 7.5 },
  { name: 'problem-end', percentage: 22 },
  { name: 'solution-1', percentage: 28 },
  { name: 'solution-2', percentage: 41 },
  { name: 'bento', percentage: 57 },
  { name: 'proofs', percentage: 70 },
  { name: 'pricing', percentage: 80 },
  { name: 'cta', percentage: 95 },
];

test.describe('Landing Page Scroll Snapshots', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate and wait for initial load
    await page.goto('/');
    
    // Wait for preloader to complete (if you have one)
    await page.waitForSelector('[data-preloader]', { state: 'hidden', timeout: 20000 });
    
    // Wait for videos to be ready
    await page.waitForFunction(() => {
      const videos = document.querySelectorAll('video');
      return Array.from(videos).every(v => v.readyState >= 3);
    }, { timeout: 15000 });
  });

  for (const checkpoint of SCROLL_CHECKPOINTS) {
    test(`Scroll checkpoint: ${checkpoint.name} (${checkpoint.percentage}%)`, async ({ page }) => {
      // Get page height
      const pageHeight = await page.evaluate(() => document.body.scrollHeight);
      const scrollTarget = (pageHeight * checkpoint.percentage) / 100;

      // Scroll to position
      await page.evaluate((scrollY) => {
        window.scrollTo({ top: scrollY, behavior: 'instant' });
      }, scrollTarget);

      // Wait for scroll position to be reached
      await page.waitForFunction(
        (target) => Math.abs(window.scrollY - target) < 10,
        scrollTarget,
        { timeout: 5000 }
      );

      // Wait for animations to settle
      await page.waitForTimeout(500);

      // Take screenshot and compare to baseline
      await expect(page).toHaveScreenshot(`scroll-${checkpoint.name}.png`, {
        maxDiffPixelRatio: 0.05,  // Allow 5% pixel difference
        animations: 'disabled',   // Disable CSS animations for consistency
      });
    });
  }
});
```

---

## Video Scrub Verification

Test that video scrubbing works correctly:

```typescript
import { test, expect } from '@playwright/test';

test.describe('Video Scrubbing', () => {
  test('Video currentTime matches scroll position', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Get reference to scrub video
    const video = page.locator('video[src*="scrub"]').first();
    
    // Scroll to 50% of video phase
    const pageHeight = await page.evaluate(() => document.body.scrollHeight);
    await page.evaluate((scrollY) => {
      window.scrollTo({ top: scrollY, behavior: 'instant' });
    }, pageHeight * 0.15); // Assuming video phase is around 15%

    // Wait for scrub animation
    await page.waitForTimeout(1000);

    // Check video currentTime is reasonable
    const currentTime = await video.evaluate((el: HTMLVideoElement) => el.currentTime);
    const duration = await video.evaluate((el: HTMLVideoElement) => el.duration);
    
    // Video should be partially played
    expect(currentTime).toBeGreaterThan(0);
    expect(currentTime).toBeLessThan(duration);
  });
});
```

---

## Interactive Element Testing

Test that buttons and links are clickable at correct scroll positions:

```typescript
test.describe('Interactive Elements', () => {
  test('CTA button is visible and clickable at end', async ({ page }) => {
    await page.goto('/');
    
    // Scroll to CTA section
    const pageHeight = await page.evaluate(() => document.body.scrollHeight);
    await page.evaluate((scrollY) => {
      window.scrollTo({ top: scrollY, behavior: 'instant' });
    }, pageHeight * 0.95);

    await page.waitForTimeout(500);

    // Check CTA button is visible
    const ctaButton = page.locator('a:has-text("INITIALIZE")');
    await expect(ctaButton).toBeVisible();
    
    // Check it's clickable (pointer-events enabled)
    const isClickable = await ctaButton.evaluate((el) => {
      const style = window.getComputedStyle(el);
      return style.pointerEvents !== 'none';
    });
    expect(isClickable).toBe(true);
  });
});
```

---

## Mobile Scroll Testing

```typescript
test.describe('Mobile Scroll', () => {
  test.use({ viewport: { width: 390, height: 844 } }); // iPhone 14 Pro

  test('Touch scroll works correctly', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Simulate touch scroll
    await page.evaluate(() => {
      window.scrollTo({ top: 1000, behavior: 'smooth' });
    });

    await page.waitForTimeout(1000);

    // Verify scroll happened
    const scrollY = await page.evaluate(() => window.scrollY);
    expect(scrollY).toBeGreaterThan(500);

    // Take mobile snapshot
    await expect(page).toHaveScreenshot('mobile-scrolled.png');
  });
});
```

---

## Performance Metrics

Capture Core Web Vitals during scroll:

```typescript
test('Performance during scroll', async ({ page }) => {
  await page.goto('/');
  
  // Start performance measurement
  await page.evaluate(() => {
    window.performanceMetrics = {
      frames: 0,
      startTime: performance.now(),
    };
    
    const countFrames = () => {
      window.performanceMetrics.frames++;
      if (performance.now() - window.performanceMetrics.startTime < 5000) {
        requestAnimationFrame(countFrames);
      }
    };
    requestAnimationFrame(countFrames);
  });

  // Perform continuous scroll
  for (let i = 0; i < 10; i++) {
    await page.mouse.wheel(0, 500);
    await page.waitForTimeout(100);
  }

  // Wait for measurement
  await page.waitForTimeout(3000);

  // Get results
  const metrics = await page.evaluate(() => window.performanceMetrics);
  const fps = (metrics.frames / 5) * 1;

  console.log(`Average FPS during scroll: ${fps.toFixed(1)}`);
  
  // Assert minimum FPS
  expect(fps).toBeGreaterThan(30);
});
```

---

## Visual Regression Workflow

### Initial Setup (Create Baselines)

```bash
# Generate baseline screenshots
npx playwright test --update-snapshots
```

### CI Pipeline

```yaml
# .github/workflows/visual-tests.yml
name: Visual Regression Tests

on:
  pull_request:
    branches: [main]

jobs:
  visual-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: pnpm install
        
      - name: Install Playwright Browsers
        run: npx playwright install --with-deps
        
      - name: Run tests
        run: npx playwright test
        
      - name: Upload test results
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
```

---

## Test Helpers

**tests/helpers.ts:**

```typescript
import { Page } from '@playwright/test';

export async function waitForPreloader(page: Page) {
  await page.waitForSelector('[data-preloader]', { 
    state: 'hidden', 
    timeout: 20000 
  });
}

export async function scrollToPercentage(page: Page, percentage: number) {
  const pageHeight = await page.evaluate(() => document.body.scrollHeight);
  const scrollTarget = (pageHeight * percentage) / 100;
  
  await page.evaluate((scrollY) => {
    window.scrollTo({ top: scrollY, behavior: 'instant' });
  }, scrollTarget);
  
  // Wait for scroll to complete
  await page.waitForFunction(
    (target) => Math.abs(window.scrollY - target) < 10,
    scrollTarget,
    { timeout: 5000 }
  );
  
  // Wait for animations
  await page.waitForTimeout(500);
}

export async function getScrollProgress(page: Page): Promise<number> {
  return page.evaluate(() => {
    const scrollHeight = document.body.scrollHeight - window.innerHeight;
    return window.scrollY / scrollHeight;
  });
}
```

---

## Debugging Tips

### Visual Test Failures

```bash
# Run with headed browser
npx playwright test --headed

# Run with debug mode
npx playwright test --debug

# Run specific test
npx playwright test -g "hero"

# Update single snapshot
npx playwright test -g "hero" --update-snapshots
```

### Video Recording

```typescript
// playwright.config.ts
use: {
  video: 'on',  // Always record
  // or
  video: 'retain-on-failure',  // Only keep on failure
}
```

---

## Gotchas

1. **Animation Timing**: Always wait after scrolling before taking screenshots
2. **Video Loading**: Videos may not be ready immediately—wait for `canplaythrough`
3. **Preloader**: Account for preloader in test setup
4. **Responsive**: Test multiple viewports—layout changes affect scroll behavior
5. **CI Environment**: Screenshots may differ slightly in CI—use appropriate thresholds
6. **RAF Loop**: Video scrubbing uses RAF—may need longer waits than expected
