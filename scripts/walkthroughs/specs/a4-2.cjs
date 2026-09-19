const { show, showAt, txt, clk, btn, type, at } = require('../lib.cjs');
module.exports = {
  id: 'a4-2-raise-off-threshold',
  start: '/config/automation/dashboard',
  title: { kicker: 'กิจกรรมที่ 4.2 · แยกเกณฑ์เปิดและปิด', head: 'ปรับเกณฑ์ปิดไฟให้สูงกว่าเกณฑ์เปิด', name: 'สว่าง-ปิดไฟ', sub: 'Settings → Automations & scenes → สว่าง-ปิดไฟ' },
  steps: [
    [1, 'เปิดกฎ สว่าง-ปิดไฟ', txt('สว่าง-ปิดไฟ'), 'click'],
    [1, 'กดที่ trigger Illuminance crossed threshold', txt('Illuminance crossed threshold'), 'click'],
    [1, 'กดช่อง Above', at(900, 783), 'click'],
    [1, 'เปลี่ยนเป็นค่าที่สูงกว่าเกณฑ์เปิด (ตัวอย่าง 60 lx)', async p => { await p.keyboard.press('Control+A'); await p.keyboard.type('60'); }, 'type'],
    [2, 'กด Save', show(p => p.getByRole('button', { name: 'Save' })), 'click'],
  ],
};
