const { show, showAt, txt, clk, btn, type, at, dlg } = require('../lib.cjs');
module.exports = {
  id: 'a4-3-time-window',
  start: '/config/automation/dashboard',
  title: { kicker: 'กิจกรรมที่ 4.3 · จำกัดช่วงเวลาเปิดไฟ', head: 'เพิ่มเงื่อนไขเวลาให้กฎเปิดไฟ', name: 'มืด-เปิดไฟ', sub: 'Settings → Automations & scenes → มืด-เปิดไฟ' },
  steps: [
    [1, 'เปิดกฎ มืด-เปิดไฟ', txt('มืด-เปิดไฟ'), 'click'],
    [1, 'ส่วน And if กด + Add condition', btn('Add condition'), 'click'],
    [1, 'ในกลุ่ม Time and sun กดที่ Time', async p => clk(p, dlg(p).getByText('Time', { exact: true })), 'click'],
    [1, 'เลือกเงื่อนไข Time — ตรวจว่าตอนนี้อยู่ในช่วงเวลาหรือไม่', txt('Time', -1), 'click'],
    [1, 'ช่อง After กดช่องชั่วโมง', at(770, 412), 'click'],
    [1, 'ใส่ 6:30 (ตัวอย่าง เปิดได้หลัง 18.30 น.)', async p => { await p.keyboard.type('6'); await p.mouse.click(845 / 1.2, 412 / 1.2); await p.keyboard.type('30'); }, 'type'],
    [1, 'กดช่อง AM/PM', at(1000, 412), 'click'],
    [1, 'เลือก PM', txt('PM', -1), 'click'],
    [1, 'ช่อง Before กดช่องชั่วโมง', at(770, 717), 'click'],
    [1, 'ใส่ 7:30 AM (ตัวอย่าง ก่อน 07.30 น. วันถัดไป)', async p => { await p.keyboard.type('7'); await p.mouse.click(845 / 1.2, 717 / 1.2); await p.keyboard.type('30'); await p.keyboard.press('Tab'); }, 'type'],
    [1, 'กด Save', show(p => p.getByRole('button', { name: 'Save' })), 'click'],
  ],
};
