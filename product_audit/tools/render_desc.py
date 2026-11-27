"""Render hand-written product fields into the approved Montnero description HTML + validate.
Input JSON list items: n,name,brand,intro,info[[k,v]],about[p1,p2],features[6],whom[3-4],usage,caution,brand_note,faq[[q,a]x4],merchant,seo_t,seo_d
Output: same list with d (html), mt, md, plus problems printed."""
import json,re,sys,html
H=lambda s:html.escape(s,quote=False)
BAD=re.compile(r'أفضل|أقوى|حصري|خصم|ضمان|شحن مجاني|يعالج|يشفي|يزيل|تبييض|نتائج مضمونة|لا يوجد|غير متوفر|غير مذكور|[$^~#]')
def render(x):
    p=[]
    p.append(f"<p>{H(x['intro'])}</p><p><br></p>")
    p.append("<p>معلومات المنتج:</p><ul>"+''.join(f"<li>{H(k)} | {H(v)}</li>" for k,v in x['info'])+"</ul><p><br></p>")
    p.append("<p>وصف المنتج:</p>"+''.join(f"<p>{H(a)}</p>" for a in x['about']))
    p.append("<p>المميزات:</p><ul>"+''.join(f"<li>{H(a)}</li>" for a in x['features'])+"</ul>")
    p.append("<p>لمن يناسب؟:</p><ul>"+''.join(f"<li>{H(a)}</li>" for a in x['whom'])+"</ul>")
    p.append(f"<p>طريقة الاستخدام:</p><p>{H(x['usage'])}</p>")
    p.append(f"<p>تنبيهات:</p><p>{H(x['caution'])}</p>")
    if x.get('brand_note'): p.append(f"<p>نبذة عن العلامة التجارية:</p><p>{H(x['brand_note'])}</p>")
    p.append("<p>الأسئلة الشائعة:</p>"+''.join(f"<p>{H(q)}</p><p>{H(a)}</p>" for q,a in x['faq']))
    return ''.join(p)
def check(x):
    pr=[];t=re.sub('<[^>]+>','',x['d'])
    if not 1800<=len(t)<=3000: pr.append(f'desc{len(t)}')
    if not 500<=len(x['merchant'])<=1000: pr.append(f"merchant{len(x['merchant'])}")
    if not 140<=len(x['md'])<=155: pr.append(f"seo_d{len(x['md'])}")
    if len(x['mt'])>=60: pr.append(f"seo_t{len(x['mt'])}")
    if len(x['name'])>150: pr.append('name')
    if len(x['faq'])!=4: pr.append('faq')
    for k in ('d','merchant','name','mt','md'):
        m=BAD.search(re.sub('<[^>]+>','',x[k]))
        if m: pr.append(f'{k}:{m.group()}')
    if re.search(r'<|https?://|@',x['merchant']): pr.append('merchant-markup')
    return pr
if __name__=='__main__':
    src,dst=sys.argv[1],sys.argv[2]
    d=[x for x in json.load(open(src)) if 'skip' not in x]; bad=0
    for x in d:
        x['d']=render(x); x['mt']=x['seo_t']; x['md']=x['seo_d']
        pr=check(x)
        if pr: bad+=1; print(x['n'],pr)
    json.dump(d,open(dst,'w'),ensure_ascii=False,indent=0)
    print(len(d),'items,',bad,'with problems')
