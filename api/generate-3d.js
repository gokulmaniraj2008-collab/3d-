export default async function handler(req,res){
res.setHeader('Cache-Control','no-store');res.setHeader('Allow','GET, POST');
if(!['GET','POST'].includes(req.method))return res.status(405).json({error:'Method not allowed'});
const key=process.env.MESHY_API_KEY;
if(!key)return res.status(503).json({error:'3D generation is not configured. Add MESHY_API_KEY to Vercel Production environment variables and redeploy. Meshy generation may use paid credits.'});
const origin=req.headers.origin;
if(origin){try{if(new URL(origin).host!==req.headers.host)return res.status(403).json({error:'Origin not allowed'});}catch{return res.status(403).json({error:'Invalid origin'});}}
let url='https://api.meshy.ai/openapi/v2/text-to-3d',options={headers:{Authorization:'Bearer '+key,Accept:'application/json'},signal:AbortSignal.timeout(20000)};
if(req.method==='POST'){
const prompt=req.body?.prompt;
if(typeof prompt!=='string'||!prompt.trim()||prompt.length>600)return res.status(400).json({error:'Enter a model description of 1–600 characters.'});
options.method='POST';options.headers['Content-Type']='application/json';options.body=JSON.stringify({mode:'preview',prompt:prompt.trim(),art_style:'realistic',should_remesh:true});
}else{
const id=req.query?.id;if(typeof id!=='string'||!/^[a-zA-Z0-9_-]{5,100}$/.test(id))return res.status(400).json({error:'Invalid generation task ID.'});
url+='/'+encodeURIComponent(id);
}
try{
const r=await fetch(url,options);const data=await r.json();
if(!r.ok){console.error('Meshy API failure',{status:r.status,code:data?.code});return res.status(r.status===429?429:502).json({error:r.status===401||r.status===403?'Meshy API key invalid or access denied. Check your Meshy account and Vercel key.':r.status===402?'Meshy credits are insufficient. Check your Meshy billing.':r.status===429?'Meshy generation limit reached. Try again later.':'Meshy request failed. Check your account, credits and model settings.'});}
if(req.method==='POST')return res.status(200).json({id:data.result});
return res.status(200).json({status:data.status||'UNKNOWN',progress:data.progress??null,glb:data.status==='SUCCEEDED'?(data.model_urls?.glb||null):null,error:data.task_error?.message||null});
}catch(e){console.error('Meshy request exception',e?.name);return res.status(502).json({error:'Unable to reach the 3D generation service. Try again.'});}
}