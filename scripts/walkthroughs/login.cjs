// Log in once and keep the session for record.cjs.  HA_USER=… HA_PASS=… node login.cjs
const C = require('./config.cjs'); const { chromium } = require(C.PW); const fs = require('fs');
(async () => {
  if (!process.env.HA_USER || !process.env.HA_PASS) throw new Error('set HA_USER and HA_PASS');
  fs.mkdirSync(C.WORK, { recursive: true });
  const b = await chromium.launch({ channel: 'chrome', headless: true });
  const ctx = await b.newContext({ viewport: { width: 1174, height: 869 } }); const p = await ctx.newPage();
  await p.goto(C.HA + '/'); await p.waitForTimeout(3000);
  await p.keyboard.type(process.env.HA_USER); await p.keyboard.press('Tab'); await p.keyboard.type(process.env.HA_PASS); await p.keyboard.press('Enter');
  await p.waitForTimeout(5000);
  if (p.url().includes('/auth/')) throw new Error('login failed: ' + p.url());
  await ctx.storageState({ path: C.STATE }); console.log('saved', C.STATE);
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
