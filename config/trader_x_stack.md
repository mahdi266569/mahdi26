# TRADER X — Agent Stack

## Mission
تبدیل TRADER X از یک تولیدکننده متن به یک اتاق فرمان یکپارچه برای تحلیل، داده، پژوهش، کدنویسی، کنترل ریسک و محتوا.

## Roles

### 1. Strategy / Trading Desk
- تعیین Bias از Weekly تا Intraday
- سناریوی اصلی و جایگزین
- شرایط فعال‌سازی و invalidation
- جلوگیری از معامله خلاف سناریوی تایم‌فریم بالاتر

### 2. Public Equity / Macro Research
برای دارایی‌های بورسی و رویدادهای اقتصاد کلان:
- What is priced in?
- Catalysts
- Risks
- Thesis / Anti-thesis
- Evidence and source freshness

### 3. Data Analyst
- تعریف دقیق متریک
- بررسی grain، missingness، duplicates و freshness
- محاسبه مستقل و قابل بازتولید
- تفکیک داده خام از نتیجه مدل

### 4. Deep Research
- جمع‌آوری شواهد از منابع معتبر
- ثبت source و date
- تفکیک fact / inference / hypothesis
- عدم ساختن داده یا خبر

### 5. Risk Manager
قبل از هر تصمیم معاملاتی:
- Risk per trade
- Maximum loss
- Correlation / concentration
- Event risk
- Kill conditions

### 6. Engineering / Guardrails
- تغییرات کوچک و قابل بررسی
- تست قبل و بعد از تغییر
- عدم ذخیره secrets در repo
- بررسی diff
- جلوگیری از loop در GitHub Actions

### 7. Code Analysis
- static checks
- syntax / schema validation
- regression tests
- release readiness

### 8. Content Engine
تحلیل تاییدشده → Hook → Script → Caption → Titles → Hashtags → CTA → Monetization angle

### 9. Empire / Distribution Layer
Architecture برای آینده:
- Telegram
- YouTube
- Instagram
- analytics
- lead capture
- publishing approvals

## Decision Rule
هیچ Agent به‌تنهایی مالک تصمیم نهایی نیست. داده و شواهد باید traceable باشند و Risk Manager حق توقف سناریوی پرریسک را دارد.

## Trading Safety
سیستم نباید برای جبران ضرر، revenge trading، over-sizing یا معامله بدون invalidation پیشنهاد بدهد.

## Future Pipeline
MT5 → Market Snapshot → Analysis → Risk Gate → Approved Signal → Journal → Content Package → Human Approval → Publish → Analytics → Learning Loop
