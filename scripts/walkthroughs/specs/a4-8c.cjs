const { txt, btn, type, at, pick } = require('../lib.cjs');
module.exports = {
  id: 'a4-8c-auto-mode-condition',
  start: '/config/automation/dashboard',
  title: { kicker: 'กิจกรรมที่ 4.8 · โหมด Auto และ Manual', head: 'ให้กฎรดน้ำตรวจโหมดก่อนสั่งปั๊ม', name: 'รดน้ำ - เปิดปั๊ม', sub: 'Settings → Automations & scenes → รดน้ำ - เปิดปั๊ม' },
  steps: [
    [7, 'เปิดกฎ รดน้ำ - เปิดปั๊ม', txt('รดน้ำ - เปิดปั๊ม'), 'click'],
    [8, 'ส่วน And if กด + Add condition', btn('Add condition'), 'click'],
    [8, 'พิมพ์ “Pump Auto Mode” เพื่อค้นหา', type('Pump Auto Mode'), 'type'],
    [8, 'กดที่ helper Pump Auto Mode', pick('Pump Auto Mode'), 'click'],
    [8, 'เลือกเงื่อนไข Switch is on — ทำงานเฉพาะโหมด Auto', pick('Switch is on'), 'click'],
    [8, 'กด Save', btn('Save'), 'click'],
  ],
};
