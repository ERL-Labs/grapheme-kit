"""Core normalization contracts and Unicode normalizer implementation."""

from __future__ import annotations

import unicodedata
from abc import ABC, abstractmethod


class BaseNormalizer(ABC):
    """Abstract base class for all text normalizers.
    
    Subclasses implement script-specific normalization rules or generic
    Unicode standardization algorithms.
    """

    @abstractmethod
    def normalize(self, text: str) -> str:
        """Normalize input string according to the normalizer's rules.

        Args:
            text: Input text to normalize.

        Returns:
            Normalized string.
        """
        raise NotImplementedError


class UnicodeNormalizer(BaseNormalizer):
    """Standard Unicode normalizer.

    Applies standard Unicode normalization forms (NFC, NFD, NFKC, NFKD).
    Defaults to NFC (Canonical Composition).
    """

    def __init__(self, form: str = "NFC") -> None:
        valid_forms = {"NFC", "NFD", "NFKC", "NFKD"}
        if form not in valid_forms:
            raise ValueError(f"Invalid Unicode normalization form: {form}. Must be one of {valid_forms}")
        self.form = form

    def normalize(self, text: str) -> str:
        """Normalize text using the configured Unicode normalization form.

        Args:
            text: Input text to normalize.

        Returns:
            Normalized string, or empty string if input is None or empty.
        """
        if text is None or not text:
            return ""
        return unicodedata.normalize(self.form, text)
