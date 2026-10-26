import json,io,sys,urllib.request,concurrent.futures as cf
from PIL import Image,ImageDraw
r={k:v for k,v in json.load(open('obf.json')).items() if v and 'url' in v}; ks=list(r)
def g(k):
    try: return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(r[k]['url'],headers={'User-Agent':'Montnero-catalog/1.0'}),timeout=30).read())).convert('RGB')
    except Exception: return Image.new('RGB',(10,10),'red')
with cf.ThreadPoolExecutor(6) as ex: ims=list(ex.map(g,ks))
T=180;cols=10;rows=(len(ks)+cols-1)//cols
sh=Image.new('RGB',(cols*T,rows*(T+14)),'white');dr=ImageDraw.Draw(sh)
it={x['sku']:x for x in json.load(open('items.json'))}
for j,(k,im) in enumerate(zip(ks,ims)):
    im.thumbnail((T-6,T-6));sh.paste(im,(j%cols*T+3,j//cols*(T+14)+3));dr.text((j%cols*T+3,j//cols*(T+14)+T),str(j),fill='red')
    print(j,it[k]['title'][:55])
sh.save(sys.argv[1],quality=75)
