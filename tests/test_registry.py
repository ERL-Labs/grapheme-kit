"""Tests for ScriptRegistry, script detection, and dynamic plugin registration."""

import pytest
from grapheme_kit.core import (
    BaseComposer,
    BaseDecomposer,
    BaseScriptProcessor,
    BaseScriptProfile,
    ScriptRegistry,
    UnicodeNormalizer,
    UnicodeSegmenter,
    registry,
)


class TestScriptRegistry:
    def test_default_registry_contains_builtin_scripts(self):
        scripts = registry.list_scripts()
        assert "tamil" in scripts
        assert "sinhala" in scripts
        assert "devanagari" in scripts
        assert "malayalam" in scripts
        assert "kannada" in scripts
        assert "generic" in scripts

    def test_alias_resolution(self):
        assert registry.get("ta").name == "tamil"
        assert registry.get("si").name == "sinhala"
        assert registry.get("hi").name == "devanagari"
        assert registry.get("hindi").name == "devanagari"
        assert registry.get("sanskrit").name == "devanagari"
        assert registry.get("ml").name == "malayalam"
        assert registry.get("kn").name == "kannada"
        assert registry.get("en").name == "generic"

    def test_detect_script(self):
        assert registry.detect_script("வணக்கம்") == "tamil"
        assert registry.detect_script("සිංහල") == "sinhala"
        assert registry.detect_script("किताब") == "devanagari"
        assert registry.detect_script("നമസ്കാരം") == "malayalam"
        assert registry.detect_script("ನಮಸ್ಕಾರ") == "kannada"
        assert registry.detect_script("hello world") == "generic"
        assert registry.detect_script("") == "generic"

    def test_dynamic_script_plugin_registration(self):
        """Demonstrates PDF Section 11: Adding a new script without modifying core classes."""
        custom_registry = ScriptRegistry()

        # 1. Create Profile for a hypothetical script
        custom_profile = BaseScriptProfile(
            name="custom_script",
            unicode_ranges=[(0x2800, 0x28FF)],  # Braille range
            virama="",
            inherent_vowel="",
        )

        class CustomBrailleComposer(BaseComposer):
            def compose(self, text: str) -> str:
                return f"[composed:{text}]"

        class CustomBrailleDecomposer(BaseDecomposer):
            def decompose(self, text: str) -> str:
                return f"[decomposed:{text}]"

        # 2. Implement Processor
        custom_processor = BaseScriptProcessor(
            profile=custom_profile,
            normalizer=UnicodeNormalizer(),
            segmenter=UnicodeSegmenter(),
            composer=CustomBrailleComposer(),
            decomposer=CustomBrailleDecomposer(),
        )

        # 3. Register Processor
        custom_registry.register(custom_processor, aliases=["braille"])

        assert custom_registry.get("braille") is custom_processor
        assert custom_registry.detect_script("⠃⠗⠁⠊⠇⠇⠑") == "custom_script"
        assert custom_processor.compose("test") == "[composed:test]"
        assert custom_processor.decompose("test") == "[decomposed:test]"
