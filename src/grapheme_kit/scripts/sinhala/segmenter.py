"""Sinhala grapheme segmenter with rules for ZWJ sequences (Yansaya, Rakaransaya, Bandi akuru)."""

from __future__ import annotations

from grapheme_kit.core.segmenter import RuleBasedSegmenter, SegmentationRule


class SinhalaZWJRule(SegmentationRule):
    """Rule handling Sinhala Zero-Width Joiner (ZWJ) conjunct sequences."""

    def apply(self, clusters: list[str]) -> list[str]:
        if not clusters:
            return []

        original_clusters = list(clusters)
        result: list[str] = []
        i = 0
        n = len(original_clusters)

        while i < n:
            current = original_clusters[i]

            if i < n - 1:
                if "\u200d" in current:
                    if current == "ර්\u200d":
                        current = "ර්"
                        original_clusters[i] = current
                    i += 1
                    x = current

                    while i < n and "\u200d" in original_clusters[i - 1]:
                        x += original_clusters[i]
                        i += 1
                    result.append(x)
                    continue

            if i == n - 1 and "\u200d" in current:
                new_c = current.replace("\u200d", "")
                result.append(new_c)
            else:
                result.append(current)
            i += 1

        return result


class SinhalaSegmenter(RuleBasedSegmenter):
    """Sinhala grapheme segmenter applying Sinhala-specific ZWJ rules."""

    def __init__(self) -> None:
        super().__init__()
        self.add_rule(SinhalaZWJRule())
