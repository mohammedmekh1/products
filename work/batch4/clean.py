"""Rule-based cleanup of batch 4 content (no rewriting): fixes heading markup/order, drops price lines,
the why-buy section, and sentences with promo/medical words. Writes clean.json {sku: {store, merchant, seo}}."""
import json, re, sys, importlib.util, openpyxl
spec = importlib.util.spec_from_file_location("gate", "../batch3/gate.py"); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
D = "/root/products/المنتجات/"
HEADS = g.HEADS
BAD = g.PROMO + g.MEDICAL

def bad(t): return any(rx.search(re.sub(r"<[^>]+>", " ", t)) for rx in BAD)

def clean_text(t):
    # drop sentences containing promo/medical words
    parts = re.split(r"(?<=[.!؟])\s+", t)
    return " ".join(p for p in parts if not bad(p) and not re.search(r"(?<![؀-ۿ])ريال|ر\.س", p)).strip()

def clean_store(h):
    h = re.sub(r"<p>\s*<br\s*/?>\s*</p>", "", h or "")
    known = {x.rstrip(":؟") for x in HEADS} | {"لماذا تشتري من Montnero"}
    def hd(m):
        t = m.group(1).strip(); k = t.rstrip(":؟ ").rstrip(":؟")
        return f"<p><b>{t}</b></p>" if k in known else f"<p><strong>{t}</strong></p>"
    h = re.sub(r"<p>(?:<strong>)?\s*([^<]{2,60}?[:؟])\s*(?:</strong>)?</p>", hd, h)
    # split into intro + sections by heading paragraphs (marked <b>)
    toks = re.split(r"(<p><b>[^<]+</b></p>)", h)
    intro, secs, cur = toks[0], {}, None
    for t in toks[1:]:
        m = re.fullmatch(r"<p><b>([^<]+)</b></p>", t)
        if m: cur = m.group(1).strip(); secs.setdefault(cur, "")
        elif cur: secs[cur] += t
    out = []
    for blk in [intro]:
        blk = re.sub(r"<p>([^<]*)</p>", lambda m: f"<p>{clean_text(m.group(1))}</p>" if m.group(1).strip() else "", blk)
        out.append(re.sub(r"<p>\s*</p>", "", blk))
    for hd in HEADS:
        key = next((k for k in secs if k.rstrip(":؟ ").replace("؟", "") == hd.rstrip(":؟ ").replace("؟", "")), None)
        if key is None: continue
        body = secs[key]
        body = re.sub(r"<li>[^<]*(?:السعر|(?<![؀-ۿ])ريال|ر\.س)[^<]*</li>", "", body)
        body = re.sub(r"<li>([^<]*)</li>", lambda m: f"<li>{c}</li>" if (c := clean_text(m.group(1))) else "", body)
        body = re.sub(r"<p>([^<]*)</p>", lambda m: f"<p>{c}</p>" if (c := clean_text(m.group(1))) else "", body)
        body = re.sub(r"<p><strong>[^<]*</strong></p>(?=<p><strong>|$)", "", body)  # FAQ question left without answer
        body = re.sub(r"<ul>\s*</ul>", "", body)
        if re.sub(r"<[^>]+>", "", body).strip(): out.append(f"<p><strong>{hd}</strong></p>" + body)
    return "".join(out)

seo = openpyxl.load_workbook(D + "batch4-merchant-seo.xlsx", read_only=True)
mer = {r[0]: r for r in seo.worksheets[0].iter_rows(min_row=2, values_only=True)}
se = {r[0]: r for r in seo.worksheets[1].iter_rows(min_row=2, values_only=True)}
res = {}
for r in openpyxl.load_workbook(D + "batch4-products-complete.xlsx", read_only=True).worksheets[0].iter_rows(min_row=3, values_only=True):
    if not r[9]: continue
    m = (mer.get(r[9]) or [None] * 3)[2] or ""; s = (se.get(r[9]) or [None] * 4)
    res[r[9]] = {"store": clean_store(r[7]), "merchant": clean_text(m), "seo": clean_text(s[3] or ""), "seo_title": s[2]}
json.dump(res, open("clean.json", "w"), ensure_ascii=False, indent=1)
# report
import collections; c = collections.Counter(); seen = set(); nbad = 0
for k, v in res.items():
    e = g.check({"new_store_desc_html": v["store"], "new_merchant_desc": v["merchant"], "new_seo_desc": v["seo"]}, {}, seen)
    e = [x for x in e if not x.startswith(("numbers", "seo len", "store len", "merchant len", "features", "who-for", "faq", "seo dup"))]
    if e: nbad += 1
    for x in e: c[" ".join(x.split()[:3])] += 1
print(len(res), "cleaned; remaining hard issues:", nbad, c.most_common(10))
