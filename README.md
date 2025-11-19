# DMSC Newsletter Automation

**Complete automation for monthly newsletter campaigns** - from Dropbox to WIX to MailChimp in a single command.

Automated monthly newsletter campaign creation for the Dormont Mt. Lebanon Sportsmen's Club (DMSC).

## Overview

This tool provides **complete end-to-end automation** for DMSC newsletter distribution:
- 📁 **Dropbox Integration**: Automatically finds newsletter PDFs and Ted's Thoughts documents
- 🌐 **WIX CMS Integration**: Uploads PDFs to WIX Media Manager and creates CMS entries
- 📧 **MailChimp Integration**: Creates email campaigns with customized content
- 🤖 **AI-Powered**: Extracts meeting information from Ted's Thoughts automatically

## Features

- ✅ **Single Command**: Run one command and everything is automated
- ✅ **Dropbox PDF Discovery**: Automatically finds the newsletter PDF by month
- ✅ **WIX Upload & CMS**: Imports PDF to WIX and creates proper CMS entry
- ✅ **Meeting Info Extraction**: Reads Ted's Thoughts to get meeting summary
- ✅ **MailChimp Campaign**: Creates draft campaign ready for review
- ✅ **Safe Draft Mode**: Always creates campaigns as drafts for manual review
- ✅ **Secure**: Uses environment variables for all API credentials

## Current Phase: Phase 3 ✅ COMPLETE

**Phase 3** implements complete Dropbox → WIX → MailChimp automation.

**Completed Phases:**
- ✅ Phase 1: MailChimp draft campaign creation
- ✅ Phase 2: Email template customization
- ✅ Phase 3: Dropbox and WIX CMS integration

**Future Enhancement:**
- Phase 4 (optional): Auto-send mode after review period

## Prerequisites

- Python 3.7 or higher
- **MailChimp** account with API access
- **WIX** account with API access (API key with Media Manager + Data permissions)
- **Dropbox** access token for newsletter folder
- Virtual environment (venv) recommended

## Installation

1. Clone this repository:
```bash
cd ~/git
git clone <your-repo-url>
cd dmsc-newsletter-automation
```

2. Create virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file with your API credentials:
```bash
cp .env.example .env
```

4. Edit `.env` and add your credentials:
```
# MailChimp API Configuration
MAILCHIMP_API_KEY=your-api-key-here
MAILCHIMP_LIST_ID=your-list-id-here

# WIX API Configuration
WIX_API_KEY=your-wix-api-key-here
WIX_SITE_ID=your-wix-site-id-here

# Dropbox API Configuration
DROPBOX_ACCESS_TOKEN=your-dropbox-token-here
```

**IMPORTANT:** Never commit the `.env` file to Git! It's already in `.gitignore`.

## Usage

### Simple Single-Command Mode

```bash
python3 create_newsletter_campaign.py November
```

That's it! The script will:
1. Find the newsletter PDF in Dropbox (`/Newsletter/Monthly Newsletters/2025 Newsletter/November/`)
2. Create a Dropbox share link
3. Extract meeting info from Ted's Thoughts document
4. Import the PDF to WIX Media Manager
5. Create a WIX CMS entry with proper formatting
6. Create a MailChimp draft campaign with the WIX URL

### Interactive Mode

```bash
python3 create_newsletter_campaign.py
```

You'll be prompted to enter the month name.

## Monthly Workflow

### Old Workflow (Manual):
1. Generate newsletter PDF
2. Upload to Dropbox
3. Upload to WIX manually
4. Copy WIX link
5. Run script with month and link
6. Review and send

### New Workflow (Automated):
1. **Upload newsletter PDF to Dropbox** (in the monthly folder)
2. **Run the script**:
   ```bash
   python3 create_newsletter_campaign.py December
   ```
3. **Review**:
   - Check WIX CMS entry at dmlsclub.com/newsletters
   - Review MailChimp campaign (link provided by script)
4. **Send**: Click "Send" in MailChimp when ready

That's it! Everything else is automated.

## Dropbox Folder Structure

The script expects this structure:
```
/Newsletter/Monthly Newsletters/
  └── 2025 Newsletter/
      ├── November/
      │   ├── DMSC_2025_Nov_Web.pdf
      │   └── Ted's Thouh Nov 25.docx
      ├── December/
      │   ├── DMSC_2025_Dec_Web.pdf
      │   └── Ted's Thoughts Dec 25.docx
      └── ...
```

**Requirements:**
- PDF filename must end with `_Web.pdf`
- Ted's Thoughts must be a `.docx` file with "ted" in the name
- Month folder name must match the command-line argument

## WIX CMS Entry Format

