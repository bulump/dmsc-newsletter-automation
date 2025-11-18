# DMSC Newsletter Automation

Automated monthly newsletter campaign creation for the Dormont Mt. Lebanon Sportsmen's Club (DMSC).

## Overview

This tool automates the creation of monthly newsletter email campaigns in MailChimp. It uses a template-based approach to ensure consistent design while allowing easy customization of the month name and WIX newsletter link.

## Features

- **Template-Based**: Uses your existing newsletter design as a reusable template
- **Automated Campaign Creation**: Creates MailChimp campaigns with proper settings
- **Safe Draft Mode**: Always creates campaigns as drafts for manual review
- **Customizable**: Easy to update month name and newsletter link
- **Secure**: Uses environment variables for API credentials

## Current Phase: Phase 1 (Draft Mode)

The script currently creates draft campaigns that require manual review and sending through the MailChimp web interface.

**Future Phases:**
- Phase 2: Auto-send mode (script sends automatically)
- Phase 3: WIX PDF upload integration

## Prerequisites

- Python 3.7 or higher
- MailChimp account with API access
- MailChimp API key
- Audience/List ID

## Installation

1. Clone this repository:
```bash
cd ~/git
git clone <your-repo-url>
cd dmsc-newsletter-automation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your MailChimp credentials:
```bash
cp .env.example .env
```

4. Edit `.env` and add your credentials:
```
MAILCHIMP_API_KEY=your-api-key-here
MAILCHIMP_LIST_ID=your-list-id-here
```

**IMPORTANT:** Never commit the `.env` file to Git! It's already in `.gitignore`.

## Usage

### Command-Line Mode (Recommended)

```bash
python3 create_newsletter_campaign.py "December" "https://your-wix-link.com/newsletter.pdf"
```

### Interactive Mode

```bash
python3 create_newsletter_campaign.py
```

Then follow the prompts to enter the month name and WIX link.

## Monthly Workflow

1. **Prepare Newsletter PDF**: Generate your monthly newsletter PDF (using the dmsc-newsletter skill)

2. **Upload to WIX**: Upload the PDF to WIX CMS (manual for now, will be automated in Phase 3)

3. **Get WIX Link**: Copy the WIX link to the uploaded newsletter

4. **Run Script**:
   ```bash
   python3 create_newsletter_campaign.py "December" "https://your-wix-link.com"
   ```

5. **Review Draft**: The script will provide a MailChimp link to review your campaign

6. **Send Campaign**: When everything looks good, click "Send" in MailChimp

## Template Updates

If you need to update the newsletter template design:

1. Create a new campaign in MailChimp with your updated design
2. Send it successfully
3. Export the HTML using the MailChimp API or by viewing the campaign
4. Replace placeholders:
   - Replace the month name with `{{MONTH}}`
   - Replace the WIX link with `{{WIX_LINK}}`
5. Save as `newsletter_template.html`

## Security Notes

- **Never commit `.env` file** - It contains your API key
- **API key is sensitive** - Anyone with it can access your MailChimp account
- **Keep repo private** - This repo should remain private to protect club data
- **Rotate API keys** - If compromised, regenerate your API key in MailChimp

## Troubleshooting

### "MAILCHIMP_API_KEY not found in environment variables"

Make sure you've created a `.env` file with your API key.

### "Template file not found"

Ensure `newsletter_template.html` is in the same directory as the script.

### Campaign created but content failed to upload

Check that the template file contains valid HTML and has the correct placeholders.

### "Error creating campaign"

Verify your API key and List ID are correct in the `.env` file.

## Configuration

Edit `.env` to configure:

```
MAILCHIMP_API_KEY=your-api-key-us21
MAILCHIMP_LIST_ID=your-list-id
```

The script automatically detects the data center (e.g., `us21`) from your API key.

## Files

- `create_newsletter_campaign.py` - Main automation script
- `newsletter_template.html` - Newsletter HTML template with placeholders
- `.env` - Configuration file (not tracked in Git)
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Club Information

- **Club**: Dormont / Mt Lebanon Sportsmen's Club (DMSC)
- **Email**: dmscnews@gmail.com
- **Newsletter Editor**: Chris Bielinski
- **Subscriber Count**: ~1,278 members
- **Average Open Rate**: 60%
- **Average Click Rate**: 17%

## Support

For issues or questions:
- Check the troubleshooting section above
- Review MailChimp API documentation: https://mailchimp.com/developer/
- Contact the newsletter editor

## License

This is internal club automation software. Not licensed for external use.

---

*Generated with Claude Code* 🤖
