# Content task — Montnero, Beauty One batch (Arabic product content for Salla)

Input: `chunk_XX_in.json` (20 products: sku, title = raw Arabic name from the supplier sheet, gtin, price).
Output: `chunk_XX_out.json` — JSON list, one object per input product, keys:
`sku, new_title, brand, category, new_store_desc_html, new_merchant_desc, seo_title, new_seo_desc, tags`

The ONLY source of facts is the input `title` plus what is universally known about the brand (its official Latin name, country of origin of the brand only if certain). Never invent ingredients, sizes, concentrations, shades, results, or scent notes not in the title. Numbers you write must appear in the title (except 1–5).

## new_title (≤150 chars)
Official brand name in Latin + product type in Arabic + distinguishing feature + size/shade exactly as in the source title. Example: `سيروم The Ordinary نياسيناميد 10% + زنك 1% - 30 مل`. Fix hamza and spacing, Arabic digits → Latin digits. No marketing words, no ALL CAPS, no repeated words. Must be unique within your chunk.

## brand
Official global Latin name as on the pack (e.g. SKIN1004, Huda Beauty, Axis-Y, Color Wow, NYX, Giovanni, SheaMoisture, The Ordinary, Medicube, Eucerin, Charlotte Tilbury, MAC, Tarte). If the title has no recognisable brand, use "".

## category — exactly one of these keys
سيروم، مرطبات، تنظيف الوجه، واقي الشمس، ماسكات وتقشير، زيوت وزبدات، تفتيح وتوحيد اللون، العناية بالعين، العناية بالبشرة، العناية بالشعر، العناية بالجسم، العناية الشخصية، الحلاقة وإزالة الشعر، مزيلات العرق، أحمر الشفاه، مرطب الشفاه، الشفاه، ماسكارا، البودرة، كريم الأساس، كريمات الإخفاء والتصحيح، الوجه، الحواجب، مكياج العيون
Use "EXCLUDE" for toothpaste, toothbrush, supplements, drinks, air fresheners, perfume, tools that are not beauty products.
(lip gloss/lip oil → الشفاه; highlighter/blush/primer/setting spray → الوجه; eyeshadow/eyeliner → مكياج العيون)

## seo_title (< 60 chars)
Keyword first: product type + brand + size. Unique. No promo words.

## tags
List of 5–8 short search phrases (Arabic name, Latin name, brand, type, category, a local Saudi search phrase).
## new_store_desc_html (1800–2950 characters INCLUDING the HTML tags)
Exact structure and order (copy these headings verbatim):
```
<p>intro paragraph: product name, main function, who it suits</p>
<p><strong>وصف المنتج:</strong></p>
<p>detailed description</p>
<p><strong>المميزات:</strong></p>
<ul><li>…</li> ×5 to 7</ul>
<p><strong>لمن يناسب؟</strong></p>
<ul><li>…</li> ×3 to 4</ul>
<p><strong>طريقة الاستخدام:</strong></p>
<p>…</p>
<p><strong>تنبيهات:</strong></p>
<p>…</p>
<p><strong>معلومات المنتج:</strong></p>
<ul><li>الاسم | …</li><li>النوع | …</li><li>الحجم | …</li><li>الدرجة | …</li><li>العلامة التجارية | …</li></ul>
<p><strong>نبذة عن العلامة التجارية:</strong></p>
<p>two lines about the brand</p>
<p><strong>الأسئلة الشائعة:</strong></p>
<p><strong>سؤال؟</strong></p><p>جواب</p>  ×EXACTLY 4
```
- Drop any "معلومات المنتج" line whose value is unknown (e.g. no shade → no الدرجة line).
- Do NOT start with a "الوصف" heading. No "لماذا تشتري من Montnero" section, no "المكونات" section, never mention the shop name.
- Only the 4 FAQ questions may contain "؟" after the الأسئلة الشائعة heading.
- Brand name in its official Latin form as given in `brand`; Arabic form allowed inside prose.

## new_merchant_desc (500–1000 characters, plain text)
Facts only: what it is, who it is for, what it does, size, type, short usage. No HTML, links, emails, phone numbers, hashtags (#), @, calls to buy, discounts, shipping, guarantees, competitor names. Must NOT copy sentences from the store description. Vary the opening sentence between products.

## new_seo_desc (140–155 characters)
Starts with a search verb/phrase (vary them: اكتشفي، تسوقي، اطلبي، احصلي على، جربي، ابحثين عن…), includes the main keyword, may mention السعودية naturally, ends with a short non-pushy invitation. Unique per product. Count characters precisely. Reach the length with real product facts (type, size, use, who it suits) — never pad with filler like "اختاري ما يناسبك" or "اطلعي على المزيد"; at most 2 sentences. Correct grammar: ابحثي (not ابحثين).

## Forbidden everywhere
- Marketing words: أفضل، أقوى، حصري، عرض، خصم، جديد، أصلي، ضمان، شحن مجاني، الأكثر مبيعاً.
- Medical claims: يعالج، يشفي، يقضي على، يزيل حب الشباب، يبيض/تبييض، يزيل التجاعيد، نتائج مضمونة. Allowed: يقلل مظهر، يساعد على، يدعم، يرطب، ينظف، يحسن مظهر. For skin conditions add "يُستحسن استشارة مختص عند وجود حالة جلدية".
- Symbols: $ ^ ~ | and emoji. The `|` inside معلومات المنتج lines is the ONE exception (store description only).
- Vary style between similar products so texts are not duplicates.


## Required self-check before finishing
Run: `/tmp/claude-0/-root-products/6faf72b7-a38d-44d5-97a8-5ab45f1cfe64/scratchpad/venv/bin/python -I /root/products/work/beauty1/gate1.py /root/products/work/beauty1/chunk_XX_out.json`
Fix every reported item (rewrite only the failing field) and re-run until it prints ALL PASS. Count characters with Python, not by eye.
Write the output file with a short Python script (json.dump, ensure_ascii=False) rather than hand-escaping JSON.