The script creates entries in the "Newsletters" collection with:
- **Title**: "November 2025"
- **Newsletter**: `wix:document://v1/ugd/{file_id}/DMSC_2025_Nov_Web.pdf`
- **Publish Month**: Empty (fill manually in WIX UI)
- **Newsletter Summary**: Extracted from Ted's Thoughts or default message

## API Configuration

### MailChimp API Key
1. Log in to MailChimp
2. Go to Account → Extras → API keys
3. Create a new key
4. Copy to `.env` as `MAILCHIMP_API_KEY`

### MailChimp List ID
1. Go to Audience → Settings
2. Copy "Audience ID"
3. Add to `.env` as `MAILCHIMP_LIST_ID`

### WIX API Key
1. Log in to WIX Dashboard
2. Go to Settings → API Keys
3. Create new API key with permissions:
   - ✅ Site Media (read + write)
   - ✅ Wix Data (read + write)
4. Copy the IST token to `.env` as `WIX_API_KEY`

### WIX Site ID
1. In WIX Dashboard, go to Settings
2. Find your Site ID (GUID format)
3. Add to `.env` as `WIX_SITE_ID`

### Dropbox Access Token
1. Go to https://www.dropbox.com/developers/apps
2. Create or select your app
3. Generate access token
4. Copy to `.env` as `DROPBOX_ACCESS_TOKEN`
5. **Note**: Tokens expire - regenerate as needed

## Template Updates

If you need to update the newsletter email template design:

1. Create a new campaign in MailChimp with your updated design
2. Send it successfully
3. Export the HTML
4. Replace placeholders:
   - Replace the month name with `{{MONTH}}`
   - Replace the WIX link with `{{WIX_LINK}}`
5. Save as `newsletter_template.html`

## Security Notes

- **Never commit `.env` file** - Contains all API credentials
- **All API keys are sensitive** - Anyone with them can access your accounts
- **Keep repo private** - This repo should remain private to protect club data
- **Rotate tokens** - If compromised, regenerate immediately
- **Dropbox tokens expire** - Regenerate access tokens when they expire

## Troubleshooting

### "expired_access_token" (Dropbox)
Dropbox access tokens expire. Generate a new one at https://www.dropbox.com/developers/apps and update `.env`.

### "Could not find newsletter PDF"
- Check the month folder exists in Dropbox
- Verify PDF filename ends with `_Web.pdf`
- Ensure folder structure matches expected pattern

### "WIX API 403 Forbidden"
- Verify WIX_API_KEY has both Media Manager and Data permissions
- Check WIX_SITE_ID is correct (not Account ID)

### "No Ted's Thoughts found"
The script will use a default summary. To enable extraction:
- Ensure `.docx` file exists in the month folder
- Filename must contain "ted" (case-insensitive)

## Testing

The repository includes test scripts for each integration:

```bash
# Test Dropbox connection and folder listing
python3 test_dropbox.py "/Newsletter/Monthly Newsletters/2025 Newsletter/November"

# Test WIX authentication
python3 test_wix_auth.py

# Test complete WIX workflow (import + CMS)
python3 test_wix_complete.py

# Test Ted's Thoughts extraction
python3 test_teds_thoughts.py November

# Test full Dropbox → WIX workflow
python3 test_full_workflow.py November
```

## Files

### Main Scripts
- `create_newsletter_campaign.py` - **Main automation script**
- `newsletter_template.html` - Newsletter HTML template with placeholders

### Test Scripts
- `test_dropbox.py` - Test Dropbox API connection
- `test_wix_auth.py` - Test WIX API authentication
- `test_wix_complete.py` - Test WIX file import + CMS entry
- `test_wix_existing_entry.py` - Query WIX CMS entries
- `test_teds_thoughts.py` - Test meeting info extraction
- `test_full_workflow.py` - Test Dropbox → WIX workflow

### Configuration
- `.env` - API credentials (not tracked in Git)
- `.env.example` - Template for `.env` file
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Dependencies

```
requests>=2.31.0         # HTTP requests for APIs
python-dotenv>=1.0.0     # Environment variable management
python-docx>=1.0.0       # Read .docx files (Ted's Thoughts)
```

## Club Information

- **Club**: Dormont / Mt Lebanon Sportsmen's Club (DMSC)
- **Email**: dmscnews@gmail.com
- **Newsletter Editor**: Chris Bielinski
- **Subscriber Count**: ~1,200 members
- **Average Open Rate**: 60%
- **Average Click Rate**: 17%

## Support

For issues or questions:
- Check the troubleshooting section above
- Review API documentation:
  - MailChimp: https://mailchimp.com/developer/
  - WIX: https://dev.wix.com/docs/rest
  - Dropbox: https://www.dropbox.com/developers/documentation
- Contact the newsletter editor

## License

This is internal club automation software. Not licensed for external use.

---

*Automated with Claude Code* 🤖
