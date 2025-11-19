#!/usr/bin/env python3
"""
Test WIX API authentication and permissions
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

WIX_API_KEY = os.getenv("WIX_API_KEY")
WIX_SITE_ID = os.getenv("WIX_SITE_ID")

print("=" * 60)
print("Testing WIX API Authentication")
print("=" * 60)
print(f"\nAPI Key: {WIX_API_KEY[:20]}...")
print(f"Site ID: {WIX_SITE_ID}")
print()

# Test 1: List collections
print("Test 1: List Data Collections")
print("-" * 60)

url = "https://www.wixapis.com/wix-data/v2/collections"
headers = {
    "Authorization": WIX_API_KEY,
    "wix-site-id": WIX_SITE_ID,
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    collections = response.json().get("collections", [])
    print(f"✓ Found {len(collections)} collections:")
    for col in collections[:10]:  # Show first 10
        print(f"  - {col.get('id')} ({col.get('displayName', 'N/A')})")
else:
    print(f"✗ Error: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text[:500])

print()

# Test 2: Try Media Manager list endpoint
print("Test 2: List Media Manager Files")
print("-" * 60)

url2 = "https://www.wixapis.com/site-media/v1/files"
response2 = requests.get(url2, headers=headers)
print(f"Status: {response2.status_code}")

if response2.status_code == 200:
    print("✓ Media Manager API accessible")
    try:
        print(json.dumps(response2.json(), indent=2)[:500])
    except:
        pass
else:
    print(f"✗ Error: {response2.status_code}")
    try:
        print(json.dumps(response2.json(), indent=2))
    except:
        print(response2.text[:500])
