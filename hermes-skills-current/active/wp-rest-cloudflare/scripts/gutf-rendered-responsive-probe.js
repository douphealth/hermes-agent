#!/usr/bin/env node
/**
 * Rendered responsive QA probe for GearUpToFit WordPress pages.
 *
 * Usage:
 *   npm install puppeteer-core
 *   node scripts/gutf-rendered-responsive-probe.js \
 *     /path/to/chrome-or-chrome-headless-shell \
 *     https://gearuptofit.com/url-1/ https://gearuptofit.com/url-2/
 *
 * Checks mobile 390px, mobile 320px, and desktop 1366px for:
 * - document/body scrollWidth larger than viewport
 * - elements wider than viewport
 * - suspicious ultra-skinny readable text columns
 */
const puppeteer = require('puppeteer-core');

const [,, executablePath, ...urls] = process.argv;
if (!executablePath || urls.length === 0) {
  console.error('Usage: node gutf-rendered-responsive-probe.js /path/to/chrome URL [URL...]');
  process.exit(2);
}

const viewports = [
  { name: 'mobile390', width: 390, height: 1400, isMobile: true },
  { name: 'mobile320', width: 320, height: 1200, isMobile: true },
  { name: 'desktop1366', width: 1366, height: 1200, isMobile: false },
];

async function probe(page) {
  return page.evaluate(() => {
    const w = window.innerWidth;
    const bad = [];
    document.querySelectorAll('body *').forEach((el) => {
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      if (r.width > w + 8 && cs.display !== 'none' && cs.visibility !== 'hidden') {
        bad.push({
          tag: el.tagName,
          id: el.id || '',
          cls: String(el.className || '').slice(0, 120),
          w: Math.round(r.width),
          left: Math.round(r.left),
          right: Math.round(r.right),
          display: cs.display,
          text: (el.innerText || el.getAttribute('aria-label') || '').replace(/\s+/g, ' ').slice(0, 120),
        });
      }
    });
    const skinny = [];
    document.querySelectorAll('p,li,h1,h2,h3,h4,td,th,div').forEach((el) => {
      const r = el.getBoundingClientRect();
      const t = (el.innerText || '').trim();
      if (t.length > 30 && r.width > 0 && r.width < 95 && r.height > 30) {
        skinny.push({
          tag: el.tagName,
          cls: String(el.className || '').slice(0, 80),
          w: Math.round(r.width),
          h: Math.round(r.height),
          text: t.replace(/\s+/g, ' ').slice(0, 100),
        });
      }
    });
    return {
      vw: w,
      docScroll: document.documentElement.scrollWidth,
      bodyScroll: document.body.scrollWidth,
      badCount: bad.length,
      skinnyCount: skinny.length,
      bad: bad.slice(0, 20),
      skinny: skinny.slice(0, 20),
      title: document.title,
    };
  });
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath,
    headless: 'new',
    args: ['--no-sandbox', '--disable-gpu'],
  });
  let failed = false;
  for (const url of urls) {
    for (const vp of viewports) {
      const page = await browser.newPage();
      await page.setViewport({ width: vp.width, height: vp.height, isMobile: vp.isMobile, deviceScaleFactor: 1 });
      if (vp.isMobile) {
        await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1');
      }
      await page.goto(url, { waitUntil: 'networkidle2', timeout: 45000 });
      await new Promise((resolve) => setTimeout(resolve, 1000));
      const result = await probe(page);
      const pass = result.docScroll <= vp.width && result.bodyScroll <= vp.width && result.badCount === 0 && (vp.isMobile ? result.skinnyCount === 0 : true);
      if (!pass) failed = true;
      console.log(JSON.stringify({ url, viewport: vp.name, pass, ...result }));
      await page.close();
    }
  }
  await browser.close();
  process.exit(failed ? 1 : 0);
})();
