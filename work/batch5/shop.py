"""Shopify stores' public storefront search by barcode -> product images (>=600px). Input list json of items; -> shop.json {gtin:[{store,title,img}]}"""
import json,sys,io,urllib.request,concurrent.futures as cf
from PIL import Image
UA={'User-Agent':'Mozilla/5.0'}
def raw(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=25).read()
def get(u): return json.loads(raw(u))
def size(u):
    try: return min(Image.open(io.BytesIO(raw(u))).size)
    except Exception: return 0
items=json.load(open(sys.argv[1])); stores=sys.argv[2:]
try: done=json.load(open('shop.json'))
except Exception: done={}
def one(x):
    g=x['gtin']; out=[]
    for s in stores:
        try:
            r=get(f"https://{s}/search/suggest.json?q={g}&resources%5Btype%5D=product&resources%5Blimit%5D=2")['resources']['results']['products']
            if len(r)!=1: continue
            p=get(f"https://{s}/products/{r[0]['handle']}.json")['product']
            for i in p['images'][:3]:
                u=i['src']
                if min(i.get('width',0),i.get('height',0))>=600 or size(u)>=600: out.append({'store':s,'title':p['title'][:60],'img':u})
        except Exception: pass
        if len(out)>=4: break
    return g,out
with cf.ThreadPoolExecutor(6) as ex:
    for g,v in ex.map(one,[x for x in items if x['gtin'] and x['gtin'] not in done]): done[g]=v
json.dump(done,open('shop.json','w'),ensure_ascii=False,indent=0)
print('with imgs',sum(1 for v in done.values() if v),'of',len(done))
