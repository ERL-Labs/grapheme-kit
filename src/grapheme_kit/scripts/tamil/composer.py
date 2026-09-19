"""Tamil grapheme composer for recombining decomposed phonetic units."""

from __future__ import annotations

from grapheme_kit.core.composer import IndicComposer
from grapheme_kit.scripts.tamil.profile import TamilProfile


class TamilComposer(IndicComposer):
    """Tamil grapheme composer combining mei consonants and uyir vowels."""

    def __init__(self, profile: TamilProfile | None = None) -> None:
        super().__init__(profile=profile or TamilProfile())

    def _compose_character(self, mei: str, uyir: str) -> str:
        """Compose a mei consonant with an uyir vowel."""
        if not mei or not mei.endswith(self.profile.virama):
            raise ValueError("Error! Not a valid mei character!")

        if not self.profile.is_vowel(uyir):
            raise ValueError("Error! Cant be merged!")

        # Strip the trailing virama rather than keeping only the first code point,
        # so multi-codepoint conjuncts (க்ஷ், ஸ்ர்) survive intact.
        sign = self.profile.vowel_to_vowel_sign(uyir)
        if sign is None:
            raise ValueError("Error! Cant be merged!")

        return mei[:-len(self.profile.virama)] + sign
