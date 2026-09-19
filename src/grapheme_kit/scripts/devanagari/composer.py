"""Devanagari grapheme composer for recombining decomposed phonetic units."""

from __future__ import annotations

from grapheme_kit.core.composer import IndicComposer
from grapheme_kit.scripts.devanagari.profile import DevanagariProfile


class DevanagariComposer(IndicComposer):
    """Devanagari grapheme composer combining halant consonants and vowels."""

    def __init__(self, profile: DevanagariProfile | None = None) -> None:
        super().__init__(profile=profile or DevanagariProfile())

    def _compose_character(self, base: str, vowel: str) -> str:
        """Compose a Devanagari consonant with Halant and an independent vowel."""
        if not base or not base.endswith(self.profile.virama):
            raise ValueError(f"Error! Base '{base}' does not end with Devanagari virama '{self.profile.virama}'.")

        if not self.profile.is_vowel(vowel):
            raise ValueError(f"Error! '{vowel}' is not a valid independent Devanagari vowel.")

        base_clean = base[:-len(self.profile.virama)]
        if vowel == self.profile.inherent_vowel:
            return base_clean

        matra = self.profile.vowel_to_vowel_sign(vowel)
        if matra is None:
            raise ValueError(f"Error! No matra found for vowel '{vowel}'.")

        return base_clean + matra
