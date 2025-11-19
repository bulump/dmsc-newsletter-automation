#!/usr/bin/env python3
"""
Test script for Dropbox API connection
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

if not DROPBOX_ACCESS_TOKEN:
    print("Error: DROPBOX_ACCESS_TOKEN not found in .env file")
    exit(1)

def test_dropbox_connection():
    """Test Dropbox API connection"""
    print("Testing Dropbox API Connection")
    print("=" * 60)

    # Test account info endpoint
    url = "https://api.dropboxapi.com/2/users/get_current_account"

    headers = {
        "Authorization": f"Bearer {DROPBOX_ACCESS_TOKEN}"
    }

    print(f"\nCalling: POST {url}")
    print()

    try:
        response = requests.post(url, headers=headers)
        print(f"Response Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("\n✓ Dropbox connection successful!")
            print(f"Account: {data.get('name', {}).get('display_name')}")
            print(f"Email: {data.get('email')}")
            return True
        else:
            print(f"\n✗ Error: {response.status_code}")
            print(response.text)
            return False

    except Exception as e:
        print(f"\n✗ Exception: {e}")
        return False


def list_folder(path=""):
    """List files in a Dropbox folder"""
    print("\n" + "=" * 60)
    print(f"Listing Dropbox folder: {path if path else '/ (root)'}")
    print("=" * 60)

    url = "https://api.dropboxapi.com/2/files/list_folder"

    headers = {
        "Authorization": f"Bearer {DROPBOX_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "path": path,
        "recursive": False,
        "include_media_info": False,
        "include_deleted": False
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            entries = result.get("entries", [])

            print(f"\nFound {len(entries)} items:\n")

            folders = [e for e in entries if e[".tag"] == "folder"]
            files = [e for e in entries if e[".tag"] == "file"]

            if folders:
                print("📁 Folders:")
                for folder in folders:
                    print(f"   {folder['name']}/")

            if files:
                print("\n📄 Files:")
                for file in files:
                    size_mb = file.get("size", 0) / (1024 * 1024)
                    print(f"   {file['name']} ({size_mb:.2f} MB)")

            return entries
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"✗ Exception: {e}")
        return None


if __name__ == "__main__":
    import sys

    # Test connection
    if not test_dropbox_connection():
        exit(1)

    # List root or specified folder
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = ""

    list_folder(folder_path)

    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Find your newsletter folder in the list above")
    print("2. Run: python3 test_dropbox.py \"/path/to/newsletter/folder\"")
    print("3. Or navigate: python3 test_dropbox.py \"/Newsletter\"")
    print("=" * 60)
