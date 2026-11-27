# تشغيل Claude Code في الطرفية لبناء الدفعات

1) تثبيت Claude Code (مرة واحدة):
```bash
npm install -g @anthropic-ai/claude-code
```
2) جلب المستودع والفرع الذي فيه العمل:
```bash
git clone https://github.com/mohammedmekh1/products.git
cd products
git checkout claude/adoring-darwin-2ctyd2
git pull
```
3) فتح Claude Code وتسجيل الدخول بحساب claude.ai (نفس حساب الموصلات مثل سلة):
```bash
claude
```
ثم اكتب `/login` إن طُلب.
4) اكتب له هذه الرسالة فقط:
```
اقرأ product_audit/TERMINAL_PROMPT.md ونفّذه حرفياً: ابنِ الدفعة التالية من 200 منتج وتابع من حيث وصل العمل.
```
5) لمتابعة العمل في جلسة جديدة لاحقاً: افتح `claude` في المجلد نفسه وأعد الرسالة نفسها. ملفات التقدم في product_audit تغنيه عن إعادة تحليل المستودع.
ملاحظات: اسمح له بأدوات البحث والويب عند السؤال. لا يرفع شيئاً إلى سلة: الرفع يتم من صفحة المزامنة التي تفتحها أنت.
