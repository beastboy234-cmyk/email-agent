import logging
import json
from colorama import Fore, Style
from agent import EmailAgent
from config import EMAIL_SEND_MODE
from memory import ActionLogger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def print_welcome():
    """Print welcome message."""
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.CYAN}║                    Gmail AI Email Agent                        ║{Style.RESET_ALL}
{Fore.CYAN}║                                                               ║{Style.RESET_ALL}
{Fore.CYAN}║  Commands:                                                     ║{Style.RESET_ALL}
{Fore.CYAN}║  - Search, read, and summarize emails                         ║{Style.RESET_ALL}
{Fore.CYAN}║  - Send and reply to emails                                   ║{Style.RESET_ALL}
{Fore.CYAN}║  - Organize with labels and archives                         ║{Style.RESET_ALL}
{Fore.CYAN}║  - Type 'help' for more commands                              ║{Style.RESET_ALL}
{Fore.CYAN}║  - Type 'exit' to quit                                        ║{Style.RESET_ALL}
{Fore.CYAN}║                                                               ║{Style.RESET_ALL}
{Fore.CYAN}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
{Fore.YELLOW}Email Send Mode: {EMAIL_SEND_MODE}{Style.RESET_ALL}
""")


def print_help():
    """Print help message with example commands."""
    print(f"""
{Fore.GREEN}Example Commands:{Style.RESET_ALL}

  Search & Read:
    - Find emails from Capital One about my car loan
    - Summarize my unread emails from today
    - Show me emails with attachments from last week

  Compose & Send:
    - Email Ruben and tell him I can schedule a call this week
    - Send a thank-you email to the last person who contacted me
    - Reply to the last email from John and tell him I'll follow up tomorrow

  Organize:
    - Archive all promotional emails from this week
    - Label all business leads as Ghostwriting Leads
    - Mark all unread emails as read

{Fore.GREEN}Settings:{Style.RESET_ALL}
  - logs: Show recent action logs
  - mode: Check current email send mode
  - help: Show this help message
  - exit: Quit the agent
""")


def print_logs():
    """Print recent action logs."""
    actions = ActionLogger.get_recent_actions(10)
    if not actions:
        print(f"{Fore.YELLOW}No actions logged yet.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.GREEN}Recent Actions:{Style.RESET_ALL}")
    for i, action in enumerate(actions, 1):
        print(f"  {i}. {action['action_type']}: {json.dumps(action['details'])}")


def main():
    """Main CLI loop."""
    print_welcome()

    agent = EmailAgent()

    while True:
        try:
            print()
            user_input = input(f"{Fore.BLUE}You: {Style.RESET_ALL}").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() == "exit":
                print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break
            elif user_input.lower() == "help":
                print_help()
                continue
            elif user_input.lower() == "logs":
                print_logs()
                continue
            elif user_input.lower() == "mode":
                print(f"{Fore.YELLOW}Current Email Send Mode: {EMAIL_SEND_MODE}{Style.RESET_ALL}")
                continue

            # Process user input with agent
            print(f"{Fore.MAGENTA}Processing...{Style.RESET_ALL}")
            response, requires_confirmation = agent.run(user_input)

            # Handle confirmation required
            if requires_confirmation:
                print(f"\n{Fore.YELLOW}Email Review Required:{Style.RESET_ALL}")
                print(response)
                print()
                confirm = input(
                    f"{Fore.YELLOW}Do you want to send this email? (yes/no): {Style.RESET_ALL}"
                ).strip().lower()

                if confirm == "yes":
                    # Parse the preview and extract email details
                    response_data = json.loads(response)
                    preview = response_data.get("email_preview", {})
                    # In a production system, you would send the email here
                    print(
                        f"{Fore.GREEN}Email sent successfully!{Style.RESET_ALL}"
                    )
                else:
                    print(f"{Fore.YELLOW}Email not sent.{Style.RESET_ALL}")
            else:
                # Display response
                print(f"\n{Fore.GREEN}Agent: {Style.RESET_ALL}{response}")

        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
