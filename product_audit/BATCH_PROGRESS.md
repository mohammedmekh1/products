# BATCH_PROGRESS
الدفعة = 200 منتج من ملف المخزون (بالترتيب). مرجع الحالة: REVIEW_LOG.csv، الفهرس: data/master_index.csv

## الدفعة A001 (منتجات 1-200)
- محتوى جاهز (كتابة فردية): 3-50 في `batches/A001_p1.json` (47 منتجاً بعد استثناء 3 السليم؛ المنتجان 1 و2 حُدّثا مباشرة سابقاً).
- مستثنى من الدفعات القديمة (لا صفحات): 51,54,55,56,57,69,73,74,89,90 ... (انظر master_index: batch=excluded).
- المتبقي في A001: 52,53,58-200 (كتابة فردية تُحفظ في batches/A001_p2.json وما بعده).
- صفحة المزامنة (Artifact): https://claude.ai/artifact/A1gB4EFpzKBLS3yiZ99h4R  (بناء: tools/make_sync_page.py A001 <ملفات json>؛ تُنشر بنفس المسار فيبقى الرابط)
- صفحة التقرير: https://claude.ai/artifact/VYyTtBJQUpENQjr5YBdP37 (بناء: tools/make_report.py)
- لا يوجد رفع بواسطة Claude: المالك يشغّل صفحة المزامنة؛ نتائجها في db باسم syncA001/n<رقم> ويقرؤها Claude بـ ArtifactData.
- أسئلة معلقة بانتظار إجابة المالك: report A001 (حُفظت في db report A001/answers).

## الدفعة التالية
إكمال A001 من المنتج 52 ثم A002 (201-400).
