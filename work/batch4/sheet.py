import json,io,sys,urllib.request,concurrent.futures as cf
from PIL import Image,ImageDraw
src,out,start=sys.argv[1],sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 0
d={k:v for k,v in json.load(open(src)).items() if v}; items={x['sku']:x for x in json.load(open('items.json'))}
ks=list(d)[start:start+60]
def g(k):
    try: return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(f"https://m.media-amazon.com/images/P/{d[k]['asin']}.01._SCRMZZZZZZ_.jpg",headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read())).convert('RGB')
    except Exception: return Image.new('RGB',(10,10),'red')
with cf.ThreadPoolExecutor(8) as ex: ims=list(ex.map(g,ks))
T=200;cols=10;rows=(len(ks)+cols-1)//cols
sh=Image.new('RGB',(cols*T,rows*(T+14)),'white');dr=ImageDraw.Draw(sh)
for j,(k,im) in enumerate(zip(ks,ims)):
    im.thumbnail((T-6,T-6));sh.paste(im,(j%cols*T+3,j//cols*(T+14)+3));dr.text((j%cols*T+3,j//cols*(T+14)+T),str(start+j),fill='red')
    print(start+j,items[k]['title'][:60])
sh.save(out,quality=80)
