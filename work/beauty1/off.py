"""Open Beauty/Food/Products Facts by barcode -> off.json {sku:[front image full-size url]}"""
import json,urllib.request,concurrent.futures as cf
G=[i['sku'] for i in json.load(open('items.json'))]
def one(sku):
    for d in ['openbeautyfacts','openfoodfacts','openproductsfacts']:
        try:
            p=json.loads(urllib.request.urlopen(urllib.request.Request(f'https://world.{d}.org/api/v2/product/{sku[4:]}.json?fields=image_front_url',headers={'User-Agent':'Montnero/1.0'}),timeout=20).read()).get('product') or {}
        except Exception: continue
        if p.get('image_front_url'): return sku,[p['image_front_url'].replace('.400.jpg','.full.jpg')]
    return sku,[]
with cf.ThreadPoolExecutor(10) as ex: R={s:v for s,v in ex.map(one,G) if v}
json.dump(R,open('off.json','w'),indent=0);print(len(R),'of',len(G))
