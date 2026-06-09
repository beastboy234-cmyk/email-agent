import base64
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_core.exceptions import GoogleAPICallError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

from config import (
    GOOGLE_CLIENT_SECRET_PATH,
    TOKEN_PATH,
    GMAIL_SCOPES,
    DEFAULT_SIGNATURE,
)

logger = logging.getLogger(__name__)


class GmailClient:
    """Handles Gmail API authentication and communication."""

    def __init__(self):
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with Gmail API using OAuth 2.0."""
        creds = None

        # Load existing token if it exists
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, GMAIL_SCOPES)

        # If no valid credentials, create new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(GOOGLE_CLIENT_SECRET_PATH):
                    raise FileNotFoundError(
                        f"credentials.json not found at {GOOGLE_CLIENT_SECRET_PATH}. "
                        "Please download it from Google Cloud Console."
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    GOOGLE_CLIENT_SECRET_PATH, GMAIL_SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials for future use
            os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())

        self.service = build("gmail", "v1", credentials=creds)
        logger.info("Gmail authentication successful")

    def search_emails(self, query, max_results=10):
        """Search for emails in Gmail."""
        try:
            results = self.service.users().messages().list(
                userId="me", q=query, maxResults=max_results
            ).execute()
            messages = results.get("messages", [])
            return messages
        except HttpError as error:
            logger.error(f"Error searching emails: {error}")
            return []

    def read_email(self, message_id):
        """Read a single email."""
        try:
            message = self.service.users().messages().get(
                userId="me", id=message_id, format="full"
            ).execute()
            return message
        except HttpError as error:
            logger.error(f"Error reading email: {error}")
            return None

    def get_email_body(self, message):
        """Extract body from email message."""
        try:
            if "parts" in message["payload"]:
                parts = message["payload"]["parts"]
                body = ""
                for part in parts:
                    if part["mimeType"] == "text/plain":
                        body = base64.urlsafe_b64decode(
                            part["body"].get("data", "")
                        ).decode("utf-8")
                        break
                return body
            else:
                body = base64.urlsafe_b64decode(
                    message["payload"]["body"].get("data", "")
                ).decode("utf-8")
                return body
        except Exception as e:
            logger.error(f"Error extracting body: {e}")
            return ""

    def get_email_subject(self, message):
        """Extract subject from email."""
        headers = message["payload"]["headers"]
        for header in headers:
            if header["name"] == "Subject":
                return header["value"]
        return "(No Subject)"

    def get_email_from(self, message):
        """Extract sender from email."""
        headers = message["payload"]["headers"]
        for header in headers:
            if header["name"] == "From":
                return header["value"]
        return "Unknown"

    def get_email_to(self, message):
        """Extract recipient from email."""
        headers = message["payload"]["headers"]
        for header in headers:
            if header["name"] == "To":
                return header["value"]
        return ""

    def get_thread_messages(self, thread_id):
        """Get all messages in a thread."""
        try:
            thread = self.service.users().threads().get(
                userId="me", id=thread_id, format="full"
            ).execute()
            return thread.get("messages", [])
        except HttpError as error:
            logger.error(f"Error reading thread: {error}")
            return []

    def send_email(self, to, subject, body, cc=None, bcc=None):
        """Send an email."""
        try:
            from email.mime.text import MIMEText

            message = MIMEText(body)
            message["to"] = to
            message["subject"] = subject
            if cc:
                message["cc"] = cc
            if bcc:
                message["bcc"] = bcc

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = {"raw": raw_message}

            result = self.service.users().messages().send(
                userId="me", body=send_message
            ).execute()
            logger.info(f"Email sent to {to}")
            return result
        except HttpError as error:
            logger.error(f"Error sending email: {error}")
            return None

    def create_draft(self, to, subject, body, cc=None, bcc=None):
        """Create a draft email."""
        try:
            from email.mime.text import MIMEText

            message = MIMEText(body)
            message["to"] = to
            message["subject"] = subject
            if cc:
                message["cc"] = cc
            if bcc:
                message["bcc"] = bcc

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            draft_message = {"message": {"raw": raw_message}}

            result = self.service.users().drafts().create(
                userId="me", body=draft_message
            ).execute()
            logger.info(f"Draft created for {to}")
            return result
        except HttpError as error:
            logger.error(f"Error creating draft: {error}")
            return None

    def reply_to_email(self, message_id, body):
        """Reply to an email."""
        try:
            # Get original message
            original_message = self.read_email(message_id)
            thread_id = original_message["threadId"]
            from_address = self.get_email_from(original_message)
            subject = self.get_email_subject(original_message)

            # Prepare reply subject
            if not subject.startswith("Re:"):
                subject = f"Re: {subject}"

            # Send reply
            result = self.send_email(from_address, subject, body)
            logger.info(f"Reply sent to {from_address}")
            return result
        except Exception as e:
            logger.error(f"Error replying to email: {e}")
            return None

    def create_draft_reply(self, message_id, body):
        """Create a draft reply to an email."""
        try:
            # Get original message
            original_message = self.read_email(message_id)
            from_address = self.get_email_from(original_message)
            subject = self.get_email_subject(original_message)

            # Prepare reply subject
            if not subject.startswith("Re:"):
                subject = f"Re: {subject}"

            # Create draft reply
            result = self.create_draft(from_address, subject, body)
            logger.info(f"Draft reply created for {from_address}")
            return result
        except Exception as e:
            logger.error(f"Error creating draft reply: {e}")
            return None

    def forward_email(self, message_id, to, note=None):
        """Forward an email."""
        try:
            original_message = self.read_email(message_id)
            subject = self.get_email_subject(original_message)
            body = self.get_email_body(original_message)
            from_address = self.get_email_from(original_message)

            # Prepare forward subject
            if not subject.startswith("Fwd:"):
                subject = f"Fwd: {subject}"

            # Add note if provided
            if note:
                body = f"{note}\n\n--- Forwarded message ---\n{body}"
            else:
                body = f"--- Forwarded message ---\n{body}"

            result = self.send_email(to, subject, body)
            logger.info(f"Email forwarded to {to}")
            return result
        except Exception as e:
            logger.error(f"Error forwarding email: {e}")
            return None

    def mark_as_read(self, message_id):
        """Mark an email as read."""
        try:
            self.service.users().messages().modify(
                userId="me", id=message_id, body={"removeLabelIds": ["UNREAD"]}
            ).execute()
            logger.info(f"Email {message_id} marked as read")
            return True
        except HttpError as error:
            logger.error(f"Error marking email as read: {error}")
            return False

    def archive_email(self, message_id):
        """Archive an email."""
        try:
            self.service.users().messages().modify(
                userId="me", id=message_id, body={"removeLabelIds": ["INBOX"]}
            ).execute()
            logger.info(f"Email {message_id} archived")
            return True
        except HttpError as error:
            logger.error(f"Error archiving email: {error}")
            return False

    def delete_email(self, message_id):
        """Delete an email."""
        try:
            self.service.users().messages().delete(
                userId="me", id=message_id
            ).execute()
            logger.info(f"Email {message_id} deleted")
            return True
        except HttpError as error:
            logger.error(f"Error deleting email: {error}")
            return False

    def label_email(self, message_id, label_name):
        """Add a label to an email."""
        try:
            # Get all labels
            results = self.service.users().labels().list(userId="me").execute()
            labels = results.get("labels", [])

            # Find label by name
            label_id = None
            for label in labels:
                if label["name"] == label_name:
                    label_id = label["id"]
                    break

            # Create label if it doesn't exist
            if not label_id:
                label_body = {
                    "name": label_name,
                    "labelListVisibility": "labelShow",
                    "messageListVisibility": "show",
                }
                label = self.service.users().labels().create(
                    userId="me", body=label_body
                ).execute()
                label_id = label["id"]

            # Apply label to message
            self.service.users().messages().modify(
                userId="me", id=message_id, body={"addLabelIds": [label_id]}
            ).execute()
            logger.info(f"Label '{label_name}' added to email {message_id}")
            return True
        except HttpError as error:
            logger.error(f"Error labeling email: {error}")
            return False
