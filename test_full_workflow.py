#!/usr/bin/env python3
"""
Test complete Dropbox -> WIX workflow
"""

import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
WIX_API_KEY = os.getenv("WIX_API_KEY")
WIX_SITE_ID = os.getenv("WIX_SITE_ID")

def find_newsletter_pdf(month, year=None):
    """Find the newsletter PDF in Dropbox for a given month"""
    if not year:
        year = datetime.now().year

    # Path pattern: /Newsletter/Monthly Newsletters/2025 Newsletter/November/DMSC_2025_Nov_Web.pdf
    folder_path = f"/Newsletter/Monthly Newsletters/{year} Newsletter/{month}"

    print(f"Looking for newsletter in: {folder_path}")

    url = "https://api.dropboxapi.com/2/files/list_folder"
    headers = {
        "Authorization": f"Bearer {DROPBOX_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"path": folder_path}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        entries = response.json().get("entries", [])
        pdf_files = [e for e in entries if e["name"].endswith("_Web.pdf")]

        if pdf_files:
            pdf_file = pdf_files[0]
            print(f"✓ Found: {pdf_file['name']}")
            return {
                "path": pdf_file["path_lower"],
                "filename": pdf_file["name"]
            }
        else:
            print(f"✗ No PDF found in {folder_path}")
            return None
    else:
        print(f"✗ Error listing folder: {response.status_code}")
        print(response.text)
        return None


def create_dropbox_share_link(file_path):
    """Create a temporary share link for a Dropbox file"""
    print(f"\nCreating share link for: {file_path}")

    url = "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings"
    headers = {
        "Authorization": f"Bearer {DROPBOX_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "path": file_path,
        "settings": {
            "requested_visibility": "public"
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        share_data = response.json()
        share_url = share_data["url"]
        # Convert to direct download URL (replace dl=0 with dl=1)
        direct_url = share_url.replace("dl=0", "dl=1").replace("www.dropbox.com", "dl.dropboxusercontent.com")
        print(f"✓ Share link created: {direct_url}")
        return direct_url
    elif response.status_code == 409:
        # Link already exists, get it
        print("  Share link already exists, retrieving...")
        get_url = "https://api.dropboxapi.com/2/sharing/list_shared_links"
        get_data = {"path": file_path}
        get_response = requests.post(get_url, headers=headers, json=get_data)

        if get_response.status_code == 200:
            links = get_response.json().get("links", [])
            if links:
                share_url = links[0]["url"]
                direct_url = share_url.replace("dl=0", "dl=1").replace("www.dropbox.com", "dl.dropboxusercontent.com")
                print(f"✓ Existing share link: {direct_url}")
                return direct_url

        print("✗ Could not retrieve existing link")
        return None
    else:
        print(f"✗ Error creating share link: {response.status_code}")
        print(response.text)
        return None


def import_to_wix(file_url, display_name):
    """Import file to WIX from URL"""
    print(f"\nImporting to WIX: {display_name}")

    url = "https://www.wixapis.com/site-media/v1/files/import"
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

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        file_id = result.get("file", {}).get("id")
        file_url_wix = result.get("file", {}).get("url")

        # Convert GUID subdomain to public domain
        file_url_wix = file_url_wix.replace(f"https://{WIX_SITE_ID}.usrfiles.com/ugd/", "https://www.dmlsclub.com/_files/ugd/")

        # Update result with vanity URL
        result["file"]["url"] = file_url_wix

        print(f"✓ File imported to WIX!")
        print(f"  File ID: {file_id}")
        print(f"  Public URL: {file_url_wix}")
        return result
    else:
        print(f"✗ Error importing to WIX: {response.status_code}")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
        return None


if __name__ == "__main__":
    import sys

    month = sys.argv[1] if len(sys.argv) > 1 else "November"

    print("=" * 60)
    print(f"Testing Full Workflow: {month} Newsletter")
    print("=" * 60)

    # Step 1: Find PDF in Dropbox
    print("\nStep 1: Finding newsletter PDF...")
    pdf_info = find_newsletter_pdf(month)

    if not pdf_info:
        print("\n✗ Failed to find PDF")
        exit(1)

    pdf_path = pdf_info["path"]
    pdf_filename = pdf_info["filename"]

    # Step 2: Create share link
    print("\nStep 2: Creating Dropbox share link...")
    share_link = create_dropbox_share_link(pdf_path)

    if not share_link:
        print("\n✗ Failed to create share link")
        exit(1)

    # Step 3: Import to WIX
    print("\nStep 3: Importing to WIX...")
    wix_result = import_to_wix(share_link, pdf_filename)

    if wix_result:
        print("\n" + "=" * 60)
        print("SUCCESS! Complete workflow tested")
        print("=" * 60)
        print(f"\nDropbox PDF: {pdf_path}")
        print(f"Share link: {share_link}")
        print(f"WIX import: Success")
        print("\nNext: Get WIX public URL and create MailChimp campaign!")
    else:
        print("\n✗ Failed to import to WIX")
        exit(1)
