"""Devanagari grapheme segmenter with conjunct clustering rules."""

from __future__ import annotations

from grapheme_kit.core.segmenter import ClusterMergeRule, RuleBasedSegmenter


class DevanagariSegmenter(RuleBasedSegmenter):
    """Devanagari segmenter supporting traditional conjuncts (क्ष, त्र, ज्ञ, श्र)."""

    def __init__(self) -> None:
        super().__init__()

        # Rule 1: क् + ष... -> क्ष...
        self.add_rule(
            ClusterMergeRule(
                name="devanagari_ksha",
                condition=lambda curr, nxt: curr == "क्" and nxt.startswith("ष"),
            )
        )

        # Rule 2: त् + र... -> त्र...
        self.add_rule(
            ClusterMergeRule(
                name="devanagari_tra",
                condition=lambda curr, nxt: curr == "त्" and nxt.startswith("र"),
            )
        )

        # Rule 3: ज् + ञ... -> ज्ञ...
        self.add_rule(
            ClusterMergeRule(
                name="devanagari_gya",
                condition=lambda curr, nxt: curr == "ज्" and nxt.startswith("ञ"),
            )
        )

        # Rule 4: श् + र... -> श्र...
        self.add_rule(
            ClusterMergeRule(
                name="devanagari_shra",
                condition=lambda curr, nxt: curr == "श्" and nxt.startswith("र"),
            )
        )
