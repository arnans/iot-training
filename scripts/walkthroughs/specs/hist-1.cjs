const { txt, clk, btn, type, at } = require('../lib.cjs');
module.exports = {
  id: 'hist-1-history-graph',
  start: '/',
  title: { kicker: 'ช่วงที่ 3 · อ่านข้อมูลย้อนหลัง', head: 'เปิดกราฟดูข้อมูลย้อนหลัง', name: '', sub: 'เมนูด้านซ้าย → History' },
  steps: [
    [1, 'เปิด History จากเมนูด้านซ้าย', txt('History'), 'click'],
    [2, 'กด Add target เพื่อเลือกข้อมูล', txt('Add target'), 'click'],
    [2, 'พิมพ์ “ความชื้นอากาศ” เพื่อค้นหา', type('ความชื้นอากาศ'), 'type'],
    [2, 'กดที่ ความชื้นอากาศ (humidity)', txt('ความชื้นอากาศ (humidity)'), 'click'],
    [2, 'กด Add target อีกครั้ง', txt('Add target'), 'click'],
    [2, 'พิมพ์ “ความสว่าง” เพื่อค้นหา', type('ความสว่าง'), 'type'],
    [2, 'กดที่ ความสว่าง (light)', txt('ความสว่าง (light)', -1), 'click'],
    [2, 'กด Add target อีกครั้ง', txt('Add target'), 'click'],
    [2, 'พิมพ์ “รีเลย์” — สวิตช์ของบอร์ดรีเลย์', type('รีเลย์'), 'type'],
    [2, 'กดที่ รีเลย์ (relay)', txt('รีเลย์ (relay)', -1), 'click'],
    [3, 'กดช่องช่วงเวลาด้านบน', at(920, 100), 'click'],
    [3, 'เลือกช่วงตั้งแต่เริ่มช่วงที่ 2 จนถึงปัจจุบัน (ตัวอย่าง Last 24 hours)', txt('Last 24 hours'), 'click'],
  ],
};
