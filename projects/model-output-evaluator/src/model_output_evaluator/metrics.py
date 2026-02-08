"""Metrics for comparing predicted and expected text outputs.

All metrics return a float between 0.0 and 1.0, where 1.0 indicates a perfect match.
"""


def exact_match(predicted: str, expected: str) -> float:
    """Return 1.0 if predicted exactly equals expected, 0.0 otherwise."""
    return 1.0 if predicted == expected else 0.0


def contains_match(predicted: str, expected: str) -> float:
    """Return 1.0 if expected is contained within predicted, 0.0 otherwise."""
    if not expected:
        return 1.0
    return 1.0 if expected in predicted else 0.0


def levenshtein_similarity(predicted: str, expected: str) -> float:
    """Compute similarity based on Levenshtein edit distance.

    Returns 1 - (edit_distance / max_len), so identical strings score 1.0
    and completely different strings score close to 0.0.
    """
    if predicted == expected:
        return 1.0
    max_len = max(len(predicted), len(expected))
    if max_len == 0:
        return 1.0
    distance = _levenshtein_distance(predicted, expected)
    return 1.0 - (distance / max_len)


def _levenshtein_distance(s: str, t: str) -> int:
    """Compute the Levenshtein edit distance between two strings."""
    n, m = len(s), len(t)
    if n == 0:
        return m
    if m == 0:
        return n

    prev = list(range(m + 1))
    curr = [0] * (m + 1)

    for i in range(1, n + 1):
        curr[0] = i
        for j in range(1, m + 1):
            cost = 0 if s[i - 1] == t[j - 1] else 1
            curr[j] = min(
                prev[j] + 1,
                curr[j - 1] + 1,
                prev[j - 1] + cost,
            )
        prev, curr = curr, prev

    return prev[m]


def jaccard_similarity(predicted: str, expected: str) -> float:
    """Compute token-level Jaccard similarity (intersection / union of word sets).

    Words are split on whitespace. Returns 1.0 for two empty strings.
    """
    pred_tokens = set(predicted.split())
    exp_tokens = set(expected.split())
    if not pred_tokens and not exp_tokens:
        return 1.0
    union = pred_tokens | exp_tokens
    if not union:
        return 1.0
    intersection = pred_tokens & exp_tokens
    return len(intersection) / len(union)


def bleu_score_simple(predicted: str, expected: str) -> float:
    """Compute a simplified unigram BLEU-like precision score.

    This calculates the proportion of predicted words that appear in the expected text.
    It is a simplified approximation and not a full BLEU implementation — it uses only
    unigram precision without brevity penalty or higher-order n-grams.

    Returns the count of overlapping words divided by the number of predicted words.
    Returns 1.0 if both strings are empty.
    """
    pred_tokens = predicted.split()
    exp_tokens = set(expected.split())
    if not pred_tokens and not exp_tokens:
        return 1.0
    if not pred_tokens:
        return 0.0
    matches = sum(1 for token in pred_tokens if token in exp_tokens)
    return matches / len(pred_tokens)


METRICS_REGISTRY: dict[str, callable] = {
    "exact_match": exact_match,
    "contains_match": contains_match,
    "levenshtein_similarity": levenshtein_similarity,
    "jaccard_similarity": jaccard_similarity,
    "bleu_score_simple": bleu_score_simple,
}

DEFAULT_METRICS = [
    "exact_match",
    "contains_match",
    "levenshtein_similarity",
    "jaccard_similarity",
]
