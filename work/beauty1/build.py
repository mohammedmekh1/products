"""Build queue.json for a Beauty One batch from chunk outputs: 1 image (web 800px+ or upscaled sheet image), 2 categories, price x1.45."""
import json, glob, re, sys
ROOT, HAIR, PERSONAL, FACE, EYES, LIPS = 2041195310, 2105502663, 1796196546, 246604359, 603229516, 1445883459
CAT = {"سيروم": (1189881341, ROOT), "مرطبات": (281625854, ROOT), "تنظيف الوجه": (1654023167, ROOT),
       "واقي الشمس": (1014792952, ROOT), "ماسكات وتقشير": (240755193, ROOT), "زيوت وزبدات": (1478934778, ROOT),
       "تفتيح وتوحيد اللون": (704901115, ROOT), "العناية بالعين": (1370828229, ROOT), "العناية بالبشرة": (ROOT, 281625854),
       "العناية بالشعر": (HAIR, ROOT), "العناية بالجسم": (1329957568, ROOT), "العناية الشخصية": (PERSONAL, ROOT),
       "الحلاقة وإزالة الشعر": (1154799555, PERSONAL), "مزيلات العرق": (PERSONAL, ROOT), "أحمر الشفاه": (569589586, LIPS),
       "مرطب الشفاه": (1620973005, LIPS), "الشفاه": (LIPS, ROOT), "ماسكارا": (993385055, EYES), "البودرة": (213554261, FACE),
       "كريم الأساس": (388642634, FACE), "كريمات الإخفاء والتصحيح": (1337903950, FACE), "الوجه": (FACE, ROOT),
       "الحواجب": (711204929, ROOT), "مكياج العيون": (EYES, ROOT)}
IMG_BASE = "https://raw.githubusercontent.com/mohammedmekh1/products/main/work/beauty1/img/"
web = json.load(open("images_ok.json")) if glob.glob("images_ok.json") else {}
src = {i["sku"]: i for i in json.load(open("items.json"))}
q, excl, fail = [], [], []
for f in sorted(glob.glob(sys.argv[1] if len(sys.argv) > 1 else "chunk_*_out.json")):
    for it in json.load(open(f)):
        s = src[it["sku"]]
        if it.get("category") == "EXCLUDE": excl.append(it["sku"]); continue
        if it.get("category") not in CAT: fail.append(it["sku"]); continue
        img = (web.get(it["sku"]) or [IMG_BASE + it["sku"][4:] + ".jpg"])[:1]
        p = {"sku": it["sku"], "name": it["new_title"], "price": float(s["price"]), "product_type": "product",
             "description": it["new_store_desc_html"], "categories": list(CAT[it["category"]]), "weight": 500, "weight_type": "g",
             "require_shipping": True, "quantity": 0, "metadata_title": it["seo_title"], "metadata_description": it["new_seo_desc"],
             "images": img, "image_alt": it["new_title"][:255]}
        if s["gtin"]: p["gtin"] = s["gtin"]
        q.append(p)
json.dump(q, open("queue.json", "w"), ensure_ascii=False)
print(len(q), "products;", sum(1 for p in q if "raw.githubusercontent" not in p["images"][0]), "with web images; excluded", len(excl), "; bad category", fail)
