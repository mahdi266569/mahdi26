# TRADER X — AI Trading & Content Command Room

نسخه پایه و قابل توسعه‌ی سیستم TRADER X برای تحلیل، داده، پژوهش، کنترل ریسک، تولید محتوا و در ادامه اتصال به MT5 و انتشار چندکاناله.

## ایجنت‌های قابل صدا زدن

هر ایجنت با نام خودش از خط فرمان فراخوانی می‌شود. نام‌های فارسی هم پشتیبانی می‌شوند؛ در یک رابط صوتی، همین نام‌ها باید به همین فرمان‌ها نگاشت شوند.

| نام صدا زدن | کار | فرمان |
| --- | --- | --- |
| `کدکس` / `codex` | برنامه‌نویسی، کارهای کامپیوتری و پژوهش | `python -m src.main کدکس "یک API امن برای ... طراحی کن"` |
| `استودیو` / `studio` | تبدیل اسکرین‌شات MT5 و ایده به بریف ویدیو و متن شبکه‌ها | `python -m src.main استودیو "ویدیوی آموزشی درباره مدیریت ریسک بساز" --screenshot /path/chart.png` |
| `منتور` / `mentor` | بازبینی آموزشی/ریسکی محتوا و چک‌لیست انتشار | `python -m src.main منتور --content output/publish.json` |
| `اخبار` / `news` | تیترهای تقویم اقتصادی فارکس | `python -m src.main اخبار` |

خروجی همه ایجنت‌ها در `output/` با وضعیت پیش‌نویس ساخته می‌شود. استودیو فقط بریف قابل ارسال به ابزار ویدیوساز می‌سازد؛ گرفتن خودکار تصویر از MetaTrader، ساخت نهایی ویدیو و انتشار در شبکه‌های اجتماعی عمداً بدون اتصال، مجوز و تأیید انسانی انجام نمی‌شود.

## وضعیت فعلی

### فعال
- GitHub Actions
- Secure Gemini API integration
- Structured JSON output
- Content package generation
- Schema validation
- Draft-only publishing state
- Modular agent architecture
- CI loop protection

### در نقشه راه
- Deep Research / source tracking
- Market data pipeline
- Risk Gate
- MT5 integration
- Automated video generation
- Telegram / YouTube / Instagram publishing
- Analytics and learning loop
- Trading Journal

### اخبار فارکس

فرمان `اخبار` تقویم JSON فعلی Forex Factory را دریافت و رویدادهای با اهمیت بالا را در `output/forex_news.md` ثبت می‌کند. این یک فهرست خبر است، نه سیگنال؛ پیش از هر تصمیم مالی زمان و ارقام را از منبع اصلی دوباره بررسی کنید. در صورت نیاز به پراکسی یا منبع جایگزین، می‌توان آدرس خوراک را صریحاً تنظیم کرد:

```bash
python -m src.main news --calendar-url https://example.invalid/calendar.json
```

## استفاده

1. فایل `input/idea.md` را تکمیل کنید.
2. از GitHub → Actions، workflow `TRADER X Content Engine` را اجرا کنید.
3. خروجی اصلی در `output/publish.json` و `output/content.md` ساخته می‌شود.

## Secret

در GitHub Repository Secrets یک secret با نام دقیق زیر بسازید:

`GEMINI_API_KEY`

هرگز API Key را داخل Repository، Prompt، README، Commit، Issue یا Log قرار ندهید.

مدل اختیاری از طریق Repository Variable با نام `GEMINI_MODEL` قابل تنظیم است؛ در صورت خالی‌بودن مقدار پیش‌فرض پروژه استفاده می‌شود.

## معماری

```text
Input
  ↓
Research / Data
  ↓
Trading Analysis
  ↓
Risk Gate
  ↓
Content Engine
  ↓
Draft Package
  ↓
Human Approval
  ↓
Publish
  ↓
Analytics
  ↓
Learning Loop
```

## ساختار

```text
input/       raw user ideas
prompts/     agent instructions
schemas/     machine-readable contracts
src/         execution code
output/      generated draft artifacts
config/      architecture and guardrails
.github/     automation
```

## ایمنی معاملاتی

سیستم برای جبران ضرر، revenge trading، over-sizing یا سیگنال تضمینی طراحی نشده است. خروجی معامله‌ای باید شامل سناریو، شرط فعال‌شدن، invalidation و ریسک قابل اندازه‌گیری باشد.
