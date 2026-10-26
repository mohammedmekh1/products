"""Beauty One batch: read source sheet -> items.json (sku, name, price x1.45, gtin if valid). Flags overlap with batches 1-5."""
import json, re, glob, openpyxl
D = "/root/products/المنتجات/"
def valid(g):
    g = str(g)
    if not g.isdigit() or len(g) not in (8, 12, 13, 14): return False
    d = [int(c) for c in g[:-1]][::-1]
    return (10 - sum(x * (3 if i % 2 == 0 else 1) for i, x in enumerate(d)) % 10) % 10 == int(g[-1])
done = set()
for f in glob.glob(D + "batch*-products-complete.xlsx"):
    for r in openpyxl.load_workbook(f, read_only=True).worksheets[0].iter_rows(min_row=3, values_only=True):
        if r[9]: done.add(str(r[9]).replace("MNT-", ""))
items, seen, dup, prior = [], set(), [], []
for r in openpyxl.load_workbook(D + "بيوتي ون1.xlsx", read_only=True).worksheets[0].iter_rows(min_row=2, values_only=True):
    if not r[0] or not r[1]: continue
    g = str(r[0]).strip().split(".")[0]
    if g in seen: dup.append(g); continue
    seen.add(g)
    if g in done: prior.append(g); continue
    name = re.sub(r"\s+", " ", str(r[1]).replace("\xa0", " ").replace("‏", "")).strip()
    items.append({"sku": "MNT-" + g, "src_name": name, "price": round(float(r[3]) * 1.45),
                  "gtin": g if valid(g) else None})
json.dump(items, open("items.json", "w"), ensure_ascii=False, indent=0)
print(len(items), "items; duplicate barcodes:", len(dup), "; already in batches 1-5:", len(prior), "; invalid gtin:", sum(1 for i in items if not i["gtin"]))
