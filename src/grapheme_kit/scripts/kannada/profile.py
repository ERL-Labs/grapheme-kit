"""Kannada script profile defining orthographic properties."""

from __future__ import annotations

from grapheme_kit.core.profile import BaseScriptProfile


class KannadaProfile(BaseScriptProfile):
    """Linguistic profile for the Kannada script (U+0C80 - U+0CFF)."""

    def __init__(self) -> None:
        vowels = [
            "ಅ", "ಆ", "ಇ", "ಈ", "ಉ", "ಊ", "ಋ", "ೠ",
            "ಌ", "ೡ", "ಎ", "ಏ", "ಐ", "ಒ", "ಓ", "ಔ", "ಅಂ", "ಅಃ",
        ]
        dependent_vowel_signs = [
            "", "ಾ", "ಿ", "ೀ", "ು", "ೂ", "ೃ", "ೄ",
            "ೢ", "ೣ", "ೆ", "ೇ", "ೈ", "ೊ", "ೋ", "ೌ", "ಂ", "ಃ",
        ]
        consonants = [
            "ಕ", "ಖ", "ಗ", "ಘ", "ಙ",
            "ಚ", "ಛ", "ಜ", "ಝ", "ಞ",
            "ಟ", "ಠ", "ಡ", "ಢ", "ಣ",
            "ತ", "ಥ", "ದ", "ಧ", "ನ",
            "ಪ", "ಫ", "ಬ", "ಭ", "ಮ",
            "ಯ", "ರ", "ಱ", "ಲ", "ವ",
            "ಶ", "ಷ", "ಸ", "ಹ", "ಳ", "ೞ",
        ]

        super().__init__(
            name="kannada",
            unicode_ranges=[(0x0C80, 0x0CFF)],
            consonants=consonants,
            vowels=vowels,
            dependent_vowel_signs=dependent_vowel_signs,
            virama="್",
            inherent_vowel="ಅ",
        )

    def is_consonant(self, char: str) -> bool:
        if not char:
            return False
        first = char[0]
        return ("ಕ" <= first <= "ಹ") or char in self._consonant_set
