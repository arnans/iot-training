/** Shared native layout for the approved two-scene automation illustrations. */
export function conceptLayout(slideId, spec, imageElement, instructionElement, imagePath) {
 const requests=[];
 const rgbColor={red:22/255,green:62/255,blue:51/255};
 const geometry=(element,x,y,w,h)=>{
  const pt=d=>d.magnitude/(d.unit==='EMU'?12700:1);
  requests.push({updatePageElementTransform:{objectId:element.objectId,applyMode:'ABSOLUTE',transform:{scaleX:w/pt(element.size.width),scaleY:h/pt(element.size.height),translateX:x,translateY:y,unit:'PT'}}});
 };
 const style=(id,size,bold)=>requests.push(
  {updateTextStyle:{objectId:id,textRange:{type:'ALL'},style:{fontFamily:'Prompt',fontSize:{magnitude:size,unit:'PT'},bold,foregroundColor:{opaqueColor:{rgbColor}}},fields:'fontFamily,fontSize,bold,foregroundColor'}},
  {updateParagraphStyle:{objectId:id,textRange:{type:'ALL'},style:{alignment:'START',lineSpacing:100,spaceAbove:{magnitude:0,unit:'PT'},spaceBelow:{magnitude:0,unit:'PT'}},fields:'alignment,lineSpacing,spaceAbove,spaceBelow'}}
 );
 const add=(suffix,text,x,y,w,h,size,bold=false)=>{
  const id=`${slideId}_${suffix}`;
  requests.push({createShape:{objectId:id,shapeType:'TEXT_BOX',elementProperties:{pageObjectId:slideId,size:{width:{magnitude:w,unit:'PT'},height:{magnitude:h,unit:'PT'}},transform:{scaleX:1,scaleY:1,translateX:x,translateY:y,unit:'PT'}}}},{insertText:{objectId:id,text,insertionIndex:0}});
  style(id,size,bold);
 };
 const compact=Boolean(spec.footer);
 geometry(imageElement,compact?105:60,103,compact?510:600,compact?170:200);
 requests.push({replaceImage:{imageObjectId:imageElement.objectId,url:imagePath,imageReplaceMethod:'CENTER_CROP'}});
 geometry(instructionElement,35,compact?302:329,315,compact?79:70);
 requests.push({deleteText:{objectId:instructionElement.objectId,textRange:{type:'ALL'}}},{insertText:{objectId:instructionElement.objectId,text:spec.left,insertionIndex:0}});
 style(instructionElement.objectId,15,false);
 add('action_instructions',spec.right,380,compact?302:329,310,compact?79:70,15);
 add('trigger_heading',spec.leftTitle,35,compact?276:303,320,27,17,true);
 add('action_heading',spec.rightTitle,380,compact?276:303,310,27,17,true);
 if(spec.showArrow!==false)add('flow_arrow','→',336,compact?168:183,50,50,33,true);
 if(spec.footer)add('worksheet_note',spec.footer,35,382,650,22,12);
 return requests;
}
