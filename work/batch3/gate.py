"""Gate check for rewrite output. Usage: gate.py chunk_XX_out.json [more...]  (exit 1 on any failure)."""
import json, re, sys
from pathlib import Path

AR = r"؀-ۿ"
def word(w):  # Arabic-aware word boundary, allows ال/و/ب/ل prefixes
    return re.compile(rf"(?<![{AR}])(?:[وبلف]?(?:ال)?){w}(?![{AR}])")

PROMO = [word(w) for w in ["أفضل", "افضل", "أقوى", "اقوى", "حصري", "حصرية", "عرض", "خصم", "جديد", "جديدة",
                           "أصلي", "اصلي", "أصلية", "ضمان", "مضمون", "مضمونة"]]
PROMO += [re.compile(p) for p in ["شحن مجاني", "الأكثر مبيعا", "الاكثر مبيعا"]]
MEDICAL = [word(w) for w in ["يعالج", "تعالج", "علاج", "يشفي", "تشفي", "يبيض", "تبيض", "تبييض"]]
MEDICAL += [re.compile(p) for p in ["يقضي على", "تقضي على", "يزيل حب الشباب", "يزيل التجاعيد", "نتائج مضمونة"]]
BAD_SYM = re.compile(r"[$^~|]|[\U0001F000-\U0001FAFF☀-➿]")
HEADS = ["وصف المنتج:", "المميزات:", "لمن يناسب؟", "طريقة الاستخدام:", "تنبيهات:",
         "معلومات المنتج:", "نبذة عن العلامة التجارية:", "الأسئلة الشائعة:"]


def text(html):
    return re.sub(r"<[^>]+>", " ", html or "")


def nums(s):
    return set(re.findall(r"\d+(?:[.,]\d+)?", s or ""))


def check(item, src, seen_seo):
    e = []
    h, m, s = item.get("new_store_desc_html", ""), item.get("new_merchant_desc", ""), item.get("new_seo_desc", "")
    if not 1800 <= len(h) <= 2950: e.append(f"store len {len(h)}")
    if not h.startswith("<p>") or h.startswith("<p><strong>"): e.append("store must open with intro paragraph")
    pos = [h.find(x) for x in HEADS]
    if -1 in pos: e.append("missing heading " + HEADS[pos.index(-1)])
    elif pos != sorted(pos): e.append("headings out of order")
    if "لماذا تشتري" in h or "Montnero" in h: e.append("store mentions shop/why-buy")
    if re.search(r"<strong>\s*المكونات", h): e.append("ingredients section")
    seg = lambda a, b: h[h.find(a): h.find(b)] if a in h and b in h else ""
    nf = seg("المميزات:", "لمن يناسب").count("<li>")
    nw = seg("لمن يناسب", "طريقة الاستخدام:").count("<li>")
    nq = h[h.find("الأسئلة الشائعة:"):].count("؟") if "الأسئلة الشائعة:" in h else 0
    if not 5 <= nf <= 7: e.append(f"features {nf}")
    if not 3 <= nw <= 4: e.append(f"who-for {nw}")
    if nq != 4: e.append(f"faq questions {nq}")
    if not 500 <= len(m) <= 1000: e.append(f"merchant len {len(m)}")
    if re.search(r"<|>|https?:|www\.|#|@", m): e.append("merchant has html/link/#")
    if not 140 <= len(s) <= 155: e.append(f"seo len {len(s)}")
    if s in seen_seo: e.append("seo duplicate")
    if s.count(".") > 2 or re.search(r"اطلعي على المزيد|اختاري ما يناسبك", s): e.append("seo filler sentences")
    if re.search(r"ابحثين|تسوقين(?![{AR}])", s + m): e.append("grammar: ابحثين -> ابحثي")
    seen_seo.add(s)
    if m.strip()[:60] in text(h): e.append("merchant copies store text")
    for name, t in (("store", text(h)), ("merchant", m), ("seo", s)):
        for rx in PROMO:
            if rx.search(t): e.append(f"{name} promo word '{rx.search(t).group(0)}'")
        for rx in MEDICAL:
            if rx.search(t): e.append(f"{name} medical claim '{rx.search(t).group(0)}'")
        # the store template itself uses "|" in معلومات المنتج lines
        if BAD_SYM.search(t.replace("|", "") if name == "store" else t): e.append(f"{name} forbidden symbol")
    srcnums = nums(" ".join(str(src.get(k) or "") for k in
                            ("title", "source_store_desc_html", "source_merchant_desc", "source_seo_desc", "gtin", "seo_title")))
    extra = (nums(text(h)) | nums(m) | nums(s)) - srcnums - {"1", "2", "3", "4", "5"}
    if extra: e.append(f"numbers not in source (possible fabrication): {sorted(extra)}")
    return e


def main(paths):
    bad = 0
    for p in paths:
        out = json.loads(Path(p).read_text())
        src = {x["sku"]: x for x in json.loads(Path(p.replace("_out", "_in")).read_text())}
        miss = set(src) - {x["sku"] for x in out}
        if miss: print(p, "MISSING SKUs:", sorted(miss)); bad += len(miss)
        seen = set()
        for it in out:
            errs = check(it, src.get(it["sku"], {}), seen)
            if errs: bad += 1; print(p, it["sku"], "; ".join(errs))
        print(p, f"{len(out)} items checked")
    print("FAILED" if bad else "ALL PASS", bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
