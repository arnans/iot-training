// Shared helpers for walkthrough specs
const clk = async (p, l) => { l = l.first(); await l.waitFor({ state: 'attached', timeout: 8000 });
  for (let i = 0; i < 30; i++) { const b = await l.boundingBox(); if (b && b.y + b.height < 600 && b.y > 60) break; await p.mouse.move(450, 400); await p.mouse.wheel(0, b && b.y < 60 ? -80 : 80); await p.waitForTimeout(90); }
  const b = await l.boundingBox(); await p.mouse.click(b.x + Math.min(b.width / 2, 80), b.y + b.height / 2); };
const dlg = p => p.locator('add-automation-element-dialog');
const pick = s => async p => clk(p, dlg(p).getByText(s));
const btn = s => async p => clk(p, p.getByRole('button', { name: s }));
const type = s => async p => p.keyboard.type(s);
// like clk but only shows the click (ripple) without pressing — for a final Save we must not commit
const show = l => async p => { l = l(p).first(); await l.waitFor({ state: 'visible', timeout: 8000 }); const b = await l.boundingBox(); await p.mouse.fakeClick(b.x + Math.min(b.width / 2, 80), b.y + b.height / 2); };
const showAt = (x, y) => async p => p.mouse.fakeClick(x / 1.2, y / 1.2);  // ripple without pressing
const at = (x, y) => async p => p.mouse.click(x / 1.2, y / 1.2);          // screenshot-pixel coordinates
const nameIt = s => async p => { await p.keyboard.press('Control+A'); await p.keyboard.type(s); };
// final dialog Save (inside ha-dialog) — used by --commit to really save
const saveDialog = async p => p.mouse.click(877 / 1.2, 566 / 1.2);  // the naming dialog's Save (same spot in every editor)
// click the smallest visible element (anywhere, through shadow roots) whose trimmed text is exactly s; topmost match wins
const findText = async (p, s, nth = -1) => p.evaluate(([s, nth]) => {
  const hits = []; const walk = n => { for (const c of n.children || []) { if (c.shadowRoot) walk(c.shadowRoot); walk(c); } };
  const all = []; (function w(n) { for (const c of (n.children || [])) { all.push(c); if (c.shadowRoot) w(c.shadowRoot); w(c); } })(document);
  for (const e of all) { if ((e.textContent || '').trim() !== s) continue; const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
    if ([...e.children].some(ch => (ch.textContent || '').trim() === s)) continue;
    const st = getComputedStyle(e); if (st.visibility === 'hidden' || st.display === 'none') continue; hits.push({ x: r.x + r.width / 2, y: r.y + r.height / 2, w: r.width }); }
  return hits.length ? hits[nth < 0 ? hits.length + nth : nth] : null; }, [s, nth]);
const txt = (s, nth) => async p => { let h; for (let i = 0; i < 40 && !(h = await findText(p, s, nth)); i++) await p.waitForTimeout(200); if (!h) throw new Error('text not found: ' + s); await p.mouse.click(h.x, h.y); };
module.exports = { showAt, txt, findText, clk, dlg, pick, btn, type, show, at, nameIt, saveDialog };
