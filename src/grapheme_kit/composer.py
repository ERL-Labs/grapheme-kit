"""Grapheme composition for Indic and multi-script text with registry-backed dispatch."""

from __future__ import annotations

from grapheme_kit.core.registry import registry
from grapheme_kit.graphemizer import Graphemizer
from grapheme_kit.scripts import register_builtin_scripts
from grapheme_kit.scripts.sinhala.composer import SinhalaComposer
from grapheme_kit.scripts.tamil.composer import TamilComposer

# Ensure built-in scripts are registered
register_builtin_scripts()


class Composer:
    """A class to handle grapheme composition across Indic and multi-script text.
    Maintains backward compatibility while delegating to script-specific composers.
    """

    SINHALA_VOWELS = SinhalaComposer.SINHALA_VOWELS
    SINHALA_ACCENT_SYMBOLS = SinhalaComposer.SINHALA_ACCENT_SYMBOLS
    ZWJ_CHARS = SinhalaComposer.ZWJ_CHARS

    TAMIL_VOWELS = ["அ", "ஆ", "இ", "ஈ", "உ", "ஊ", "எ", "ஏ", "ஐ", "ஒ", "ஓ", "ஔ"]
    TAMIL_ACCENT_SYMBOLS = ["", "ா", "ி", "ீ", "ு", "ூ", "ெ", "ே", "ை", "ொ", "ோ", "ௌ"]

    @staticmethod
    def _is_sinhala(chars: str) -> bool:
        """Check if all characters in string are Sinhala characters or ZWJ."""
        if not chars:
            return False
        return all("\u0D80" <= c <= "\u0DFF" or c == "\u200d" for c in chars)

    @staticmethod
    def _is_tamil(chars: str) -> bool:
        """Check if all characters in string are Tamil characters or ZWJ."""
        if not chars:
            return False
        return all("\u0B80" <= c <= "\u0BFF" or c == "\u200d" for c in chars)

    @classmethod
    def _compose_tamil_character(cls, mei: str, uyir: str) -> str:
        proc = registry.get("tamil")
        if proc and isinstance(proc.composer, TamilComposer):
            return proc.composer._compose_character(mei, uyir)
        return TamilComposer()._compose_character(mei, uyir)

    @classmethod
    def _compose_sinhala_character(cls, base: str, vowel: str) -> str:
        proc = registry.get("sinhala")
        if proc and isinstance(proc.composer, SinhalaComposer):
            return proc.composer._compose_sinhala_character(base, vowel)
        return SinhalaComposer()._compose_sinhala_character(base, vowel)

    @classmethod
    def compose(cls, text: str) -> str:
        """Composes a decomposed sequence of Indic characters back into standard graphemes."""
        if not text:
            return ""

        gr = list(Graphemizer(text))
        new_string: list[str] = []
        i = 0
        n = len(gr)

        while i < n:
            current = gr[i]

            if cls._is_tamil(current):
                if current.endswith("்") and i + 1 < n and gr[i + 1] in cls.TAMIL_VOWELS:
                    new_string.append(cls._compose_tamil_character(current, gr[i + 1]))
                    i += 2
                else:
                    new_string.append(current)
                    i += 1

            elif cls._is_sinhala(current):
                if current in cls.SINHALA_VOWELS:
                    new_string.append(current)
                    i += 1
                    continue

                while (
                    i + 1 < n
                    and cls._is_sinhala(gr[i + 1])
                    and (
                        current + "\u200d" + gr[i + 1] in cls.ZWJ_CHARS
                        or gr[i + 1] in cls.ZWJ_CHARS
                    )
                ):
                    new_string.append(current + "\u200d")
                    i += 1
                    current = gr[i]

                if i + 1 < n and gr[i + 1] in cls.SINHALA_VOWELS:
                    new_string.append(cls._compose_sinhala_character(current, gr[i + 1]))
                    i += 2
                else:
                    new_string.append(current)
                    i += 1

            else:
                # Check other registered scripts (Devanagari, Kannada, Malayalam)
                proc = registry.get_processor_for_char(current)
                if proc is not None and proc.name not in ("generic", "tamil", "sinhala"):
                    # Process cluster with the script's composer
                    if current.endswith(proc.profile.virama) and i + 1 < n and proc.profile.is_vowel(gr[i + 1]):
                        new_string.append(proc.composer._compose_character(current, gr[i + 1]))
                        i += 2
                    else:
                        new_string.append(current)
                        i += 1
                else:
                    new_string.append(current)
                    i += 1

        return "".join(new_string)


def compose(text: str) -> str:
    """Public helper function for grapheme composition."""
    return Composer.compose(text)