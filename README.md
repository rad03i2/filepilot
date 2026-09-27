<!-- FilePilot identity: reversible-by-design -->
<p align="center">
  <img src="assets/filepilot-brand-cover.svg" alt="FilePilot — Preview. Organize. Undo." width="100%">
</p>

<p align="center">
  <strong>Safe, local-first file organization with preview and undo.</strong><br>
  A small cross-platform Python CLI built around reversible filesystem operations.
</p>

<p align="center">
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="License MIT" src="https://img.shields.io/badge/License-MIT-16A085">
  <img alt="Local first" src="https://img.shields.io/badge/Privacy-local--first-0B6E69">
  <img alt="CI" src="https://img.shields.io/badge/CI-Linux%20%7C%20Windows%20%7C%20macOS-47A8FF">
</p>

# FilePilot

FilePilot organizes noisy folders into useful type-based directories **without sending data anywhere**. Its safety model is deliberate: preview first, avoid filename collisions, record successful moves in an undo manifest, and roll back completed moves if an operation fails midway.

> **Design principle:** understand the plan before touching the filesystem.

## ✦ What makes it different

| Capability | FilePilot behavior |
|---|---|
| Preview | `filepilot plan` changes nothing |
| Collisions | Generates a safe unique name instead of overwriting |
| Recovery | Writes an undo manifest for successful moves |
| Partial failure | Attempts transactional rollback |
| Hidden files | Skipped by default |
| Recursive mode | Requires a separate destination for safety |
| Integrity | Includes SHA-256 hashing |
| Runtime | Python standard library only |

## Quick start

**Requirements:** Python 3.10+. `pytest` is only needed for tests.

```bash
git clone https://github.com/rad03i2/filepilot.git
cd filepilot
python -m pip install -e .
```

Preview first:

```bash
filepilot plan ~/Downloads
```

Then organize and keep a recovery manifest:

```bash
filepilot organize ~/Downloads --manifest ~/filepilot-run.json
```

Undo the run:

```bash
filepilot undo ~/filepilot-run.json
```

Recursive organization uses a separate destination:

```bash
filepilot plan ~/Downloads --destination ~/Sorted --recursive
filepilot organize ~/Downloads --destination ~/Sorted --recursive --manifest ~/filepilot-run.json
```

Calculate SHA-256:

```bash
filepilot hash path/to/file.iso
```

## Safety & privacy

FilePilot runs locally and contains no network code. Organization uses filesystem moves rather than deleting source files. Existing destination files are never overwritten. Hidden files remain untouched unless `--include-hidden` is explicitly supplied. During undo, an occupied original path causes the operation to stop instead of overwriting the new file.

These safeguards reduce risk, but irreplaceable data should still be backed up before filesystem automation.

## Architecture

```text
src/filepilot/
├── core.py        # planning, classification, moves, rollback, hashing
├── cli.py         # command-line interface
└── __init__.py

tests/
└── test_core.py   # behavior tests

.github/workflows/
└── ci.yml         # Python 3.10/3.12/3.13 × Linux/Windows/macOS
```

## Quality

The test suite covers case-insensitive classification, collision-safe naming, apply/undo round trips, recursive safety, hidden-file behavior, and SHA-256 hashing.

```bash
python -m pip install -e . pytest
pytest -q
```

CI runs the suite across Ubuntu, Windows, and macOS on Python 3.10, 3.12, and 3.13.

## Current boundaries

- Classification is extension-based; MIME signatures are not inspected.
- Undo restores moved files but intentionally leaves empty category directories.
- Recursive organization requires a destination outside the source directory to prevent repeated processing.

---

## العربية

### ما هو FilePilot؟

**FilePilot** أداة سطر أوامر بلغة بايثون لتنظيم الملفات محليًا بطريقة قابلة للتراجع. الفكرة الأساسية ليست «النقل بسرعة»، بل **المعاينة أولًا ثم التنفيذ بأمان**: ترى الخطة قبل أي تغيير، ولا يُستبدل ملف موجود، وتُسجّل النقلات الناجحة لتتمكن من إرجاعها.

### أهم المزايا

- **معاينة بلا تغيير** عبر `filepilot plan`.
- تصنيف الصور والفيديو والصوت والمستندات والجداول والعروض والأرشيفات وملفات البرمجة وغيرها.
- إنشاء اسم فريد تلقائيًا عند تعارض الأسماء بدل الاستبدال.
- إنشاء Manifest لعمليات النقل الناجحة لإتاحة التراجع.
- محاولة إرجاع النقلات السابقة إذا فشل التنفيذ في منتصف العملية.
- تجاهل الملفات المخفية افتراضيًا.
- دعم الفحص المتكرر للمجلدات الفرعية مع اشتراط وجهة منفصلة للأمان.
- حساب SHA-256 للتحقق من سلامة الملفات.
- لا توجد مكتبات مطلوبة وقت التشغيل؛ يعتمد البرنامج على مكتبة بايثون القياسية.

### الاستخدام السريع

```bash
filepilot plan ~/Downloads
filepilot organize ~/Downloads --manifest ~/filepilot-run.json
filepilot undo ~/filepilot-run.json
```

### الخصوصية والأمان

تعمل الأداة محليًا ولا تحتوي على كود شبكي. لا تستبدل ملفًا موجودًا في الوجهة، وتتجاهل الملفات المخفية افتراضيًا. وإذا أصبح المسار الأصلي مشغولًا أثناء التراجع، تتوقف بدل استبدال الملف الجديد. تبقى النسخ الاحتياطية موصى بها للبيانات التي لا يمكن تعويضها.

### الحدود الحالية

- التصنيف يعتمد على امتداد الملف، وليس فحص المحتوى الداخلي.
- التراجع يعيد الملفات لكنه لا يحذف مجلدات التصنيف الفارغة.
- الفحص المتكرر للمجلدات الفرعية يتطلب وجهة منفصلة لتجنب إعادة معالجة الملفات.

## Project identity

<p align="center">
  <img src="assets/filepilot-logo-square.svg" alt="FilePilot logo" width="150">
</p>

The visual system is documented in [docs/BRAND.md](docs/BRAND.md). The folder/checkmark mark represents **organized files + a verified reversible action**.

## Contributing & security

- Contribution guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security policy: [SECURITY.md](SECURITY.md)
- License: [MIT](LICENSE)

## Author / المطور

**رضوان عبدالهادي أحمد — Radwan Abdulhadi Ahmed**  
GitHub: **@rad03i2**

<p align="center"><sub>Preview. Organize. Undo. — built with a reversible-by-design philosophy.</sub></p>

<!-- radwan-repo-polisher:v1 -->
