// Check source numbering and the actual list starts emitted by the renderer.
// Usage: node scripts/test_worksheet_steps.cjs /path/to/node_modules/jsdom
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { JSDOM } = require(process.argv[2] || 'jsdom');
for (const session of [1, 2, 3]) {
  const source = fs.readFileSync(`docs/session-${session}.md`, 'utf8');
  const dom = new JSDOM(fs.readFileSync(`docs/renders/session-${session}.html`, 'utf8'));
  let checked = 0;
  for (const match of source.matchAll(/^### [^\n]*\{ #(a[1-7]-[\w-]+|hist-[1-4]) \}\r?\n([\s\S]*?)(?=^### |^## |$(?![\s\S]))/gm)) {
    const [, id, body] = match;
    const numbers = [...body.matchAll(/^(\d+)\. /gm)].map(m => Number(m[1]));
    assert.ok(numbers.length, `${id}: missing numbered procedure`);
    assert.deepEqual(numbers, numbers.map((_, i) => i + 1), `${id}: source numbering restarts`);
    const heading = dom.window.document.getElementById(id);
    assert.ok(heading, `${id}: missing rendered heading`);
    let next = 1;
    for (let el = heading.nextElementSibling; el && !/^H[23]$/.test(el.tagName); el = el.nextElementSibling) {
      if (el.tagName !== 'OL') continue;
      assert.equal(Number(el.getAttribute('start') || 1), next, `${id}: rendered numbering restarts`);
      next += [...el.children].filter(child => child.tagName === 'LI').length;
    }
    assert.equal(next - 1, numbers.length, `${id}: rendered steps missing or merged`);
    checked++;
  }
  console.log(`PASS session-${session}: ${checked} procedures have continuous source and rendered numbering`);
  dom.window.close();
}
