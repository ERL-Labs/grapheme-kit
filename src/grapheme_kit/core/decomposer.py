"""Core decomposition contracts and reusable Indic decomposer implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
import grapheme

from grapheme_kit.core.profile import BaseScriptProfile


class BaseDecomposer(ABC):
    """Abstract base class for grapheme decomposers."""

    @abstractmethod
    def decompose(self, text: str) -> str:
        """Decompose text into fundamental phonetic sequences.

        Args:
            text: Input text.

        Returns:
            Decomposed phonetic representation.
        """
        raise NotImplementedError


class IndicDecomposer(BaseDecomposer):
    """Reusable Indic decomposition engine driven by a BaseScriptProfile.

    Decomposes consonant grapheme clusters into constituent base consonant,
    virama, and independent vowel units according to linguistic rules.
    """

    def __init__(self, profile: BaseScriptProfile) -> None:
        self.profile = profile

    def _is_consonant(self, char: str) -> bool:
        """Check if character is built on a consonant in this script."""
        return self.profile.is_consonant(char)

    def _decompose_character(self, char: str) -> list[str]:
        """Decompose a single script grapheme cluster into phonetic units."""
        virama = self.profile.virama

        # 1. Standalone independent vowel decomposes to itself
        if self.profile.is_vowel(char):
            return [char]

        # 2. Non-consonants (e.g. digits, signs, aytham, symbols) decompose to themselves
        if not self._is_consonant(char):
            return [char]

        # 3. Already has pure virama ending (and no trailing dependent vowel)
        if char.endswith(virama):
            return [char]

        # 4. Single codepoint base consonant -> consonant + virama + inherent vowel
        if len(char) == 1:
            return [char + virama, self.profile.inherent_vowel]

        # 5. Two codepoints: base consonant + dependent vowel sign
        if len(char) == 2 and self.profile.is_dependent_vowel_sign(char[1]):
            vowel = self.profile.vowel_sign_to_vowel(char[1])
            if vowel:
                return [char[0] + virama, vowel]

        # 6. ZWJ sequence handling (e.g. Sinhala)
        if "\u200d" in char:
            idx = char.find("\u200d")
            base = char[:idx]
            rest = char[idx + 1:]
            return [base + virama] + self._decompose_character(rest)

        # 7. Multi-codepoint conjuncts (e.g. decomposed by Unicode grapheme boundaries)
        sub_clusters = list(grapheme.graphemes(char))
        if len(sub_clusters) > 1:
            result: list[str] = []
            for sub in sub_clusters:
                result.extend(self._decompose_character(sub))
            return result

        # 8. Multi-codepoint dependent vowel sign combinations or fallback
        # Check if last char(s) are dependent vowel signs
        for sign_len in range(len(char) - 1, 0, -1):
            sign = char[-sign_len:]
            base = char[:-sign_len]
            if self.profile.is_dependent_vowel_sign(sign):
                vowel = self.profile.vowel_sign_to_vowel(sign)
                if vowel:
                    return [base + virama, vowel]

        # Fallback: single consonant with inherent vowel
        return [char + virama, self.profile.inherent_vowel]

    def decompose(self, text: str) -> str:
        """Decompose text into fundamental phonetic sequences."""
        if text is None or not text:
            return ""

        gr = list(grapheme.graphemes(text))
        result: list[str] = []

        for each_char in gr:
            if self.profile.is_in_script(each_char):
                units = self._decompose_character(each_char)
                result.append("".join(units))
            else:
                result.append(each_char)

        return "".join(result)
