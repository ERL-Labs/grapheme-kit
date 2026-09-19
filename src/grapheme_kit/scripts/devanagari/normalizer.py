"""Devanagari normalizer implementing NFC and nukta standardization."""

from __future__ import annotations

from grapheme_kit.core.normalizer import UnicodeNormalizer


class DevanagariNormalizer(UnicodeNormalizer):
    """Handles Devanagari-specific normalization and nukta canonical composition."""

    NUKTA_MAP: dict[str, str] = {
        "क\u093c": "क़",
        "ख\u093c": "ख़",
        "ग\u093c": "ग़",
        "ज\u093c": "ज़",
        "ड\u093c": "ड़",
        "ढ\u093c": "ढ़",
        "फ\u093c": "फ़",
        "य\u093c": "य़",
        "र\u093c": "ऱ",
        "ळ\u093c": "ऴ",
    }

    def normalize(self, text: str) -> str:
        """Standardize Devanagari text with NFC and canonical nukta compositions."""
        if text is None or not text:
            return ""

        text = super().normalize(text)
        for decomp, comp in self.NUKTA_MAP.items():
            text = text.replace(decomp, comp)

        return text
