"""Grapheme decomposition for Indic and multi-script text with registry-backed dispatch."""

from __future__ import annotations

import grapheme
from grapheme_kit.core.registry import registry
from grapheme_kit.graphemizer import Graphemizer
from grapheme_kit.scripts import register_builtin_scripts
from grapheme_kit.scripts.sinhala.decomposer import SinhalaDecomposer
from grapheme_kit.scripts.tamil.decomposer import TamilDecomposer

# Ensure built-ins are registered
register_builtin_scripts()


class Decomposer:
    """A class to handle grapheme decomposition for Indic and multi-script text.
    Maintains backward compatibility while delegating to script-specific decomposers.
    """

    SINHALA_VOWELS = SinhalaDecomposer.SINHALA_VOWELS
    SINHALA_ACCENT_SYMBOLS = SinhalaDecomposer.SINHALA_ACCENT_SYMBOLS
    ZWJ_CHARS = SinhalaDecomposer.ZWJ_CHARS

    TAMIL_VOWELS = ["அ", "ஆ", "இ", "ஈ", "உ", "ஊ", "எ", "ஏ", "ஐ", "ஒ", "ஓ", "ஔ"]
    TAMIL_ACCENT_SYMBOLS = ["", "ா", "ி", "ீ", "ு", "ூ", "ெ", "ே", "ை", "ொ", "ோ", "ௌ"]

    TAMIL_CONSONANT_FIRST = "க"
    TAMIL_CONSONANT_LAST = "ஹ"

    @classmethod
    def _is_tamil_consonant(cls, char: str) -> bool:
        """True if the grapheme is built on a Tamil consonant (mei)."""
        return bool(char) and (
            cls.TAMIL_CONSONANT_FIRST <= char[0] <= cls.TAMIL_CONSONANT_LAST
        )

    @staticmethod
    def _is_sinhala(chars: str) -> bool:
        """Check if all characters in the string are Sinhala characters or ZWJ."""
        if not chars:
            return False
        return all("\u0D80" <= c <= "\u0DFF" or c == "\u200d" for c in chars)

    @staticmethod
    def _is_tamil(chars: str) -> bool:
        """Check if all characters in the string are Tamil characters or ZWJ."""
        if not chars:
            return False
        return all("\u0B80" <= c <= "\u0BFF" or c == "\u200d" for c in chars)

    @classmethod
    def _decompose_sinhala_character(cls, char: str) -> list[str]:
        proc = registry.get("sinhala")
        if proc and isinstance(proc.decomposer, SinhalaDecomposer):
            return proc.decomposer._decompose_character(char)
        return SinhalaDecomposer()._decompose_character(char)

    @classmethod
    def _decompose_tamil_character(cls, char: str) -> list[str]:
        proc = registry.get("tamil")
        if proc and isinstance(proc.decomposer, TamilDecomposer):
            return proc.decomposer._decompose_character(char)
        return TamilDecomposer()._decompose_character(char)

    @classmethod
    def decompose(cls, text: str) -> str:
        """Decomposes Indic strings into fundamental phonetic sequences."""
        if not text:
            return ""

        gr = list(Graphemizer(text))
        new_string: list[str] = []

        for each_char in gr:
            if cls._is_sinhala(each_char):
                new_string.append("".join(cls._decompose_sinhala_character(each_char)))
            elif cls._is_tamil(each_char):
                new_string.append("".join(cls._decompose_tamil_character(each_char)))
            else:
                proc = registry.get_processor_for_char(each_char)
                if proc is not None and proc.name not in ("generic", "tamil", "sinhala"):
                    new_string.append(proc.decompose(each_char))
                else:
                    new_string.append(each_char)

        return "".join(new_string)


def decompose(text: str) -> str:
    """Public helper function for grapheme decomposition."""
    return Decomposer.decompose(text)
