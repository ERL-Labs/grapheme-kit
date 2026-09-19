"""Standardized Grapheme Clustering delegating to script segmenter rules."""

from __future__ import annotations

import grapheme
from grapheme_kit.core.registry import registry
from grapheme_kit.scripts import register_builtin_scripts

# Ensure built-in scripts are registered
register_builtin_scripts()


class GraphemeSplitter:
    """Standardized Grapheme Clustering class.
    Extends 'grapheme' library to handle Indic conjuncts (e.g. க்ஷ, ஸ்ரீ, ஶ்ரீ, क्ष, त्र, ज्ञ, श्र)
    and Sinhala ZWJ sequences.
    """

    @staticmethod
    def split(string: str) -> list[str]:
        """Returns a list of grapheme clusters from the given string."""
        if not string or string is None:
            return []

        original_clusters = list(grapheme.graphemes(string))
        result: list[str] = []
        i = 0
        n = len(original_clusters)

        while i < n:
            current = original_clusters[i]

            if i < n - 1:
                next_cluster = original_clusters[i + 1]

                # Tamil conjunct merges
                # Case 1: க் + ஷ... -> க்ஷ...
                if current == "க்" and next_cluster.startswith("ஷ"):
                    result.append(current + next_cluster)
                    i += 2
                    continue

                # Case 2: ஸ் + ரீ -> ஸ்ரீ
                if current == "ஸ்" and next_cluster == "ரீ":
                    result.append(current + next_cluster)
                    i += 2
                    continue

                # Case 3: ஶ் + ரீ -> ஶ்ரீ
                if current == "ஶ்" and next_cluster == "ரீ":
                    result.append(current + next_cluster)
                    i += 2
                    continue

                # Devanagari conjunct merges
                if current == "क्" and next_cluster.startswith("ष"):
                    result.append(current + next_cluster)
                    i += 2
                    continue
                if current == "त्" and next_cluster.startswith("र"):
                    result.append(current + next_cluster)
                    i += 2
                    continue
                if current == "ज्" and next_cluster.startswith("ञ"):
                    result.append(current + next_cluster)
                    i += 2
                    continue
                if current == "श्" and next_cluster.startswith("र"):
                    result.append(current + next_cluster)
                    i += 2
                    continue

                # Sinhala ZWJ sequence handling
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

            # End-of-string trailing ZWJ cleanup (Sinhala)
            if i == n - 1 and "\u200d" in current:
                new = current.replace("\u200d", "")
                result.append(new)
            else:
                result.append(current)
            i += 1

        return result