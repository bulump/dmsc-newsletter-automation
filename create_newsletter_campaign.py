#!/usr/bin/env python3
"""
DMSC Newsletter Campaign Automation
Phase 1: Creates draft campaigns for manual review before sending

This script:
1. Reads the newsletter HTML template
2. Replaces {{MONTH}} and {{WIX_LINK}} placeholders
3. Creates a new campaign with the customized content
4. Leaves campaign as DRAFT for manual review

Phase 2 (future): Will auto-send after review
Phase 3 (future): Will upload PDF to WIX CMS automatically
"""

import requests
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# MailChimp API Configuration from environment
API_KEY = os.getenv("MAILCHIMP_API_KEY")
LIST_ID = os.getenv("MAILCHIMP_LIST_ID")

if not API_KEY:
    print("Error: MAILCHIMP_API_KEY not found in environment variables")
    print("Please create a .env file with your API key")
    sys.exit(1)

if not LIST_ID:
    print("Error: MAILCHIMP_LIST_ID not found in environment variables")
    print("Please create a .env file with your list ID")
    sys.exit(1)

# Extract data center from API key
DC = API_KEY.split("-")[-1]
BASE_URL = f"https://{DC}.api.mailchimp.com/3.0"

# Template file location (in same directory as script)
SCRIPT_DIR = Path(__file__).parent
TEMPLATE_FILE = SCRIPT_DIR / "newsletter_template.html"

# Authentication
AUTH = ("anystring", API_KEY)
HEADERS = {"Content-Type": "application/json"}


def read_template():
    """Read the newsletter HTML template."""
    if not TEMPLATE_FILE.exists():
        raise Exception(f"Template file not found: {TEMPLATE_FILE}")

    with open(TEMPLATE_FILE, 'r') as f:
        return f.read()


def create_campaign(month, year):
    """Create a new campaign with title and subject."""
    url = f"{BASE_URL}/campaigns"

    data = {
        "type": "regular",
        "recipients": {
            "list_id": LIST_ID
        },
        "settings": {
            "subject_line": f"DMSC {month} Newsletter is available!",
            "title": f"{month} Newsletter",
            "from_name": "DMSC",
            "reply_to": "dmscnews@gmail.com"
        }
    }

    response = requests.post(url, auth=AUTH, headers=HEADERS, json=data)
    response.raise_for_status()

    return response.json()


def set_campaign_content(campaign_id, html_content):
    """Set the HTML content for a campaign."""
    url = f"{BASE_URL}/campaigns/{campaign_id}/content"

    data = {"html": html_content}

    response = requests.put(url, auth=AUTH, headers=HEADERS, json=data)
    response.raise_for_status()

    return response.json()


def get_campaign_web_url(campaign_id):
    """Get the MailChimp web UI URL for the campaign."""
    url = f"{BASE_URL}/campaigns/{campaign_id}"
    response = requests.get(url, auth=AUTH, headers=HEADERS)
    response.raise_for_status()

    campaign = response.json()
    web_id = campaign.get("web_id")

    # MailChimp campaign editor URL format
    return f"https://{DC}.admin.mailchimp.com/campaigns/edit?id={web_id}"


def main():
    """Main workflow for creating newsletter campaign."""
    print("=" * 60)
    print("DMSC Newsletter Campaign Creator")
    print("Phase 1: Draft Mode")
    print("=" * 60)
    print()

    # Check for command-line arguments
    if len(sys.argv) >= 3:
        new_month = sys.argv[1]
        wix_link = sys.argv[2]
        print(f"Using command-line arguments:")
        print(f"  Month: {new_month}")
        print(f"  WIX Link: {wix_link}")
        print()
    else:
        # Interactive mode
        print("Usage: python3 create_newsletter_campaign.py <month> <wix_link>")
        print("Example: python3 create_newsletter_campaign.py December https://yourlink.com")
        print()
        print("Or run without arguments for interactive mode:")
        print()

        new_month = input(f"Enter new month (e.g., 'December', 'January'): ").strip()
        if not new_month:
            print("✗ Month is required")
            sys.exit(1)

        wix_link = input("Enter WIX newsletter link: ").strip()
        if not wix_link:
            print("✗ WIX link is required")
            sys.exit(1)
        print()

    # Step 1: Read template
    print("Step 1: Reading newsletter template...")
    try:
        template_html = read_template()
        print(f"✓ Template loaded ({len(template_html)} characters)")
        print()
    except Exception as e:
        print(f"✗ Error reading template: {e}")
        sys.exit(1)

    # Step 2: Customize template
    print("Step 2: Customizing template...")
    try:
        customized_html = template_html.replace("{{MONTH}}", new_month)
        customized_html = customized_html.replace("{{WIX_LINK}}", wix_link)
        print(f"✓ Replaced {{{{MONTH}}}} with '{new_month}'")
        print(f"✓ Replaced {{{{WIX_LINK}}}} with WIX URL")
        print()
    except Exception as e:
        print(f"✗ Error customizing template: {e}")
        sys.exit(1)

    # Step 3: Create campaign
    print("Step 3: Creating new campaign...")
    try:
        current_year = datetime.now().year
        new_campaign = create_campaign(new_month, current_year)
        campaign_id = new_campaign["id"]
        print(f"✓ Campaign created")
        print(f"  Campaign ID: {campaign_id}")
        print(f"  Title: {new_month} Newsletter")
        print(f"  Subject: DMSC {new_month} Newsletter is available!")
        print()
    except Exception as e:
        print(f"✗ Error creating campaign: {e}")
        sys.exit(1)

    # Step 4: Upload content
    print("Step 4: Uploading customized HTML content...")
    try:
        set_campaign_content(campaign_id, customized_html)
        print(f"✓ HTML content uploaded successfully")
        print()
    except Exception as e:
        print(f"✗ Error uploading content: {e}")
        print(f"  Campaign ID {campaign_id} was created but content failed to upload")
        sys.exit(1)

    # Step 5: Provide next steps
    print("=" * 60)
    print("SUCCESS! Draft campaign created")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review the campaign in MailChimp:")
    web_url = get_campaign_web_url(campaign_id)
    print(f"   {web_url}")
    print()
    print("2. Check that:")
    print(f"   - '{new_month}' appears correctly in the button text")
    print(f"   - WIX link ({wix_link[:50]}...) works correctly")
    print("   - Email design looks perfect")
    print()
    print("3. When ready, click 'Send' in MailChimp")
    print()
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
