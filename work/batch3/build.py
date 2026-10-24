"""Write rewritten content into the batch3 deliverables (in place; originals are in git)."""
import json, glob, openpyxl
from pathlib import Path

D = Path("/root/products/المنتجات")
W = Path(__file__).parent
EXCLUDED = {
    "MNT-3014260101626": "فرشاة أسنان - العناية بالفم خارج فئات التجميل",
    "MNT-3014260807214": "فرشاة أسنان - العناية بالفم خارج فئات التجميل",
    "MNT-3574661177120": "غسول فم - العناية بالفم خارج فئات التجميل",
    "MNT-3574661177144": "غسول فم - العناية بالفم خارج فئات التجميل",
    "MNT-3574661177151": "غسول فم - العناية بالفم خارج فئات التجميل",
    "MNT-3574661397634": "غسول فم - العناية بالفم خارج فئات التجميل",
}
out = {x["sku"]: x for p in sorted(glob.glob(str(W / "chunk_*_out.json"))) for x in json.loads(Path(p).read_text())}
src = {x["sku"]: x for p in sorted(glob.glob(str(W / "chunk_*_in.json"))) for x in json.loads(Path(p).read_text())}
cats = json.loads((W / "categories.json").read_text())

titles = {}
for s, x in src.items():
    titles.setdefault(x["title"].strip(), []).append(s)
for t, skus in titles.items():
    if len(skus) > 1:
        for s in skus:
            EXCLUDED[s] = "عنوان مكرر مع منتج آخر بباركود مختلف - يحتاج تمييز المتغير قبل الرفع"
assert set(out) == set(src) and len(out) == 298

# products file: rows 0-1 are headers; col 2 category, col 7 description, col 9 sku
wb = openpyxl.load_workbook(D / "batch3-products-complete.xlsx")
ws = wb.worksheets[0]
for r in range(ws.max_row, 2, -1):
    sku = ws.cell(r, 10).value
    if not sku:
        continue
    if sku in EXCLUDED:
        ws.delete_rows(r)
        continue
    ws.cell(r, 3).value = cats[sku]
    ws.cell(r, 8).value = out[sku]["new_store_desc_html"]
wb.save(D / "batch3-products-complete.xlsx")

wb = openpyxl.load_workbook(D / "batch3-merchant-seo.xlsx")
gm, seo = wb.worksheets[0], wb.worksheets[1]
for ws, col, field in ((gm, 3, "new_merchant_desc"), (seo, 4, "new_seo_desc")):
    for r in range(ws.max_row, 1, -1):
        sku = ws.cell(r, 1).value
        if sku in EXCLUDED:
            ws.delete_rows(r)
        elif sku in out:
            ws.cell(r, col).value = out[sku][field]
for r in range(2, seo.max_row + 1):
    if seo.cell(r, 1).value in cats:
        seo.cell(r, 5).value = cats[seo.cell(r, 1).value]
wb.save(D / "batch3-merchant-seo.xlsx")

wb = openpyxl.load_workbook(D / "batch3-review.xlsx")
rv = wb["تقرير-المراجعة"] if "تقرير-المراجعة" in wb.sheetnames else wb.worksheets[1]
for s, why in EXCLUDED.items():
    rv.append([s, src[s]["title"], "مستثنى من ملف الرفع", why])
rv.append(["-", "-", "إعادة كتابة شاملة", "أُعيدت كتابة وصف المتجر وميرشنت وSEO لـ 298 منتجاً، واجتازت بوابة 3.17 الآلية وفحص التكرار"])
rv.append(["-", "-", "تصحيح الأقسام", "أُضيف الفاصل > ومستوى المكياج لمسارات الأقسام"])
rv.append(["-", "-", "الصور", "لم تُسحب بعد - مطلوبة قبل الرفع"])
wb.save(D / "batch3-review.xlsx")
print("ready", 298 - len(EXCLUDED), "excluded", len(EXCLUDED))
