const { txt, pick, btn, type, at, nameIt, saveDialog } = require('../lib.cjs');
module.exports = {
  id: 'a4-7-watering-on',
  title: { kicker: 'กิจกรรมที่ 4.7 · สร้างกฎรดน้ำ', head: 'สร้างกฎเปิดปั๊มเมื่ออากาศแห้ง', name: 'รดน้ำ - เปิดปั๊ม' },
  steps: [
    [2, 'ส่วน When กด + Add trigger', btn('Add trigger'), 'click'],
    [2, 'พิมพ์ “ความชื้นอากาศ” เพื่อค้นหา', type('ความชื้นอากาศ'), 'type'],
    [2, 'กดที่ ความชื้นอากาศ (humidity)', pick('ความชื้นอากาศ (humidity)'), 'click'],
    [2, 'เลือก Relative humidity crossed threshold', pick('Relative humidity crossed threshold'), 'click'],
    [2, 'Threshold type กดช่อง Fire when the value goes', at(935, 657), 'click'],
    [2, 'เลือก Below — ความชื้นลดลงต่ำกว่าเกณฑ์', txt('Below'), 'click'],
    [2, 'กดช่อง Below', at(900, 783), 'click'],
    [2, 'ใส่ค่าที่สูงกว่าค่าห้องเล็กน้อย (ตัวอย่าง 70 %)', type('70'), 'type'],
    [3, 'ส่วน Then do กด + Add action', btn('Add action'), 'click'],
    [3, 'พิมพ์ “รีเลย์” เพื่อค้นหา', type('รีเลย์'), 'type'],
    [3, 'กดที่ รีเลย์ (relay) ของกลุ่ม', pick('รีเลย์ (relay)'), 'click'],
    [3, 'เลือก Turn on switch — สั่งเปิดปั๊ม', pick('Turn on switch'), 'click'],
    [3, 'กด Save', btn('Save'), 'click'],
    [3, 'ตั้งชื่อ รดน้ำ - เปิดปั๊ม แล้วกด Save', nameIt('รดน้ำ - เปิดปั๊ม'), 'type'],
  ],
  commit: saveDialog,
};
