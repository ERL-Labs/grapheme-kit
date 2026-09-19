"""Sinhala grapheme composer for recombining decomposed phonetic units."""

from __future__ import annotations

import grapheme
from grapheme_kit.core.composer import IndicComposer
from grapheme_kit.scripts.sinhala.profile import SinhalaProfile


class SinhalaComposer(IndicComposer):
    """Sinhala grapheme composer combining hal akuru and vowels."""

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

    def _compose_sinhala_character(self, base: str, vowel: str) -> str:
        """Compose a Sinhala consonant base with a vowel."""
        if vowel not in self.SINHALA_VOWELS:
            raise ValueError("Error! Not a valid Sinhala vowel!")

        base_clean = base[:-1] if base.endswith("්") else base
        if vowel == "අ":
            return base_clean
        return base_clean + self.SINHALA_ACCENT_SYMBOLS[self.SINHALA_VOWELS.index(vowel)]

    def compose(self, text: str) -> str:
        """Compose decomposed Sinhala sequence into standard graphemes."""
        if not text:
            return ""

        from grapheme_kit.core.segmenter import UnicodeSegmenter
        gr = UnicodeSegmenter().segment(text)
        new_string: list[str] = []
        i = 0
        n = len(gr)

        while i < n:
            current = gr[i]

            if self.profile.is_in_script(current):
                if current in self.SINHALA_VOWELS:
                    new_string.append(current)
                    i += 1
                    continue

                while (
                    i + 1 < n
                    and self.profile.is_in_script(gr[i + 1])
                    and (
                        current + "\u200d" + gr[i + 1] in self.ZWJ_CHARS
                        or gr[i + 1] in self.ZWJ_CHARS
                    )
                ):
                    new_string.append(current + "\u200d")
                    i += 1
                    current = gr[i]

                if i + 1 < n and gr[i + 1] in self.SINHALA_VOWELS:
                    new_string.append(self._compose_sinhala_character(current, gr[i + 1]))
                    i += 2
                else:
                    new_string.append(current)
                    i += 1
            else:
                new_string.append(current)
                i += 1

        return "".join(new_string)
