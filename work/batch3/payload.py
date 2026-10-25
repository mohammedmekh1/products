"""Build upload payloads for products that have a verified image. Usage: payload.py [price_factor]"""
import json, glob, sys, openpyxl
from pathlib import Path

D, W = Path("/root/products/المنتجات"), Path(__file__).parent
CAT = {  # last path segment -> Salla category id (verified 2026-10-24)
    "سيروم": 1189881341, "مرطبات": 281625854, "تنظيف الوجه": 1654023167, "واقي الشمس": 1014792952,
    "ماسكات وتقشير": 240755193, "زيوت وزبدات": 1478934778, "تفتيح وتوحيد اللون": 704901115,
    "العناية بالعين": 1370828229, "العناية بالبشرة": 2041195310, "العناية بالشعر": 2105502663,
    "العناية بالجسم": 1329957568, "العناية الشخصية": 1796196546, "الحلاقة وإزالة الشعر": 1154799555,
    "أحمر الشفاه": 569589586, "ماسكارا": 603229516, "البودرة": 246604359, "كريم الأساس": 246604359,
    "كريمات الإخفاء والتصحيح": 246604359,
}
ALL = "--all" in sys.argv
args = [a for a in sys.argv[1:] if a != "--all"]
factor = float(args[0]) if args else 1.0
imgs = {k: v for p in glob.glob(str(W / "chunk_*_img.json")) for k, v in json.loads(Path(p).read_text()).items()}
out = {x["sku"]: x for p in glob.glob(str(W / "chunk_*_out.json")) for x in json.loads(Path(p).read_text())}
seo = {r[0]: r for r in openpyxl.load_workbook(D / "batch3-merchant-seo.xlsx", read_only=True).worksheets[1].iter_rows(min_row=2, values_only=True)}
qty = {r[0]: r[2] for r in openpyxl.load_workbook(D / "batch3-review.xlsx", read_only=True)["الكميات"].iter_rows(min_row=2, values_only=True)}

payload = []
for r in openpyxl.load_workbook(D / "batch3-products-complete.xlsx", read_only=True).worksheets[0].iter_rows(min_row=3, values_only=True):
    sku = r[9]
    if not sku or (sku not in imgs and not ALL):
        continue
    cat = r[2].split(">")[-1].strip()
    p = {
        "sku": sku, "name": r[1].strip(), "price": round(float(r[6]) * factor, 2), "product_type": "product",
        "description": r[7], "categories": [CAT[cat]], "weight": 500, "weight_type": "g",
        "require_shipping": True, "status": "hidden", "quantity": int(qty.get(sku) or 0),
        "metadata_title": seo[sku][2], "metadata_description": out[sku]["new_seo_desc"],
        "image_url": imgs.get(sku, {}).get("url"), "image_alt": r[1].strip()[:255],
    }
    if r[25]:
        p["gtin"] = str(r[25])
    payload.append(p)
(W / "upload_payload.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1))
print(len(payload), "products with images ready; categories:", sorted({c for p in payload for c in p["categories"]}))
