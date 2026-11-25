// 用法：node print/to_pdf.js  → 把 print/out/*.html 轉成 A4 PDF（另存一張預覽 PNG）
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const dir = path.join(__dirname, 'out'); const b = await chromium.launch(); const p = await b.newPage();
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html'))) {
    await p.goto('file://' + path.join(dir, f)); await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: path.join(dir, f.replace('.html', '.pdf')), format: 'A4', printBackground: true, preferCSSPageSize: true });
    await p.setViewportSize({ width: 794, height: 1123 });
    await p.screenshot({ path: path.join(dir, f.replace('.html', '.png')), fullPage: true });
  }
  await b.close();
})();
