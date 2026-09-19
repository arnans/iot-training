const { showAt, txt, clk, btn, type, at, nameIt, show } = require('../lib.cjs');
module.exports = {
  id: 'a4-8a-auto-mode-helper',
  start: '/',
  title: { kicker: 'กิจกรรมที่ 4.8 · โหมด Auto และ Manual', head: 'สร้างสวิตช์เลือกโหมด', name: 'Pump Auto Mode', nameLabel: 'ชื่อสวิตช์', sub: 'Settings → Devices & services → Helpers → Create helper' },
  steps: [
    [1, 'เปิด Settings จากเมนูด้านซ้าย', txt('Settings'), 'click'],
    [1, 'กด Devices & services', txt('Devices & services'), 'click'],
    [1, 'เลือกแท็บ Helpers', txt('Helpers'), 'click'],
    [2, 'กด + Create helper', txt('Create helper'), 'click'],
    [2, 'พิมพ์ “Toggle” เพื่อค้นหา', type('Toggle'), 'type'],
    [2, 'เลือก Toggle', txt('Toggle'), 'click'],
    [3, 'กดช่อง Name', at(587, 343), 'click'],
    [3, 'ตั้งชื่อ Pump Auto Mode', type('Pump Auto Mode'), 'type'],
    [3, 'กด Create', showAt(870, 634), 'click'],
  ],
  commit: async p => p.mouse.click(870 / 1.2, 634 / 1.2),   // the real Create, for --commit setup runs
};
