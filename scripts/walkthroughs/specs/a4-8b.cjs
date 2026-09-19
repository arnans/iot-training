const { showAt, txt, btn, type, at } = require('../lib.cjs');
module.exports = {
  id: 'a4-8b-farm-dashboard',
  start: '/',
  title: { kicker: 'กิจกรรมที่ 4.8 · โหมด Auto และ Manual', head: 'เปิดใช้แดชบอร์ดเพื่อดูสวิตช์โหมด', name: 'Farm Dashboard', nameLabel: 'ชื่อแดชบอร์ด', sub: 'Settings → Dashboards → Add dashboard' },
  steps: [
    [4, 'เปิด Settings จากเมนูด้านซ้าย', txt('Settings'), 'click'],
    [4, 'กด Dashboards', txt('Dashboards'), 'click'],
    [4, 'กด + Add dashboard', txt('Add dashboard'), 'click'],
    [5, 'เลือก Overview (Legacy)', txt('Overview (Legacy)'), 'click'],
    [5, 'กดช่อง Title', at(587, 191), 'click'],
    [5, 'ตั้งชื่อ Farm Dashboard', type('Farm Dashboard'), 'type'],
    [5, 'ตรวจว่า Add to sidebar เปิดอยู่', async p => p.mouse.move(877 / 1.2, 642 / 1.2), 'click'],
    [5, 'กด Create', showAt(870, 743), 'click'],
  ],
};
