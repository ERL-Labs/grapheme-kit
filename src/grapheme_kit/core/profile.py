"""Script profile architecture defining linguistic properties for each script."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class BaseScriptProfile:
    """Base class / dataclass representing linguistic properties of a script.

    Provides Unicode ranges, vowel/consonant sets, virama, inherent vowels,
    special clusters, and mappings between independent and dependent vowels.
    """

    name: str
    unicode_ranges: list[tuple[int, int]] = field(default_factory=list)
    consonants: list[str] = field(default_factory=list)
    vowels: list[str] = field(default_factory=list)
    dependent_vowel_signs: list[str] = field(default_factory=list)
    virama: str = ""
    inherent_vowel: str = ""
    special_clusters: list[str] = field(default_factory=list)
    exceptions: dict[str, str] = field(default_factory=dict)
    zwj_chars: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Build cached fast lookup sets and maps
        self._consonant_set: set[str] = set(self.consonants)
        self._vowel_set: set[str] = set(self.vowels)
        self._dependent_sign_set: set[str] = set(self.dependent_vowel_signs)

        # Mapping: dependent sign -> independent vowel
        self._sign_to_vowel: dict[str, str] = {}
        # Mapping: independent vowel -> dependent sign
        self._vowel_to_sign: dict[str, str] = {}

        min_len = min(len(self.vowels), len(self.dependent_vowel_signs))
        for i in range(min_len):
            v = self.vowels[i]
            s = self.dependent_vowel_signs[i]
            self._sign_to_vowel[s] = v
            self._vowel_to_sign[v] = s

    def is_in_script(self, text: str) -> bool:
        """Check if all non-whitespace characters in text fall within this script's Unicode ranges."""
        if not text:
            return False
        for c in text:
            if c.isspace():
                continue
            cp = ord(c)
            # Allow ZWJ/ZWNJ if relevant for Indic scripts
            if c in ("\u200c", "\u200d"):
                continue
            if not any(start <= cp <= end for start, end in self.unicode_ranges):
                return False
        return True

    def is_consonant(self, char: str) -> bool:
        """Check if character is a base consonant in this script."""
        if not char:
            return False
        return char in self._consonant_set or char[0] in self._consonant_set

    def is_vowel(self, char: str) -> bool:
        """Check if character is an independent vowel in this script."""
        return char in self._vowel_set

    def is_dependent_vowel_sign(self, char: str) -> bool:
        """Check if character is a dependent vowel sign (matra) in this script."""
        return char in self._dependent_sign_set

    def vowel_sign_to_vowel(self, sign: str) -> str | None:
        """Map dependent vowel sign to corresponding independent vowel."""
        return self._sign_to_vowel.get(sign)

    def vowel_to_vowel_sign(self, vowel: str) -> str | None:
        """Map independent vowel to corresponding dependent vowel sign."""
        return self._vowel_to_sign.get(vowel)
