"""Download full public Shopify catalogs of brand stores -> cat_<store>.json (title, sku, images)."""
import json,sys,time,urllib.request
for s in sys.argv[1:]:
    out=[]
    for page in range(1,30):
        time.sleep(4)
        try: p=json.loads(urllib.request.urlopen(urllib.request.Request(f"https://{s}/products.json?limit=250&page={page}",headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read())['products']
        except Exception as e:
            print(s,page,e); time.sleep(30); continue
        if not p: break
        out+=[{'title':x['title'],'handle':x['handle'],'vendor':x.get('vendor'),'skus':[v.get('sku') for v in x['variants']],'barcodes':[v.get('barcode') for v in x['variants']],'imgs':[(i['src'],i.get('width'),i.get('height')) for i in x['images']],'body':(x.get('body_html') or '')[:600]} for x in p]
    json.dump(out,open(f'cat_{s}.json','w'),ensure_ascii=False); print(s,len(out))
