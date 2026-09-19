const { txt, clk, pick, btn, type, at, nameIt } = require('../lib.cjs');
module.exports = {
  id: 'a3-6-timer-off',
  title: { kicker: 'กิจกรรมที่ 3.6 · โจทย์เสริม', head: 'สร้างกฎปิดไฟตามเวลา', name: 'ปิดไฟตามเวลา' },
  steps: [
    [2, 'ส่วน When กด + Add trigger', btn('Add trigger'), 'click'],
    [2, 'พิมพ์ “time” เพื่อค้นหา', type('time'), 'type'],
    [2, 'เลือก Time', txt('Time'), 'click'],
    [2, 'ช่อง At time กดช่องชั่วโมง (hh)', at(770, 412), 'click'],
    [2, 'ใส่เวลาประมาณ 2 นาทีข้างหน้า (ตัวอย่าง 4:30 PM)', async p => { await p.keyboard.type('4'); await p.mouse.click(845 / 1.2, 412 / 1.2); await p.keyboard.type('30'); }, 'type'],
    [2, 'กดช่อง AM/PM', at(1000, 412), 'click'],
    [2, 'เลือก PM — เวลาช่วงบ่าย', txt('PM', -1), 'click'],
    [2, 'ส่วน Then do กด + Add action', btn('Add action'), 'click'],
    [2, 'พิมพ์ “รีเลย์” เพื่อค้นหา', type('รีเลย์'), 'type'],
    [2, 'กดที่ รีเลย์ (relay)', pick('รีเลย์ (relay)'), 'click'],
    [2, 'เลือก Turn off switch — สั่งปิดไฟ', pick('Turn off switch'), 'click'],
    [2, 'กด Save', btn('Save'), 'click'],
    [2, 'ตั้งชื่อ ปิดไฟตามเวลา แล้วกด Save', nameIt('ปิดไฟตามเวลา'), 'type'],
  ],
};
