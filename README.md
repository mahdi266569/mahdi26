# TRADER X — AI Trading & Content Command Room

نسخه پایه و قابل توسعه‌ی سیستم TRADER X برای تحلیل، داده، پژوهش، کنترل ریسک، تولید محتوا و در ادامه اتصال به MT5 و انتشار چندکاناله.

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
