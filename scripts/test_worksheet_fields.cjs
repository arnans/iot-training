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
// Every task-list row whose bold link names a section gets a "ทำข้อนี้เสร็จแล้ว" box at the foot of
// that section. It is a second view of the row's box: ticking either sets both, only the row's box is
// saved (no extra check keys) and reported. Boxes in a ws-untracked list are saved but never reported.
async function testDoneBoxes() {
  const saved = JSON.stringify({ fields: { 'team.no': '17' }, checks: {}, sentAs: '17', dev: 'devtest' });
  const calls = [];
  let dom = await open('activity-8', saved, calls);
  let w = dom.window, d = w.document;
  const rows = [...d.querySelectorAll('.ws-tasks .task-list-item')];
  const mirrors = [...d.querySelectorAll('label.ws-done input.ws-mirror')];
  assert.equal(mirrors.length, rows.length, 'one done box per task-list row');
  assert.equal(rows.length, 6);
  for (const row of rows) {                      // each box sits at the foot of the section its row links to
    const id = decodeURIComponent(row.querySelector('strong a').getAttribute('href').slice(1));
    let el = d.getElementById(id), foot = null;
    for (el = el.nextElementSibling; el && !/^H[23]$/.test(el.tagName); el = el.nextElementSibling) {
      if (el.classList.contains('ws-foot')) foot = el;
    }
    assert.ok(foot && foot.querySelector('label.ws-done') && foot.querySelector('a.ws-back'), `${id}: done box and back link on one footer line`);
  }
  const untracked = [...d.querySelectorAll('.ws-untracked .task-list-item input[type=checkbox]')];
  assert.equal(untracked.length, 3, '8.3 acknowledgement boxes');
  // tick the second mirror: its row box follows, is saved under the row's index, and is reported
  const listBoxes = [...d.querySelectorAll('.task-list-item input[type=checkbox]')];
  calls.length = 0;
  mirrors[1].checked = true;
  mirrors[1].dispatchEvent(new w.Event('change', { bubbles: true }));
  await wait(50);
  const rowBox = rows[1].querySelector('input[type=checkbox]');
  assert.ok(rowBox.checked, 'row box follows the done box');
  const checks = JSON.parse(w.localStorage.getItem(storeKey)).checks;
  assert.deepEqual(Object.keys(checks), [`/activity-8/#${listBoxes.indexOf(rowBox)}`], 'only the row box is saved');
  let put = calls.filter(c => c.opts && c.opts.method === 'PUT').pop();
  assert.ok(put, 'done box reported');
  let a8 = JSON.parse(put.opts.body).pages['session-3'].acts.a8;
  assert.deepEqual([a8.done, a8.total], [1, 6], 'activity 8 counts the six list boxes only');
  assert.equal(JSON.parse(put.opts.body).last.label.slice(0, 3), '8.2');
  // untick from the list: the mirror follows
  rowBox.checked = false;
  rowBox.dispatchEvent(new w.Event('change', { bubbles: true }));
  assert.equal(mirrors[1].checked, false, 'done box follows the row box');
  // an acknowledgement box is remembered but not reported
  calls.length = 0;
  untracked[0].checked = true;
  untracked[0].dispatchEvent(new w.Event('change', { bubbles: true }));
  await wait(50);
  assert.equal(calls.filter(c => c.opts && c.opts.method === 'PUT').length, 0, 'untracked tick not sent');
  assert.equal(Object.keys(JSON.parse(w.localStorage.getItem(storeKey)).checks).length, 1, 'untracked tick saved');
  const kept = w.localStorage.getItem(storeKey);
  dom.window.close();
  // reload: the saved state reaches both views
  rowBox.checked = true; rowBox.dispatchEvent(new w.Event('change', { bubbles: true }));
  dom = await open('activity-8', kept.replace('"checks":{', `"checks":{"/activity-8/#${listBoxes.indexOf(rowBox)}":true,`), calls);
  w = dom.window; d = w.document;
  assert.ok([...d.querySelectorAll('label.ws-done input.ws-mirror')][1].checked, 'done box restored with its row');
  assert.ok(d.querySelectorAll('.ws-untracked input[type=checkbox]')[0].checked, 'acknowledgement restored');
  dom.window.close();
  console.log('PASS done boxes: one per task-list row at the foot of its section, one state with the row, 8.3 acknowledgements saved but not counted');
}
// The 🙋 button sends one message and then offers to withdraw it: pressing it again writes
// `cancelled` onto that same message, and the label goes back to asking. The id of the open
// call is kept in the store, so the offer survives moving to the next worksheet page.
async function testHelpCancel() {
  const d = new Date();
  const today = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  const saved = JSON.stringify({ fields: { 'team.no': '17' }, checks: {}, sentAs: '17', dev: 'devtest' });
  const calls = [];
  let dom = await open('activity-2', saved, calls);
  let w = dom.window;
  w.fetch = async (url, opts) => {               // the database answers a POST with the id it picked
    calls.push({ url, opts });
    return { ok: true, json: async () => (/\/messages\/[\d-]+\.json$/.test(url) ? { name: '-Nhelp1' } : {}) };
  };
  const btn = w.document.querySelector('#ws-bar .ws-help');
  assert.ok(btn, 'help button');
  assert.match(btn.textContent, /ขอความช่วยเหลือ/);
  btn.dispatchEvent(new w.Event('click', { bubbles: true }));
  await wait(50);
  const post = calls.filter(c => c.opts && c.opts.method === 'POST').pop();
  assert.ok(post, 'help message sent');
  assert.equal(post.url, `https://iot-farm-workshop-default-rtdb.asia-southeast1.firebasedatabase.app/messages/${today}.json`);
  assert.equal(JSON.parse(post.opts.body).kind, 'help');
  assert.match(btn.textContent, /ยกเลิกคำขอ/, 'button offers to withdraw');
  assert.ok(btn.classList.contains('is-open'));
  await wait(350);
  let help = JSON.parse(w.localStorage.getItem(storeKey)).help;
  assert.equal(help && help.id, '-Nhelp1', 'the open call is remembered');
  assert.equal(help.day, today);
  const kept = w.localStorage.getItem(storeKey);
  dom.window.close();

  // the next worksheet page still offers to withdraw it
  calls.length = 0;
  dom = await open('activity-3', kept, calls);
  w = dom.window;
  w.fetch = async (url, opts) => { calls.push({ url, opts }); return { ok: true, json: async () => ({}) }; };
  const btn2 = w.document.querySelector('#ws-bar .ws-help');
  assert.match(btn2.textContent, /ยกเลิกคำขอ/, 'offer survives the page change');
  btn2.dispatchEvent(new w.Event('click', { bubbles: true }));
  await wait(50);
  const put = calls.filter(c => c.opts && c.opts.method === 'PUT').pop();
  assert.ok(put, 'cancel written');
  assert.match(put.url, new RegExp(`/messages/${today}/-Nhelp1/cancelled\\.json`));
  assert.ok(Number(put.opts.body) > 0, 'cancelled is a timestamp');
  assert.equal(calls.filter(c => c.opts && c.opts.method === 'POST').length, 0, 'cancel sends no new message');
  assert.match(btn2.textContent, /ขอความช่วยเหลือ/, 'button asks again once the call is withdrawn');
  await wait(350);
  assert.equal(JSON.parse(w.localStorage.getItem(storeKey)).help, undefined, 'the withdrawn call is forgotten');
  dom.window.close();

  // a call from another day is never offered for cancelling
  dom = await open('activity-2', JSON.stringify({ fields: { 'team.no': '17' }, checks: {}, sentAs: '17', dev: 'devtest',
                                                  help: { id: '-Nold', day: '2020-01-01', ts: Date.now() } }), calls);
  assert.match(dom.window.document.querySelector('#ws-bar .ws-help').textContent, /ขอความช่วยเหลือ/, 'yesterday\'s call is not cancellable');
  dom.window.close();
  console.log('PASS help: one message sent, withdrawn from a later page, stale calls dropped');
}
(async () => {
  for (const slug of ['session-1-start', 'activity-1', 'activity-2', 'activity-3', 'activity-4', 'activity-5',
                      'activity-6', 'activity-7', 'activity-8', 'record-sheet']) await testPage(slug);
  await testDoneBoxes();
  await testProgressMerge();
  await testHelpCancel();
})().catch(err => { console.error(err); process.exit(1); });
