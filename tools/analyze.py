import openpyxl,json,re,collections,glob
D='المنتجات/'
def sheet(f,i=0):
    return list(openpyxl.load_workbook(D+f,read_only=True).worksheets[i].iter_rows(values_only=True))
inv=[r for r in sheet('مخزون محل جديد.xlsx')[1:] if r[0]]
b1=[r for r in sheet('بيوتي ون1.xlsx')[1:] if r[0]]
print('inventory',len(inv),'beauty1 rows',len(b1))
norm=lambda x:re.sub(r'\D','',str(x or '')).lstrip('0')
invb={norm(r[0]):r for r in inv}
print('inv unique barcodes',len(invb))
b1b=collections.Counter(norm(r[0]) for r in b1)
print('b1 unique',len(b1b),'dups',sum(v-1 for v in b1b.values() if v>1),'b1 with price',sum(1 for r in b1 if r[3]),'b1 in inv',len(set(b1b)&set(invb)))
ready=json.load(open('montnero_state/local_ready.json'))
rg={norm(o['gtin'] or o['barcode']) for o in ready}-{''}
print('ready with gtin',len(rg),'gtin in inv',len(rg&set(invb)),'gtin in b1',len(rg&set(b1b)))
print('inv not in ready gtin',len(set(invb)-rg))
# beauty1 prepared (chunk outs)
b1out=[]
for f in sorted(glob.glob('work/beauty1/chunk_*_out.json')): b1out+=json.load(open(f))
print('beauty1 prepared',len(b1out), 'sku sample',b1out[0].get('sku'))
bs={o['sku'] for o in b1out}; rs={o['sku'] for o in ready}
print('beauty1 prepared overlap ready',len(bs&rs))
# excluded/review: batch reviews
exc=0
# quality of ready
