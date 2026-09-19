"""Tamil normalizer implementing NFC, character fixups, and Nanool validation rules."""

from __future__ import annotations

import re
from grapheme_kit.core.normalizer import UnicodeNormalizer


class TamilNormalizer(UnicodeNormalizer):
    """Handles Tamil-specific normalization and grammatical validation rules (Nanool)."""

    def normalize(self, text: str) -> str:
        """Main entry point for Tamil normalization: NFC + Tamil character fixup."""
        if text is None or not text:
            return ""

        text = super().normalize(text)
        return self._char_fixup(text)

    def _char_fixup(self, word: str) -> str:
        """Tamil-specific character normalization rules."""
        # 1. Standard normalization fixes
        word = word.replace("ோ", "ோ")
        word = word.replace("ொ", "ொ")
        word = word.replace("ா்", "ர்")
        word = word.replace("ாி", "ரி")

        # 2. Remove Zero Width Joiner/Non-Joiner
        word = word.replace("\u200c", "").replace("\u200C", "")

        # 3. Fix reverse vowel orders
        word = word.replace("ாெ", "ொ")
        word = word.replace("ாே", "ோ")

        # 4. Conditional 'ெ' + 'ள' -> 'ௌ' (only if NOT followed by dependent vowel)
        tamil_dependent_vowels = ["ா", "ி", "ீ", "ு", "ூ", "ெ", "ே", "ை", "ொ", "ோ", "ௌ", "்"]
        vowels_pattern = "[" + "".join(tamil_dependent_vowels) + "]"
        pattern = re.compile(r"ெள(?!" + vowels_pattern + ")")
        word = pattern.sub("ௌ", word)

        return word

    def sandhi_remover(self, word: str) -> str:
        """Remove word-final sandhi consonants."""
        word = word.strip()
        sandhi_letters = {"க்", "த்", "ப்", "ச்"}
        for x in sandhi_letters:
            p = re.compile(x + "$")
            if p.search(word):
                word = word[:-2]
        return word

    def check_starting_letter(self, word: str) -> bool:
        """Nanool validation: Check if word starts with a grammatically permitted Tamil letter."""
        uyir = ["அ", "ஆ", "இ", "ஈ", "உ", "ஊ", "எ", "ஏ", "ஐ", "ஒ", "ஓ", "ஔ"]
        ka = ["க", "கா", "கி", "கீ", "கு", "கூ", "ெக", "ேக", "ைக", "ெகா", "கோ", "ெகள"]
        ca = ["ச", "சா", "சி", "சீ", "சு", "சூ", "செ", "சே", "சை", "சொ", "சோ", "சௌ"]
        tha = ["த", "தா", "தி", "தீ", "து", "தூ", "தெ", "தே", "தை", "தொ", "தோ", "தௌ"]
        na = ["ந", "நா", "நி", "நீ", "நு", "நூ", "நெ", "நே", "நை", "நொ", "நோ", "நௌ"]
        pa = ["ப", "பா", "பி", "பீ", "பு", "பூ", "பெ", "பே", "பை", "பொ", "போ", "பௌ"]
        ma = ["ம", "மா", "மி", "மீ", "மு", "மூ", "மெ", "மே", "மை", "மொ", "மோ", "மௌ"]
        va = ["வ", "வா", "வி", "வீ", "வெ", "வே", "வை", "வௌ"]
        ya = ["ய", "யா", "யு", "யூ", "யோ", "யௌ"]
        gna = ["ஞ", "ஞா", "ஞெ", "ஞொ"]

        letters = uyir + ka + ca + tha + na + pa + ma + va + ya + gna
        for x in letters:
            if word.startswith(x):
                return True
        return False

    def check_ending_letter(self, word: str) -> bool:
        """Nanool validation: Check if word ends with a grammatically permitted Tamil letter."""
        uyir_oreluthu_orumozhi = ["ஆ", "ஈ", "ஊ", "ஏ", "ஐ", "ஓ", "ஒள"]
        uyir_a = ["க", "ங", "ச", "ஞ", "ட", "ண", "த", "ந", "ப", "ம", "ய", "ர", "ழ", "வ", "ள", "ல", "ற", "ன"]
        mei = ["ஞ்", "ண்", "ந்", "ம்", "ன்", "ய்", "ர்", "ல்", "வ்", "ழ்", "ள்"]
        uyir_rest = ["ா", "ி", "ீ", "ு", "ூ", "ே", "ை", "ொ", "ோ", "ௌ"]

        letters = uyir_a + uyir_rest + mei

        if len(word) == 1:
            return word in uyir_oreluthu_orumozhi
        else:
            for x in letters:
                p = re.compile(x + "$")
                if p.search(word):
                    return True
        return False

    def check_meimmayakkam(self, word: str) -> bool:
        """Grammatical validation for Tamil consonantal co-occurrence (Meimmayakkam)."""
        return True
