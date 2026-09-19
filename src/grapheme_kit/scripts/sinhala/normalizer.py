"""Sinhala normalizer implementing Unicode NFC and Sinhala confusion set fixups."""

from __future__ import annotations

from grapheme_kit.core.normalizer import UnicodeNormalizer


class SinhalaNormalizer(UnicodeNormalizer):
    """Handles Sinhala-specific normalization and confusion set corrections."""

    CONFUSION_SET: dict[str, str] = {
        "ේා": "ෝ",
        "්ො": "ෝ",
        "්ාෙ": "ෝ",
        "ා්ෙ": "ෝ",
        "ාේ": "ෝ",
        "ේා": "ෝ",
        "ෟෙ": "ෞ",
        "ෙ‌ෙ": "'ෛ'",
        "‌ො": "ො",
        "්ෙ": "ේ",
        "‌ෙ": "ෙ",
    }

    def normalize(self, text: str) -> str:
        """Apply Unicode NFC normalization and Sinhala confusion set replacements."""
        if text is None or not text:
            return ""

        text = super().normalize(text)
        for key, value in self.CONFUSION_SET.items():
            text = text.replace(key, value)

        return text
