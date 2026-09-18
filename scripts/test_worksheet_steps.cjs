// Check source numbering, the list starts emitted by the renderer, and the counter seed the CSS needs to display them.
// Usage: node scripts/test_worksheet_steps.cjs /path/to/node_modules/jsdom
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { JSDOM } = require(process.argv[2] || 'jsdom');
const PAGES = ['activity-1', 'activity-2', 'activity-3', 'activity-4', 'activity-5', 'session-3-history', 'activity-6', 'activity-7'];
for (const slug of PAGES) {
  const source = fs.readFileSync(`docs/${slug}.md`, 'utf8');
  const dom = new JSDOM(fs.readFileSync(`docs/renders/${slug}.html`, 'utf8'));
  let checked = 0;
  // every in-page link resolves: the split into one page per activity must not strand an anchor
  for (const a of dom.window.document.querySelectorAll('.md-typeset a[href^="#"]')) {
    const id = decodeURIComponent(a.getAttribute('href').slice(1));
    assert.ok(dom.window.document.getElementById(id), `${slug}: link to missing anchor #${id}`);
  }
  for (const match of source.matchAll(/^### [^\n]*\{ #(a[1-7]-[\w-]+|hist-[1-4]) \}\r?\n([\s\S]*?)(?=^### |^## |$(?![\s\S]))/gm)) {
    const [, id, body] = match;
    const numbers = [...body.matchAll(/^(\d+)\. /gm)].map(m => Number(m[1]));
    if (!numbers.length) {
      // a listen-only section (7.3 since 18 Sep 2026): acknowledgement checkboxes and no procedure at all
      assert.ok(/^- \[ \] /m.test(body), `${id}: missing numbered procedure`);
      const heading = dom.window.document.getElementById(id);
      assert.ok(heading, `${id}: missing rendered heading`);
      let lists = 0, boxes = 0;
      for (let el = heading.nextElementSibling; el && !/^H[23]$/.test(el.tagName); el = el.nextElementSibling) {
        if (el.tagName === 'OL') lists++;
        boxes += el.querySelectorAll('input[type="checkbox"]').length;
      }
      assert.equal(lists, 0, `${id}: listen-only section renders a numbered list`);
      assert.ok(boxes, `${id}: listen-only section renders no checkboxes`);
      checked++;
      continue;
    }
    assert.deepEqual(numbers, numbers.map((_, i) => i + 1), `${id}: source numbering restarts`);
    const heading = dom.window.document.getElementById(id);
    assert.ok(heading, `${id}: missing rendered heading`);
    let next = 1;
    for (let el = heading.nextElementSibling; el && !/^H[23]$/.test(el.tagName); el = el.nextElementSibling) {
      if (el.tagName !== 'OL') continue;
      const start = Number(el.getAttribute('start') || 1);
      assert.equal(start, next, `${id}: rendered numbering restarts`);
      // extra.css draws the step number from a CSS counter, which ignores start=; hooks/steps.py must seed it
      const expectReset = start > 1 ? `step ${start - 1}` : '';
      assert.equal(el.style.getPropertyValue('counter-reset'), expectReset, `${id}: displayed number does not honour start=${start}`);
      next += [...el.children].filter(child => child.tagName === 'LI').length;
    }
    assert.equal(next - 1, numbers.length, `${id}: rendered steps missing or merged`);
    checked++;
  }
  console.log(`PASS ${slug}: ${checked} procedures have continuous source and rendered numbering, all anchors resolve`);
  dom.window.close();
}
