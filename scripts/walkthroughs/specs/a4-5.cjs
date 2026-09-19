const { txt, btn, type, at, pick } = require('../lib.cjs');
module.exports = {
  id: 'a4-5-notification',
  start: '/config/automation/dashboard',
  title: { kicker: 'กิจกรรมที่ 4.5 · ลองเพิ่มการแจ้งเตือน', head: 'ให้กฎเปิดไฟส่งข้อความแจ้งเตือน', name: 'มืด-เปิดไฟ', sub: 'Settings → Automations & scenes → มืด-เปิดไฟ' },
  steps: [
    [1, 'เปิดกฎ มืด-เปิดไฟ', txt('มืด-เปิดไฟ'), 'click'],
    [1, 'ส่วน Then do กด + Add action', btn('Add action'), 'click'],
    [1, 'พิมพ์ “notification” เพื่อค้นหา', type('notification'), 'type'],
    [1, 'เลือก Send a persistent notification', pick('Send a persistent notification'), 'click'],
    [1, 'กดช่อง Message', at(935, 365), 'click'],
    [1, 'พิมพ์ข้อความ เช่น “ไฟสวนเปิดแล้ว”', type('ไฟสวนเปิดแล้ว'), 'type'],
    [1, 'กด Save — ข้อความจะไปอยู่ที่ไอคอนกระดิ่ง', btn('Save'), 'click'],
  ],
};
