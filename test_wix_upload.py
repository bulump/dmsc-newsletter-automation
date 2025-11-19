#!/usr/bin/env python3
"""
Test script for WIX Media Manager API file upload
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

WIX_API_KEY = os.getenv("WIX_API_KEY")
WIX_SITE_ID = os.getenv("WIX_SITE_ID")

if not WIX_API_KEY:
    print("Error: WIX_API_KEY not found in .env file")
    exit(1)

if not WIX_SITE_ID:
    print("Error: WIX_SITE_ID not found in .env file")
    exit(1)

# WIX API endpoint
BASE_URL = "https://www.wixapis.com"

def test_import_file_from_url(file_url):
    """Test importing a file from URL using WIX Import File API"""

    print("Testing WIX API - Import File from URL")
    print("=" * 60)

    # WIX Import File endpoint
    endpoint = f"{BASE_URL}/site-media/v1/files/import"

    headers = {
        "Authorization": WIX_API_KEY,
        "wix-site-id": WIX_SITE_ID,
        "Content-Type": "application/json"
    }

    # Request body for importing file
    data = {
        "url": file_url,
        "mimeType": "application/pdf",
        "displayName": "DMSC_Newsletter.pdf"
    }

    print(f"\nCalling: POST {endpoint}")
    print(f"Headers: {json.dumps({k: v[:50] + '...' if len(v) > 50 else v for k, v in headers.items()}, indent=2)}")
    print(f"Body: {json.dumps(data, indent=2)}")
    print()

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"\nResponse Body:")

        # Try to parse as JSON, fall back to text if that fails
        try:
            response_data = response.json()
            print(json.dumps(response_data, indent=2))
        except:
            print(f"(Not JSON) {response.text}")
            response_data = None

        if response.status_code == 200:
            print("\n✓ Successfully generated upload URL!")
            return response_data
        else:
            print(f"\n✗ Error: {response.status_code}")
            return None

    except Exception as e:
        print(f"\n✗ Exception occurred: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    import sys

    # For testing, use a test Dropbox URL or ask for one
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
    else:
        print("\nUsage: python3 test_wix_upload.py <dropbox-share-link>")
        print("Example: python3 test_wix_upload.py https://www.dropbox.com/s/abc123/newsletter.pdf")
        print("\nOr just test with a sample URL for now...")
        test_url = input("Enter Dropbox share link (or press Enter to skip): ").strip()

        if not test_url:
            print("\nSkipping test - no URL provided")
            exit(0)

    result = test_import_file_from_url(test_url)

    if result:
        print("\n" + "=" * 60)
        print("Success! File imported to WIX Media Manager")
        print("Next steps:")
        print("1. Get the file URL from WIX to use in MailChimp")
        print("2. Use the fileId to retrieve file details")
        print("=" * 60)
