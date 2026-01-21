# Email Setup Guide for Notch Chatbot

The chatbot can automatically create and send professional PDF proposals to prospects. This guide explains how to set up the email functionality.

## 📧 Automatic BCC for Tracking

**IMPORTANT**: All proposals sent to clients are automatically BCC'd to:
- `darko.spoljaric@wearenotch.com`
- `sanja.buterin@wearenotch.com`

This allows the Notch team to:
- Track all proposals sent by the bot
- Follow up with prospects
- Monitor bot performance
- Maintain records

The client will NOT see these BCC recipients - they'll only see their own email address.

**To modify BCC recipients**: Edit `src/notch_chatbot/tools.py` and update the `bcc` list in the `create_and_send_offer` function.

## Overview

The chatbot includes a powerful tool:
- **`create_and_send_offer`** - Generates a professional PDF proposal with Notch branding and sends it via email using SendGrid

## SendGrid Setup (Free - 100 emails/day)

### Step 1: Create SendGrid Account
1. Go to [https://sendgrid.com/free/](https://sendgrid.com/free/)
2. Sign up for a free account (no credit card required)
3. Free tier includes 100 emails per day - perfect for a chatbot

### Step 2: Create API Key
1. Log in to SendGrid dashboard
2. Go to **Settings** → **API Keys**
3. Click **Create API Key**
4. Name it (e.g., "Notch Chatbot")
5. Select **Full Access** (or at minimum: Mail Send access)
6. Click **Create & View**
7. **IMPORTANT**: Copy the API key immediately (you won't be able to see it again)

### Step 3: Verify Sender Identity
1. Go to **Settings** → **Sender Authentication**
2. Choose **Single Sender Verification** (easiest for free tier)
3. Add your email address (e.g., proposals@wearenotch.com or your personal email)
4. Fill in the form with sender details
5. Check your email and click the verification link
6. Wait for approval (usually instant)

### Step 4: Configure Environment Variables
Add to your `.env` file:

```bash
SENDGRID_API_KEY=SG.your_actual_api_key_here
SENDGRID_FROM_EMAIL=verified-email@example.com  # Must match verified sender
```

**Important**:
- Use the email you verified in Step 3
- Keep the API key secret (never commit to git)

## How It Works

### Automated Workflow
When a prospect shows interest, the chatbot:
1. Collects their name and email during conversation
2. Gathers project requirements from context
3. Identifies relevant Notch services
4. Creates a professional PDF proposal including:
   - Project overview
   - Recommended services
   - Team composition
   - Pricing estimates based on scope
   - Next steps
   - Legal disclaimer (orientational, non-binding)
5. Sends the PDF via email with a professional message

### Pricing Estimates
The chatbot automatically includes pricing based on project scope:
- **Small projects**: Starting from $15,000 - $35,000
- **Medium projects**: $35,000 - $100,000 (most common)
- **Large projects**: $100,000+ for enterprise/complex systems

### PDF Features
- Notch branding and professional formatting
- Client information
- Project description based on conversation
- Relevant services matched to their needs
- Team composition breakdown
- Investment estimates
- Clear next steps
- Legal disclaimer about proposal being orientational

## Testing

### Test Without Sending Emails
To test the PDF generation without sending emails:
1. Don't set `SENDGRID_API_KEY` in `.env`
2. The chatbot will create the offer but report the missing key
3. You can still verify the PDF generation logic works

### Send Test Email
Once configured:
1. Start a chat with the bot
2. Describe a project need
3. Provide your name and test email
4. Bot will create and send the proposal
5. Check your inbox (and spam folder)

## Troubleshooting

### Error: "SENDGRID_API_KEY not configured"
- Make sure you've added the API key to `.env`
- Restart the application after adding the key
- Check for typos in the environment variable name

### Error: "Sender email not verified"
- Verify your sender email in SendGrid dashboard
- Make sure `SENDGRID_FROM_EMAIL` matches the verified email exactly
- Wait a few minutes after verification

### Email not received
- Check spam/junk folder
- Verify the recipient email is correct
- Check SendGrid dashboard for delivery status
- Ensure you haven't exceeded free tier limit (100/day)

### PDF generation errors
- Ensure `fpdf2` is installed: `uv pip install fpdf2`
- Check that project description isn't too long
- Verify all required parameters are provided

## Free Tier Limits

SendGrid free tier includes:
- **100 emails per day**
- Single sender verification
- Email API access
- Delivery analytics
- Email activity tracking

This is more than enough for a chatbot handling prospect inquiries.

## Security Best Practices

1. **Never commit API keys** - Use `.env` file (already in `.gitignore`)
2. **Rotate keys periodically** - Generate new keys every few months
3. **Use environment-specific keys** - Different keys for dev/staging/production
4. **Monitor usage** - Check SendGrid dashboard for suspicious activity
5. **Verify sender identity** - Only use verified email addresses

## Support

- SendGrid documentation: [https://docs.sendgrid.com](https://docs.sendgrid.com)
- SendGrid support: [https://support.sendgrid.com](https://support.sendgrid.com)
- Free tier FAQ: [https://sendgrid.com/pricing/](https://sendgrid.com/pricing/)
