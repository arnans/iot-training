// Records one walkthrough: drives the HA automation editor per specs/<name>.cjs, captures frames and a mouse log.
// Never presses the final Save, so HA is left unchanged.   node record.cjs a5-1
const C = require('./config.cjs'); const { chromium } = require(C.PW);
const fs = require('fs'); const spec = C.spec(process.argv[2]); const W = C.WORK + '/' + spec.id; const OUT = W + '/frames';
const steps = spec.steps;
fs.rmSync(OUT, { recursive: true, force: true }); fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch({ channel: 'chrome', headless: true });
  const ctx = await b.newContext({ viewport: { width: 978, height: 724 }, deviceScaleFactor: 1.2, storageState: C.STATE, locale: 'en-US' });
  const p = await ctx.newPage();
  await p.goto(C.HA + (spec.start || '/config/automation/edit/new'));
  await p.waitForTimeout(3500);
  // wrap the mouse: eased movement, every position and click logged with wall-clock time
  const log = []; const m = p.mouse; const orig = { move: m.move.bind(m), down: m.down.bind(m), up: m.up.bind(m), wheel: m.wheel.bind(m) };
  let cx = 640, cy = 360; const now = () => Date.now() / 1000;
  m.move = async (x, y) => { const d = Math.hypot(x - cx, y - cy); if (d < 1) return; const n = Math.max(8, Math.min(28, Math.round(d / 18)));
    const x0 = cx, y0 = cy; for (let i = 1; i <= n; i++) { const t = i / n, e = t < .5 ? 2*t*t : 1 - (-2*t+2)**2/2;
      cx = x0 + (x - x0) * e; cy = y0 + (y - y0) * e; await orig.move(cx, cy); log.push({ t: now(), x: cx, y: cy }); await p.waitForTimeout(22); } };
  m.click = async (x, y) => { await m.move(x, y); await p.waitForTimeout(350); await orig.down(); log.push({ t: now(), x, y, click: 1 }); await orig.up(); };
  m.fakeClick = async (x, y) => { await m.move(x, y); await p.waitForTimeout(350); log.push({ t: now(), x, y, click: 1 }); };  // shown, not pressed
  m.wheel = async (dx, dy) => { await orig.wheel(dx, dy); };
  const kb = p.keyboard, origType = kb.type.bind(kb); kb.type = (s, o) => origType(s, { delay: 85 });
  // capture loop: scaled clip gives device-pixel frames
  const cdp = await ctx.newCDPSession(p); const frames = []; let k = 0, run = true;
  const loop = (async () => { while (run) { const ts = now();
    const r = await cdp.send('Page.captureScreenshot', { format: 'png', optimizeForSpeed: true, clip: { x: 0, y: 0, width: 978, height: 724, scale: 1.2 } }).catch(() => null);
    if (r) { const file = `${OUT}/${String(k++).padStart(5, '0')}.png`; fs.writeFileSync(file, Buffer.from(r.data, 'base64')); frames.push({ t: ts, file }); }
    const w = 66 - (now() - ts) * 1000; if (w > 0) await new Promise(res => setTimeout(res, w)); } })();
  await p.waitForTimeout(300); await orig.move(cx, cy); log.push({ t: now(), x: cx, y: cy });
  const t0 = now(); await p.waitForTimeout(800);
  const caps = [];
  for (const [, cap, run, kind] of steps) { caps.push({ t: now(), cap }); await p.waitForTimeout(500); await run(p); await p.waitForTimeout(kind === 'click' ? 1600 : 1000); }
  await p.waitForTimeout(1200);
  const t1 = now(); run = false; await loop;
  fs.writeFileSync(W + '/timeline.json', JSON.stringify({ t0, t1, frames, log, caps }));
  console.log('frames', frames.length, 'secs', (t1 - t0).toFixed(1));
  await b.close();   // closing without saving: nothing is written to HA
})().catch(e => { console.error(e); process.exit(1); });
