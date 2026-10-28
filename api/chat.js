export default async function handler(req,res){
res.setHeader('Cache-Control','no-store');
if(req.method!=='POST'){res.setHeader('Allow','POST');return res.status(405).json({error:'Method not allowed'});}
const key=process.env.GEMINI_API_KEY;
if(!key)return res.status(503).json({error:'Gemini API key is missing from this deployment. In Vercel, open the tnstc-bus-3d project, add GEMINI_API_KEY under Settings > Environment Variables for Production, save it, then redeploy the latest deployment. Do not enter your key in this chat.'});
const origin=req.headers.origin,host=req.headers.host;
if(origin){try{if(new URL(origin).host!==host)return res.status(403).json({error:'Origin not allowed'});}catch{return res.status(403).json({error:'Invalid origin'});}}
const {message,history}=req.body||{};
if(typeof message!=='string'||!message.trim()||message.length>3000||!Array.isArray(history)||history.length>12)return res.status(400).json({error:'Invalid message or history'});
const contents=history.filter(x=>x&&['user','assistant'].includes(x.role)&&typeof x.content==='string'&&x.content.length<=3000).map(x=>({role:x.role==='assistant'?'model':'user',parts:[{text:x.content}]}));
contents.push({role:'user',parts:[{text:message.trim()}]});
try{
const model=process.env.GEMINI_MODEL||'gemini-2.5-flash';
const r=await fetch('https://generativelanguage.googleapis.com/v1beta/models/'+encodeURIComponent(model)+':generateContent',{method:'POST',headers:{'Content-Type':'application/json','x-goog-api-key':key},body:JSON.stringify({systemInstruction:{parts:[{text:'You are the AI 3D Studio assistant. Help users develop clear text-to-3D prompts, GLB workflow ideas, model materials, camera angles, and 3D presentation advice. Be concise. You cannot generate or attach actual GLB files; never claim to have generated a model.'}]},contents,generationConfig:{maxOutputTokens:700}}),signal:AbortSignal.timeout(25000)});
const data=await r.json();
if(!r.ok){console.error('Gemini API error',{status:r.status,reason:data?.error?.status});let error='Gemini service unavailable. Try again later.',status=502;if(r.status===429){status=429;error='Gemini free-tier quota or rate limit reached. Check Google AI Studio usage and try again later.';}else if(r.status===400){error='Gemini rejected the request. Check model configuration.';}else if(r.status===401||r.status===403){error='Gemini API key invalid or access denied. Check GEMINI_API_KEY in Vercel.';}else if(r.status===404){error='Gemini model unavailable. Check GEMINI_MODEL in Vercel.';}else if(r.status>=500){error='Gemini is temporarily unavailable. Try again later.';}return res.status(status).json({error});}
const reply=(data.candidates?.[0]?.content?.parts||[]).filter(x=>typeof x.text==='string').map(x=>x.text).join('\n').trim();
return res.status(200).json({reply:reply||'Gemini returned no text. Please try another prompt.'});
}catch(e){console.error('Gemini request failed',e?.name);return res.status(502).json({error:'Unable to reach Gemini. Try again.'});}
}