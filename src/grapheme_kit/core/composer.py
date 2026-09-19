"""Core composition contracts and reusable Indic composer implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
import grapheme

from grapheme_kit.core.profile import BaseScriptProfile


class BaseComposer(ABC):
    """Abstract base class for grapheme composers."""

    @abstractmethod
    def compose(self, text: str) -> str:
        """Compose decomposed phonetic units back into standard grapheme clusters.

        Args:
            text: Decomposed phonetic text.

        Returns:
            Composed text with standard grapheme clusters.
        """
        raise NotImplementedError


class IndicComposer(BaseComposer):
    """Reusable Indic composition engine driven by a BaseScriptProfile.

    Handles merging of consonants with virama and independent vowels into
    combined grapheme clusters (consonant + dependent vowel sign), while
    preserving standalone vowels, non-script characters, punctuation, and spaces.
    """

    def __init__(self, profile: BaseScriptProfile) -> None:
        self.profile = profile

    def _compose_character(self, base_with_virama: str, vowel: str) -> str:
        """Compose a consonant ending with virama with an independent vowel."""
        if not base_with_virama or not base_with_virama.endswith(self.profile.virama):
            raise ValueError(f"Error! Base '{base_with_virama}' does not end with virama '{self.profile.virama}'.")

        if not self.profile.is_vowel(vowel):
            raise ValueError(f"Error! '{vowel}' is not a valid independent vowel in {self.profile.name}.")

        base_clean = base_with_virama[:-len(self.profile.virama)]
        if vowel == self.profile.inherent_vowel:
            return base_clean

        dependent_sign = self.profile.vowel_to_vowel_sign(vowel)
        if dependent_sign is None:
            raise ValueError(f"Error! No dependent vowel sign found for vowel '{vowel}'.")

        return base_clean + dependent_sign

    def compose(self, text: str) -> str:
        """Compose decomposed units in text back into standard graphemes."""
        if text is None or not text:
            return ""

        gr = list(grapheme.graphemes(text))
        new_string: list[str] = []
        i = 0
        n = len(gr)

        while i < n:
            current = gr[i]

            # Check if this grapheme belongs to this script
            if self.profile.is_in_script(current):
                # Check for consonant ending in virama followed by independent vowel
                if current.endswith(self.profile.virama) and i + 1 < n and self.profile.is_vowel(gr[i + 1]):
                    composed = self._compose_character(current, gr[i + 1])
                    new_string.append(composed)
                    i += 2
                    continue

                # Sinhala ZWJ sequence handling if profile defines zwj_chars
                if self.profile.zwj_chars:
                    if current in self.profile.vowels:
                        new_string.append(current)
                        i += 1
                        continue

                    while (
                        i + 1 < n
                        and self.profile.is_in_script(gr[i + 1])
                        and (
                            current + "\u200d" + gr[i + 1] in self.profile.zwj_chars
                            or gr[i + 1] in self.profile.zwj_chars
                        )
                    ):
                        new_string.append(current + "\u200d")
                        i += 1
                        current = gr[i]

                    if current.endswith(self.profile.virama) and i + 1 < n and self.profile.is_vowel(gr[i + 1]):
                        composed = self._compose_character(current, gr[i + 1])
                        new_string.append(composed)
                        i += 2
                        continue

                new_string.append(current)
                i += 1
            else:
                new_string.append(current)
                i += 1

        return "".join(new_string)
