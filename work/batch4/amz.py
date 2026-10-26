"""For each item: Amazon.sa search by EAN (fallback: barcodespider/upcitemdb pages for ASIN), then by title.
Keeps first ASIN whose main image is >=1000px. Output amz.json {sku: {asin, how, size}}."""
import json,re,io,sys,urllib.request,urllib.parse,concurrent.futures as cf
from PIL import Image
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36','Accept-Language':'en'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=25).read().decode('utf8','ignore')
def search(q):
    try: h=get('https://www.amazon.sa/s?k='+urllib.parse.quote(q)+'&language=en_AE')
    except Exception: return []
    out=[]
    for m in re.finditer(r'data-asin="(B0[0-9A-Z]{8})"[^>]*data-index="(\d+)"',h):
        if m.group(1) not in out: out.append(m.group(1))
    return out[:2]
def img_ok(a):
    try:
        im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(f'https://m.media-amazon.com/images/P/{a}.01._SCRMZZZZZZ_.jpg',headers=UA),timeout=25).read()))
        return im.size if max(im.size)>=1000 else None
    except Exception: return None
def one(x):
    tries=[]
    if x['gtin']:
        tries+= [(a,'ean') for a in search(x['gtin'])]
        if not tries:
            for src in (f"https://www.barcodespider.com/{x['gtin']}",f"https://www.upcitemdb.com/upc/{x['gtin']}"):
                try: tries+=[(a,'eandb') for a in dict.fromkeys(re.findall(r'B0[0-9A-Z]{8}',get(src)))][:1]
                except Exception: pass
                if tries: break
    for a,how in tries:
        s=img_ok(a)
        if s: return x['sku'],{'asin':a,'how':how,'size':s}
    return x['sku'],None
items=json.load(open('items.json'))
try: done=json.load(open('amz.json'))
except Exception: done={}
todo=[x for x in items if x['sku'] not in done]
with cf.ThreadPoolExecutor(4) as ex:
    for i,(s,v) in enumerate(ex.map(one,todo)):
        done[s]=v
        if i%20==0: json.dump(done,open('amz.json','w'))
json.dump(done,open('amz.json','w'))
print('found',sum(1 for v in done.values() if v),'/',len(done))
