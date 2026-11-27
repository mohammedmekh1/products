"""Builds product_audit/data/master_index.csv from the inventory + batch files (read-only on sources)."""
import openpyxl, csv, re, sys
from collections import Counter
R='المنتجات/'
def gtin_ok(s):
    s=re.sub(r'\D','',str(s))
    if len(s) not in (8,12,13,14): return False
    d=[int(c) for c in s]; chk=d.pop()
    tot=sum(x*(3 if i%2==0 else 1) for i,x in enumerate(reversed(d)))
    return (10-tot%10)%10==chk
def norm(s): return re.sub(r'\s+',' ',str(s or '')).strip()
inv=list(openpyxl.load_workbook(R+'مخزون محل جديد.xlsx',read_only=True).active.iter_rows(values_only=True))[1:]
# batch rows keyed by sku
batch={}
for b in range(1,6):
    ws=openpyxl.load_workbook(R+f'batch{b}-products-complete.xlsx',read_only=True).active
    for r in list(ws.iter_rows(values_only=True))[2:]:
        if r[9]: batch[str(r[9]).strip()]=(b,r[1],r[6])
rows=[];used=set()
for n,(bc,name,price,qty) in enumerate(inv,1):
    bc=str(bc).strip(); sku=None
    for k in (f'MNT-{bc}',f'MNT-R{n}',f'MNT-{bc.zfill(12)}',f'MNT-{bc.zfill(13)}'):
        if k in batch: sku=k;break
    b=batch.get(sku) if sku else None
    if sku: used.add(sku)
    p=float(price) if price not in (None,'') else None
    rows.append(dict(n=n,barcode=bc,name=norm(name),orig_price=p,qty=qty,target_price=(round(p*1.45) if p is not None else ''),
      gtin_valid=int(gtin_ok(bc)),sku=sku or '',batch=(b[0] if b else (6+(n-1301)//150 if n>1300 else 'excluded')),
      batch_price=(b[2] if b else ''),range='old' if n<=1300 else 'new'))
for r in rows:
    r['price_matches']= '' if r['batch_price']=='' else int(abs(float(r['batch_price'])-float(r['target_price']))<=1)
with open('product_audit/data/master_index.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
old=[r for r in rows if r['n']<=1300]
print('inventory',len(rows),'| rows1-1300 matched to batch:',sum(1 for r in old if r['sku']),'excluded/unmatched:',sum(1 for r in old if not r['sku']))
print('batch skus not matched to inventory:',len(set(batch)-used))
print('price mismatches (>1 SAR):',sum(1 for r in old if r['price_matches']==0))
print('gtin valid total:',sum(r['gtin_valid'] for r in rows),'of',len(rows))
print('dup barcodes:',[k for k,v in Counter(r['barcode'] for r in rows).items() if v>1])
print('missing price rows:',[r['n'] for r in rows if r['orig_price'] is None])
