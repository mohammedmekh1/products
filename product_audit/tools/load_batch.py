import openpyxl,csv,re,json,sys
R='المنتجات/'
def load_items():
    idx=list(csv.DictReader(open('product_audit/data/master_index.csv',encoding='utf-8-sig')))
    bs={}
    for b in range(1,6):
        ws=openpyxl.load_workbook(R+f'batch{b}-products-complete.xlsx',read_only=True).active
        for r in list(ws.iter_rows(values_only=True))[2:]:
            if r[9]: bs[str(r[9]).strip()]=dict(batch=b,title=r[1],cat=r[2],img=r[3],price=r[6],desc=r[7] or '',sku=r[9],brand=r[19],gtin=r[25],barcode=r[22])
    out=[]
    for r in idx:
        r['row']=bs.get(r['sku']); out.append(r)
    return out
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for r in load_items()[a-1:b]:
        x=r['row']
        if not x: print(r['n'],'EXCL',r['name'][:50]); continue
        d=re.sub('<[^>]+>','',x['desc'])
        print(r['n'],'|',x['title'][:55],'|',x['brand'],'|',(x['cat'] or '').split('>')[-1].strip(),'|',x['price'],'| g',r['gtin_valid'],'| img' if x['img'] else '| NOIMG',len(d))
