# XAUUSD Paper Assistant

پروژه‌ای مستقل و فقط برای تحقیق و شبیه‌سازی است. این برنامه هیچ اتصال MT5، API کارگزاری، LLM یا مسیر اجرای واقعی ندارد. خروجی آن صرفاً `PAPER` است و نباید مبنای معامله با پول واقعی باشد.

## قابلیت‌های نسخه ۰.۱

- خواندن OHLCV از CSV با زمان‌های `event_time_utc` و `available_at_utc`
- کنترل Point-in-Time و کیفیت داده
- setup قطعی و کوچک: swing-confirmed BOS به همراه FVG سه‌-کندلی
- موتور ریسک قطعی: R:R، حجم گام‌دار، سقف افت روزانه و حداکثر یک پوزیشن
- Paper fill با spread، commission و slippage محافظه‌کارانه
- لاگ JSONL قابل حسابرسی با `config_hash` و `strategy_version`
- تست‌های بدون وابستگی خارجی

## اتصال به استاد تریدر

خروجی Paper فقط شواهد پژوهشی است. برای فرستادن خلاصه به «استاد تریدر»، از قرارداد `schemas/paper_research_report.schema.json` و دستورالعمل `prompts/paper_research_agent.md` استفاده کنید. این اتصال یک‌طرفه است: Paper → Report → Mentor/Content. استاد تریدر و LLM اجازه ندارند تصمیم ریسک، حجم یا اجرای Paper را تغییر دهند.

## اجرا

نیازی به نصب پکیج خارجی نیست (Python 3.11+):

```bash
python -m xauusd_paper_assistant.src.cli backtest \
  --data xauusd_paper_assistant/data/sample_xauusd_m5.csv \
  --config xauusd_paper_assistant/config/paper.json \
  --audit-dir /tmp/xauusd-audit
```

خروجی شامل `events.jsonl` و `summary.json` در پوشه‌ی audit است. داده‌ی نمونه ساختگی است و فقط برای صحت مسیر اجراست، نه سنجش عملکرد.

## دریافت خودکار داده از MT5 (فقط خواندن)

این دستور فقط کندل‌های **بسته‌شده** را از MetaTrader 5 نصب‌شده روی همان کامپیوتر می‌خواند و به CSV تبدیل می‌کند. این دستور هیچ login، credential، سفارش، `order_send` یا حالت live ندارد. باید MT5 باز باشد، به یک حساب/سرور داده‌ای که خودتان وارد شده‌اید متصل باشد، نماد در Market Watch دیده شود، و پکیج `MetaTrader5` برای همان Python نصب شده باشد.

```bash
python -m xauusd_paper_assistant.src.cli fetch-mt5 \
  --symbol XAUUSD \
  --timeframe M5 \
  --bars 500 \
  --output xauusd_paper_assistant/data/xauusd_m5.csv
```

سپس همان CSV را با فرمان `backtest` اجرا کنید. زمان هر bar به زمان بسته‌شدن آن تبدیل می‌شود و bar در حال شکل‌گیری عمداً خوانده نمی‌شود تا داده‌ی آینده وارد آزمون نشود.

## قرارداد داده

ستون‌های اجباری CSV:

```text
event_time_utc,available_at_utc,open,high,low,close,spread_points,tick_volume,symbol,source
```

هر ردیف فقط زمانی وارد تصمیم می‌شود که `available_at_utc <= event_time_utc` باشد. سیستم داده‌ی ناقص، حجم صفر و spread غیرعادی را رد و در audit ثبت می‌کند.

## مرزهای ایمنی

- تنها حالت اجرا `PAPER` است؛ هیچ `LIVE_TRADING`، `order_send` یا credential وجود ندارد.
- LLM بخشی از مسیر تحلیل، ریسک یا fill نیست.
- XAUUSD spot فاقد order flow متمرکز است؛ بنابراین Footprint/Delta/CVD در این نسخه عمداً پیاده‌سازی نشده‌اند.
- از داده‌ی GC futures فقط در صورت داشتن bid/ask معتبر و policy آزموده‌شده برای basis استفاده کنید؛ tick volume بروکر جایگزین Footprint نیست.
- پیش از هر توسعه‌ای فراتر از شبیه‌سازی: داده‌ی خارج از نمونه، Walk-Forward، Monte Carlo و حداقل ۱۰۰ معامله‌ی Paper لازم است.
