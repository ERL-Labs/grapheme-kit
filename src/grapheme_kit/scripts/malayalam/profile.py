"""Malayalam script profile defining orthographic properties."""

from __future__ import annotations

from grapheme_kit.core.profile import BaseScriptProfile


class MalayalamProfile(BaseScriptProfile):
    """Linguistic profile for the Malayalam script (U+0D00 - U+0D7F)."""

    def __init__(self) -> None:
        vowels = [
            "അ", "ആ", "ഇ", "ഈ", "ഉ", "ഊ", "ഋ", "ൠ",
            "ൡ", "എ", "ഏ", "ഐ", "ഒ", "ഓ", "ഔ", "അം", "അഃ",
        ]
        dependent_vowel_signs = [
            "", "ാ", "ി", "ീ", "ു", "ൂ", "ൃ", "ൄ",
            "ൣ", "െ", "േ", "ൈ", "ൊ", "ോ", "ൌ", "ം", "ഃ",
        ]
        consonants = [
            "ക", "ഖ", "ഗ", "ഘ", "ങ",
            "ച", "ഛ", "ജ", "ഝ", "ഞ",
            "ട", "ഠ", "ഡ", "ഢ", "ണ",
            "ത", "ഥ", "ദ", "ധ", "ന",
            "പ", "ഫ", "ബ", "ഭ", "മ",
            "യ", "ര", "റ", "ല", "ള", "ഴ", "വ",
            "ശ", "ഷ", "സ", "ഹ",
        ]
        special_clusters = ["ൺ", "ൻ", "ർ", "ൽ", "ൾ", "ൿ"]

        super().__init__(
            name="malayalam",
            unicode_ranges=[(0x0D00, 0x0D7F)],
            consonants=consonants,
            vowels=vowels,
            dependent_vowel_signs=dependent_vowel_signs,
            virama="്",
            inherent_vowel="അ",
            special_clusters=special_clusters,
        )

    def is_consonant(self, char: str) -> bool:
        if not char:
            return False
        first = char[0]
        return ("ക" <= first <= "ഹ") or char in self._consonant_set
