"""
PII Detection and Redaction Engine for Review Lens.
Detects and redacts personally identifiable information from review text.
"""

import re
from typing import Dict, Any, List


class PIIEngine:
    """Detects and redacts PII from text using regex patterns."""

    PATTERNS = [
        ("EMAIL", re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')),
        ("PHONE", re.compile(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}')),
        ("CREDIT_CARD", re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b')),
        ("SSN", re.compile(r'\b\d{3}-\d{2}-\d{4}\b')),
        ("AADHAAR", re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b')),
        ("IP_ADDRESS", re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')),
    ]

    REDACTION_MAP = {
        "EMAIL": "[REDACTED_EMAIL]",
        "PHONE": "[REDACTED_PHONE]",
        "CREDIT_CARD": "[REDACTED_CARD]",
        "SSN": "[REDACTED_SSN]",
        "AADHAAR": "[REDACTED_AADHAAR]",
        "IP_ADDRESS": "[REDACTED_IP]",
    }

    @classmethod
    def detect(cls, text: str) -> List[Dict[str, Any]]:
        """Detect PII entities in text."""
        detections = []
        for pii_type, pattern in cls.PATTERNS:
            for match in pattern.finditer(text):
                detections.append({
                    "type": pii_type,
                    "value_masked": cls._mask(match.group(), pii_type),
                    "start": match.start(),
                    "end": match.end(),
                })
        return detections

    @classmethod
    def sanitize(cls, text: str) -> Dict[str, Any]:
        """Sanitize text by redacting all PII."""
        detections = cls.detect(text)
        sanitized = text
        # Process in reverse order to preserve positions
        for det in sorted(detections, key=lambda d: d["start"], reverse=True):
            replacement = cls.REDACTION_MAP.get(det["type"], "[REDACTED]")
            sanitized = sanitized[:det["start"]] + replacement + sanitized[det["end"]:]

        return {
            "original_text": text,
            "sanitized_text": sanitized,
            "pii_detected": len(detections) > 0,
            "redactions": detections,
            "total_redactions": len(detections),
        }

    @classmethod
    def _mask(cls, value: str, pii_type: str) -> str:
        """Create a masked version of the PII value."""
        if pii_type == "EMAIL":
            parts = value.split("@")
            return f"{parts[0][:2]}***@{parts[1]}" if len(parts) == 2 else "***"
        elif pii_type == "PHONE":
            return f"***{value[-4:]}"
        elif pii_type == "CREDIT_CARD":
            return f"****{value[-4:]}"
        else:
            return f"{value[:3]}***"
