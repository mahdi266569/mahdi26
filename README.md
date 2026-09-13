# TRADER X Content Agent

نسخهٔ اول ایجنت تولید محتوای TRADER X.

## جریان فعلی

1. ایده را در `input/idea.md` می‌نویسید.
2. GitHub Actions اجرا می‌شود.
3. Gemini ایده را به بستهٔ محتوایی تبدیل می‌کند.
4. خروجی در `output/content.md` ذخیره می‌شود.

## تنظیم API

کلید Gemini را با نام `GEMINI_API_KEY` در GitHub Secrets قرار دهید.
هرگز کلید API را داخل فایل‌ها یا کد Commit نکنید.

## اجرا

از تب **Actions**، workflow با نام **TRADER X Content Agent** را دستی اجرا کنید.
