"""Devanagari script profile defining orthographic properties for Hindi, Sanskrit, Marathi, Nepali."""

from __future__ import annotations

from grapheme_kit.core.profile import BaseScriptProfile


class DevanagariProfile(BaseScriptProfile):
    """Linguistic profile for the Devanagari script (U+0900 - U+097F)."""

    def __init__(self) -> None:
        vowels = [
            "अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ॠ",
            "ऌ", "ॡ", "ए", "ऐ", "ओ", "औ", "अं", "अः",
        ]
        dependent_vowel_signs = [
            "", "ा", "ि", "ी", "ु", "ू", "ृ", "ॄ",
            "ॢ", "ॣ", "े", "ै", "ो", "ौ", "ं", "ः",
        ]
        consonants = [
            "क", "ख", "ग", "घ", "ङ",
            "च", "छ", "ज", "झ", "ञ",
            "ट", "ठ", "ड", "ढ", "ण",
            "त", "थ", "द", "ध", "न",
            "प", "फ", "ब", "भ", "म",
            "य", "र", "ल", "व",
            "श", "ष", "स", "ह", "ळ",
            "क़", "ख़", "ग़", "ज़", "ड़", "ढ़", "फ़", "य़",
        ]
        special_clusters = ["क्ष", "त्र", "ज्ञ", "श्र"]

        super().__init__(
            name="devanagari",
            unicode_ranges=[(0x0900, 0x097F)],
            consonants=consonants,
            vowels=vowels,
            dependent_vowel_signs=dependent_vowel_signs,
            virama="्",
            inherent_vowel="अ",
            special_clusters=special_clusters,
        )

    def is_consonant(self, char: str) -> bool:
        """Check if character is built on a Devanagari consonant."""
        if not char:
            return False
        first = char[0]
        return ("क" <= first <= "ह") or first == "ळ" or char in self._consonant_set
