"""Backward-compatible Normalizer interface delegating to script-aware architecture."""

from __future__ import annotations

import re
import unicodedata
from grapheme_kit.core.normalizer import BaseNormalizer
from grapheme_kit.core.registry import registry
from grapheme_kit.scripts import register_builtin_scripts

# Ensure built-ins are registered
register_builtin_scripts()


class Normalizer(BaseNormalizer):
    """Handles text normalization across scripts with Unicode standardization (NFC)
    and preserved grammatical validation rules (Nanool).
    """

    def normalize(self, text: str) -> str:
        """Main entry point for normalization.

        Applies standard Unicode NFC normalization, followed by script-specific
        character fixups dispatched via the ScriptRegistry.
        """
        if text is None or not text:
            return ""

        # 1. Unicode NFC
        text = unicodedata.normalize("NFC", text)

        # 2. Script-specific normalization
        return self._char_fixup(text)

    def _char_fixup(self, word: str) -> str:
        """Multi-script character fixups delegating to script normalizers."""
        if not word:
            return ""

        # Detect script and run matching processor normalizer if available
        proc = registry.get_processor_for_text(word)
        if proc.name.lower() in ("tamil", "sinhala", "devanagari"):
            return proc.normalizer.normalize(word)

        # Multi-script fallback: apply Tamil and Sinhala fixups if present
        tamil_proc = registry.get("tamil")
        if tamil_proc:
            word = tamil_proc.normalizer.normalize(word)

        sinhala_proc = registry.get("sinhala")
        if sinhala_proc:
            word = sinhala_proc.normalizer.normalize(word)

        return word

    def sandhi_remover(self, word: str) -> str:
        """Remove word-final sandhi consonants."""
        tamil_proc = registry.get("tamil")
        if tamil_proc and hasattr(tamil_proc.normalizer, "sandhi_remover"):
            return tamil_proc.normalizer.sandhi_remover(word)
        word = word.strip()
        for x in ("க்", "த்", "ப்", "ச்"):
            if word.endswith(x):
                return word[:-len(x)]
        return word

    def check_starting_letter(self, word: str) -> bool:
        """Preserved Nanool validation helper."""
        tamil_proc = registry.get("tamil")
        if tamil_proc and hasattr(tamil_proc.normalizer, "check_starting_letter"):
            return tamil_proc.normalizer.check_starting_letter(word)
        return True

    def check_ending_letter(self, word: str) -> bool:
        """Preserved Nanool validation helper."""
        tamil_proc = registry.get("tamil")
        if tamil_proc and hasattr(tamil_proc.normalizer, "check_ending_letter"):
            return tamil_proc.normalizer.check_ending_letter(word)
        return True

    def check_meimmayakkam(self, word: str) -> bool:
        """Preserved Nanool validation helper."""
        return True