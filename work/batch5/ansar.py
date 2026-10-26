"""Ansar Gallery images by barcode (files named <EAN>_<n>.jpg). Checks _1.._4, keeps >=800px. -> ansar.json {sku:[urls]}"""
import json,io,urllib.request,concurrent.futures as cf
from PIL import Image
it=json.load(open('items.json'))
def ok(u):
    try:
        im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read()))
        return min(im.size)>=800
    except Exception: return False
def one(x):
    g=x['gtin']
    if not g: return x['sku'],[]
    us=[f"https://media.ansargallery.com/media/catalog/product/{g[0]}/{g[1]}/{g}_{n}.jpg" for n in (1,2,3,4)]
    return x['sku'],[u for u in us if ok(u)]
with cf.ThreadPoolExecutor(8) as ex: r={s:v for s,v in ex.map(one,it) if v}
json.dump(r,open('ansar.json','w'))
im=json.load(open('images.json'))
print('any',len(r),'missing-set',sum(1 for s in r if s not in im),'2+ imgs',sum(1 for v in r.values() if len(v)>1))
