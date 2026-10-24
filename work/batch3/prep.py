"""Split batch3 into rewrite chunks of 25 products (source facts only)."""
import json, sys, openpyxl
from pathlib import Path

SRC = Path("/root/products/المنتجات")
OUT = Path(__file__).parent
MAKEUP = {"الوجه", "العيون", "الشفاه", "الحواجب", "الأظافر", "الاظافر", "الفرش"}
SUBS = ["الحلاقة وإزالة الشعر", "تفتيح وتوحيد اللون", "تنظيف الوجه", "ماسكات وتقشير",
        "مرطبات", "أحمر الشفاه", "البودرة"]


def fix_category(c):
    # "العناية بالبشرة مرطبات" -> "العناية بالبشرة > مرطبات"
    parts = [p.strip() for p in c.split(">")]
    out = []
    for p in parts:
        for s in SUBS:
            if p.endswith(" " + s) and p != s:
                out += [p[: -len(s) - 1].strip(), s]
                break
        else:
            out.append(p)
    if len(out) > 1 and out[1] in MAKEUP:
        out.insert(1, "المكياج")
    return " > ".join(out)


def main():
    rows = list(openpyxl.load_workbook(SRC / "batch3-products-complete.xlsx", read_only=True)
                .worksheets[0].iter_rows(values_only=True))
    hdr = rows[1]
    col = {h.strip(): i for i, h in enumerate(hdr) if h}
    m = openpyxl.load_workbook(SRC / "batch3-merchant-seo.xlsx", read_only=True)
    merch = {r[0]: r for r in list(m.worksheets[0].iter_rows(values_only=True))[1:]}
    seo = {r[0]: r for r in list(m.worksheets[1].iter_rows(values_only=True))[1:]}
    items = []
    for r in rows[2:]:
        if not r[col["أسم المنتج"]]:
            continue
        sku = r[col["رمز المنتج sku"]]
        mr, sr = merch.get(sku), seo.get(sku)
        items.append({
            "sku": sku,
            "title": r[col["أسم المنتج"]],
            "category": fix_category(r[col["تصنيف المنتج"]] or ""),
            "brand": r[col["الماركة"]] or (mr[6] if mr else None),
            "gtin": r[col["GTIN"]],
            "price": r[col["سعر المنتج"]],
            "source_store_desc_html": r[col["الوصف"]],
            "source_merchant_desc": mr[2] if mr else None,
            "seo_title": sr[2] if sr else None,
            "source_seo_desc": sr[3] if sr else None,
        })
    for i in range(0, len(items), 25):
        (OUT / f"chunk_{i // 25 + 1:02d}_in.json").write_text(
            json.dumps(items[i:i + 25], ensure_ascii=False, indent=1))
    (OUT / "categories.json").write_text(
        json.dumps({it["sku"]: it["category"] for it in items}, ensure_ascii=False, indent=1))
    print(len(items), "items,", -(-len(items) // 25), "chunks")
    print(sorted({it["category"] for it in items}))


if __name__ == "__main__":
    assert fix_category("العناية والجمال > العناية بالبشرة مرطبات") == "العناية والجمال > العناية بالبشرة > مرطبات"
    assert fix_category("العناية والجمال > الشفاه أحمر الشفاه") == "العناية والجمال > المكياج > الشفاه > أحمر الشفاه"
    assert fix_category("العناية والجمال > العناية بالشعر") == "العناية والجمال > العناية بالشعر"
    main()
