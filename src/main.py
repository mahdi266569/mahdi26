from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "input" / "idea.md"
PROMPT = ROOT / "prompts" / "content_agent.md"
SCHEMA = ROOT / "schemas" / "publish.schema.json"
OUTPUT = ROOT / "output"


def extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("No JSON object found in model output")
    return json.loads(text[start : end + 1])


def main() -> None:
    # Keep the original no-argument content command intact, while allowing the
    # named command-room agents to be invoked from the same entry point.
    if len(sys.argv) > 1:
        from src.agent_cli import main as agent_main

        agent_main(sys.argv[1:])
        return

    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise SystemExit("GEMINI_API_KEY secret is not configured.")

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    prompt = PROMPT.read_text(encoding="utf-8")
    idea = INPUT.read_text(encoding="utf-8")
    schema = SCHEMA.read_text(encoding="utf-8")
    full_prompt = f"{prompt}\n\nJSON Schema:\n{schema}\n\nایده خام:\n{idea}"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {"temperature": 0.7, "responseMimeType": "application/json"},
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Gemini HTTP {exc.code}: {detail[:1500]}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Gemini connection error: {exc.reason}") from exc

    try:
        model_text = body["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as exc:
        raise SystemExit("Gemini returned an unexpected response shape.") from exc

    data = extract_json(model_text)
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "publish.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUTPUT / "content.md").write_text(
        "# TRADER X Content Package\n\n"
        f"## Hook\n{data['hook']}\n\n"
        f"## YouTube Titles\n" + "\n".join(f"- {x}" for x in data["youtube_titles"])
        + f"\n\n## Short Script\n{data['short_script']}\n\n"
        f"## Long Script\n{data['long_script']}\n\n"
        f"## Instagram Caption\n{data['instagram_caption']}\n\n"
        f"## Hashtags\n{' '.join(data['hashtags'])}\n\n"
        f"## CTA\n{data['cta']}\n\n"
        f"## Monetization Angle\n{data['monetization_angle']}\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
