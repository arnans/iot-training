const { showAt, txt, clk, btn, type, at } = require('../lib.cjs');
// one card: open the +, pick the card type, choose the entity, give it a custom name, Save
const card = (plus, kind, search, entity, name, nameAt) => [
  [2, `กด + เพื่อเพิ่มการ์ด`, plus, 'click'],
  [2, 'เลือกแท็บ By card', txt('By card'), 'click'],
  [2, `พิมพ์ “${kind}” แล้วเลือกการ์ด ${kind}`, async p => { await p.mouse.click(587 / 1.2, 264 / 1.2); await p.keyboard.type(kind.toLowerCase()); await p.waitForTimeout(700); await txt(kind)(p); }, 'click'],
  [2, 'กดช่อง Entity', at(500, 279), 'click'],
  [2, `พิมพ์ “${search}” แล้วกดที่ ${entity}`, async p => { await p.keyboard.type(search); await p.waitForTimeout(700); await txt(entity, -1)(p); }, 'click'],
  ...(kind === 'Tile' ? [[2, 'เปิดส่วน Content', txt('Content'), 'click']] : []),
  [2, 'ช่อง Name เลือก Custom', at(kind === 'Tile' ? 1064 : 1080, kind === 'Tile' ? 432 : 456), 'click'],
  [2, `ตั้งชื่อบนจอ “${name}”`, async p => { await p.mouse.click(584 / 1.2, nameAt / 1.2); await p.keyboard.type(name); }, 'type'],
  [2, 'กด Save', at(1086, 815), 'click'],
];
const scrollThenPlus = async p => { await p.mouse.move(700 / 1.2, 500 / 1.2); await p.mouse.wheel(0, 160); await p.waitForTimeout(600); await p.mouse.click(520 / 1.2, 618 / 1.2); };
module.exports = {
  id: 'a6-3-build-dashboard',
  start: '/',
  title: { kicker: 'กิจกรรมที่ 6.3 · สร้างแดชบอร์ด', head: 'สร้างแดชบอร์ดของแปลงเรา', name: 'แปลง 1', nameLabel: 'ชื่อแดชบอร์ด', sub: 'Settings → Dashboards → Add dashboard → New dashboard from scratch' },
  steps: [
    [1, 'เปิด Settings จากเมนูด้านซ้าย', txt('Settings'), 'click'],
    [1, 'กด Dashboards', txt('Dashboards'), 'click'],
    [1, 'กด + Add dashboard', txt('Add dashboard'), 'click'],
    [1, 'เลือก New dashboard from scratch', txt('New dashboard from scratch'), 'click'],
    [1, 'กดช่อง Title', at(587, 191), 'click'],
    [1, 'ตั้งชื่อ แปลง 1', type('แปลง 1'), 'type'],
    [1, 'ตรวจว่า Add to sidebar เปิดอยู่ แล้วกด Create', at(870, 743), 'click'],
    [2, 'เปิดแดชบอร์ด แปลง 1 จากเมนูด้านซ้าย', txt('แปลง 1', 0), 'click'],
    [2, 'กดไอคอนดินสอเพื่อแก้ไขแดชบอร์ด', at(1130, 33), 'click'],
    ...card(at(520, 487), 'Gauge', 'ความชื้นอากาศ', 'ความชื้นอากาศ (humidity)', 'ความชื้นอากาศ (%)', 518),
    ...card(at(520, 734), 'Tile', 'ลูกลอย', 'สวิตช์ลูกลอย (float switch)', 'ระดับน้ำที่ลูกลอย', 495),
    ...card(at(813, 734), 'Tile', 'รีเลย์', 'รีเลย์ (relay)', 'สั่งปั๊ม', 495),
    ...card(scrollThenPlus, 'Tile', 'Pump Auto Mode', 'Pump Auto Mode', 'โหมดรดน้ำอัตโนมัติ', 495),
    [3, 'จัดการ์ดสำคัญไว้ด้านบน แล้วกด Done', async p => { await p.mouse.click(1009 / 1.2, 33 / 1.2); await p.waitForTimeout(500); await p.mouse.move(640 / 1.2, 650 / 1.2); }, 'click'],
  ],
};
