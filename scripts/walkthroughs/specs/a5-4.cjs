const { pick, btn, type } = require('../lib.cjs');
module.exports = {
  id: 'a5-4-pump-timeout',
  title: { kicker: 'กิจกรรมที่ 5.4 · ปั๊มเดินนานเกินไป', head: 'สร้างกฎจำกัดเวลาเปิดปั๊ม', name: 'Fail-safe - จำกัดเวลาเปิดปั๊ม' },
  steps: [
    [4, 'ส่วน When กด + Add trigger', btn('Add trigger'), 'click'],
    [4, 'พิมพ์ “รีเลย์” เพื่อค้นหา', type('รีเลย์'), 'type'],
    [4, 'กดที่ รีเลย์ (relay)', pick('รีเลย์ (relay)'), 'click'],
    [4, 'เลือก Switch turned on', pick('Switch turned on'), 'click'],
    [4, 'ช่อง For at least กดช่อง ss (วินาที)', async p => p.mouse.click(916 / 1.2, 516 / 1.2), 'click'],
    [4, 'ใส่ 30 วินาที — ยาวกว่ากฎสั่งแล้วไม่เดิน (15 วินาที)', async p => { await p.keyboard.press('Control+A'); await p.keyboard.type('30'); }, 'type'],
    [5, 'ส่วน Then do กด + Add action', btn('Add action'), 'click'],
    [5, 'พิมพ์ “รีเลย์” เพื่อค้นหา', type('รีเลย์'), 'type'],
    [5, 'กดที่ รีเลย์ (relay)', pick('รีเลย์ (relay)'), 'click'],
    [5, 'เลือก Turn off switch — สั่งหยุดปั๊ม', pick('Turn off switch'), 'click'],
    [5, 'กด + Add action อีกครั้ง เพื่อเพิ่มการแจ้งเตือน', btn('Add action'), 'click'],
    [5, 'พิมพ์ “persistent” เพื่อค้นหา', type('persistent'), 'type'],
    [5, 'เลือก Send a persistent notification', pick('Send a persistent notification'), 'click'],
    [5, 'กดช่อง Message', async p => p.mouse.click(935 / 1.2, 365 / 1.2), 'click'],
    [5, 'พิมพ์ข้อความ “ปั๊มเดินเกินเวลา ตัดการทำงานแล้ว โปรดตรวจสอบ”', type('ปั๊มเดินเกินเวลา ตัดการทำงานแล้ว โปรดตรวจสอบ'), 'type'],
    [3, 'กด Save', btn('Save'), 'click'],
    [3, 'ตั้งชื่อ Fail-safe - จำกัดเวลาเปิดปั๊ม แล้วกด Save', async p => { await p.keyboard.press('Control+A'); await p.keyboard.type('Fail-safe - จำกัดเวลาเปิดปั๊ม'); }, 'type'],
  ],
};
