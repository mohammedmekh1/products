"""Crawl brand-site sitemaps, find pages containing our barcodes, take og:image + gallery images. -> brand.json {sku:{page,imgs}}"""
import json,re,sys,gzip,urllib.request,concurrent.futures as cf
UA={'User-Agent':'Mozilla/5.0'}
def get(u):
    b=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=25).read()
    if b[:2]==b'\x1f\x8b': b=gzip.decompress(b)
    return b.decode('utf8','ignore')
rest=json.load(open(sys.argv[1])); sitemaps=sys.argv[2:]
g2s={x['gtin']:x['sku'] for x in rest if x['gtin']}
def locs(sm,depth=0):
    try: t=get(sm)
    except Exception: return []
    L=re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',t)
    if '<sitemapindex' in t and depth<2:
        out=[]
        for s in L: out+=locs(s,depth+1)
        return out
    return L
pages=[]
for sm in sitemaps: pages+=locs(sm)
pages=[p for p in dict.fromkeys(pages) if re.search(r'product|/p/|\d{6,}|\.html|/en-ae/|/ar-ae/|/en/',p,re.I) and not re.search(r'/ar-|/fr/|article',p) and (len(sys.argv)<4 or True) and not re.search(r'\.(jpg|png|pdf)$',p)]
print('pages',len(pages),file=sys.stderr)
try: found=json.load(open('brand.json'))
except Exception: found={}
def one(p):
    try: h=get(p)
    except Exception: return []
    hits=[g for g in g2s if g in h]
    if not hits: return []
    imgs=re.findall(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"',h)
    imgs+=[u for u in re.findall(r'"(https?://[^"\s]+?\.(?:jpg|jpeg|png|webp)[^"\s]*)"',h) if not re.search(r'logo|icon|banner|sprite|thumb',u,re.I)]
    return [(g2s[g],{'page':p,'imgs':list(dict.fromkeys(imgs))[:8]}) for g in hits]
with cf.ThreadPoolExecutor(8) as ex:
    for r in ex.map(one,pages):
        for s,v in r: found.setdefault(s,v)
json.dump(found,open('brand.json','w'),indent=0)
print('found total',len(found))
