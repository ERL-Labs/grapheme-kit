"""Tamil phonetic decomposer for splitting graphemes into mei + uyir components."""

from __future__ import annotations

import grapheme
from grapheme_kit.core.decomposer import IndicDecomposer
from grapheme_kit.scripts.tamil.profile import TamilProfile


class TamilDecomposer(IndicDecomposer):
    """Tamil grapheme decomposer splitting syllables into mei (consonant) and uyir (vowel)."""

    def __init__(self, profile: TamilProfile | None = None) -> None:
        super().__init__(profile=profile or TamilProfile())

    def _decompose_character(self, char: str) -> list[str]:
        base_char = self.profile.virama

        if self.profile.is_vowel(char):
            return [char]

        # Already a complete grapheme with no consonant to split off (e.g. aytham ஃ, digits): leave it be.
        if not self.profile.is_consonant(char):
            return [char]

        if len(char) == 1:
            return [char + base_char, self.profile.inherent_vowel]
        elif len(char) == 2 and char[1] == base_char:
            return [char]
        elif len(char) == 2 and self.profile.is_dependent_vowel_sign(char[1]):
            vowel = self.profile.vowel_sign_to_vowel(char[1])
            if vowel:
                return [char[0] + base_char, vowel]
            return [char]
        else:
            gr = list(grapheme.graphemes(char))
            if len(gr) == 2:
                return self._decompose_character(gr[0]) + self._decompose_character(gr[1])
            raise ValueError(f"Not a valid single Tamil character grapheme: {char}!")
