import json,sys,csv
sys.path.insert(0,'product_audit/tools')
from load_batch import load_items
batch=sys.argv[1]; files=sys.argv[2:]
old={r['n']:r for r in load_items()}
rows=[]
for f in files:
    for x in json.load(open(f)):
        r=old[str(x['n'])]['row']
        rows.append([x['n'],(r or {}).get('title','').strip(),x['name']])
rows.sort()
questions=json.load(open('product_audit/data/questions_%s.json'%batch))
stats=json.load(open('product_audit/data/stats_%s.json'%batch))
html=open('product_audit/tools/report_template.html',encoding='utf8').read()
for k,v in {'__BATCH__':batch,'__ROWS__':json.dumps(rows,ensure_ascii=False),'__Q__':json.dumps(questions,ensure_ascii=False),'__STATS__':json.dumps(stats,ensure_ascii=False)}.items():
    html=html.replace(k,v.replace('<','\\u003c') if k!='__BATCH__' else v)
open('product_audit/pages/report_%s.html'%batch,'w',encoding='utf8').write(html)
print(len(rows),'rows')
