# Image task — Montnero batch 3

Input: `chunk_XX_in.json` (use `sku`, `title`, `brand`, `gtin`). Skip skus listed in `excluded.txt`.
Output: `chunk_XX_img.json` = `{"sku": {"url": "https://...", "source": "brand site|retailer name", "w": 1000, "h": 1000}}`. Omit a sku when no acceptable image is found and list it in `chunk_XX_noimg.txt` with a short reason.

## Where to look (in order)
1. Official brand site product page (og:image / main product image).
2. Authorized retailers: Amazon (amazon.sa / amazon.com), Noon, iHerb, Nahdi, Boots, the brand's regional site.
Match the EXACT product: same variant, size, shade, scent. Barcode (gtin) search helps (e.g. upcitemdb, barcodelookup) to identify the product, but take the image from a store page.

## Acceptance rules (strict)
- Main image shows the closed pack/bottle/tube/jar of THIS product only, on a white or near-white background. A clean studio packshot with some white margin is ACCEPTED (the product need not touch the edges). Reject only staged scenes: mid/dark grey or coloured backdrops, strong cast shadows on a surface, or the product occupying under about a quarter of the frame.
- If a store shows the same product in several sizes/scents, the image must show the matching one (read the label in the picture).
- Minimum 800×800 px (verify by downloading and reading real pixel size with PIL).
- Reject: before/after, product applied on face/hair/body, people/models, collage, multiple different products, discount badges, store logos, watermarks, promo text, frames, AI-generated or graphic designs.
- Must be HTTPS, directly downloadable image (jpg/png/webp), under 10 MB.

## Verification (required)
Download each candidate to `/tmp/claude-0/-root-products/6faf72b7-a38d-44d5-97a8-5ab45f1cfe64/scratchpad/img_XX/` (XX = your chunk), check size with PIL, then build ONE contact sheet (grid, each thumb labelled with sku) and look at it with the Read tool. Remove any image that breaks a rule or does not match the title (wrong shade/size/variant). Name your scripts with your chunk number (e.g. `img_XX.py`) inside that folder so they never clash with other agents.

Python with PIL: `/tmp/claude-0/-root-products/6faf72b7-a38d-44d5-97a8-5ab45f1cfe64/scratchpad/venv/bin/python` (install pillow with its pip if missing).
