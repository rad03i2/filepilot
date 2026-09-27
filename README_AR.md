<div dir="rtl" align="right">

<p align="center">
<img src="assets/filepilot-brand-cover.svg" alt="FilePilot" width="100%" />
</p>

# FilePilot — الدليل العربي

**أداة سطر أوامر صغيرة لتنظيم الملفات محليًا، مع معاينة قبل التنفيذ وإمكانية التراجع باستخدام Manifest.**

[README الرئيسي](README.md) · [المعمارية](docs/ARCHITECTURE.md) · [الهوية](docs/BRAND.md) · [الأمان](SECURITY.md)

## الفكرة الأساسية

FilePilot لا يبدأ بالنقل مباشرة. المسار المقصود هو:

<pre>
معاينة → مراجعة → تنظيم → Manifest → تراجع
</pre>

الأمر <code>filepilot plan</code> يعرض ما سيحدث من دون تغيير الملفات، ثم <code>filepilot organize</code> ينفذ الخطة، وتُحفظ النقلات الناجحة داخل ملف JSON يمكن استعماله لاحقًا مع <code>filepilot undo</code>.

لا يحتاج البرنامج إلى خدمة سحابية أو حساب أو قاعدة بيانات أو برنامج يعمل في الخلفية.

## ما الذي ينفذه فعليًا؟

| الجزء | السلوك الحالي |
|---|---|
| المعاينة | عرض النقلات المقترحة دون تعديل الملفات |
| التصنيف | يعتمد على امتداد الملف |
| تعارض الأسماء | إنشاء اسم فريد بدل استبدال ملف موجود |
| التراجع | تسجيل النقلات في Manifest وإعادتها بترتيب عكسي |
| الفشل أثناء التنفيذ | محاولة إرجاع النقلات التي تمت قبل الخطأ |
| الملفات المخفية | تُتجاهل افتراضيًا |
| الوضع المتكرر | يتطلب وجهة مختلفة عن المصدر |
| التحقق | حساب SHA-256 |
| اعتماديات التشغيل | مكتبة Python القياسية فقط |
| الاختبارات | pytest مع CI متعدد الأنظمة |

> FilePilot يقلل مخاطر التنظيم الآلي، لكنه ليس بديلًا عن النسخ الاحتياطية للملفات التي لا يمكن تعويضها.

## التثبيت والاستخدام

~~~bash
git clone https://github.com/rad03i2/filepilot.git
cd filepilot
python -m venv .venv
python -m pip install -e .

filepilot plan ~/Downloads
filepilot organize ~/Downloads --manifest ~/filepilot-run.json
filepilot undo ~/filepilot-run.json
~~~

للتنظيم المتكرر يجب تحديد وجهة مستقلة:

~~~bash
filepilot plan ~/Downloads --destination ~/Sorted --recursive
filepilot organize ~/Downloads --destination ~/Sorted --recursive --manifest ~/filepilot-run.json
~~~

وللملفات المخفية والتحقق:

~~~bash
filepilot plan ~/Downloads --include-hidden
filepilot hash path/to/file.iso
~~~

## كيف يحمي الملفات؟

قبل النقل:
- المعاينة لا تغير أي ملف.
- الملفات المخفية مستثناة افتراضيًا.
- الوضع المتكرر لا يسمح باستخدام المصدر نفسه كوجهة.
- الخطة تحجز الأسماء المقترحة لمنع التعارض.

أثناء التنفيذ:
- لا يتم استبدال ملف موجود في الوجهة.
- إذا وقع خطأ بعد عدة نقلات، يحاول البرنامج إرجاع النقلات السابقة.
- لا يقبل الكتابة فوق Manifest موجود مسبقًا.

أثناء التراجع:
- تتم إعادة النقلات بترتيب عكسي.
- إذا اختفى الملف المنقول يتم تجاوزه.
- إذا أصبح المسار الأصلي مشغولًا، يتوقف بدل استبداله.

## الحدود الحالية

- التصنيف يعتمد على الامتداد وليس محتوى الملف.
- لا توجد واجهة رسومية.
- لا توجد مزامنة سحابية أو كود شبكي.
- لا يوجد تشغيل تلقائي بالخلفية أو جدولة.
- التراجع يعيد الملفات لكنه لا يحذف مجلدات التصنيف الفارغة.
- الـManifest يسجل مسارات النقل ولا يخزن نسخة من المحتوى.

## الاختبارات

~~~bash
python -m pip install -e . pytest
pytest -q
~~~

الـCI الحالي يعمل على Ubuntu وWindows وmacOS مع Python 3.10 و3.12 و3.13.

## المطور

**رضوان عبدالهادي**  
**Radwan Abd alhady Ahmed**  
GitHub: [@rad03i2](https://github.com/rad03i2)

</div>
