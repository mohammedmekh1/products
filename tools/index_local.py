"""Build a local product index from the approved xlsx files (no network, no AI)."""
import openpyxl, csv, re, sys, json, collections
D='المنتجات/'
OK=['batch1-products-complete','batch2-products-complete','batch3-products-complete','batch4-products-complete','batch5-products-complete']
def rows(f):
    ws=openpyxl.load_workbook(D+f+'.xlsx',read_only=True).worksheets[0]
    return list(ws.iter_rows(values_only=True))
out=[]
hdr=None
for f in OK:
    r=rows(f)
    h=[str(c or '').strip() for c in r[1]]
    if hdr is None: hdr=h
    ix={n:i for i,n in enumerate(h)}
    def g(row,key):
        for n,i in ix.items():
            if n.startswith(key): return row[i]
    for row in r[2:]:
        if not row or not row[1]: continue
        out.append(dict(file=f,sku=str(g(row,'رمز المنتج') or '').strip(),name=g(row,'أسم المنتج'),cat=g(row,'تصنيف'),price=g(row,'سعر المنتج'),brand=g(row,'الماركة'),gtin=str(g(row,'GTIN') or '').strip(),barcode=str(g(row,'الباركود') or '').strip(),img=bool(g(row,'صورة المنتج')),desc_len=len(str(g(row,'الوصف') or ''))))
json.dump(out,open('montnero_state/local_ready.json','w'),ensure_ascii=False)
c=collections.Counter(o['file'] for o in out); print(c, len(out))
print('empty sku',sum(1 for o in out if not o['sku']),'dup sku',sum(v-1 for v in collections.Counter(o['sku'] for o in out).values() if v>1))
print('with img',sum(o['img'] for o in out),'brand empty',sum(1 for o in out if not o['brand']),'gtin',sum(1 for o in out if o['gtin'] not in('','None')))
