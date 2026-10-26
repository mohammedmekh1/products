"""Open Beauty/Food/Products Facts by barcode -> off.json {sku:[full-size front image urls]}"""
import json,urllib.request,concurrent.futures as cf
G=[l.split('\t')[0] for l in open('no_image_yet.txt')]
def one(sku):
    g=sku[4:]
    for d in ['openbeautyfacts','openfoodfacts','openproductsfacts']:
        try:
            p=json.loads(urllib.request.urlopen(urllib.request.Request(f'https://world.{d}.org/api/v2/product/{g}.json?fields=image_front_url,selected_images',headers={'User-Agent':'Montnero/1.0'}),timeout=20).read()).get('product') or {}
        except Exception: continue
        u=p.get('image_front_url')
        if u:
            ims=[x for x in ((p.get('selected_images') or {}).get('front',{}).get('display',{}) or {}).values()]
            return sku,[u.replace('.400.jpg','.jpg')]
    return sku,[]
with cf.ThreadPoolExecutor(8) as ex: R={s:v for s,v in ex.map(one,G) if v}
json.dump(R,open('off.json','w'),indent=0);print(len(R),'of',len(G))
