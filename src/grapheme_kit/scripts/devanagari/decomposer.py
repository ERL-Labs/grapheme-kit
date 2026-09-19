"""Devanagari phonetic decomposer for splitting graphemes into halant consonant and vowel."""

from __future__ import annotations

import grapheme
from grapheme_kit.core.decomposer import IndicDecomposer
from grapheme_kit.scripts.devanagari.profile import DevanagariProfile


class DevanagariDecomposer(IndicDecomposer):
    """Devanagari grapheme decomposer splitting syllables into consonant + halant + vowel."""

    def __init__(self, profile: DevanagariProfile | None = None) -> None:
        super().__init__(profile=profile or DevanagariProfile())

    def _decompose_character(self, char: str) -> list[str]:
        halant = self.profile.virama

        # Standalone independent vowels
        if self.profile.is_vowel(char):
            return [char]

        # Non-consonant characters (dandas, om, digits, punctuation)
        if not self.profile.is_consonant(char):
            return [char]

        # Already ending with virama/halant
        if char.endswith(halant):
            return [char]

        # Single base consonant -> consonant + halant + inherent 'अ'
        if len(char) == 1:
            return [char + halant, self.profile.inherent_vowel]

        # Base consonant + single matra
        if len(char) == 2 and self.profile.is_dependent_vowel_sign(char[1]):
            vowel = self.profile.vowel_sign_to_vowel(char[1])
            if vowel:
                return [char[0] + halant, vowel]
            return [char]

        # Multi-character conjunct or multi-codepoint sequences
        sub_clusters = list(grapheme.graphemes(char))
        if len(sub_clusters) > 1:
            result: list[str] = []
            for sub in sub_clusters:
                result.extend(self._decompose_character(sub))
            return result

        # Check trailing matras
        for sign_len in range(len(char) - 1, 0, -1):
            sign = char[-sign_len:]
            base = char[:-sign_len]
            if self.profile.is_dependent_vowel_sign(sign):
                vowel = self.profile.vowel_sign_to_vowel(sign)
                if vowel:
                    return [base + halant, vowel]

        return [char + halant, self.profile.inherent_vowel]
