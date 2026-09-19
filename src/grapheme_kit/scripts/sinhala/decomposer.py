"""Sinhala phonetic decomposer for splitting graphemes into constituent phonetic units."""

from __future__ import annotations

import grapheme
from grapheme_kit.core.decomposer import IndicDecomposer
from grapheme_kit.scripts.sinhala.profile import SinhalaProfile


class SinhalaDecomposer(IndicDecomposer):
    """Sinhala grapheme decomposer splitting syllables into hal akuru and vowels."""

    SINHALA_VOWELS = [
        "අ", "ආ", "ඇ", "ඈ", "ඉ", "ඊ", "උ", "ඌ",
        "ඍ", "ඎ", "එ", "ඒ", "ඓ", "ඔ", "ඕ", "ඖ",
        "අං", "අඃ",
    ]

    SINHALA_ACCENT_SYMBOLS = [
        "", "ා", "ැ", "ෑ", "ի", "ී", "ු", "ූ", "ෘ",
        "ෲ", "ෙ", "ේ", "ෛ", "ො", "ෝ", "ෞ",
        "ං", "ඃ",
    ]

    ZWJ_CHARS = [
        "ක්ව්", "ක්ෂ්", "ග්ධ්", "ට්ඨ්", "ත්ව්", "ත්ථ්",
        "ද්ධ්", "න්ථ්", "න්ද්", "න්ධ්", "ර්", "ය්",
    ]

    def __init__(self, profile: SinhalaProfile | None = None) -> None:
        super().__init__(profile=profile or SinhalaProfile())

    def _decompose_character(self, char: str) -> list[str]:
        base_char = "්"

        if char in self.SINHALA_VOWELS:
            return [char, ""]

        if len(char) == 1:
            return [char + base_char, self.SINHALA_VOWELS[0]]
        elif len(char) == 2 and char[1] in self.SINHALA_ACCENT_SYMBOLS:
            return [char[0] + base_char, self.SINHALA_VOWELS[self.SINHALA_ACCENT_SYMBOLS.index(char[1])]]
        elif "\u200d" in char:
            newchar = char[char.find("\u200d") + 1:]
            return [char[0] + base_char] + self._decompose_character(newchar)
        else:
            return [char]

    def decompose(self, text: str) -> str:
        """Decompose Sinhala string into fundamental phonetic sequences."""
        if not text:
            return ""

        from grapheme_kit.core.segmenter import UnicodeSegmenter
        gr = UnicodeSegmenter().segment(text)
        new_string: list[str] = []

        for each_char in gr:
            if self.profile.is_in_script(each_char):
                new_string.append("".join(self._decompose_character(each_char)))
            else:
                new_string.append(each_char)

        return "".join(new_string)
