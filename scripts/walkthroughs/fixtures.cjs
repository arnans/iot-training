// Home Assistant state some walkthroughs need (test site only).
//   node fixtures.cjs show            list automations/helpers/dashboards
//   node fixtures.cjs get <id>        print an automation's config
//   node fixtures.cjs put <id> <json> create/replace an automation config
//   node fixtures.cjs del-auto <id> | del-helper <input_boolean id> | del-dash <dashboard id>
const C = require('./config.cjs'); const { chromium } = require(C.PW);
(async () => {
  let [cmd, a, b2] = process.argv.slice(2); if (b2 && b2.endsWith('.json')) b2 = require('fs').readFileSync(b2, 'utf8');
  const b = await chromium.launch({ channel: 'chrome', headless: true });
  const ctx = await b.newContext({ storageState: C.STATE }); const p = await ctx.newPage();
  await p.goto(C.HA + '/config/automation/dashboard'); await p.waitForTimeout(3500);
  const r = await p.evaluate(async ([cmd, a, b2]) => {
    const h = document.querySelector('home-assistant').hass;
    if (cmd === 'show') return { automations: Object.values(h.states).filter(s => s.entity_id.startsWith('automation.')).map(s => [s.attributes.id, s.attributes.friendly_name, s.state]),
      helpers: await h.callWS({ type: 'input_boolean/list' }), dashboards: await h.callWS({ type: 'lovelace/dashboards/list' }) };
    if (cmd === 'get') return h.callApi('GET', 'config/automation/config/' + a);
    if (cmd === 'put') return h.callApi('POST', 'config/automation/config/' + a, JSON.parse(b2));
    if (cmd === 'del-auto') return h.callApi('DELETE', 'config/automation/config/' + a);
    if (cmd === 'del-helper') return h.callWS({ type: 'input_boolean/delete', input_boolean_id: a });
    if (cmd === 'del-dash') return h.callWS({ type: 'lovelace/dashboards/delete', dashboard_id: a });
  }, [cmd, a, b2]);
  console.log(JSON.stringify(r, null, 1));
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
