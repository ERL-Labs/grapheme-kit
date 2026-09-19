"""Tamil script profile defining Tamil orthographic and linguistic properties."""

from __future__ import annotations

from grapheme_kit.core.profile import BaseScriptProfile


class TamilProfile(BaseScriptProfile):
    """Linguistic profile for the Tamil script (U+0B80 - U+0BFF)."""

    def __init__(self) -> None:
        vowels = ["அ", "ஆ", "இ", "ஈ", "உ", "ஊ", "எ", "ஏ", "ஐ", "ஒ", "ஓ", "ஔ"]
        dependent_vowel_signs = ["", "ா", "ி", "ீ", "ு", "ூ", "ெ", "ே", "ை", "ொ", "ோ", "ௌ"]
        consonants = [
            "க", "ங", "ச", "ஞ", "ட", "ண", "த", "ந", "ப", "ம",
            "ய", "ர", "ல", "வ", "ழ", "ள", "ற", "ன",
            "ஜ", "ஷ", "ஸ", "ஹ",
        ]
        special_clusters = ["க்ஷ", "ஸ்ரீ", "ஶ்ரீ"]

        super().__init__(
            name="tamil",
            unicode_ranges=[(0x0B80, 0x0BFF)],
            consonants=consonants,
            vowels=vowels,
            dependent_vowel_signs=dependent_vowel_signs,
            virama="்",
            inherent_vowel="அ",
            special_clusters=special_clusters,
        )

    def is_consonant(self, char: str) -> bool:
        """True if the character is built on a Tamil consonant (mei: U+0B95..U+0BB9)."""
        if not char:
            return False
        first = char[0]
        return "க" <= first <= "ஹ"
