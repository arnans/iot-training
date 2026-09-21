/** Build native Google Slides requests from the approved Activity 1 exemplars.
 * This script writes private batches only; the connected Slides tool applies them.
 * Usage: node scripts/build_workshop_slides.mjs SOURCE_JSON OUTPUT_DIR
 */
import fs from 'node:fs';
import path from 'node:path';
import {conceptLayout} from './concept_slide_layout.mjs';
import {energyFormulaLayout} from './energy_formula_layout.mjs';
const [sourceFile, outputDir] = process.argv.slice(2);
if (!sourceFile || !outputDir) throw new Error('Usage: node scripts/build_workshop_slides.mjs SOURCE_JSON OUTPUT_DIR');
const source = JSON.parse(fs.readFileSync(sourceFile, 'utf8').replace(/^\uFEFF/, ''));
const manifest = JSON.parse(fs.readFileSync('planning/slides/activity-2-8.json', 'utf8'));
const rgb = hex => ({red:parseInt(hex.slice(0,2),16)/255,green:parseInt(hex.slice(2,4),16)/255,blue:parseInt(hex.slice(4,6),16)/255});
const color = {green:'163E33',cream:'F6F2E8',sage:'617D6D',ink:'263E34',gold:'D3AD65',ochre:'A3652C'};
const exemplars = {cover:'a1_cover',visual:'a1_slide_5',dark:'a1_slide_4',table:'a1_slide_6',split:'a1_slide_7'};
const index = new Map(source.slides.map(s=>[s.objectId,s]));
function imageDimensions(file) {
 const b=fs.readFileSync(file);
 if(b.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10]))) return {width:b.readUInt32BE(16),height:b.readUInt32BE(20)};
 if(b[0]===255&&b[1]===216){
  let p=2;
  while(p<b.length){
   if(b[p++]!==255)continue;
   while(b[p]===255)p++;
   const marker=b[p++];
   if(marker===217||marker===218)break;
   if(marker===216||marker===1||(marker>=208&&marker<=215))continue;
   const len=b.readUInt16BE(p);
   if([192,193,194,195,197,198,199,201,202,203,205,206,207].includes(marker))return {height:b.readUInt16BE(p+3),width:b.readUInt16BE(p+5)};
   p+=len;
  }
 }
 throw new Error(`Unsupported image dimensions: ${file}`);
}
fs.mkdirSync(outputDir,{recursive:true});
const batches=[];
for(const slide of manifest.slides){
 const ref=index.get(exemplars[slide.type]);
 if(!ref) throw new Error(`Missing exemplar ${slide.type}`);
 const activity=manifest.activities.find(a=>a.n===slide.activity);
 const map=Object.fromEntries([[ref.objectId,slide.id],...ref.pageElements.map((e,i)=>[e.objectId,`${slide.id}_e${i}`])]);
 const req=[{duplicateObject:{objectId:ref.objectId,objectIds:map}}];
 const id=old=>map[old];
 const del=old=>req.push({deleteObject:{objectId:id(old)}});
 const geo=(old,x,y,w,h)=>{
  const e=ref.pageElements.find(e=>e.objectId===old); if(!e)throw new Error(old);
  const sw=e.size.width.magnitude/(e.size.width.unit==='EMU'?12700:1),sh=e.size.height.magnitude/(e.size.height.unit==='EMU'?12700:1);
  req.push({updatePageElementTransform:{objectId:id(old),applyMode:'ABSOLUTE',transform:{scaleX:w/sw,scaleY:h/sh,translateX:x,translateY:y,unit:'PT'}}});
 };
 const txt=(old,text,size,hex,bold=false)=>{
  if(!id(old))throw new Error(old);
  req.push({deleteText:{objectId:id(old),textRange:{type:'ALL'}}},{insertText:{objectId:id(old),text,insertionIndex:0}});
  if(size)req.push({updateTextStyle:{objectId:id(old),textRange:{type:'ALL'},style:{fontFamily:'Prompt',fontSize:{magnitude:size,unit:'PT'},bold,foregroundColor:{opaqueColor:{rgbColor:rgb(hex)}}},fields:'fontFamily,fontSize,bold,foregroundColor'}});
 };
 const para=(old,alignment='START')=>req.push({updateParagraphStyle:{objectId:id(old),textRange:{type:'ALL'},style:{alignment,lineSpacing:100,spaceAbove:{magnitude:0,unit:'PT'},spaceBelow:{magnitude:0,unit:'PT'}},fields:'alignment,lineSpacing,spaceAbove,spaceBelow'}});
 let imagePath=null;
 const image=(old,file,x,y,w,h)=>{
  imagePath=path.resolve(file).replaceAll('\\','/');
  if(!fs.existsSync(imagePath))throw new Error(`Missing ${file}`);
  geo(old,x,y,w,h);
  req.push({replaceImage:{imageObjectId:id(old),url:imagePath,imageReplaceMethod:'CENTER_CROP'}});
 };
 const header=n=>{
  txt(`a1_${n}_activity`,`กิจกรรมที่ ${slide.activity}  /  ${activity.label}`,10.5,slide.type==='dark'?color.cream:color.sage);
  txt(`a1_${n}_title`,slide.title,slide.titleFontSize??(slide.type==='split'?29:28),slide.type==='dark'?color.cream:color.green,true);
  if(slide.type!=='split'){
   const b=slide.titleBox??{x:30,y:44,w:660,h:52};
   geo(`a1_${n}_title`,b.x,b.y,b.w,b.h);
  }
  if(slide.section)txt(`a1_${n}_section`,slide.section,18,slide.type==='dark'||slide.type==='split'?color.green:'FFFFFF',true);
  else{
   del(`badge_a1_${n}_section`);geo(`a1_${n}_section`,574,12,111,28);
   txt(`a1_${n}_section`,slide.title.includes('ก่อน')?'เตรียมพร้อม':'ท้ายกิจกรรม',12,slide.type==='dark'||slide.type==='split'?color.cream:color.green,true);
  }
 };
 if(slide.type==='cover'){
  txt('cover_sample_activity',`กิจกรรมที่ ${slide.activity}  /  ${activity.en}`,14,color.ochre,true);
  txt('cover_sample_title',slide.title,34,color.green,true);
  txt('cover_duration',`${activity.minutes} นาที`,14,color.sage);
  txt('cover_purpose',slide.purpose,17,color.ink);
  image('cover_warm_a1_farm_panorama',slide.image,0,0,720,190);
 }else if(slide.type==='visual'){
  header(5);
  if(slide.concept){
   imagePath=path.resolve(slide.image).replaceAll('\\','/');
   const mapped=old=>({...ref.pageElements.find(e=>e.objectId===old),objectId:id(old)});
   req.push(...conceptLayout(slide.id,slide.concept,mapped('a1_5_board'),mapped('a1_5_task'),imagePath));
  }else{
  const dims=imageDimensions(slide.image);
  const ratio=dims.width/dims.height;
  const wide=ratio>2.3;
  const box=wide?{x:35,y:166,w:650,h:219}:{x:282,y:116,w:403,h:272};
  const scale=Math.min(box.w/dims.width,box.h/dims.height),w=dims.width*scale,h=dims.height*scale;
  image('a1_5_board',slide.image,box.x+(box.w-w)/2,box.y+(box.h-h)/2,w,h);
  geo('a1_5_task',35,wide?107:126,wide?650:232,wide?55:246);
  txt('a1_5_task',slide.caption,wide?18:19,color.ink);para('a1_5_task');
  }
 }else if(slide.type==='dark'){
  header(4);
  for(const [old,line,y] of [['a1_4_route',slide.lines[0],122],['a1_4_name',slide.lines[1],208],['a1_4_ip',slide.lines[2],294]]){geo(old,88,y,597,79);txt(old,line,21,color.cream);para(old);}
  for(const [old,num,y] of [['a1_4_name_label','01',124],['a1_4_ip_label','02',210],['a1_4_hint','03',296]]){geo(old,35,y,49,47);txt(old,num,25,color.gold,true);para(old);}
 }else if(slide.type==='table'){
  header(6);
  if(slide.energyFormula){
   req.push(...energyFormulaLayout(slide.id,ref.pageElements.map(e=>({...e,objectId:id(e.objectId)})),slide.energyFormula));
  }else{
  txt('rd_6_col1',slide.heads[0],16,color.sage,true);txt('rd_6_col2',slide.heads[1],16,color.sage,true);
  geo('rd_6_col1',35,114,300,32);geo('rd_6_col2',367,114,318,32);
  for(let i=0;i<4;i++){
   geo(`a1_6_action${i}`,35,151+i*56,320,54);txt(`a1_6_action${i}`,slide.rows[i][0],18,color.ink);para(`a1_6_action${i}`);
   geo(`a1_6_result${i}`,367,151+i*56,318,54);txt(`a1_6_result${i}`,slide.rows[i][1],18,color.ink);para(`a1_6_result${i}`);
   geo(`rd_6_rule${i}`,35,204+i*56,650,0.7);
  }
  }
 }else if(slide.type==='split'){
  header(7);geo('a1_7_title',29,48,321,101);
  const sets=[['a1_7_num','a1_7_numval','a1_7_meaning',slide.left,35,color.green,color.ink,color.sage],['a1_7_state','a1_7_stateval','a1_7_meaning2',slide.right,391,color.gold,color.cream,color.cream]];
  for(const [head,body,foot,text,x,hc,bc,fc]of sets){geo(head,x,178,294,50);txt(head,text[0],23,hc,true);geo(body,x,237,294,94);txt(body,text[1],22,bc);geo(foot,x,341,294,50);txt(foot,text[2],16,fc);}
  if(slide.formulaFocus){
   for(const [head,body,foot,text,x,w,hc,bc]of [['a1_7_num','a1_7_numval','a1_7_meaning',slide.left,35,300,color.green,color.ink],['a1_7_state','a1_7_stateval','a1_7_meaning2',slide.right,385,310,color.gold,color.cream]]){
    geo(head,x,178,w,36);txt(head,text[0],21,hc,true);para(head);
    geo(foot,x,224,w,76);txt(foot,text[2],36,hc,true);para(foot);
    geo(body,x,318,w,73);txt(body,text[1],18,bc);para(body);
   }
  }
 }
 batches.push({id:slide.id,activity:slide.activity,exemplar:ref.objectId,requests:req,image_uris:imagePath,notes:`${slide.title.replaceAll('\n',' ')}\nใบงานกิจกรรมที่ ${slide.activity}${slide.section?' ข้อ '+slide.section:''}\n${slide.notes}\n\n[Sources]\nเนื้อหา: docs/activity-${slide.activity}.md\n${slide.image?'ภาพ: '+slide.image+'\n':''}${(slide.sources||[]).join('\n')}\n[/Sources]`});
}
fs.writeFileSync(path.join(outputDir,'batches.json'),JSON.stringify(batches));
fs.writeFileSync(path.join(outputDir,'slide-plan.json'),JSON.stringify(batches.map(b=>({id:b.id,activity:b.activity,exemplar:b.exemplar,image:b.image_uris?path.relative(process.cwd(),b.image_uris):null})),null,2));
console.log(JSON.stringify({slides:batches.length,images:batches.filter(b=>b.image_uris).length,requests:batches.reduce((n,b)=>n+b.requests.length,0)}));
