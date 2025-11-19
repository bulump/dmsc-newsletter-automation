#!/usr/bin/env python3
"""
Check existing WIX CMS newsletter entry to see correct format
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

WIX_API_KEY = os.getenv("WIX_API_KEY")
WIX_SITE_ID = os.getenv("WIX_SITE_ID")

# Get all newsletter entries to see the format
url = "https://www.wixapis.com/wix-data/v2/items/query"

headers = {
    "Authorization": WIX_API_KEY,
    "wix-site-id": WIX_SITE_ID,
    "Content-Type": "application/json"
}

data = {
    "dataCollectionId": "Newsletters",
    "query": {
        "sort": [{"fieldName": "_createdDate", "order": "DESC"}],
        "paging": {"limit": 5}
    }
}

response = requests.post(url, headers=headers, json=data)

print(f"Status: {response.status_code}\n")

if response.status_code == 200:
    items = response.json().get("dataItems", [])
    print(f"Found {len(items)} newsletter entries:\n")

    for i, item in enumerate(items, 1):
        data = item.get("data", {})
        print(f"{i}. Title: {data.get('title')}")
        print(f"   Publish Month: {data.get('publishMonth')}")
        print(f"   Newsletter: {data.get('newsletter')}")
        print(f"   Summary: {data.get('newsletterSummary', 'N/A')[:50]}...")
        print()
else:
    print(json.dumps(response.json(), indent=2))
