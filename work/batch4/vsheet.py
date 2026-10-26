"""Contact sheet from a JSON list [[label,url],...] -> jpg. Usage: vsheet.py list.json out.jpg"""
import json,io,sys,urllib.request,concurrent.futures as cf
from PIL import Image,ImageDraw
L=json.load(open(sys.argv[1]))
def g(u):
    try: return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read())).convert('RGB')
    except Exception: return Image.new('RGB',(10,10),'red')
with cf.ThreadPoolExecutor(8) as ex: ims=list(ex.map(g,[u for _,u in L]))
T=150;cols=12;rows=(len(L)+cols-1)//cols
sh=Image.new('RGB',(cols*T,rows*(T+12)),'white');dr=ImageDraw.Draw(sh)
for j,((lab,_),im) in enumerate(zip(L,ims)):
    im.thumbnail((T-4,T-4));x,y=j%cols*T+2,j//cols*(T+12)+2;sh.paste(im,(x,y));dr.text((x,y+T-4),lab,fill='red')
sh.save(sys.argv[2],quality=72)
