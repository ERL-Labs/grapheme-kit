# grapheme-kit

Grapheme-aware evaluation metrics and text processing utilities for any language.

[![PyPI](https://img.shields.io/pypi/v/grapheme-kit)](https://pypi.org/project/grapheme-kit/)
[![Python](https://img.shields.io/pypi/pyversions/grapheme-kit)](https://pypi.org/project/grapheme-kit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**[Live Demo](https://grapheme-kit.pages.dev) · [Documentation](https://grapheme-kit-docs.pages.dev)**

---

## Why grapheme-kit?

Unicode text is complex: a single *visible* character (grapheme cluster) often spans multiple code points. Naive string operations get lengths, distances, and evaluation metrics wrong when combining marks, diacritics, or conjuncts are present.

`grapheme-kit` operates at the grapheme-cluster level, ensuring all measurements reflect human-perceived text structure, not raw byte or code point counts.

```python
from grapheme_kit import Graphemizer

# Burmese
g = Graphemizer("ကျွန်ုပ်")
len("ကျွန်ုပ်")     # 8 code points (naive)
len(g)           # 3 grapheme clusters (correct)

# Bengali
g = Graphemizer("নমস্কার")
len("নমস্কার")    # 5 code points (naive)
len(g)           # 7 grapheme clusters (correct)
```

---

## Installation

```bash
pip install grapheme-kit
```

```bash
# development
git clone https://github.com/vmenan/grapheme-kit.git
cd grapheme-kit
uv sync
```

---

## Features

### Segmentation
Split text from any script into correct grapheme clusters:
```python
from grapheme_kit import Graphemizer

# Hindi
g = Graphemizer("किताब")
g.graphemes   # ['कि', 'ता', 'ब']
len(g)        # 3

# Burmese
g = Graphemizer("ကျွန်ုပ်")
g.graphemes   # ['ကျွ', 'န်ု', 'ပ်']
len(g)        # 3
```

### String Distance
Grapheme-aware implementations of popular distance and similarity algorithms:
```python
from grapheme_kit import levenshtein
from grapheme_kit.distance import jaro_winkler, damerau_levenshtein

# Hebrew
levenshtein("שָׁלוֹם", "שָׁלוֹב")          # 1 (only one cluster differs)

# Arabic 
levenshtein("مُعَلِّمٌ", "مُعَلِّمُ")          # 1 (diacritic-level edit, one grapheme)

# Hindi
levenshtein("किताब", "कताब")          # 1 (one grapheme cluster removed)

# Latin/English
levenshtein("kitten", "sitting")       # 3
jaro_winkler("martha", "marhta")       # 0.9611
```

### Evaluation Metrics
Compute machine translation or text generation metrics based on grapheme clusters rather than character code points:
```python
from grapheme_kit.metric import GraphemeCHRF, CER, charbleu

# chrF
GraphemeCHRF().sentence_score("நல்ல", ["நல்ல மாணவன்"]).score  # 37.1051

# Character Error Rate (CER)
CER("كِتَابٌ", "كِتَابَ")  # 0.25

# CharBLEU
charbleu("the quick brown fox", "the quick red fox")  # 0.7086
```

### Decompose / Compose
Phonetic decomposition and composition across Indic scripts (Tamil, Sinhala, Devanagari/Hindi, Malayalam, Kannada):
```python
from grapheme_kit import decompose, compose

# Sinhala
decompose("කා")                                # 'ක්ආ'
compose("ක්ආ")                                 # 'කා'

# Tamil
compose(decompose("வணக்கம்")) == "வணக்கம்"       # True

# Hindi / Devanagari
decompose("किताब")                             # 'क्इत्आब्अ'
compose("क्इत्आब्अ")                           # 'किताब'
compose(decompose("भारत")) == "भारत"           # True

# Malayalam & Kannada
compose(decompose("നമസ്കാരം")) == "നമസ്കാരം"    # True
compose(decompose("ನಮಸ್ಕಾರ")) == "ನಮಸ್ಕಾರ"      # True
```

---

## Extensible Script-Aware Architecture

`grapheme-kit` is built on a modular, 5-layer object-oriented architecture designed for easy extension to new scripts without touching core logic:

1. **Core Contracts (`grapheme_kit.core`)**: `BaseNormalizer`, `BaseSegmenter`, `BaseComposer`, `BaseDecomposer`, `BaseScriptProfile`, `BaseScriptProcessor`.
2. **Reusable Indic Engines**: `IndicComposer`, `IndicDecomposer`, `RuleBasedSegmenter`, `UnicodeNormalizer`.
3. **Script Plugins (`grapheme_kit.scripts`)**: Isolated implementations for `tamil`, `sinhala`, `devanagari`, `malayalam`, `kannada`, and `generic`.
4. **Script Registry (`ScriptRegistry`)**: Automatic script detection, alias resolution, and dynamic plugin registration.
5. **Metric Base Contract (`grapheme_kit.metrics`)**: Concrete distance, similarity, and evaluation metrics inherit directly from the single `BaseMetric` abstraction.

### Supported Scripts Matrix

| Script | Languages | Unicode Range | Normalizer | Segmenter | Compose / Decompose |
|---|---|---|:---:|:---:|:---:|
| **Tamil** | Tamil | `U+0B80 - U+0BFF` | ✅ | ✅ | ✅ |
| **Sinhala** | Sinhala | `U+0D80 - U+0DFF` | ✅ | ✅ | ✅ |
| **Devanagari** | Hindi, Sanskrit, Marathi, Nepali | `U+0900 - U+097F` | ✅ | ✅ | ✅ |
| **Malayalam** | Malayalam | `U+0D00 - U+0D7F` | ✅ | ✅ | ✅ |
| **Kannada** | Kannada | `U+0C80 - U+0CFF` | ✅ | ✅ | ✅ |
| **Generic** | Latin, Arabic, Hebrew, Burmese, etc. | All Unicode | ✅ | ✅ | ✅ (Pass-through) |

### Adding a New Script in 4 Steps

```python
from grapheme_kit.core import BaseScriptProfile, BaseScriptProcessor, UnicodeNormalizer, UnicodeSegmenter, IndicComposer, IndicDecomposer, registry

# 1. Define script profile
profile = BaseScriptProfile(
    name="telugu",
    unicode_ranges=[(0x0C00, 0x0C7F)],
    virama="్",
    inherent_vowel="అ",
    consonants=["క", "ఖ", "గ", ...],
    vowels=["అ", "ఆ", "ఇ", ...],
    dependent_vowel_signs=["", "ా", "ి", ...],
)

# 2. Assemble processor
processor = BaseScriptProcessor(
    profile=profile,
    normalizer=UnicodeNormalizer(),
    segmenter=UnicodeSegmenter(),
    composer=IndicComposer(profile),
    decomposer=IndicDecomposer(profile),
)

# 3. Register into global registry
registry.register(processor, aliases=["te"])

# 4. Ready to use immediately!
from grapheme_kit import Graphemizer, decompose, compose
compose(decompose("తెలుగు")) == "తెలుగు"  # True
```

---

## Command Line

The package exposes a `grapheme-kit` executable with a short alias `gkit`:

```bash
gkit graphemize "مَرْحَبًا" --count
gkit graphemize "किताब" --count
gkit distance "שָׁלוֹם" "שָׁלוֹב" --level both
gkit evaluate "நல்ல மாணவன்" "நல்ல" --metric chrf
gkit decompose "ලංකාව" --round-trip
```

Use `gkit --help` or `gkit <command> --help` for the full list of commands and options.

---

## Documentation

Full documentation, guides, and API reference: [grapheme-kit-docs.pages.dev](https://grapheme-kit-docs.pages.dev)

Try it interactively in the [live demo](https://grapheme-kit.pages.dev/graphemizer/).

---

## Contributing

Issues and pull requests are welcome. Please open an issue first for major changes.

## License

MIT © grapheme-kit contributors. See [LICENSE](LICENSE) for details.
