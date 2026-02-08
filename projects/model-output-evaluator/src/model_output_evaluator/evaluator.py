"""Core evaluation logic for comparing model predictions against references."""

from dataclasses import dataclass, field

from model_output_evaluator.metrics import DEFAULT_METRICS, METRICS_REGISTRY


@dataclass
class EvalResult:
    """Result of evaluating a single prediction against its reference."""

    predicted: str
    expected: str
    scores: dict[str, float] = field(default_factory=dict)


@dataclass
class EvalSummary:
    """Summary of evaluation across all prediction-reference pairs."""

    results: list[EvalResult] = field(default_factory=list)
    avg_scores: dict[str, float] = field(default_factory=dict)
    metric_names: list[str] = field(default_factory=list)


def evaluate(
    predictions: list[str],
    references: list[str],
    metrics: list[str] | None = None,
) -> EvalSummary:
    """Evaluate predictions against references using the specified metrics.

    Args:
        predictions: List of predicted strings from the model.
        references: List of expected reference strings.
        metrics: Optional list of metric names to use. Defaults to
            exact_match, contains_match, levenshtein_similarity, jaccard_similarity.

    Returns:
        An EvalSummary with per-pair results and averaged scores.

    Raises:
        ValueError: If predictions and references have different lengths,
            or if an unknown metric name is provided.
    """
    if len(predictions) != len(references):
        raise ValueError(
            f"Predictions ({len(predictions)}) and references ({len(references)}) "
            f"must have the same length."
        )

    metric_names = metrics if metrics is not None else list(DEFAULT_METRICS)
    for name in metric_names:
        if name not in METRICS_REGISTRY:
            raise ValueError(
                f"Unknown metric: '{name}'. "
                f"Available metrics: {', '.join(METRICS_REGISTRY.keys())}"
            )

    metric_fns = {name: METRICS_REGISTRY[name] for name in metric_names}
    results: list[EvalResult] = []

    for pred, ref in zip(predictions, references):
        scores = {name: fn(pred, ref) for name, fn in metric_fns.items()}
        results.append(EvalResult(predicted=pred, expected=ref, scores=scores))

    avg_scores: dict[str, float] = {}
    if results:
        for name in metric_names:
            total = sum(r.scores[name] for r in results)
            avg_scores[name] = total / len(results)
    else:
        avg_scores = {name: 0.0 for name in metric_names}

    return EvalSummary(results=results, avg_scores=avg_scores, metric_names=metric_names)
