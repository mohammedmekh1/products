"""Fallback main image from the source sheet thumbnail: trim, pad square on white, upscale to 800x800 -> img/<gtin>.jpg"""
import json, os
from PIL import Image, ImageFilter, ImageOps
src = json.load(open("b1img.json"))  # gtin -> [extracted file, size]
os.makedirs("img", exist_ok=True)
n = 0
for i in json.load(open("items.json")):
    g = i["sku"][4:]
    if g not in src: continue
    im = Image.open(src[g][0])
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im); im = bg
    im = im.convert("RGB")
    box = ImageOps.invert(im).getbbox()  # trim white margins
    if box: im = im.crop(box)
    s = int(max(im.size) * 1.08)
    sq = Image.new("RGB", (s, s), "white"); sq.paste(im, ((s - im.width) // 2, (s - im.height) // 2))
    sq = sq.resize((800, 800), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    sq.save(f"img/{g}.jpg", quality=88); n += 1
print(n, "images written")
