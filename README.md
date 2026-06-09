# Gmail-Connected AI Email Agent

A Python-based AI agent that manages your Gmail inbox, searches emails, drafts replies, and sends emails on your behalf with built-in safety controls.

## Features

✅ **Email Management**
- Search emails with natural language queries
- Read and summarize emails
- Mark emails as read
- Archive and delete emails
- Add labels to emails

✅ **Compose & Send**
- Draft new emails
- Send emails with CC/BCC support
- Reply to emails
- Forward emails with optional notes

✅ **AI-Powered**
- Uses OpenAI's GPT-4 to understand natural language commands
- Writes professional emails in your voice
- Intelligent safety classification before sending

✅ **Safety Controls**
- Risk classification (low/medium/high)
- Email preview before sending sensitive emails
- Blocks emails with suspicious patterns
- Configurable send modes (draft_only, confirm_before_send, auto_send_allowed)
- Action logging

## Tech Stack

- **Python 3.8+**
- **Gmail API** - for email management
- **OpenAI API** - for AI agent functionality
- **OAuth 2.0** - for secure authentication
- **Google Auth** - for credential management

## Prerequisites

1. Python 3.8 or higher
2. Google Cloud Project with Gmail API enabled
3. OpenAI API key
4. Gmail account

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd email-agent
```

### 2. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Go to **APIs & Services > Enabled APIs & services**
4. Click **Enable APIs and Services**
5. Search for "Gmail API" and enable it
6. Search for "Google+ API" and enable it

### 3. Create OAuth 2.0 Credentials

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > OAuth client ID**
3. Choose **Desktop application**
4. Download the JSON file
5. Save it as `credentials/credentials.json`

### 4. Configure OAuth Consent Screen

1. Go to **APIs & Services > OAuth consent screen**
2. Choose **External** user type
3. Fill in the required information:
   - App name: "Gmail Email Agent"
   - User support email: Your email
   - Developer contact: Your email
4. Add scopes:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.compose`
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/gmail.modify`
5. Add yourself as a test user
6. Save and continue

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-...
   ```

3. (Optional) Customize other settings:
   ```
   EMAIL_SEND_MODE=confirm_before_send  # or draft_only, auto_send_allowed
   DEFAULT_USER_NAME=Your Name
   DEFAULT_SIGNATURE=Your signature
   ```

### 7. Create Credentials Directory

```bash
mkdir -p credentials
# Place your credentials.json here
```

### 8. Run the Agent

```bash
python app.py
```

On first run, you'll be directed to authenticate with Google. Follow the browser prompts and authorize the app.

## Usage Examples

### Search Emails
```
You: Find emails from Capital One about my car loan
Agent: [searches and displays results]

You: Show me unread emails from today
Agent: [displays unread emails from today]
```

### Read & Summarize
```
You: Read the latest email from John and summarize it
Agent: [reads and summarizes the email]
```

### Send Emails
```
You: Send an email to ruben@example.com and tell him I can schedule a call this week
Agent: [drafts email, shows preview for confirmation]
Agent: Awaiting confirmation...
You: yes
```

### Reply to Emails
```
You: Reply to the last email from John and tell him I'll follow up tomorrow
Agent: [creates reply draft, asks for confirmation if needed]
```

### Organize Emails
```
You: Archive all promotional emails from this week
Agent: [archives promotional emails]

You: Label all ghostwriting leads as "Ghostwriting Leads"
Agent: [adds labels to specified emails]
```

## Configuration

### Email Send Modes

#### `draft_only`
The agent only creates drafts and never sends emails automatically.

```
EMAIL_SEND_MODE=draft_only
```

#### `confirm_before_send` (Default)
The agent asks for confirmation before sending medium and high-risk emails.
Low-risk emails are sent without asking.

```
EMAIL_SEND_MODE=confirm_before_send
```

#### `auto_send_allowed`
The agent can send low and medium-risk emails without asking.
High-risk emails still require confirmation.

```
EMAIL_SEND_MODE=auto_send_allowed
```

### Risk Classification

**Low-Risk Emails:**
- Thank-you messages
- Scheduling confirmations
- Follow-ups
- Simple business replies

**Medium-Risk Emails:**
- Proposals and quotes
- Price discussions
- Work-related concerns
- Emails with attachments
- Important commitments

**High-Risk Emails:**
- Financial decisions
- Legal matters
- Medical information
- Disciplinary matters
- Payment details
- Personal identifiers
- Any email with forbidden content

## Project Structure

```
email-agent/
├── app.py                 # CLI interface
├── agent.py              # AI agent logic
├── gmail_client.py       # Gmail API wrapper
├── tools.py              # Tool implementations
├── config.py             # Configuration management
├── safety.py             # Email safety classification
├── memory.py             # Action logging
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
├── README.md             # This file
├── credentials/          # Store credentials.json here
│   └── README.md
└── logs/                 # Action logs
    └── actions.log
```

## Action Logging

All email actions are logged to `logs/actions.log` in JSON format.

View logs in the CLI:
```
You: logs
```

## Troubleshooting

### "credentials.json not found"
Make sure you've downloaded your credentials from Google Cloud Console and placed them in the `credentials/` directory.

### "Invalid Gmail scopes"
Ensure your OAuth consent screen includes all required scopes:
- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/gmail.compose`
- `https://www.googleapis.com/auth/gmail.send`
- `https://www.googleapis.com/auth/gmail.modify`

### "Authentication failed"
Delete `credentials/token.json` and run the agent again. You'll be prompted to authenticate.

### "Email blocked for sensitive content"
The agent detected sensitive information (SSN, credit card, password) in the email. Remove it and try again.

## Safety & Privacy

- **Secure Credentials**: OAuth tokens and credentials are stored locally and never exposed
- **Sensitive Content Blocking**: Emails with passwords, SSNs, or credit card numbers are blocked
- **Forbidden Content**: Emails with threatening, fraudulent, or discriminatory content are blocked
- **Confirmation Prompts**: High-risk emails require user confirmation before sending
- **Action Logging**: All actions are logged for audit purposes

## API Rate Limits

- **Gmail API**: 1 billion queries per day (per account)
- **OpenAI API**: Check your plan at https://platform.openai.com/account/billing/limits

## Contributing

Contributions are welcome! Please submit a pull request with:
- Clear description of changes
- Tests for new functionality
- Updated documentation

## License

MIT License

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the Gmail API documentation: https://developers.google.com/gmail/api
3. Check OpenAI documentation: https://platform.openai.com/docs

## Disclaimer

This agent has safety controls, but always review important emails before sending. The agent is not responsible for any unintended emails sent.
