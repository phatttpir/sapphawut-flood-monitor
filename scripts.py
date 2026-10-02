import json,requests,pandas as pd
from datetime import datetime,timezone
u='https://ichpp.egat.co.th/hydrointernet/statusdam_report_internet.php'
o={'source':u,'updated':datetime.now(timezone.utc).isoformat(),'rows':[]}
try:
 t=next((x for x in pd.read_html(requests.get(u,timeout=30).text) if 'เขื่อน' in ' '.join(map(str,x.columns))),None)
 if t is not None:
  t.columns=[' '.join(map(str,c)).replace('nan','').strip() if isinstance(c,tuple) else str(c) for c in t.columns]
  def g(r,k):
   c=next((c for c in t.columns if any(z in c for z in k)),None); return '' if c is None or pd.isna(r[c]) else str(r[c]).strip()
  for _,r in t.iterrows():
   dam=g(r,['เขื่อน'])
   if dam:o['rows'].append({'dam':dam,'level':g(r,['ระดับกักเก็บปัจจุบัน']),'max':g(r,['ระดับกักเก็บสูงสุด']),'inflow':g(r,['ปริมาณน้ำไหลเข้าอ่าง']),'release':g(r,['ระบายน้ำผ่าน','ระบายผ่าน']),'updated':datetime.now().astimezone().strftime('%d/%m/%Y %H:%M')})
except Exception as e:o['error']=str(e)
open('data/egat.json','w',encoding='utf8').write(json.dumps(o,ensure_ascii=False,indent=2))
