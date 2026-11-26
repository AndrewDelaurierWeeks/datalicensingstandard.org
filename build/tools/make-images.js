// Renders build/assets/og.png (1200 x 630, the link preview) from the site's own fonts and the cover's device.
// The icons come from build/tools/make-icons.py. Run once after a change: node build/tools/make-images.js
// Needs Playwright with Chromium. MIT License (build/LICENSE).
const fs = require('fs'), os = require('os'), path = require('path'), { chromium } = require('playwright');
const A = path.resolve(__dirname, '..', 'assets');
const h = 'e2a4c2f89cb919f0757333c8b96200dd389d23674a35e627c2e5e4cc4ae29ea1';
let cells = '';
for (let i = 0; i < 15; i++) for (let j = 0; j < 15; j++) if (parseInt(h[(i * 15 + j) % 64], 16) % 2) cells += `<i style="grid-column:${i + 1};grid-row:${j + 1}"></i>`;
const font = (f, w, s) => `@font-face{font-family:"${f}";font-weight:${w};font-style:${s};src:url(file://${A}/fonts/${f.toLowerCase().replace(/ /g, '-')}-latin-${w}-${s}.woff2)}`;
const css = font('EB Garamond', 500, 'normal') + font('EB Garamond', 400, 'italic') + font('IBM Plex Mono', 500, 'normal') +
  `body{margin:0}.mk{display:grid;grid-template-columns:repeat(15,1fr);grid-template-rows:repeat(15,1fr);gap:1px}.mk i{background:#1b2420}`;
const og = `<html><head><style>${css}
.c{width:1200px;height:630px;box-sizing:border-box;background:#fff;border:2px solid #1b2420;display:grid;grid-template-columns:520px 1fr;align-items:center;padding:48px 56px;gap:40px;font-family:"EB Garamond"}
img{width:520px;height:auto}.s{font:500 20px/1.4 "IBM Plex Mono";letter-spacing:.16em;color:#1f5a3a;margin:0 0 18px}
h1{font:500 64px/1.04 "EB Garamond";color:#000;margin:0}.sub{font:italic 400 30px/1.25 "EB Garamond";color:#1f5a3a;margin:18px 0 0}
.u{font:500 18px/1.4 "IBM Plex Mono";letter-spacing:.12em;color:#5b6368;margin:26px 0 0}</style></head><body><div class="c">
<img src="file://${A}/device/plate.webp"><div><p class="s">TDLS-AI v0.1</p><h1>The Data Licensing Standard for AI</h1>
<p class="sub">Requirements, evidence and scoring for AI training data vendors</p><p class="u">datalicensingstandard.org</p></div></div></body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tdls-img-'));
  fs.writeFileSync(path.join(tmp, 'og.html'), og);
  await p.goto('file://' + path.join(tmp, 'og.html'), { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(A, 'og.png') });
  await b.close();
})();
