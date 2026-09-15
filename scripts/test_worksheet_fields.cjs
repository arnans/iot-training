// Requires jsdom: node scripts/test_worksheet_fields.cjs [path-to-jsdom]
const { JSDOM } = require(process.argv[2] || 'jsdom');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const behavior = fs.readFileSync(path.join(root, 'docs/javascripts/extra.js'), 'utf8');
const storeKey = 'farm-worksheet.v1';
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
async function open(slug, saved) {
  const dom = new JSDOM(fs.readFileSync(path.join(root, `docs/renders/${slug}.html`), 'utf8'), {
    url: `https://worksheet.test/${slug}/`, runScripts: 'outside-only',
  });
  const w = dom.window;
  // Keep this test offline: no progress reports, external resources, or downloads.
  w.fetch = async () => ({ ok: true, json: async () => ({}) });
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
(async () => {
  let dom = await open('session-1');
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
  for (const el of w.document.querySelectorAll('.task-list-item input[type=checkbox]')) {
    el.checked = true;
    el.dispatchEvent(new w.Event('change', { bubbles: true }));
  }
  const saved = w.localStorage.getItem(storeKey);
  assert.equal(Object.keys(JSON.parse(saved).checks).length, 30);
  dom.window.close();
  dom = await open('session-1', saved);
  verify(dom.window, expected);
  assert([...dom.window.document.querySelectorAll('.task-list-item input[type=checkbox]')].every(el => el.checked));
  // Change a repeated radio group from its second occurrence.
  const choices = controls(dom.window, 's1.timer.ok');
  choices[4].checked = true;
  choices[4].dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  expected['s1.timer.ok'] = choices[4].value;
  verify(dom.window, expected);
  const changed = dom.window.localStorage.getItem(storeKey);
  dom.window.close();
  dom = await open('record-sheet', changed);
  verify(dom.window, expected);
  dom.window.close();
  console.log(`PASS: ${keys.length} answer keys, duplicate text/radio synchronization, save/restore, 30 checkboxes, and record-sheet transfer`);
})().catch(err => { console.error(err); process.exit(1); });
