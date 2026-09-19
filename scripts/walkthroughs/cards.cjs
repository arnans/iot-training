// Renders the title card and one caption strip per step with Chrome (proper Thai shaping, Prompt font)
const C = require('./config.cjs'); const { chromium } = require(C.PW);
const fs = require('fs'); const S = __dirname;
const W = 1174, H = 869, STRIP = 72;
const spec = C.spec(process.argv[2]); const D = C.WORK + '/' + spec.id + '/cards';
const title = { sub: 'Home Assistant → Settings → Automations → Create automation', ...spec.title };
const caps = spec.steps.map(s => s[1]); const wsStep = i => spec.steps[i][0];
const font = `@font-face{font-family:P;src:local('Prompt Medium'),local('Prompt-Medium');font-weight:500}
@font-face{font-family:P;src:local('Prompt SemiBold'),local('Prompt-SemiBold');font-weight:600}
@font-face{font-family:P;src:local('Prompt'),local('Prompt-Regular');font-weight:400}
*{margin:0;box-sizing:border-box} body{font-family:P,'Prompt',sans-serif}`;
(async () => {
  const b = await chromium.launch({ channel: 'chrome', headless: true });
  const p = await (await b.newContext({ viewport: { width: W, height: H + STRIP } })).newPage();
  fs.mkdirSync(D, { recursive: true });
  await p.setContent(`<style>${font}
    body{width:${W}px;height:${H + STRIP}px;background:#1b5e20;color:#fff;display:flex;flex-direction:column;justify-content:center;padding:0 96px}
    .k{display:inline-block;align-self:flex-start;background:#f5a524;color:#1e2a1f;font-weight:600;font-size:26px;padding:6px 22px;border-radius:999px}
    h1{font-weight:600;font-size:62px;line-height:1.35;margin:34px 0 18px}
    .n{font-weight:500;font-size:30px;color:#dcedc8}
    .n code{font-family:P;background:rgba(255,255,255,.14);padding:2px 14px;border-radius:8px;color:#fff}
    .s{font-weight:400;font-size:22px;color:#c5e1a5;margin-top:44px;padding-top:22px;border-top:2px solid rgba(255,255,255,.18)}
    .play{position:absolute;right:96px;bottom:${STRIP + 60}px;font-size:22px;color:#c5e1a5;font-weight:500}</style>
    <div class=k>${title.kicker}</div><h1>${title.head}</h1>${title.name ? `<div class=n>${title.nameLabel || "ชื่อกฎ"} <code>${title.name}</code></div>` : ""}
    <div class=s>${title.sub}</div><div class=play>▶ เริ่ม</div>`);
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: D + '/title.png' });
  await p.setViewportSize({ width: W, height: STRIP });
  for (let i = 0; i < caps.length; i++) {
    await p.setContent(`<style>${font} body{width:${W}px;height:${STRIP}px;background:#1e2a1f;color:#fff;display:flex;align-items:center;justify-content:center;gap:18px;font-size:27px;font-weight:500}
      .i{background:#f5a524;color:#1e2a1f;font-weight:600;font-size:20px;height:40px;border-radius:20px;display:flex;align-items:center;justify-content:center;padding:0 16px}</style>
      <span class=i>ข้อ ${wsStep(i)}</span><span>${caps[i].replace(/&/g, '&amp;').replace(/</g, '&lt;')}</span>`);
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: `${D}/cap${String(i).padStart(2, '0')}.png` });
  }
  console.log('cards', caps.length + 1, await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + f.weight).join(',')));
  await b.close();
})();
