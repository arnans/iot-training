// Requires jsdom: node scripts/test_worksheet_fields.cjs [path-to-jsdom]
const { JSDOM } = require(process.argv[2] || 'jsdom');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const behavior = fs.readFileSync(path.join(root, 'docs/javascripts/extra.js'), 'utf8');
const storeKey = 'farm-worksheet.v1';
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
async function open(slug, saved, calls) {
  const dom = new JSDOM(fs.readFileSync(path.join(root, `docs/renders/${slug}.html`), 'utf8'), {
    url: `https://worksheet.test/${slug}/`, runScripts: 'outside-only',
  });
  const w = dom.window;
  // Keep this test offline: progress reports are captured in `calls` (when given), never sent.
  w.fetch = async (url, opts) => { if (calls) calls.push({ url, opts }); return { ok: true, json: async () => ({}) }; };
  w.matchMedia = () => ({ matches: false });
  if (saved) w.localStorage.setItem(storeKey, saved);
  await wait(0);
  w.eval(behavior);
  return dom;
}
function controls(w, key) {
  return [...w.document.querySelectorAll('input.fld, textarea.fld')].filter(el => el.dataset.k === key);
}
function verify(w, expected) {
  for (const [key, value] of Object.entries(expected)) {
    const fields = controls(w, key);
    assert(fields.length, `missing ${key}`);
    for (const el of fields) {
      if (el.type === 'radio') assert.equal(el.checked, el.value === value, `radio ${key}: ${el.value}`);
      else assert.equal(el.value, value, `field ${key}`);
    }
  }
}
async function testPage(slug) {
  let dom = await open(slug);
  let w = dom.window;
  const expected = {};
  const keys = [...new Set([...w.document.querySelectorAll('input.fld,textarea.fld')].map(el => el.dataset.k))];
  for (const key of keys) {
    const el = controls(w, key)[0];
    const value = el.type === 'radio' ? el.value : key === 'team.no' ? '17' : 'ทดสอบ 42.5';
    expected[key] = value;
    if (el.type === 'radio') el.checked = true;
    else el.value = value;
    el.dispatchEvent(new w.Event(el.type === 'radio' ? 'change' : 'input', { bubbles: true }));
  }
  await wait(350);
  verify(w, expected);
  const checkCount = w.document.querySelectorAll('.task-list-item input[type=checkbox]').length;
  for (const el of w.document.querySelectorAll('.task-list-item input[type=checkbox]')) {
    el.checked = true;
    el.dispatchEvent(new w.Event('change', { bubbles: true }));
  }
  const saved = w.localStorage.getItem(storeKey);
  assert.equal(Object.keys(JSON.parse(saved).checks).length, checkCount);
  dom.window.close();
  dom = await open(slug, saved);
  verify(dom.window, expected);
  assert([...dom.window.document.querySelectorAll('.task-list-item input[type=checkbox]')].every(el => el.checked));
  // Change every radio key, using the second copy when a field is repeated.
  for (const key of keys) {
    const choices = controls(dom.window, key).filter(el => el.type === 'radio');
    if (!choices.length) continue;
    const groups = [...new Set(choices.map(el => el.name))];
    const copy = choices.filter(el => el.name === groups[Math.min(1, groups.length - 1)]);
    const choice = copy[copy.length - 1];
    choice.checked = true;
    choice.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
    expected[key] = choice.value;
    verify(dom.window, expected);
  }
  const changed = dom.window.localStorage.getItem(storeKey);
  dom.window.close();
  dom = await open('record-sheet', changed);
  verify(dom.window, expected);
  dom.window.close();
  console.log(`PASS ${slug}: ${keys.length} answer keys, duplicate text/radio synchronization, save/restore, ${checkCount} checkboxes, and record-sheet transfer`);
}
// A tick on an activity page is reported under its session, merged with the counts this browser
// cached for the session's other pages, in course order: activity 2 never replaces activity 1.
async function testProgressMerge() {
  const cached = { acts: { a1: { done: 2, total: 5, filled: 1, nf: 3 } }, order: ['a1'], names: {}, steps: { a1: [] }, ts: 1 };
  const saved = JSON.stringify({ fields: { 'team.no': '17', 'team.zone': 'แดง' }, checks: {}, sentAs: '17', dev: 'devtest',
                                 progPages: { 'activity-1': cached } });
  const calls = [];
  const dom = await open('activity-2', saved, calls);
  const w = dom.window;
  const box = w.document.querySelector('.task-list-item input[type=checkbox]');
  box.checked = true;
  box.dispatchEvent(new w.Event('change', { bubbles: true }));
  await wait(50);
  const put = calls.filter(c => c.opts && c.opts.method === 'PUT').pop();
  assert.ok(put, 'no progress report sent');
  assert.match(put.url, /\/progress\/\d{4}-\d\d-\d\d\/17\/devtest\.json/);
  const doc = JSON.parse(put.opts.body);
  assert.equal(doc.page, 'session-1');
  assert.equal(doc.last.page, 'session-1');
  assert.deepEqual(Object.keys(doc.pages), ['session-1']);
  const s1 = doc.pages['session-1'];
  assert.deepEqual(s1.acts.a1, cached.acts.a1, 'activity 1 counts lost');
  assert.ok(s1.acts.a2 && s1.acts.a2.done === 1, 'activity 2 tick missing');
  assert.deepEqual(s1.order.slice(0, 2), ['a1', 'a2']);
  dom.window.close();
  console.log('PASS progress: activity page reports under its session, merged in course order');
}
(async () => {
  for (const slug of ['session-1-start', 'activity-1', 'activity-2', 'activity-3', 'activity-4', 'activity-5',
                      'session-3-history', 'activity-6', 'activity-7', 'record-sheet']) await testPage(slug);
  await testProgressMerge();
})().catch(err => { console.error(err); process.exit(1); });
