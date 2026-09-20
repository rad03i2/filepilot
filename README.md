# FilePilot

**Safe, local-first file organization with preview and undo.**

FilePilot is a cross-platform Python CLI that organizes files into useful type-based folders without sending data anywhere. Its safety model is deliberate: preview first, avoid filename collisions, write an undo manifest, and roll back completed moves if an operation fails midway.

## English

### Why FilePilot?
Downloads and working folders become noisy quickly. Simple organizer scripts often overwrite files or move content with no recovery path. FilePilot provides a small, auditable tool designed around reversible operations.

### Features
- **Dry-run planning** with `filepilot plan` — changes nothing.
- **Type-based organization** for images, videos, audio, documents, spreadsheets, presentations, archives, code, and unknown files.
- **Collision-safe naming** (`report (1).pdf`, etc.) instead of overwriting.
- **Undo manifests** recording every successful move.
- **Transactional rollback** if an apply operation fails partway through.
- **Hidden-file protection** by default; opt in explicitly.
- **Optional recursive scanning**, requiring a separate destination for safety.
- **SHA-256 hashing** for quick integrity checks.
- No runtime dependencies; Python standard library only.

### Requirements
- Python 3.10+
- `pytest` only for running the test suite.

### Installation
```bash
git clone https://github.com/rad03i2/filepilot.git
cd filepilot
python -m pip install -e .
```

For development/testing:
```bash
python -m pip install pytest
pytest
```

### Usage
Preview a folder first:
```bash
filepilot plan ~/Downloads
```

Organize it after reviewing the plan:
```bash
filepilot organize ~/Downloads --manifest ~/filepilot-run.json
```

For unattended/local automation after you have verified the plan:
```bash
filepilot organize ~/Downloads --manifest ~/filepilot-run.json --yes
```

Use a separate destination and recurse through subfolders:
```bash
filepilot plan ~/Downloads --destination ~/Sorted --recursive
filepilot organize ~/Downloads --destination ~/Sorted --recursive --manifest ~/filepilot-run.json
```

Undo a completed run:
```bash
filepilot undo ~/filepilot-run.json
```

Calculate SHA-256:
```bash
filepilot hash path/to/file.iso
```

### Safety and privacy
FilePilot runs locally and has no network code. It does not delete source files: organization uses filesystem moves. Existing destination files are never overwritten. Hidden files are skipped unless `--include-hidden` is supplied. An undo can stop if an original path has become occupied; this is intentional to avoid data loss. As with any filesystem tool, preview important folders and keep backups of irreplaceable data.

### Project structure
```text
src/filepilot/core.py   planning, categories, moves, rollback, hashing
src/filepilot/cli.py    command-line interface
src/filepilot/__init__.py
 tests/test_core.py      behavior tests
.github/workflows/ci.yml
```

### Limitations
- Classification is extension-based; FilePilot does not inspect MIME/file signatures.
- Undo restores moved files but intentionally does not delete empty category directories.
- Recursive organization requires a destination outside the source directory to prevent repeated processing.

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Please include tests for behavior changes and keep destructive behavior opt-in.

---

## العربية

### ما هو FilePilot؟
**FilePilot** أداة سطر أوامر بلغة بايثون لتنظيم الملفات محليًا وبطريقة قابلة للتراجع. صُممت لتكون آمنة قبل أن تكون سريعة: يمكنك معاينة الخطة أولًا، ولا تستبدل الملفات الموجودة، وتحفظ سجلًا يسمح بإرجاع الملفات إلى أماكنها الأصلية.

### لماذا هذا المشروع؟
تمتلئ مجلدات التنزيل والعمل بالملفات بسرعة، بينما قد تقوم سكربتات التنظيم البسيطة بالنقل مباشرة أو باستبدال ملف موجود. يعالج FilePilot ذلك بخطة واضحة قبل التنفيذ ومسار تراجع موثق.

### المزايا
- معاينة كاملة قبل أي تغيير بواسطة `filepilot plan`.
- تصنيف الصور والفيديو والصوت والمستندات والجداول والعروض والأرشيفات وملفات البرمجة وغيرها.
- منع استبدال الملفات عبر إنشاء اسم فريد تلقائيًا عند التعارض.
- إنشاء Manifest لكل عملية ناجحة لإمكانية التراجع.
- إرجاع النقلات المنفذة تلقائيًا إذا فشلت العملية في منتصف التنفيذ.
- تجاهل الملفات المخفية افتراضيًا لحمايتها.
- فحص المجلدات الفرعية اختياريًا مع اشتراط وجهة منفصلة للأمان.
- حساب SHA-256 للتحقق من سلامة الملفات.
- لا توجد مكتبات مطلوبة وقت التشغيل؛ يعتمد على مكتبة بايثون القياسية.

### التثبيت
```bash
git clone https://github.com/rad03i2/filepilot.git
cd filepilot
python -m pip install -e .
```

### الاستخدام
عاين الخطة أولًا:
```bash
filepilot plan ~/Downloads
```

نفّذ التنظيم واحفظ سجل التراجع:
```bash
filepilot organize ~/Downloads --manifest ~/filepilot-run.json
```

للتراجع:
```bash
filepilot undo ~/filepilot-run.json
```

ولحساب بصمة ملف:
```bash
filepilot hash path/to/file.iso
```

### الخصوصية والأمان
تعمل الأداة محليًا ولا تحتوي على كود شبكي. لا تستبدل ملفًا موجودًا في الوجهة، وتتجاهل الملفات المخفية افتراضيًا. عند التراجع، إذا أصبح المسار الأصلي مشغولًا بملف جديد تتوقف الأداة بدل استبداله. يوصى دائمًا بمعاينة الخطة والاحتفاظ بنسخة احتياطية من البيانات المهمة.

### القيود الحالية
- التصنيف يعتمد على امتداد الملف ولا يفحص نوع المحتوى الداخلي.
- التراجع يعيد الملفات لكنه لا يحذف مجلدات التصنيف الفارغة.
- الفحص المتكرر للمجلدات الفرعية يتطلب وجهة منفصلة لتجنب إعادة معالجة الملفات.

### المساهمة
راجع [CONTRIBUTING.md](CONTRIBUTING.md). أي تغيير في السلوك يجب أن يتضمن اختبارات مناسبة، ويجب أن تبقى العمليات الخطرة اختيارية وواضحة.

## Author / المؤلف

**Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

## License / الترخيص
Released under the [MIT License](LICENSE). / متاح بموجب ترخيص MIT.
