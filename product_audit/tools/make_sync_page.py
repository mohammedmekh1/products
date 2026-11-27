"""Build the Salla sync (update/create) HTML page for one batch.
usage: python3 product_audit/tools/make_sync_page.py A001 product_audit/batches/A001_p1.json [more.json ...]
Output: product_audit/pages/sync_<BATCH>.html  (published as an Artifact; data embedded)."""
import json,sys,csv
batch=sys.argv[1]; files=sys.argv[2:]
idx={int(r['n']):r for r in csv.DictReader(open('product_audit/data/master_index.csv',encoding='utf-8-sig'))}
skip=set(json.load(open('product_audit/data/skip_%s.json'%batch))) if __import__('os').path.exists('product_audit/data/skip_%s.json'%batch) else set()
items=[]
for f in files:
    for x in json.load(open(f)):
        if x['n'] in skip: continue
        r=idx[x['n']]
        items.append(dict(n=x['n'],barcode=r['barcode'],gtin=r['gtin'],price=int(r['target_price']),name=x['name'],brand=x.get('brand',''),
          description=x['d'],mt=x['mt'],md=x['md'],skus=[ 'MNT-'+r['barcode'], 'MNT-R%d'%x['n'], r['sku'] ]))
items.sort(key=lambda i:i['n'])
data=json.dumps(items,ensure_ascii=False).replace('<','\\u003c')
html=open('product_audit/tools/sync_template.html',encoding='utf8').read().replace('__BATCH__',batch).replace('__DATA__',data)
open('product_audit/pages/sync_%s.html'%batch,'w',encoding='utf8').write(html)
print(len(items),'items',len(html)//1024,'KB')
