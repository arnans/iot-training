// Paths and HA connection for the walkthrough recorder.
// HA_URL, HA_USER, HA_PASS come from the environment; the login is never stored in the repo.
const path = require('path');
const ROOT = path.resolve(__dirname, '../..');
module.exports = {
  PW: process.env.PLAYWRIGHT_CORE || path.join(process.env.APPDATA || '', 'npm/node_modules/n8n/node_modules/playwright-core'),
  HA: (process.env.HA_URL || 'http://192.168.8.163').replace(/\/$/, ''),
  WORK: path.join(ROOT, '.tmp/walkthroughs'),           // git-ignored: login state, frames, cards
  STATE: path.join(ROOT, '.tmp/walkthroughs/ha-state.json'),
  OUT: path.join(ROOT, 'docs/images/walkthroughs'),
  spec: name => require(path.join(__dirname, 'specs', name.replace(/\.cjs$/, '') + '.cjs')),
};
