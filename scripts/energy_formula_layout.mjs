/** Reuse the native table exemplar for two prominent, editable energy equations. */
export function energyFormulaLayout(slideId, elements, spec) {
 const req=[];
 const color={red:22/255,green:62/255,blue:51/255};
 const box=(n,text,x,y,w,h,size,bold=false)=>{
  const e=elements.find(e=>e.objectId===`${slideId}_e${n}`);
  const pt=d=>d.magnitude/(d.unit==='EMU'?12700:1);
  req.push({updatePageElementTransform:{objectId:e.objectId,applyMode:'ABSOLUTE',transform:{scaleX:w/pt(e.size.width),scaleY:h/pt(e.size.height),translateX:x,translateY:y,unit:'PT'}}},
   {deleteText:{objectId:e.objectId,textRange:{type:'ALL'}}},{insertText:{objectId:e.objectId,text,insertionIndex:0}},
   {updateTextStyle:{objectId:e.objectId,textRange:{type:'ALL'},style:{fontFamily:'Prompt',fontSize:{magnitude:size,unit:'PT'},bold,foregroundColor:{opaqueColor:{rgbColor:color}}},fields:'fontFamily,fontSize,bold,foregroundColor'}},
   {updateParagraphStyle:{objectId:e.objectId,textRange:{type:'ALL'},style:{alignment:'START',lineSpacing:100,spaceAbove:{magnitude:0,unit:'PT'},spaceBelow:{magnitude:0,unit:'PT'}},fields:'alignment,lineSpacing,spaceAbove,spaceBelow'}});
 };
 for(const n of [0,1,2,3,12,13,14,15])req.push({deleteObject:{objectId:`${slideId}_e${n}`}});
 box(16,spec.headings[0],35,117,650,30,19,true);
 box(8,spec.formulas[0],35,149,650,48,28,true);
 box(9,spec.explanations[0],35,204,650,43,17);
 box(17,spec.headings[1],35,259,650,30,19,true);
 box(10,spec.formulas[1],35,291,650,48,27,true);
 box(11,spec.explanations[1],35,344,650,45,17);
 return req;
}
