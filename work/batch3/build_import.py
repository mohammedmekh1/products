"""Write a Salla import xlsx for verified-image products not yet uploaded and not in a previous import file. Usage: build_import.py out.xlsx [previous.xlsx ...]"""
import json, glob, sys, re, openpyxl
from pathlib import Path
D, W = Path("/root/products/المنتجات"), Path(__file__).parent
imgs = {k: v for p in glob.glob(str(W / "chunk_*_img.json")) for k, v in json.loads(Path(p).read_text()).items()}
skip = set(json.loads((W / "uploaded.json").read_text()))
for prev in sys.argv[2:]:
    skip |= {r[9] for r in openpyxl.load_workbook(D / prev, read_only=True).worksheets[0].iter_rows(min_row=3, values_only=True) if r[9]}
wb = openpyxl.load_workbook(D / "batch3-import-remaining.xlsx"); ws = wb.worksheets[0]
for i in range(ws.max_row, 2, -1):
    sku = ws.cell(i, 10).value
    if sku in imgs and sku not in skip:
        ws.cell(i, 4).value = imgs[sku]["url"]; ws.cell(i, 5).value = re.sub(r"[./+]", "-", ws.cell(i, 2).value.strip())[:255]
    else:
        ws.delete_rows(i)
wb.save(D / sys.argv[1]); print(ws.max_row - 2, "products ->", sys.argv[1])
