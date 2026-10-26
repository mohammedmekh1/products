"""Beauty One gate: batch3 gate checks + title/brand/category/seo_title/tags. Usage: gate1.py chunk_XX_out.json"""
import json, re, sys, importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location("gate", "/root/products/work/batch3/gate.py"); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
CATS = {"سيروم", "مرطبات", "تنظيف الوجه", "واقي الشمس", "ماسكات وتقشير", "زيوت وزبدات", "تفتيح وتوحيد اللون", "العناية بالعين",
        "العناية بالبشرة", "العناية بالشعر", "العناية بالجسم", "العناية الشخصية", "الحلاقة وإزالة الشعر", "مزيلات العرق", "أحمر الشفاه",
        "مرطب الشفاه", "الشفاه", "ماسكارا", "البودرة", "كريم الأساس", "كريمات الإخفاء والتصحيح", "الوجه", "الحواجب", "مكياج العيون", "EXCLUDE"}
AR_DIG = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
def extra(it, src, titles, seo_titles):
    e = []
    if it.get("category") not in CATS: e.append(f"bad category {it.get('category')!r}")
    if it.get("category") == "EXCLUDE": return e
    t, st = it.get("new_title", ""), it.get("seo_title", "")
    if not t or len(t) > 150: e.append(f"title len {len(t)}")
    if t in titles: e.append("title duplicate")
    titles.add(t)
    if not st or len(st) >= 60: e.append(f"seo_title len {len(st)}")
    if st in seo_titles: e.append("seo_title duplicate")
    seo_titles.add(st)
    tags = it.get("tags") or []
    if not 5 <= len(tags) <= 8: e.append(f"tags {len(tags)}")
    srcn = g.nums(str(src.get("title", "")).translate(AR_DIG)) | g.nums(src.get("gtin", ""))
    bad = (g.nums(t) | g.nums(st)) - srcn - {"1", "2", "3", "4", "5"}
    if bad: e.append(f"title numbers not in source {sorted(bad)}")
    for name, x in (("title", t), ("seo_title", st)):
        for rx in g.PROMO + g.MEDICAL:
            if rx.search(x): e.append(f"{name} forbidden word '{rx.search(x).group(0)}'")
        if g.BAD_SYM.search(x): e.append(f"{name} forbidden symbol")
    return e
bad = 0
for p in sys.argv[1:]:
    out = json.loads(Path(p).read_text())
    src = {x["sku"]: x for x in json.loads(Path(p.replace("_out", "_in")).read_text())}
    for x in src.values(): x["title"] = x["title"].translate(AR_DIG)
    miss = set(src) - {x["sku"] for x in out}
    if miss: print("MISSING SKUs:", sorted(miss)); bad += len(miss)
    seen, titles, st = set(), set(), set()
    for it in out:
        s = src.get(it["sku"], {})
        errs = extra(it, s, titles, st)
        if it.get("category") != "EXCLUDE": errs += g.check(it, s, seen)
        if errs: bad += 1; print(it["sku"], "; ".join(errs))
    print(p, len(out), "items checked")
print("FAILED" if bad else "ALL PASS", bad); sys.exit(1 if bad else 0)
