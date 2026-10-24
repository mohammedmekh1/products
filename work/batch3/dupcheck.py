"""Flag templated texts. Usage: dupcheck.py chunk_*_out.json  (prints sku + field, exit 1 if any)."""
import json, re, sys
from collections import Counter
from pathlib import Path

def sents(t, store):
    if store:  # warnings and info lines legitimately repeat
        t = re.sub(r"<p><strong>تنبيهات:</strong></p><p>.*?</p>", "", t, flags=re.S)
        t = re.sub(r"<p><strong>معلومات المنتج:</strong></p><ul>.*?</ul>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", "\n", t)
    out = {s.strip() for s in re.split(r"[.\n؟!:]", t) if len(s.strip()) > 30}
    return {s for s in out if "مختص" not in s and "تهيج" not in s}

def main(paths, shared=3, limit=0.25):
    items = [x for p in paths for x in json.loads(Path(p).read_text())]
    bad = []
    for field in ("new_store_desc_html", "new_merchant_desc"):
        S = {x["sku"]: sents(x[field], field.startswith("new_store")) for x in items}
        freq = Counter(s for v in S.values() for s in v)
        for sku, v in S.items():
            rep = [s for s in v if freq[s] > shared]
            if len(rep) / max(len(v), 1) > limit:
                bad.append((sku, field, len(rep), rep[0][:60]))
    for b in bad:
        print(*b)
    print(f"{len(bad)} templated items")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main(sys.argv[1:])
