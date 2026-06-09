import json
import os
from datetime import datetime
from config import ACTION_LOG_FILE


class ActionLogger:
    """Logs all email actions taken by the agent."""

    @staticmethod
    def log_action(action_type, details):
        """Log an action to the action log file."""
        os.makedirs(os.path.dirname(ACTION_LOG_FILE), exist_ok=True)

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "details": details,
        }

        with open(ACTION_LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    @staticmethod
    def get_recent_actions(limit=10):
        """Get recent actions from the log."""
        if not os.path.exists(ACTION_LOG_FILE):
            return []

        actions = []
        with open(ACTION_LOG_FILE, "r") as f:
            for line in f:
                try:
                    actions.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

        return actions[-limit:]

    @staticmethod
    def clear_log():
        """Clear the action log."""
        if os.path.exists(ACTION_LOG_FILE):
            os.remove(ACTION_LOG_FILE)
