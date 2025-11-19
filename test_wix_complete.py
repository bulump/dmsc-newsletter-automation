#!/usr/bin/env python3
"""
Test complete WIX workflow: Import file + Create CMS entry
"""

import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

WIX_API_KEY = os.getenv("WIX_API_KEY")
WIX_SITE_ID = os.getenv("WIX_SITE_ID")


def import_file_to_wix(file_url, display_name):
    """Import file to WIX Media Manager from URL"""
    print(f"\n1. Importing file to WIX Media Manager...")
    print(f"   File: {display_name}")
    print(f"   URL: {file_url[:80]}...")

    endpoint = "https://www.wixapis.com/site-media/v1/files/import"

    headers = {
        "Authorization": WIX_API_KEY,
        "wix-site-id": WIX_SITE_ID,
        "Content-Type": "application/json"
    }

    data = {
        "url": file_url,
        "mimeType": "application/pdf",
        "displayName": display_name
    }

    response = requests.post(endpoint, headers=headers, json=data)

    print(f"   Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        file_info = result.get("file", {})
        file_id = file_info.get("id")
        file_url_wix = file_info.get("url")

        # Convert GUID subdomain to public domain
        file_url_wix = file_url_wix.replace(f"https://{WIX_SITE_ID}.usrfiles.com/ugd/", "https://www.dmlsclub.com/_files/ugd/")

        # Create WIX document reference for CMS
        wix_doc_ref = f"wix:document://v1/ugd/{file_id}/{display_name}"

        print(f"   ✓ File imported successfully!")
        print(f"   File ID: {file_id}")
        print(f"   WIX URL: {file_url_wix}")

        return {
            "fileId": file_id,
            "wixDocRef": wix_doc_ref,
            "url": file_url_wix,
            "displayName": display_name
        }
    else:
        print(f"   ✗ Error: {response.status_code}")
        try:
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"   Response: {response.text[:500]}")
        return None


def create_cms_entry(title, wix_doc_ref, publish_date, summary):
    """Create entry in Newsletters CMS collection"""
    print(f"\n2. Creating CMS entry in 'Newsletters' collection...")
    print(f"   Title: {title}")
    print(f"   Summary: {summary}")

    endpoint = "https://www.wixapis.com/wix-data/v2/items"

    headers = {
        "Authorization": WIX_API_KEY,
        "wix-site-id": WIX_SITE_ID,
        "Content-Type": "application/json"
    }

    # Format publish date as "Nov 18, 2025"
    if publish_date:
        date_obj = datetime.fromisoformat(publish_date.replace('Z', '+00:00')) if isinstance(publish_date, str) else publish_date
        formatted_date = date_obj.strftime("%b %d, %Y")
    else:
        formatted_date = None

    data = {
        "dataCollectionId": "Newsletters",
        "dataItem": {
            "data": {
                "title": title,
                "newsletter": wix_doc_ref,  # WIX document reference
                "newsletterSummary": summary
            }
        }
    }

    # Only add publishMonth if we have a date
    if formatted_date:
        data["dataItem"]["data"]["publishMonth"] = formatted_date

    response = requests.post(endpoint, headers=headers, json=data)

    print(f"   Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        item_id = result.get("dataItem", {}).get("id")

        print(f"   ✓ CMS entry created successfully!")
        print(f"   Item ID: {item_id}")
        if formatted_date:
            print(f"   Publish Date: {formatted_date}")

        return result
    else:
        print(f"   ✗ Error: {response.status_code}")
        try:
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"   Response: {response.text[:500]}")
        return None


if __name__ == "__main__":
    import sys

    print("=" * 60)
    print("Testing Complete WIX Integration")
    print("=" * 60)

    # Test with the Dropbox link we already generated
    test_url = "https://dl.dropboxusercontent.com/scl/fi/k45i7w7jae5rim6vt3jmj/DMSC_2025_Nov_Web.pdf?rlkey=8a2lm4u80p265aw307qhex18r&dl=1"
    test_title = "November 2025"
    test_summary = "Monthly Meeting Thursday November 20 at 7 PM"
    test_date = None  # Leave empty - filled manually in WIX UI

    # Step 1: Import file
    file_result = import_file_to_wix(test_url, "DMSC_November_2025.pdf")

    if not file_result:
        print("\n✗ Failed at file import step")
        exit(1)

    # Step 2: Create CMS entry
    cms_result = create_cms_entry(
        title=test_title,
        wix_doc_ref=file_result["wixDocRef"],
        publish_date=test_date,
        summary=test_summary
    )

    if cms_result:
        print("\n" + "=" * 60)
        print("SUCCESS! Complete WIX workflow tested")
        print("=" * 60)
        print(f"\n✓ File imported to WIX Media Manager")
        print(f"✓ CMS entry created in Newsletters collection")
        print(f"\nWIX URL: {file_result['url']}")
    else:
        print("\n✗ Failed at CMS entry creation step")
        exit(1)
