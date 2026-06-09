import logging
import re
from enum import Enum

logger = logging.getLogger(__name__)


class EmailCategory(Enum):
    LEGITIMATE = "legitimate"
    MARKETING = "marketing"
    SPAM = "spam"
    PROMOTIONAL = "promotional"


class SpamDetector:
    """Detects spam, marketing, and promotional emails."""

    # Common spam indicators
    SPAM_KEYWORDS = [
        "click here",
        "verify account",
        "confirm identity",
        "update payment",
        "act now",
        "urgent action required",
        "limited time",
        "don't miss out",
        "prize",
        "winner",
        "congratulations",
        "claim reward",
        "free money",
        "nigerian prince",
        "inheritance",
        "bitcoin",
        "crypto",
        "forex",
        "unsubscribe",
        "click below",
        "must act",
        "expires today",
        "virus",
        "malware",
    ]\n\n    # Marketing/promotional keywords
    MARKETING_KEYWORDS = [\n        \"sale\",\n        \"discount\",\n        \"offer\",\n        \"deal\",\n        \"save now\",\n        \"limited offer\",\n        \"exclusive\",\n        \"special offer\",\n        \"new product\",\n        \"summer sale\",\n        \"clearance\",\n        \"free shipping\",\n        \"coupon\",\n        \"code\",\n        \"newsletter\",\n        \"marketing\",\n        \"promotional\",\n        \"shop now\",\n        \"buy now\",\n        \"order now\",\n        \"subscribe\",\n        \"seasonal\",\n        \"promotion\",\n        \"campaign\",\n    ]\n\n    # Common spam sender patterns\n    SPAM_SENDER_PATTERNS = [\n        r\"noreply@\",\n        r\"no-reply@\",\n        r\"donotreply@\",\n        r\"notification@\",\n        r\"alert@\",\n        r\"promo@\",\n        r\"marketing@\",\n        r\"sales@\",\n        r\"campaign@\",\n        r\"newsletter@\",\n    ]\n\n    # Marketing sender patterns\n    MARKETING_SENDER_PATTERNS = [\n        r\"marketing@\",\n        r\"promotions@\",\n        r\"sales@\",\n        r\"offers@\",\n        r\"deals@\",\n        r\"newsletter@\",\n        r\"noreply@\",\n    ]\n\n    # Phrases that indicate unsubscribe links (typical of marketing)\n    UNSUBSCRIBE_PATTERNS = [\n        r\"unsubscribe\",\n        r\"manage preferences\",\n        r\"manage your subscription\",\n        r\"opt out\",\n        r\"stop receiving\",\n    ]\n\n    # Suspicious patterns (phishing, scams)\n    SUSPICIOUS_PATTERNS = [\n        r\"verify\\s+(your|account|password|credentials)\",\n        r\"confirm\\s+(your|account|password|payment)\",\n        r\"update\\s+(your|account|payment|billing)\",\n        r\"re-enter\\s+(your|password|credentials)\",\n        r\"click\\s+here.{0,50}(urgent|immediately|now)\",\n        r\"suspicious\\s+activity\",\n        r\"unauthorized\\s+access\",\n    ]\n\n    @classmethod\n    def classify(cls, subject: str, body: str, from_address: str) -> EmailCategory:\n        \"\"\"Classify email as spam, marketing, or legitimate.\"\"\"\n        combined_text = f\"{subject} {body}\".lower()\n        from_lower = from_address.lower()\n\n        # Check for suspicious/phishing patterns (highest priority)\n        for pattern in cls.SUSPICIOUS_PATTERNS:\n            if re.search(pattern, combined_text, re.IGNORECASE):\n                logger.warning(f\"Suspicious pattern detected: {pattern}\")\n                return EmailCategory.SPAM\n\n        # Check for spam keywords\n        spam_count = sum(\n            1 for keyword in cls.SPAM_KEYWORDS if keyword in combined_text\n        )\n        if spam_count >= 2:\n            return EmailCategory.SPAM\n\n        # Check for unsubscribe patterns (indicates marketing)\n        has_unsubscribe = any(\n            re.search(pattern, combined_text, re.IGNORECASE)\n            for pattern in cls.UNSUBSCRIBE_PATTERNS\n        )\n\n        # Check for marketing keywords\n        marketing_count = sum(\n            1 for keyword in cls.MARKETING_KEYWORDS if keyword in combined_text\n        )\n\n        # Check sender patterns\n        is_spam_sender = any(\n            re.search(pattern, from_lower) for pattern in cls.SPAM_SENDER_PATTERNS\n        )\n        is_marketing_sender = any(\n            re.search(pattern, from_lower) for pattern in cls.MARKETING_SENDER_PATTERNS\n        )\n\n        # Determine category\n        if is_spam_sender and spam_count > 0:\n            return EmailCategory.SPAM\n\n        if marketing_count >= 3 or (has_unsubscribe and marketing_count >= 1):\n            return EmailCategory.MARKETING\n\n        if is_marketing_sender and (marketing_count >= 1 or has_unsubscribe):\n            return EmailCategory.MARKETING\n\n        if marketing_count >= 1 and (is_marketing_sender or has_unsubscribe):\n            return EmailCategory.MARKETING\n\n        # Check for promotional nature\n        if (\"promo\" in combined_text or \"promotional\" in combined_text) and marketing_count >= 1:\n            return EmailCategory.PROMOTIONAL\n\n        # Check if it's a newsletter\n        if (\n            \"newsletter\" in combined_text\n            or \"monthly digest\" in combined_text\n            or \"weekly update\" in combined_text\n        ):\n            if has_unsubscribe or is_marketing_sender:\n                return EmailCategory.MARKETING\n            return EmailCategory.PROMOTIONAL\n\n        return EmailCategory.LEGITIMATE\n\n    @classmethod\n    def get_spam_score(cls, subject: str, body: str, from_address: str) -> float:\n        \"\"\"Calculate spam likelihood score (0.0 to 1.0).\"\"\"\n        combined_text = f\"{subject} {body}\".lower()\n        from_lower = from_address.lower()\n        score = 0.0\n\n        # Check suspicious patterns\n        suspicious_count = sum(\n            1\n            for pattern in cls.SUSPICIOUS_PATTERNS\n            if re.search(pattern, combined_text, re.IGNORECASE)\n        )\n        score += suspicious_count * 0.15\n\n        # Check spam keywords\n        spam_count = sum(\n            1 for keyword in cls.SPAM_KEYWORDS if keyword in combined_text\n        )\n        score += spam_count * 0.1\n\n        # Check sender patterns\n        if any(\n            re.search(pattern, from_lower) for pattern in cls.SPAM_SENDER_PATTERNS\n        ):\n            score += 0.2\n\n        # Multiple links often indicate spam\n        link_count = len(re.findall(r\"http[s]?://\", combined_text))\n        if link_count > 5:\n            score += 0.15\n\n        # ALL CAPS text\n        caps_ratio = sum(1 for c in combined_text if c.isupper()) / max(\n            len(combined_text), 1\n        )\n        if caps_ratio > 0.3:\n            score += 0.1\n\n        # Excessive punctuation\n        punct_count = sum(\n            1 for c in combined_text if c in \"!?!?!?!?\"\n        ) / max(len(combined_text), 1)\n        if punct_count > 0.05:\n            score += 0.1\n\n        return min(score, 1.0)\n\n    @classmethod\n    def is_likely_spam(cls, subject: str, body: str, from_address: str) -> bool:\n        \"\"\"Check if email is likely spam (score > 0.6).\"\"\"\n        return cls.get_spam_score(subject, body, from_address) > 0.6\n\n    @classmethod\n    def is_marketing(cls, subject: str, body: str, from_address: str) -> bool:\n        \"\"\"Check if email is marketing/promotional.\"\"\"\n        category = cls.classify(subject, body, from_address)\n        return category in [EmailCategory.MARKETING, EmailCategory.PROMOTIONAL]\n