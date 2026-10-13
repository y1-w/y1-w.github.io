"""Rebuild the self-contained website and CSV from chips.json. Standard library only."""
import csv
import json
from datetime import date
from pathlib import Path
p=Path(__file__).resolve().parent
obj=json.loads((p/'chips.json').read_text(encoding='utf-8'))
assert isinstance(obj['chips'],list) and obj['chips']
ids=[x['id'] for x in obj['chips']]
assert len(ids)==len(set(ids)), 'Duplicate chip IDs'
for chip in obj['chips']:
    assert chip['category'] in obj['taxonomy']
    assert all(s['url'].startswith('https://') for s in chip['sources'])
    for k in ('sram_mb','hbm_gb','hbm_tbps','power_w','die_area_mm2'):
        assert chip[k] is None or (isinstance(chip[k], (int,float)) and chip[k]>=0)
encoded=json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
tmpl=(p/'index.template.html').read_text(encoding='utf8')
assert tmpl.count('__JSON__')==1
snapshot=date.fromisoformat(obj['snapshot_date']).strftime('%d %b %Y').lstrip('0')
(p/'index.html').write_text(tmpl.replace('__JSON__',encoded).replace('__SNAPSHOT__',snapshot),encoding='utf8')
cols='vendor,name,category,year,status,compute,memory_model,sram_mb,hbm_gb,hbm_type,hbm_tbps,power_w,power_scope,node,die_area_mm2,interconnect,scale,scheduling,workload,verification,last_verified,notes'.split(',')
with (p/'chips.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
    for chip in obj['chips']: w.writerow({c:chip.get(c) for c in cols})
print('Built',len(obj['chips']),'records')
