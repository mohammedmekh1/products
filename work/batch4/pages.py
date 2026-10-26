"""Extract product images from retailer/brand pages found by web search. Input web_urls.json {gtin:[url|ASIN:xxx,...]} -> web_cand.json {gtin:[img,...]}"""
import json,re,io,urllib.request,urllib.parse,concurrent.futures as cf
from PIL import Image
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=25).read()
def imgs_of(u):
    if u.startswith('ASIN:'): return [f"https://m.media-amazon.com/images/P/{u[5:]}.01._SCRMZZZZZZ_.jpg"]
    out=[]
    if '/products/' in u:
        try:
            p=json.loads(get(u.split('?')[0].rstrip('/')+'.json'))['product']; out+=[i['src'] for i in p['images']]
        except Exception: pass
    if not out:
        try: h=get(u).decode('utf8','ignore')
        except Exception: return []
        out+=re.findall(r'<meta[^>]+(?:property|name)="og:image"[^>]+content="([^"]+)"',h)
        for m in re.findall(r'"image"\s*:\s*(\[[^\]]*\]|"[^"]+")',h):
            try: v=json.loads(m); out+=v if isinstance(v,list) else [v]
            except Exception: pass
    return [urllib.parse.urljoin(u,x.replace('&amp;','&')) for x in out if isinstance(x,str)]
def size(u):
    try: return min(Image.open(io.BytesIO(get(u))).size)
    except Exception: return 0
W=json.load(open('web_urls.json'))
try: C=json.load(open('web_cand.json'))
except Exception: C={}
def one(g):
    res=[]
    for u in W[g]:
        for i in dict.fromkeys(imgs_of(u)):
            if i not in res and size(i)>=600: res.append(i)
            if len(res)>=4: return g,res
    return g,res
with cf.ThreadPoolExecutor(6) as ex:
    for g,r in ex.map(one,[g for g in W if g not in C]): C[g]=r
json.dump(C,open('web_cand.json','w'),indent=0)
print({g:len(v) for g,v in C.items()})
