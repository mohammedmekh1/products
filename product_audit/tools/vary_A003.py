"""Rotate/trim sentences repeated in 3+ A003 products. usage: python3 product_audit/tools/vary_A003.py"""
import json,glob,re,collections,sys
sys.path.insert(0,'product_audit/tools')
from render_desc import check
R={
"يمكنك الرجوع إلى إرشادات العبوة لمزيد من التفاصيل.":["للمزيد من التفاصيل راجعي النشرة المطبوعة على العبوة.","تجدين بقية المعلومات في الإرشادات المكتوبة على العبوة.","وتوضح العبوة تفاصيل أخرى تُقرأ قبل الاستخدام.","ويُستحسن الاطلاع على ما كُتب على العبوة قبل البدء."],
"للاستخدام الخارجي فقط مع تجنب العينين.":["للاستخدام الخارجي، وابعديه عن العينين.","هذا المنتج للاستعمال الخارجي فقط، فتجنبي ملامسة العين.","يُستعمل خارجياً مع الحرص على إبعاده عن العينين."],
"أوقفي الاستخدام وراجعي مختصاً عند ظهور تهيج.":["عند ظهور تهيج توقفي عن الاستخدام واستشيري مختصاً.","إذا ظهر تهيج فأوقفي الاستخدام وراجعي مختصاً.","توقفي عن الاستخدام وتحدثي مع مختص عند أي تهيج."],
"وبملاحظة استجابة البشرة خلال الأيام الأولى.":["مع متابعة تفاعل البشرة في الأيام الأولى.","وراقبي كيف تستجيب بشرتك في بداية الاستخدام."],
"إن شعرتِ بأي انزعاج توقفي عن الاستخدام.":["إذا أحسستِ بانزعاج فتوقفي عن الاستعمال.","عند أي إحساس بعدم الراحة أوقفي الاستخدام."],
}
c=collections.Counter()
files=sorted(glob.glob('product_audit/batches_v2/A003_in_*.out.json'))
data={f:json.load(open(f)) for f in files}
def sents(t): return [s.strip() for s in re.split(r'(?<=[.،])\s|</p>|</li>|\n',re.sub(r'<[^>]+>','\n',t)) if len(s.strip())>30]
for d in data.values():
    for x in d:
        for k in('d','merchant'):
            for s in set(sents(x[k])): c[s]+=1
rep=0;trim=0
for f,d in data.items():
    for x in d:
        for k in('d','merchant'):
            for s,n in c.items():
                if n<3 or s not in x[k]: continue
                alts=R.get(s)
                if alts:
                    i=x['n']%(len(alts)+1)
                    if i>0: x[k]=x[k].replace(s,alts[i-1]);rep+=1
                elif x['n']%3:
                    new=x[k].replace(s,'',1)
                    old=x[k];x[k]=new
                    if check(x): x[k]=old
                    else: trim+=1
    json.dump(d,open(f,'w'),ensure_ascii=False,indent=0)
bad=[(x['n'],check(x)) for d in data.values() for x in d if check(x)]
print('replaced',rep,'trimmed',trim,'problems',bad[:5])
