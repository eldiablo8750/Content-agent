"""
send_telegram_report.py
------------------------
Reads dashboard/data.json (the same data your dashboard uses) and sends
a daily summary report to your Telegram bot.

Run this from the content-agent/ folder with:
    python scripts/send_telegram_report.py

Requires:
    pip install python-dotenv requests
"""

import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise SystemExit(
        "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env"
    )

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "dashboard", "data.json")


def avg(values):
    return sum(values) / len(values) if values else 0


def build_report(data: dict) -> str:
    self_acc = next(a for a in data["accounts"] if a["is_self"])
    comp_accs = [a for a in data["accounts"] if not a["is_self"]]

    self_likes = avg([p.get("likesCount", 0) or 0 for p in self_acc["posts"]])
    self_comments = avg([p.get("commentsCount", 0) or 0 for p in self_acc["posts"]])

    top_post = max(
        self_acc["posts"],
        key=lambda p: p.get("likesCount", 0) or 0,
        default=None,
    )

    lines = [
        "📊 *ZuniMove Daily Content Report*",
        "",
        f"Data pulled: {data.get('pulled_at', 'unknown')[:10]}",
        "",
        f"Your posts tracked: *{self_acc['post_count']}*",
        f"Avg likes/post: *{self_likes:.1f}*",
        f"Avg comments/post: *{self_comments:.1f}*",
        "",
        "Competitor benchmark (avg likes):",
    ]

    for acc in comp_accs:
        c_likes = avg([p.get("likesCount", 0) or 0 for p in acc["posts"]])
        lines.append(f"  • @{acc['handle']}: {c_likes:.1f} ({acc['post_count']} posts)")

    if top_post:
        caption = (top_post.get("caption") or "").split("\n")[0][:80]
        lines += [
            "",
            f"🏆 Your top post: \"{caption}\"",
            f"   {top_post.get('likesCount', 0)} likes · {top_post.get('commentsCount', 0)} comments",
        ]

    return "\n".join(lines)


def send_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    })
    resp.raise_for_status()
    return resp.json()


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    report = build_report(data)
    result = send_message(report)

    if result.get("ok"):
        print("✅ Report sent to Telegram successfully.")
    else:
        print("❌ Something went wrong:", result)


if __name__ == "__main__":
    main()
