"""Named, draft-only agents for the TRADER X command room."""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
PROMPTS = ROOT / "prompts"

AGENT_ALIASES = {
    "codex": "codex",
    "کدکس": "codex",
    "studio": "studio",
    "استودیو": "studio",
    "mentor": "mentor",
    "منتور": "mentor",
    "news": "news",
    "اخبار": "news",
}


def call_gemini(instruction: str, payload: str) -> str:
    """Request a response without ever placing credentials in files or output."""
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise SystemExit("GEMINI_API_KEY secret is not configured.")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    request = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps(
            {"contents": [{"parts": [{"text": f"{instruction}\n\n{payload}"}]}]},
            ensure_ascii=False,
        ).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = json.load(response)
        return body["candidates"][0]["content"]["parts"][0]["text"].strip()
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Gemini HTTP {exc.code}: {exc.read().decode(errors='replace')[:1500]}") from exc
    except (urllib.error.URLError, KeyError, IndexError, TypeError) as exc:
        raise SystemExit(f"Gemini request failed: {exc}") from exc


def write_draft(filename: str, content: str) -> Path:
    OUTPUT.mkdir(exist_ok=True)
    target = OUTPUT / filename
    target.write_text(content.rstrip() + "\n", encoding="utf-8")
    return target


def run_codex(task: str) -> Path:
    return write_draft("codex_response.md", call_gemini(PROMPTS.joinpath("codex_agent.md").read_text(encoding="utf-8"), f"درخواست کاربر:\n{task}"))


def run_studio(prompt: str, screenshot: Path | None) -> Path:
    screenshot_context = "اسکرین‌شات ارائه نشده است؛ آن را اختراع نکن."
    if screenshot:
        if not screenshot.is_file():
            raise SystemExit(f"Screenshot not found: {screenshot}")
        screenshot_context = f"مسیر اسکرین‌شات MT5: {screenshot}. فقط بر اساس توصیف کاربر و همین فایل کار کن."
    response = call_gemini(
        PROMPTS.joinpath("studio_agent.md").read_text(encoding="utf-8"),
        f"{screenshot_context}\n\nپرامپت کاربر:\n{prompt}",
    )
    return write_draft("studio_video_brief.md", response)


def run_mentor(content_path: Path) -> Path:
    if not content_path.is_file():
        raise SystemExit(f"Content package not found: {content_path}")
    response = call_gemini(
        PROMPTS.joinpath("mentor_agent.md").read_text(encoding="utf-8"),
        f"بسته محتوای در حال بررسی (پیش‌نویس):\n{content_path.read_text(encoding='utf-8')}",
    )
    return write_draft("mentor_review.md", response)


def fetch_calendar(url: str) -> list[dict[str, Any]]:
    request = urllib.request.Request(url, headers={"User-Agent": "TRADER-X-News/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Could not fetch the Forex Factory calendar: {exc}") from exc
    if not isinstance(data, list):
        raise SystemExit("Forex Factory calendar returned an unexpected response.")
    return [item for item in data if isinstance(item, dict)]


def run_news(url: str) -> Path:
    events = fetch_calendar(url)
    now = datetime.now(UTC)
    # The source feed uses ISO dates. Keep only upcoming, high-impact events if
    # available; never turn calendar entries into a trading recommendation.
    high = [e for e in events if str(e.get("impact", "")).lower() == "high"]
    selected = high[:12] or events[:12]
    lines = [
        "# گزارش اخبار فارکس — پیش‌نویس",
        "",
        f"زمان دریافت (UTC): {now.isoformat(timespec='seconds')}",
        "منبع تقویم: Forex Factory. زمان‌ها و ارقام را پیش از تصمیم مالی دوباره بررسی کنید.",
        "",
        "## تیترهای مهم",
    ]
    for event in selected:
        title = re.sub(r"\s+", " ", str(event.get("title", "بدون عنوان"))).strip()
        date = str(event.get("date", "زمان نامشخص"))
        country = str(event.get("country", ""))
        impact = str(event.get("impact", ""))
        lines.append(f"- **{country} | {date}** — {title} ({impact})")
    lines.extend(["", "## یادآوری ریسک", "این فهرست خبر است، نه سیگنال یا توصیه معامله. در زمان خبر از اندازه پوزیشن و نقدشوندگی مطمئن شوید."])
    return write_draft("forex_news.md", "\n".join(lines))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="TRADER X named agents")
    parser.add_argument("agent", help="codex/کدکس، studio/استودیو، mentor/منتور، news/اخبار")
    parser.add_argument("prompt", nargs="?", default="", help="task or creative brief")
    parser.add_argument("--screenshot", type=Path, help="local MT5 screenshot for studio")
    parser.add_argument("--content", type=Path, default=OUTPUT / "publish.json", help="draft content for mentor")
    parser.add_argument("--calendar-url", default="https://nfs.faireconomy.media/ff_calendar_thisweek.json", help="Forex Factory calendar JSON endpoint")
    args = parser.parse_args(argv)
    agent = AGENT_ALIASES.get(args.agent.casefold())
    if not agent:
        parser.error("Unknown agent. Use codex/کدکس, studio/استودیو, mentor/منتور, or news/اخبار.")
    if agent == "codex":
        if not args.prompt:
            parser.error("codex needs a task prompt.")
        target = run_codex(args.prompt)
    elif agent == "studio":
        if not args.prompt:
            parser.error("studio needs a video/content prompt.")
        target = run_studio(args.prompt, args.screenshot)
    elif agent == "mentor":
        target = run_mentor(args.content)
    else:
        target = run_news(args.calendar_url)
    print(f"Draft created: {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
