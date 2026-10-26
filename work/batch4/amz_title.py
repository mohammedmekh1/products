import json,re,io,urllib.request,urllib.parse,concurrent.futures as cf
from PIL import Image
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36','Accept-Language':'en'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=25).read().decode('utf8','ignore')
items={x['sku']:x for x in json.load(open('items.json'))}; done=json.load(open('amz.json'))
try: t=json.load(open('amz_t.json'))
except Exception: t={}
def one(s):
    x=items[s]
    try: h=get('https://www.amazon.sa/s?k='+urllib.parse.quote(x['title']))
    except Exception: return s,None
    for m in list(re.finditer(r'data-asin="(B0[0-9A-Z]{8})"[^>]*data-index="(\d+)"',h))[:1]:
        a=m.group(1)
        try:
            im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(f'https://m.media-amazon.com/images/P/{a}.01._SCRMZZZZZZ_.jpg',headers=UA),timeout=25).read()))
            if max(im.size)>=1000: return s,{'asin':a,'how':'title','size':im.size}
        except Exception: pass
    return s,None
todo=[s for s,v in done.items() if not v and s not in t]
with cf.ThreadPoolExecutor(4) as ex:
    for s,v in ex.map(one,todo): t[s]=v
json.dump(t,open('amz_t.json','w'));print('title found',sum(1 for v in t.values() if v),'/',len(t))
