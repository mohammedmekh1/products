"""Batch 4 images from Open Beauty Facts (open API, by barcode): full-size front image, keep >=800px. -> obf.json"""
import json,io,urllib.request,concurrent.futures as cf
from PIL import Image
UA={'User-Agent':'Montnero-catalog/1.0 (montnero.com)'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read()
it=json.load(open('items.json'));im=json.load(open('images.json'))
todo=[x for x in it if x['sku'] not in im and x['gtin']]
def one(x):
    try:
        p=json.loads(get(f"https://world.openbeautyfacts.org/api/v2/product/{x['gtin']}.json?fields=image_front_url"))['product']
        u=p.get('image_front_url')
        if not u: return x['sku'],None
        full=u.rsplit('.',2)[0]+'.full.jpg' if '.400.' in u else u
        for c in (full,u):
            try:
                s=Image.open(io.BytesIO(get(c))).size
                if min(s)>=800: return x['sku'],{'url':c,'size':s}
            except Exception: pass
        return x['sku'],{'small':u}
    except Exception: return x['sku'],None
with cf.ThreadPoolExecutor(6) as ex: r=dict(ex.map(one,todo))
json.dump(r,open('obf.json','w'))
print(len(todo),'big',sum(1 for v in r.values() if v and 'url' in v),'small only',sum(1 for v in r.values() if v and 'small' in v))
