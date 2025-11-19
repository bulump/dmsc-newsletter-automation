#!/usr/bin/env python3
"""
Check WIX CMS entry to see what format fields need
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

WIX_API_KEY = os.getenv("WIX_API_KEY")
WIX_SITE_ID = os.getenv("WIX_SITE_ID")

# Get the CMS entry we just created
url = "https://www.wixapis.com/wix-data/v2/items/query"

headers = {
    "Authorization": WIX_API_KEY,
    "wix-site-id": WIX_SITE_ID,
    "Content-Type": "application/json"
}

data = {
    "dataCollectionId": "Newsletters",
    "query": {
        "filter": {
            "title": "November 2025"
        }
    }
}

response = requests.post(url, headers=headers, json=data)

print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))
