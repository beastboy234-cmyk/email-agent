import json
import logging
from typing import Any
from openai import OpenAI
from gmail_client import GmailClient
from tools import EmailTools
from config import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)


class EmailAgent:
    """AI agent for managing Gmail."""

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.gmail_client = GmailClient()
        self.email_tools = EmailTools(self.gmail_client)
        self.model = OPENAI_MODEL
        self.conversation_history = []

    def get_tool_definitions(self):
        """Get the definitions of available tools for the agent."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_emails",
                    "description": "Search for emails in Gmail using a query",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (e.g., 'from:john subject:meeting')",
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of results to return",
                                "default": 10,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "read_email",
                    "description": "Read the full content of an email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "The ID of the message to read",
                            },
                        },
                        "required": ["message_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "read_thread",
                    "description": "Read all emails in a conversation thread",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "thread_id": {
                                "type": "string",
                                "description": "The ID of the thread to read",
                            },
                        },
                        "required": ["thread_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "send_email",
                    "description": "Send an email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "to": {"type": "string", "description": "Recipient email address"},
                            "subject": {"type": "string", "description": "Email subject"},
                            "body": {"type": "string", "description": "Email body"},
                            "cc": {
                                "type": "string",
                                "description": "CC recipients (optional)",
                            },
                            "bcc": {
                                "type": "string",
                                "description": "BCC recipients (optional)",
                            },
                        },
                        "required": ["to", "subject", "body"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "reply_to_email",
                    "description": "Reply to an email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "The ID of the email to reply to",
                            },
                            "body": {"type": "string", "description": "Reply body text"},
                        },
                        "required": ["message_id", "body"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "forward_email",
                    "description": "Forward an email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "The ID of the email to forward",
                            },
                            "to": {"type": "string", "description": "Recipient email address"},
                            "note": {
                                "type": "string",
                                "description": "Optional note to include (optional)",
                            },
                        },
                        "required": ["message_id", "to"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "create_draft",
                    "description": "Create a draft email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "to": {"type": "string", "description": "Recipient email address"},
                            "subject": {"type": "string", "description": "Email subject"},
                            "body": {"type": "string", "description": "Email body"},
                            "cc": {
                                "type": "string",
                                "description": "CC recipients (optional)",
                            },
                            "bcc": {
                                "type": "string",
                                "description": "BCC recipients (optional)",
                            },
                        },
                        "required": ["to", "subject", "body"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "create_draft_reply",
                    "description": "Create a draft reply to an email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "The ID of the email to reply to",
                            },
                            "body": {"type": "string", "description": "Reply body text"},
                        },
                        "required": ["message_id", "body"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "mark_as_read",
                    "description": "Mark an email as read",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "The ID of the email to mark as read",
                            },
                        },
                        "required": ["message_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "archive_email",
                    "description": "Archive an email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "The ID of the email to archive",
                            },
                        },
                        "required": ["message_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_email",
                    "description": "Delete an email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "The ID of the email to delete",
                            },
                        },
                        "required": ["message_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "label_email",
                    "description": "Add a label to an email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "The ID of the email to label",
                            },
                            "label": {
                                "type": "string",
                                "description": "The label name to add",
                            },
                        },
                        "required": ["message_id", "label"],
                    },
                },
            },
        ]

    def execute_tool(self, tool_name: str, tool_input: dict) -> str:
        """Execute a tool based on its name and input."""
        if tool_name == "search_emails":
            return self.email_tools.search_emails(
                tool_input.get("query"), tool_input.get("max_results", 10)
            )
        elif tool_name == "read_email":
            return self.email_tools.read_email(tool_input.get("message_id"))
        elif tool_name == "read_thread":
            return self.email_tools.read_thread(tool_input.get("thread_id"))
        elif tool_name == "send_email":
            return self.email_tools.send_email(
                tool_input.get("to"),
                tool_input.get("subject"),
                tool_input.get("body"),
                tool_input.get("cc"),
                tool_input.get("bcc"),
            )
        elif tool_name == "reply_to_email":
            return self.email_tools.reply_to_email(
                tool_input.get("message_id"), tool_input.get("body")
            )
        elif tool_name == "forward_email":
            return self.email_tools.forward_email(
                tool_input.get("message_id"),
                tool_input.get("to"),
                tool_input.get("note"),
            )
        elif tool_name == "create_draft":
            return self.email_tools.create_draft(
                tool_input.get("to"),
                tool_input.get("subject"),
                tool_input.get("body"),
                tool_input.get("cc"),
                tool_input.get("bcc"),
            )
        elif tool_name == "create_draft_reply":
            return self.email_tools.create_draft_reply(
                tool_input.get("message_id"), tool_input.get("body")
            )
        elif tool_name == "mark_as_read":
            return self.email_tools.mark_as_read(tool_input.get("message_id"))
        elif tool_name == "archive_email":
            return self.email_tools.archive_email(tool_input.get("message_id"))
        elif tool_name == "delete_email":
            return self.email_tools.delete_email(tool_input.get("message_id"))
        elif tool_name == "label_email":
            return self.email_tools.label_email(
                tool_input.get("message_id"), tool_input.get("label")
            )
        else:
            return json.dumps(
                {"status": "error", "message": f"Unknown tool: {tool_name}"}
            )

    def run(self, user_message: str) -> tuple[str, bool]:
        """Run the agent with a user message.

        Returns:
            Tuple of (response_text, requires_confirmation)
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})

        # System message for the agent
        system_message = """You are a helpful Gmail AI agent. You help users manage their emails by:
- Searching and finding emails
- Reading and summarizing emails
- Composing and sending emails
- Replying to emails
- Organizing emails with labels and archives

When the user asks you to send or reply to an email, be professional, clear, and write in their voice.
If you need to send an email, use the send_email or reply_to_email tools.
If the tool returns a confirmation_required status, inform the user that the email requires confirmation before sending.

Always be helpful and try to complete the user's request."""

        # Make initial API call
        messages = [{"role": "system", "content": system_message}] + self.conversation_history

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.get_tool_definitions(),
            tool_choice="auto",
        )

        # Process response
        requires_confirmation = False
        final_response = ""

        while response.choices[0].finish_reason == "tool_calls":
            tool_calls = response.choices[0].message.tool_calls
            assistant_message = response.choices[0].message

            # Add assistant message to history
            self.conversation_history.append({"role": "assistant", "content": assistant_message.content or "", "tool_calls": [
                {"id": tc.id, "type": tc.type, "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in tool_calls
            ]})

            # Execute tools
            tool_results = []
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_input = json.loads(tool_call.function.arguments)
                tool_result = self.execute_tool(tool_name, tool_input)

                # Check if confirmation is required
                result_json = json.loads(tool_result)
                if result_json.get("status") == "confirmation_required":
                    requires_confirmation = True
                    final_response = json.dumps(result_json, indent=2)
                    return final_response, requires_confirmation

                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": tool_result,
                    }
                )

            # Add tool results to history
            self.conversation_history.append({"role": "user", "content": tool_results})

            # Continue conversation
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages + [{"role": "assistant", "content": assistant_message.content or "", "tool_calls": [
                    {"id": tc.id, "type": tc.type, "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                    for tc in tool_calls
                ]} for assistant_message in [response.choices[0].message]] + [{"role": "user", "content": tool_results}],
                tools=self.get_tool_definitions(),
                tool_choice="auto",
            )

        # Extract final response
        final_response = response.choices[0].message.content or "No response"

        # Add assistant response to history
        self.conversation_history.append({"role": "assistant", "content": final_response})

        return final_response, requires_confirmation
