"""Eucerin UK: map barcode -> product page via /products listing teasers, take product gallery images."""
import json,re,io,urllib.request
from PIL import Image
S='/tmp/claude-0/-root-products/0122d1e7-ca9d-4ec6-8a65-59bc32362dbc/scratchpad/'
h=open(S+'eu.html',encoding='utf8',errors='ignore').read()
r=json.load(open(S+'rest.json')); out={}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read()
for x in r:
    m=re.search(r'data-tracking-product-id=%s>\s*<a href="([^"]+)"'%x['gtin'],h) if x['gtin'] else None
    if not m: continue
    p='https://www.eucerin.co.uk'+m.group(1); t=get(p).decode('utf8','ignore')
    us=list(dict.fromkeys(u.replace('&amp;','&') for u in re.findall(r'(https://images-\d\.eucerin\.com/[^"\s]+?\.(?:png|jpg)[^"\s]*)',t) if 'product' in u.lower() and 'teaser' not in u.lower()))
    ok=[]
    for u in us:
        try:
            if min(Image.open(io.BytesIO(get(u))).size)>=500: ok.append(u)
        except Exception: pass
        if len(ok)>=4: break
    if ok: out[x['sku']]={'page':p,'imgs':ok}
json.dump(out,open('eu_cand.json','w'),indent=0)
it={x['sku']:x for x in r};L=[];sk=list(out)
for i,k in enumerate(sk):
    print(i,it[k]['title'][:50],'|',out[k]['page'][26:])
    for n,u in enumerate(out[k]['imgs']): L.append([f"{i}.{n+1}",u])
json.dump(L,open(S+'s3.json','w'));json.dump(sk,open(S+'s3_skus.json','w'))
