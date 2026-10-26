"""Match local-brand items (Arabic titles) to Awarid catalog (English titles) by brand + keywords + size. -> match.json"""
import json,re
D={'شامبو':'shampoo','بلسم':'conditioner','ماسك':'mask','حمام زيت':'oil','سيروم':'serum','مقشر':'scrub','جل':'gel','واكس':'wax','كولونيا':'cologne',
'بعد الحلاقة':'after shave','كريم':'cream','لوشن':'lotion','زبدة':'butter','الشيا':'shea','صابون':'soap','أرغان':'argan','ارغان':'argan','قهوة':'coffee','بالقهوة':'coffee',
'ثوم':'garlic','عسل':'honey','كيراتين':'keratin','بوتكس':'botox','الأرز':'rice','أرز':'rice','كيوي':'kiwi','رمان':'pomegranate','الرمان':'pomegranate','ورد':'rose','بالورد':'rose',
'تفتيح':'whitening','فروة':'scalp','عرق السوس':'licorice','توتي فروتي':'tutti','لاتيه':'latte','السكر':'sugar','الرغوي':'foam','العنب':'grape','التوت':'berry',
'تركواز':'turquoise','أسود':'black','الأسود':'black','أخضر':'green','أحمر':'red','أزرق':'blue','ذهبي':'gold','زيتي':'oil','لحية':'beard','اللحية':'beard','حلاقة':'shaving',
'رغوة':'foam','بروتين':'protein','كولاجين':'collagen','جوز الهند':'coconut','الصبار':'aloe','صبار':'aloe','فانيلا':'vanilla','شوكولاتة':'chocolate','فراولة':'strawberry',
'مانجو':'mango','بطيخ':'watermelon','خيار':'cucumber','الشاي الأخضر':'green tea','زيت':'oil','بخاخ':'spray','مزيل':'remover','شمع':'wax','سبراي':'spray','عطر':'mist','معطر':'mist',
'الجوجوبا':'jojoba','جوجوبا':'jojoba','البصل':'onion','بصل':'onion','حليب':'milk','الحليب':'milk','لوز':'almond','اللوز':'almond','الكافيار':'caviar','فيتامين':'vitamin'}
B={'Global Star':'globalstar','Oplus':'oplus','SK5':'sk5','VAI':'vai','فاي':'vai'}
cat=json.load(open('cat_ae.awarid.com.json'));left=json.load(open('left.json'))
def kw(t): return {v for k,v in D.items() if k in t}
def size(t):
    m=re.search(r'(\d{2,4})\s*(?:مل|ml|غ|جم|g)',t,re.I); return m.group(1) if m else None
res={}
for x in left:
    b=B.get(x['brand']) or ('?' if x['gtin'].startswith('6253364') or x['gtin'].startswith('6253504') else None)
    if not b: continue
    k,s=kw(x['title']),size(x['title'])
    best=[]
    for c in cat:
        T=c['title'].lower()
        if b!='?' and b not in T.replace(' ','') and b not in (c['vendor'] or '').lower().replace(' ',''): continue
        sc=sum(2 for w in k if w in T)+(3 if s and re.search(rf'\b{s}\s*(ml|g|gm)',T) else 0)
        if sc>=3 and c['imgs']: best.append((sc,c['title'],c['imgs'][0][0]))
    best.sort(key=lambda z:-z[0])
    if best: res[x['sku']]=best[:2]
json.dump(res,open('match.json','w'),ensure_ascii=False,indent=0)
print('candidates for',len(res),'of',sum(1 for x in left if B.get(x['brand']) or x['gtin'][:7] in ('6253364','6253504')))
