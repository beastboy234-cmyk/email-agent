import json
import logging
from typing import Optional
from gmail_client import GmailClient
from memory import ActionLogger
from safety import EmailSafetyClassifier, RiskLevel
from spam_detector import SpamDetector, EmailCategory
from config import EMAIL_SEND_MODE, DEFAULT_USER_NAME, DEFAULT_SIGNATURE

logger = logging.getLogger(__name__)


class EmailTools:
    """Gmail tools for the AI agent."""

    def __init__(self, gmail_client: GmailClient):
        self.gmail = gmail_client

    def search_emails(self, query: str, max_results: int = 10) -> str:
        """Search for emails in Gmail.

        Args:
            query: Search query (can be natural language, will be converted to Gmail query)
            max_results: Maximum number of results to return

        Returns:
            JSON string with search results
        """
        try:
            messages = self.gmail.search_emails(query, max_results)
            results = []

            for msg in messages:
                message = self.gmail.read_email(msg["id"])
                if message:
                    results.append(
                        {
                            "id": msg["id"],
                            "thread_id": message["threadId"],
                            "subject": self.gmail.get_email_subject(message),
                            "from": self.gmail.get_email_from(message),
                            "snippet": message["snippet"],
                        }
                    )

            ActionLogger.log_action(
                "search_emails", {"query": query, "results_count": len(results)}
            )
            return json.dumps({"status": "success", "results": results})
        except Exception as e:
            logger.error(f"Error in search_emails: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def read_email(self, message_id: str) -> str:
        """Read the full content of an email.

        Args:
            message_id: The ID of the message to read

        Returns:
            JSON string with email content
        """
        try:
            message = self.gmail.read_email(message_id)
            if not message:
                return json.dumps({"status": "error", "message": "Email not found"})

            subject = self.gmail.get_email_subject(message)
            from_addr = self.gmail.get_email_from(message)
            body = self.gmail.get_email_body(message)

            # Detect spam/marketing
            category = SpamDetector.classify(subject, body, from_addr)
            spam_score = SpamDetector.get_spam_score(subject, body, from_addr)

            result = {
                "id": message_id,
                "subject": subject,
                "from": from_addr,
                "to": self.gmail.get_email_to(message),
                "body": body,
                "thread_id": message["threadId"],
                "category": category.value,
                "spam_score": round(spam_score, 2),
                "is_spam": SpamDetector.is_likely_spam(subject, body, from_addr),
                "is_marketing": SpamDetector.is_marketing(subject, body, from_addr),
            }

            ActionLogger.log_action(
                "read_email",
                {
                    "message_id": message_id,
                    "subject": result["subject"],
                    "category": category.value,
                },
            )
            return json.dumps({"status": "success", "email": result})
        except Exception as e:
            logger.error(f"Error in read_email: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def read_thread(self, thread_id: str) -> str:
        """Read all emails in a thread.

        Args:
            thread_id: The ID of the thread to read

        Returns:
            JSON string with all emails in the thread
        """
        try:
            messages = self.gmail.get_thread_messages(thread_id)
            results = []

            for msg in messages:
                subject = self.gmail.get_email_subject(msg)
                from_addr = self.gmail.get_email_from(msg)
                body = self.gmail.get_email_body(msg)

                result = {
                    "id": msg["id"],
                    "subject": subject,
                    "from": from_addr,
                    "body": body,
                    "category": SpamDetector.classify(subject, body, from_addr).value,
                }
                results.append(result)

            ActionLogger.log_action(
                "read_thread", {"thread_id": thread_id, "message_count": len(results)}
            )
            return json.dumps({"status": "success", "messages": results})
        except Exception as e:
            logger.error(f"Error in read_thread: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def detect_spam_emails(self, query: str = "", max_results: int = 20) -> str:
        """Detect and list spam and marketing emails.

        Args:
            query: Search query (optional, defaults to recent emails)
            max_results: Maximum number of emails to check

        Returns:
            JSON string with spam detection results
        """
        try:
            if not query:
                query = "in:inbox"

            messages = self.gmail.search_emails(query, max_results)
            spam_emails = []
            marketing_emails = []
            legitimate_emails = []

            for msg in messages:
                message = self.gmail.read_email(msg["id"])
                if message:
                    subject = self.gmail.get_email_subject(message)
                    from_addr = self.gmail.get_email_from(message)
                    body = self.gmail.get_email_body(message)

                    category = SpamDetector.classify(subject, body, from_addr)
                    spam_score = SpamDetector.get_spam_score(subject, body, from_addr)

                    email_info = {
                        "id": msg["id"],
                        "subject": subject,
                        "from": from_addr,
                        "snippet": message["snippet"],
                        "category": category.value,
                        "spam_score": round(spam_score, 2),
                    }

                    if category == EmailCategory.SPAM:
                        spam_emails.append(email_info)
                    elif category in [EmailCategory.MARKETING, EmailCategory.PROMOTIONAL]:
                        marketing_emails.append(email_info)
                    else:
                        legitimate_emails.append(email_info)

            ActionLogger.log_action(
                "detect_spam_emails",
                {
                    "query": query,
                    "spam_count": len(spam_emails),
                    "marketing_count": len(marketing_emails),
                    "legitimate_count": len(legitimate_emails),
                },
            )

            return json.dumps(
                {
                    "status": "success",
                    "spam_emails": spam_emails,
                    "marketing_emails": marketing_emails,
                    "legitimate_emails": legitimate_emails,
                    "summary": {
                        "total_spam": len(spam_emails),
                        "total_marketing": len(marketing_emails),
                        "total_legitimate": len(legitimate_emails),
                    },
                }
            )
        except Exception as e:
            logger.error(f"Error in detect_spam_emails: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def delete_spam_emails(self, query: str = "") -> str:
        """Delete spam emails matching query.

        Args:
            query: Search query to find spam emails

        Returns:
            JSON string with deletion results
        """
        try:
            if not query:
                query = "in:inbox"

            messages = self.gmail.search_emails(query, max_results=50)
            deleted_count = 0
            failed_count = 0
            deleted_emails = []

            for msg in messages:
                message = self.gmail.read_email(msg["id"])
                if message:
                    subject = self.gmail.get_email_subject(message)
                    from_addr = self.gmail.get_email_from(message)
                    body = self.gmail.get_email_body(message)

                    # Check if email is spam
                    if SpamDetector.is_likely_spam(subject, body, from_addr):
                        success = self.gmail.delete_email(msg["id"])
                        if success:
                            deleted_count += 1
                            deleted_emails.append(
                                {"id": msg["id"], "subject": subject, "from": from_addr}
                            )
                        else:
                            failed_count += 1

            ActionLogger.log_action(
                "delete_spam_emails",
                {"query": query, "deleted_count": deleted_count, "failed_count": failed_count},
            )

            return json.dumps(
                {
                    "status": "success",
                    "deleted_count": deleted_count,
                    "failed_count": failed_count,
                    "deleted_emails": deleted_emails,
                    "message": f"Deleted {deleted_count} spam emails",
                }
            )
        except Exception as e:
            logger.error(f"Error in delete_spam_emails: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def delete_marketing_emails(self, query: str = "", auto_delete: bool = False) -> str:
        """Delete or archive marketing emails.

        Args:
            query: Search query to find marketing emails
            auto_delete: If False, archives instead of deleting

        Returns:
            JSON string with results
        """
        try:
            if not query:
                query = "in:inbox"

            messages = self.gmail.search_emails(query, max_results=50)
            processed_count = 0
            failed_count = 0
            processed_emails = []

            for msg in messages:
                message = self.gmail.read_email(msg["id"])
                if message:
                    subject = self.gmail.get_email_subject(message)
                    from_addr = self.gmail.get_email_from(message)
                    body = self.gmail.get_email_body(message)

                    # Check if email is marketing
                    if SpamDetector.is_marketing(subject, body, from_addr):
                        if auto_delete:
                            success = self.gmail.delete_email(msg["id"])
                        else:
                            success = self.gmail.archive_email(msg["id"])

                        if success:
                            processed_count += 1
                            processed_emails.append(
                                {"id": msg["id"], "subject": subject, "from": from_addr}
                            )
                        else:
                            failed_count += 1

            action_type = "delete" if auto_delete else "archive"
            ActionLogger.log_action(
                f"{action_type}_marketing_emails",
                {
                    "query": query,
                    "processed_count": processed_count,
                    "failed_count": failed_count,
                },
            )

            return json.dumps(
                {
                    "status": "success",
                    "processed_count": processed_count,
                    "failed_count": failed_count,
                    "processed_emails": processed_emails,
                    "message": f"{'Deleted' if auto_delete else 'Archived'} {processed_count} marketing emails",
                }
            )
        except Exception as e:
            logger.error(f"Error in delete_marketing_emails: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def send_email(
        self, to: str, subject: str, body: str, cc: Optional[str] = None, bcc: Optional[str] = None
    ) -> str:
        """Send an email.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            cc: CC recipients (optional)
            bcc: BCC recipients (optional)

        Returns:
            JSON string with send status
        """
        try:
            # Check if content is safe
            if not EmailSafetyClassifier.validate_sensitive_content(body):
                return json.dumps(
                    {
                        "status": "blocked",
                        "message": "Email contains sensitive information. Please remove it before sending.",
                    }
                )

            # Classify risk level
            risk_level = EmailSafetyClassifier.classify(subject, body, to)

            # Check if confirmation is needed
            if EmailSafetyClassifier.should_require_confirmation(risk_level, EMAIL_SEND_MODE):
                return json.dumps(
                    {
                        "status": "confirmation_required",
                        "risk_level": risk_level.value,
                        "email_preview": {
                            "to": to,
                            "subject": subject,
                            "body": body,
                            "cc": cc,
                            "bcc": bcc,
                        },
                        "message": f"This email is classified as {risk_level.value}-risk. Please review and confirm sending.",
                    }
                )

            # Send the email
            result = self.gmail.send_email(to, subject, body, cc, bcc)
            if result:
                ActionLogger.log_action(
                    "send_email",
                    {"to": to, "subject": subject, "risk_level": risk_level.value},
                )
                return json.dumps(
                    {
                        "status": "success",
                        "message": f"Email sent to {to}",
                        "risk_level": risk_level.value,
                    }
                )
            else:
                return json.dumps({"status": "error", "message": "Failed to send email"})
        except Exception as e:
            logger.error(f"Error in send_email: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def reply_to_email(self, message_id: str, body: str) -> str:
        """Reply to an email.

        Args:
            message_id: The ID of the email to reply to
            body: Reply body text

        Returns:
            JSON string with reply status
        """
        try:
            # Get original email details for safety check
            original = self.gmail.read_email(message_id)
            if not original:
                return json.dumps({"status": "error", "message": "Original email not found"})

            subject = self.gmail.get_email_subject(original)
            to = self.gmail.get_email_from(original)

            # Check if content is safe
            if not EmailSafetyClassifier.validate_sensitive_content(body):
                return json.dumps(
                    {
                        "status": "blocked",
                        "message": "Reply contains sensitive information. Please remove it before sending.",
                    }
                )

            # Classify risk level
            risk_level = EmailSafetyClassifier.classify(subject, body, to)

            # Check if confirmation is needed
            if EmailSafetyClassifier.should_require_confirmation(risk_level, EMAIL_SEND_MODE):
                return json.dumps(
                    {
                        "status": "confirmation_required",
                        "risk_level": risk_level.value,
                        "email_preview": {"to": to, "subject": f"Re: {subject}", "body": body},
                        "message": f"This reply is classified as {risk_level.value}-risk. Please review and confirm sending.",
                    }
                )

            # Send the reply
            result = self.gmail.reply_to_email(message_id, body)
            if result:
                ActionLogger.log_action(
                    "reply_to_email",
                    {"message_id": message_id, "to": to, "risk_level": risk_level.value},
                )
                return json.dumps(
                    {
                        "status": "success",
                        "message": f"Reply sent to {to}",
                        "risk_level": risk_level.value,
                    }
                )
            else:
                return json.dumps({"status": "error", "message": "Failed to send reply"})
        except Exception as e:
            logger.error(f"Error in reply_to_email: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def forward_email(
        self, message_id: str, to: str, note: Optional[str] = None
    ) -> str:
        """Forward an email.

        Args:
            message_id: The ID of the email to forward
            to: Recipient email address
            note: Optional note to include (optional)

        Returns:
            JSON string with forward status
        """
        try:
            result = self.gmail.forward_email(message_id, to, note)
            if result:
                ActionLogger.log_action(
                    "forward_email",
                    {"message_id": message_id, "to": to, "has_note": note is not None},
                )
                return json.dumps(
                    {"status": "success", "message": f"Email forwarded to {to}"}
                )
            else:
                return json.dumps({"status": "error", "message": "Failed to forward email"})
        except Exception as e:
            logger.error(f"Error in forward_email: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def create_draft(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
    ) -> str:
        """Create a draft email.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            cc: CC recipients (optional)
            bcc: BCC recipients (optional)

        Returns:
            JSON string with draft creation status
        """
        try:
            result = self.gmail.create_draft(to, subject, body, cc, bcc)
            if result:
                ActionLogger.log_action(
                    "create_draft", {"to": to, "subject": subject}
                )
                return json.dumps(
                    {
                        "status": "success",
                        "message": f"Draft created for {to}",
                        "draft_id": result["id"],
                    }
                )
            else:
                return json.dumps({"status": "error", "message": "Failed to create draft"})
        except Exception as e:
            logger.error(f"Error in create_draft: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def create_draft_reply(self, message_id: str, body: str) -> str:
        """Create a draft reply to an email.

        Args:
            message_id: The ID of the email to reply to
            body: Reply body text

        Returns:
            JSON string with draft creation status
        """
        try:
            result = self.gmail.create_draft_reply(message_id, body)
            if result:
                ActionLogger.log_action(
                    "create_draft_reply",
                    {"message_id": message_id, "body_length": len(body)},
                )
                return json.dumps(
                    {
                        "status": "success",
                        "message": "Draft reply created",
                        "draft_id": result["id"],
                    }
                )
            else:
                return json.dumps(
                    {"status": "error", "message": "Failed to create draft reply"}
                )
        except Exception as e:
            logger.error(f"Error in create_draft_reply: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def mark_as_read(self, message_id: str) -> str:
        """Mark an email as read.

        Args:
            message_id: The ID of the email to mark as read

        Returns:
            JSON string with operation status
        """
        try:
            success = self.gmail.mark_as_read(message_id)
            if success:
                ActionLogger.log_action("mark_as_read", {"message_id": message_id})
                return json.dumps(
                    {"status": "success", "message": "Email marked as read"}
                )
            else:
                return json.dumps(
                    {"status": "error", "message": "Failed to mark as read"}
                )
        except Exception as e:
            logger.error(f"Error in mark_as_read: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def archive_email(self, message_id: str) -> str:
        """Archive an email.

        Args:
            message_id: The ID of the email to archive

        Returns:
            JSON string with operation status
        """
        try:
            success = self.gmail.archive_email(message_id)
            if success:
                ActionLogger.log_action("archive_email", {"message_id": message_id})
                return json.dumps(
                    {"status": "success", "message": "Email archived"}
                )
            else:
                return json.dumps(
                    {"status": "error", "message": "Failed to archive email"}
                )
        except Exception as e:
            logger.error(f"Error in archive_email: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def delete_email(self, message_id: str) -> str:
        """Delete an email.

        Args:
            message_id: The ID of the email to delete

        Returns:
            JSON string with operation status
        """
        try:
            success = self.gmail.delete_email(message_id)
            if success:
                ActionLogger.log_action("delete_email", {"message_id": message_id})
                return json.dumps(
                    {"status": "success", "message": "Email deleted"}
                )
            else:
                return json.dumps(
                    {"status": "error", "message": "Failed to delete email"}
                )
        except Exception as e:
            logger.error(f"Error in delete_email: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def label_email(self, message_id: str, label: str) -> str:
        """Add a label to an email.

        Args:
            message_id: The ID of the email to label
            label: The label name to add

        Returns:
            JSON string with operation status
        """
        try:
            success = self.gmail.label_email(message_id, label)
            if success:
                ActionLogger.log_action(
                    "label_email", {"message_id": message_id, "label": label}
                )
                return json.dumps(
                    {"status": "success", "message": f"Label '{label}' added to email"}
                )
            else:
                return json.dumps(
                    {"status": "error", "message": "Failed to label email"}
                )
        except Exception as e:
            logger.error(f"Error in label_email: {e}")
            return json.dumps({"status": "error", "message": str(e)})
