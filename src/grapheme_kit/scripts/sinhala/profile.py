"""Sinhala script profile defining Sinhala orthographic and linguistic properties."""

from __future__ import annotations

from grapheme_kit.core.profile import BaseScriptProfile


class SinhalaProfile(BaseScriptProfile):
    """Linguistic profile for the Sinhala script (U+0D80 - U+0DFF)."""

    def __init__(self) -> None:
        vowels = [
            "අ", "ආ", "ඇ", "ඈ", "ඉ", "ඊ", "උ", "ඌ",
            "ඍ", "ඎ", "එ", "ඒ", "ඓ", "ඔ", "ඕ", "ඖ",
            "අං", "අඃ",
        ]
        # Primary accent symbols mapping to vowels. Note: include both standard U+0DD2 (ි) and variant (ի)
        dependent_vowel_signs = [
            "", "ා", "ැ", "ෑ", "ි", "ී", "ු", "ූ", "ෘ",
            "ෲ", "ෙ", "ේ", "ෛ", "ො", "ෝ", "ෞ",
            "ං", "ඃ",
        ]
        consonants = [
            "ක", "ඛ", "ග", "ඝ", "ඞ", "ඟ",
            "ච", "ඡ", "ජ", "ඣ", "ඤ", "ඥ", "ඦ",
            "ට", "ඨ", "ඩ", "ඪ", "ණ", "ඬ",
            "ත", "ථ", "ද", "ධ", "න", "ඳ",
            "ප", "ඵ", "බ", "භ", "ම", "ඹ",
            "ය", "ර", "ල", "ව", "ශ", "ෂ", "ස", "හ", "ළ", "ෆ",
        ]
        zwj_chars = [
            "ක්ව්", "ක්ෂ්", "ග්ධ්", "ට්ඨ්", "ත්ව්", "ත්ථ්",
            "ද්ධ්", "න්ථ්", "න්ද්", "න්ධ්", "ර්", "ය්",
        ]

        super().__init__(
            name="sinhala",
            unicode_ranges=[(0x0D80, 0x0DFF)],
            consonants=consonants,
            vowels=vowels,
            dependent_vowel_signs=dependent_vowel_signs,
            virama="්",
            inherent_vowel="අ",
            zwj_chars=zwj_chars,
        )
        # Register both standard Sinhala 'ි' (U+0DD2) and legacy variant 'ի' (U+056B)
        self._sign_to_vowel["ի"] = "ඉ"
        self._dependent_sign_set.add("ի")
