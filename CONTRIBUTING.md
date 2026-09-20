# Contributing / المساهمة

Thank you for improving FilePilot. Keep changes focused, local-first, and safe for user data.

1. Create a branch from `main`.
2. Install with `python -m pip install -e . pytest`.
3. Add or update tests for behavior changes.
4. Run `pytest -q` before opening a pull request.
5. Keep filesystem-destructive behavior explicit and opt-in; never silently overwrite user files.
6. Update both English and Arabic README sections when user-facing behavior changes.

## العربية
نرحب بالمساهمات التي تحافظ على بساطة FilePilot وأمان بيانات المستخدم. أضف اختبارات لأي تغيير سلوكي، وشغّل `pytest -q`، ولا تضف سلوكًا يستبدل ملفات المستخدم أو يحذفها بصمت. حدّث التوثيق الإنجليزي والعربي عند تغيير سلوك ظاهر للمستخدم.

Maintainer: **Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد (@rad03i2)**
