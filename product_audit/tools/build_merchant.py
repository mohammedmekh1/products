"""Build/refresh the per-batch Merchant feed from v2 content + (optionally) sync results exported from the page db.
usage: python3 product_audit/tools/build_merchant.py A001 batches_v2/A001_*.out.json [--sync DIR]
Writes product_audit/merchant/MERCHANT_<BATCH>.csv and refreshes the cumulative MERCHANT_FEED.csv."""
import json,csv,sys,glob,os
batch=sys.argv[1]; args=sys.argv[2:]
sync=None
if '--sync' in args: i=args.index('--sync'); sync=args[i+1]; args=args[:i]+args[i+2:]
files=[f for a in args for f in glob.glob(a)]
sys.path.insert(0,'product_audit/tools')
from load_batch import load_items
cat={int(r['n']):((r.get('row') or {}).get('cat') or '') for r in load_items()}
idx={int(r['n']):r for r in csv.DictReader(open('product_audit/data/master_index.csv',encoding='utf-8-sig'))}
res={}
if sync:
    for f in glob.glob(sync+'/*.json'):
        d=json.load(open(f)); d=d.get('data',d)
        if d.get('n'): res[int(d['n'])]=d
GPC={'ماسكارا':'Health & Beauty > Personal Care > Cosmetics > Makeup > Eye Makeup > Mascara','كونسيلر':'Health & Beauty > Personal Care > Cosmetics > Makeup > Face Makeup > Concealers & Neutralizers',
'أحمر شفاه':'Health & Beauty > Personal Care > Cosmetics > Makeup > Lip Makeup > Lipstick','مرطب شفاه':'Health & Beauty > Personal Care > Cosmetics > Lip Care > Lip Balms & Treatments',
'كريم أساس':'Health & Beauty > Personal Care > Cosmetics > Makeup > Face Makeup > Foundations & Concealers','مزيل عرق':'Health & Beauty > Personal Care > Cosmetics > Deodorant & Antiperspirant',
'شامبو':'Health & Beauty > Personal Care > Hair Care > Shampoo & Conditioner','لوشن':'Health & Beauty > Personal Care > Skin Care > Lotion & Moisturizer','كريم':'Health & Beauty > Personal Care > Skin Care > Lotion & Moisturizer'}
def gpc(name):
    for k,v in GPC.items():
        if k in name: return v
    return ''
cols=['n','id','title','description','link','image_link','additional_image_link','price','availability','condition','brand','gtin','mpn','identifier_exists','google_product_category','product_type','salla_id','review_note']
rows=[]
for f in sorted(files):
    for x in json.load(open(f)):
        r=idx[x['n']]; s=res.get(x['n'],{})
        gt=r['gtin']; 
        rows.append(dict(n=x['n'],id='MNT-'+r['barcode'].lstrip('0') if not r['sku'].startswith('MNT-R') else r['sku'],title=x['name'],description=x['merchant'],link=s.get('url',''),image_link=s.get('image',''),additional_image_link='',
          price=f"{r['target_price']} SAR",availability='in_stock',condition='new',brand=x.get('brand',''),gtin=gt,mpn='',identifier_exists='yes' if gt else 'no',
          google_product_category=gpc(x['name']),product_type=cat.get(x['n'],'').replace(' > ',' > '),salla_id=s.get('id',''),
          review_note='; '.join(filter(None,[ 'link missing (run sync)' if not s.get('url') else '', 'image missing' if not s.get('image') else '', 'gtin duplicate in store' if s.get('gtinDuplicate') else '']))))
os.makedirs('product_audit/merchant',exist_ok=True)
out=f'product_audit/merchant/MERCHANT_{batch}.csv'
with open(out,'w',newline='',encoding='utf-8-sig') as o:
    w=csv.DictWriter(o,fieldnames=cols);w.writeheader();w.writerows(sorted(rows,key=lambda r:r['n']))
# cumulative
allrows={}
for f in sorted(glob.glob('product_audit/merchant/MERCHANT_A*.csv')):
    for r in csv.DictReader(open(f,encoding='utf-8-sig')): allrows[r['id']]=r
with open('product_audit/merchant/MERCHANT_FEED_ALL.csv','w',newline='',encoding='utf-8-sig') as o:
    w=csv.DictWriter(o,fieldnames=cols);w.writeheader();w.writerows(sorted(allrows.values(),key=lambda r:int(r['n'])))
print(len(rows),'rows ->',out,'| cumulative',len(allrows))
