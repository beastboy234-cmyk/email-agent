import logging
from enum import Enum

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EmailSafetyClassifier:
    """Classifies emails by risk level for sending."""

    # Low-risk keywords
    LOW_RISK_KEYWORDS = [
        "thank",
        "thanks",
        "schedule",
        "confirm",
        "follow up",
        "availability",
        "appreciate",
        "gratitude",
    ]

    # Medium-risk keywords
    MEDIUM_RISK_KEYWORDS = [
        "proposal",
        "price",
        "cost",
        "quote",
        "conflict",
        "concern",
        "issue",
        "problem",
        "attachment",
        "commitment",
        "deadline",
    ]

    # High-risk keywords
    HIGH_RISK_KEYWORDS = [
        "payment",
        "financial",
        "legal",
        "medical",
        "health",
        "password",
        "ssn",
        "tax",
        "bank",
        "credit",
        "disciplinary",
        "complaint",
        "sensitive",
        "confidential",
        "secret",
    ]

    # Forbidden content that should never be sent
    FORBIDDEN_PATTERNS = [
        "i hate",
        "you suck",
        "threat",
        "blackmail",
        "extortion",
        "fraudulent",
        "illegal",
        "harass",
        "discriminate",
        "slur",
    ]

    @classmethod
    def classify(cls, subject, body, to):
        """Classify email by risk level."""
        combined_text = f"{subject} {body}".lower()

        # Check for forbidden content
        for pattern in cls.FORBIDDEN_PATTERNS:
            if pattern in combined_text:
                logger.warning(f"Forbidden content detected: {pattern}")
                return RiskLevel.HIGH

        # Check for sensitive indicators
        high_risk_count = sum(
            1
            for keyword in cls.HIGH_RISK_KEYWORDS
            if keyword in combined_text
        )
        if high_risk_count >= 2:
            return RiskLevel.HIGH

        medium_risk_count = sum(
            1
            for keyword in cls.MEDIUM_RISK_KEYWORDS
            if keyword in combined_text
        )
        if medium_risk_count >= 3:
            return RiskLevel.MEDIUM

        low_risk_count = sum(
            1 for keyword in cls.LOW_RISK_KEYWORDS if keyword in combined_text
        )
        if low_risk_count >= 2:
            return RiskLevel.LOW

        # Default to medium if mixed indicators
        if medium_risk_count > 0:
            return RiskLevel.MEDIUM
        if high_risk_count > 0:
            return RiskLevel.HIGH

        return RiskLevel.LOW

    @classmethod
    def validate_sensitive_content(cls, body):
        """Check if email contains sensitive personal information."""
        sensitive_patterns = [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"\b\d{16}\b",  # Credit card
            r"\bpassword\s*:?\s*\w+\b",  # Password pattern
        ]
        import re

        for pattern in sensitive_patterns:
            if re.search(pattern, body, re.IGNORECASE):
                logger.warning(f"Sensitive content pattern detected: {pattern}")
                return False
        return True

    @classmethod
    def should_require_confirmation(cls, risk_level, send_mode):
        """Determine if confirmation is needed before sending."""
        if send_mode == "draft_only":
            return True

        if send_mode == "confirm_before_send":
            return risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH]

        if send_mode == "auto_send_allowed":
            return risk_level == RiskLevel.HIGH

        return True
