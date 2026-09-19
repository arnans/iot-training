// Runs a spec without recording, screenshotting after each step into .tmp/walkthroughs/dry/.
//   node dryrun.cjs a3-5 [n]      first n steps only
//   node dryrun.cjs a3-5 --commit  also runs spec.commit (e.g. the final Save), to set up state other walkthroughs need
const C = require('./config.cjs'); const { chromium } = require(C.PW); const fs = require('fs');
const spec = C.spec(process.argv[2]); const commit = process.argv.includes('--commit');
const n = Math.min(+process.argv[3] || 999, spec.steps.length); const D = C.WORK + '/' + (process.env.DRY || 'dry');  // DRY=dry2 lets two dry runs work side by side
(async () => {
  fs.rmSync(D, { recursive: true, force: true }); fs.mkdirSync(D, { recursive: true });
  const b = await chromium.launch({ channel: 'chrome', headless: true });
  const ctx = await b.newContext({ viewport: { width: 978, height: 724 }, deviceScaleFactor: 1.2, storageState: C.STATE, locale: 'en-US' });
  const p = await ctx.newPage(); p.mouse.fakeClick = async (x, y) => p.mouse.move(x, y);
  await p.goto(C.HA + (spec.start || '/config/automation/edit/new')); await p.waitForTimeout(3500);
  if (spec.setup) await spec.setup(p);
  for (let i = 0; i < n; i++) {
    try { await spec.steps[i][2](p); } catch (e) { console.error('step', i, spec.steps[i][1], '→', e.message.split('\n')[0]); await p.screenshot({ path: D + '/err.png' }); break; }
    await p.waitForTimeout(900); await p.screenshot({ path: `${D}/${String(i).padStart(2, '0')}.png` });
  }
  if (commit && spec.commit) { await spec.commit(p); await p.waitForTimeout(2500); await p.screenshot({ path: D + '/commit.png' }); console.log('committed', p.url()); }
  await b.close();
})();
