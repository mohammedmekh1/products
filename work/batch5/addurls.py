"""Append candidate pages to web_urls.json: args gtin=url1|url2 ..."""
import json,sys
try: w=json.load(open('web_urls2.json'))
except Exception: w={}
for a in sys.argv[1:]:
    g,us=a.split('=',1); w.setdefault(g,[]); w[g]+= [u for u in us.split('|') if u not in w[g]]
json.dump(w,open('web_urls2.json','w'),indent=0); print(len(w))
