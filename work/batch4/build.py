"""Build queue.json for batch 4: every product with a verified image, up to 2 images (main + secondary), 2 categories."""
import json, re, openpyxl
D = "/root/products/المنتجات/"
ROOT, HAIR, PERSONAL, FACE, EYES, LIPS = 2041195310, 2105502663, 1796196546, 246604359, 603229516, 1445883459
CAT = {  # last path segment -> (usual category, second category: parent or closest related)
    "سيروم": (1189881341, ROOT), "مرطبات": (281625854, ROOT), "تنظيف الوجه": (1654023167, ROOT),
    "واقي الشمس": (1014792952, ROOT), "ماسكات وتقشير": (240755193, ROOT), "زيوت وزبدات": (1478934778, ROOT),
    "تفتيح وتوحيد اللون": (704901115, ROOT), "العناية بالعين": (1370828229, ROOT),
    "العناية بالبشرة": (ROOT, 281625854), "العناية بالشعر": (HAIR, ROOT), "العناية بالجسم": (1329957568, ROOT),
    "العناية الشخصية": (PERSONAL, ROOT), "الحلاقة وإزالة الشعر": (1154799555, PERSONAL),
    "أحمر الشفاه": (569589586, LIPS), "ماسكارا": (993385055, EYES), "البودرة": (213554261, FACE),
    "كريم الأساس": (388642634, FACE), "كريمات الإخفاء والتصحيح": (1337903950, FACE),
    "مزيلات العرق": (PERSONAL, ROOT), "مرطب الشفاه": (1620973005, LIPS), "الحواجب": (711204929, ROOT),
    "مكياج العيون": (EYES, ROOT), "العيون": (EYES, ROOT),
}
clean = json.load(open("clean.json"))
qty = {r[0]: r[2] for r in openpyxl.load_workbook(D + "batch4-review.xlsx", read_only=True)["الكميات"].iter_rows(min_row=2, values_only=True)}
imgs = {k: [v] for k, v in json.load(open("images.json")).items()}
for k, v in json.load(open("img2_secondary.json")).items(): imgs[k].append(v)
for f in ("img2_ansar.json", "img2_brand.json", "img2_eu.json", "img2_web.json", "img2_web2.json"):
    for k, v in json.load(open(f)).items(): imgs.setdefault(k, v)
over = json.load(open("seo_override.json"))  # SEO fields missing from the sheet, kept from the first queue
junk = re.compile(r"<p>(?:(?![؀-ۿ])[^<]){0,80}</p>|<p><strong>[^<]*exclude_reason[^<]*</strong></p>")
q, miss = [], set()
for r in openpyxl.load_workbook(D + "batch4-products-complete.xlsx", read_only=True).worksheets[0].iter_rows(min_row=3, values_only=True):
    sku = r[9]
    if not sku or sku not in imgs: continue
    seg = r[2].split(">")[-1].strip()
    if seg not in CAT: miss.add(seg); continue
    c = clean[sku]
    p = {"sku": sku, "name": r[1].strip(), "price": float(r[6]), "product_type": "product",
         "description": junk.sub("", c["store"]), "categories": list(CAT[seg]), "weight": 500, "weight_type": "g",
         "require_shipping": True, "quantity": int(qty.get(sku) or 0),
         "metadata_title": c["seo_title"], "metadata_description": c["seo"],
         "images": imgs[sku][:2], "image_alt": r[1].strip()[:255]}
    p.update(over.get(sku, {}))
    if r[25]: p["gtin"] = str(r[25])
    q.append(p)
json.dump(q, open("queue.json", "w"), ensure_ascii=False)
print(len(q), "products;", sum(len(p["images"]) > 1 for p in q), "with 2 images; unmapped categories:", miss)
