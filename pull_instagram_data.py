"""
pull_instagram_data.py
-----------------------
Pulls Instagram post data for your account + your competitors using
Apify's instagram-scraper actor, and saves everything into
dashboard/data.json.

Run this from the content-agent/ folder with:
    python scripts/pull_instagram_data.py

Requires:
    pip install apify-client python-dotenv
"""

import json
import os
from datetime import datetime, timezone

from apify_client import ApifyClient
from dotenv import load_dotenv

# ---- CONFIG ----------------------------------------------------------

# Load your Apify token from .env (never hardcode it here)
load_dotenv()
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

if not APIFY_API_TOKEN:
    raise SystemExit(
        "No APIFY_API_TOKEN found. Make sure your .env file has "
        "APIFY_API_TOKEN=your_token_here"
    )

# Your account + competitors (edit this list any time you add/drop a competitor)
YOUR_HANDLE = "zunimoveconveyorsystem"
COMPETITOR_HANDLES = [
    "panther_conveyor_belt",
    "lbsconveyorbeltsemmen",
    "farookconveyors",
]

# How many recent posts to pull per account (keep this modest at first —
# you can raise it once we confirm everything works)
POSTS_PER_ACCOUNT = 30

# Where the output goes
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "dashboard", "data.json")


# ---- SCRAPE ------------------------------------------------------------

def scrape_account(client: ApifyClient, handle: str, is_self: bool) -> dict:
    """Run the instagram-scraper actor for one account and return its posts."""
    print(f"Scraping @{handle} ...")

    run_input = {
        "directUrls": [f"https://www.instagram.com/{handle}/"],
        "resultsType": "posts",
        "resultsLimit": POSTS_PER_ACCOUNT,
        "searchType": "user",
    }

    # "apify/instagram-scraper" is the actor's public ID on the Apify store
    run = client.actor("apify/instagram-scraper").call(run_input=run_input)

    posts = []
    for item in client.dataset(run.default_dataset_id).iterate_items():
        posts.append({
            "id": item.get("id"),
            "shortCode": item.get("shortCode"),
            "caption": item.get("caption"),
            "url": item.get("url"),
            "timestamp": item.get("timestamp"),
            "likesCount": item.get("likesCount"),
            "commentsCount": item.get("commentsCount"),
            "videoViewCount": item.get("videoViewCount"),
            "type": item.get("type"),  # Image, Video, Sidecar
            "hashtags": item.get("hashtags", []),
        })

    return {
        "handle": handle,
        "is_self": is_self,
        "post_count": len(posts),
        "posts": posts,
    }


def main():
    client = ApifyClient(APIFY_API_TOKEN)

    accounts = [scrape_account(client, YOUR_HANDLE, is_self=True)]
    for handle in COMPETITOR_HANDLES:
        accounts.append(scrape_account(client, handle, is_self=False))

    output = {
        "pulled_at": datetime.now(timezone.utc).isoformat(),
        "your_handle": YOUR_HANDLE,
        "competitor_handles": COMPETITOR_HANDLES,
        "accounts": accounts,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    total_posts = sum(a["post_count"] for a in accounts)
    print(f"\nDone. Saved {total_posts} posts across {len(accounts)} accounts to:")
    print(f"  {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
