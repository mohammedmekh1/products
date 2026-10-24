# Rewrite task — Montnero batch 3 (Arabic product content for Salla)

Input: `chunk_XX_in.json` (25 products). Output: `chunk_XX_out.json` — a JSON list, one object per input product:
`{"sku": ..., "new_store_desc_html": ..., "new_merchant_desc": ..., "new_seo_desc": ...}`

Write fresh Arabic text for each product. The ONLY source of facts is the input item (title, brand, gtin, source_* fields). Never invent ingredients, sizes, concentrations, countries, years, results or scent notes. If a fact is not in the source, leave it out silently — never write "غير متوفر" or "غير مذكور".

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
Run: `/tmp/claude-0/-root-products/6faf72b7-a38d-44d5-97a8-5ab45f1cfe64/scratchpad/venv/bin/python -I /root/products/work/batch3/gate.py /root/products/work/batch3/chunk_XX_out.json`
Fix every reported item and re-run until it prints ALL PASS. "numbers not in source" means you wrote a number absent from the source — remove it.

Then run the duplicate check across the WHOLE batch (all chunks):
`/tmp/claude-0/-root-products/6faf72b7-a38d-44d5-97a8-5ab45f1cfe64/scratchpad/venv/bin/python -I /root/products/work/batch3/dupcheck.py /root/products/work/batch3/chunk_*_out.json`
It lists skus whose store or merchant text reuses sentences that appear in more than 3 other products (templated/padded text). For every listed sku in YOUR chunk, rewrite that field with sentences specific to that product (its type, size, shade, use, who it suits) — never pad length with generic sentences shared across products. Edit only your chunk's file. Re-run both gate.py (your chunk) and dupcheck.py until none of your skus are listed and the gate still passes.
