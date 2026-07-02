"""HuggingFace Transformers zero-shot failure classifier with rule-based fallback."""

from __future__ import annotations

from functools import lru_cache

# Human-readable labels for zero-shot -> internal category codes.
CATEGORIES = {
    "flaky ui timing issue": "flaky-ui",
    "real product defect or regression": "product-defect",
    "broken test locator after ui change": "locator-issue",
    "asynchronous processing timing issue": "async-timing",
    "infrastructure or environment outage": "infra",
}

_RULES = [
    ("infra", ["connection refused", "err_connection", "dns", "502", "503", "environment down"]),
    ("product-defect", ["500", "internal server error", "null pointer", "regression", "sla", "exceeded"]),
    ("locator-issue", ["strict mode violation", "resolved to", "selector", "locator"]),
    ("async-timing", ["pending", "eventually", "poll", "async", "still processing"]),
    ("flaky-ui", ["timeout", "not visible", "intermittent", "flaky", "iframe"]),
]


@lru_cache(maxsize=1)
def _hf_pipeline():
    from transformers import pipeline

    return pipeline(
        "zero-shot-classification",
        model="typeform/distilbert-base-uncased-mnli",
    )


def classify_rule_based(text: str) -> tuple[str, float]:
    lowered = text.lower()
    for category, keywords in _RULES:
        hits = sum(1 for kw in keywords if kw in lowered)
        if hits:
            return category, min(0.5 + 0.15 * hits, 0.95)
    return "unknown", 0.3


HF_MIN_CONFIDENCE = 0.5


def classify(text: str, use_hf: bool = True) -> dict:
    """Return {category, confidence, engine}.

    Hybrid strategy: try the HuggingFace zero-shot model first; if it is
    unavailable or not confident enough, fall back to deterministic rules.
    """
    if use_hf:
        try:
            result = _hf_pipeline()(text, candidate_labels=list(CATEGORIES.keys()))
            confidence = round(float(result["scores"][0]), 3)
            if confidence >= HF_MIN_CONFIDENCE:
                return {
                    "category": CATEGORIES[result["labels"][0]],
                    "confidence": confidence,
                    "engine": "huggingface-zero-shot",
                }
        except Exception:
            pass  # no torch / offline -> fall back to rules

    category, confidence = classify_rule_based(text)
    engine = "hybrid-rule-fallback" if use_hf else "rule-based"
    return {"category": category, "confidence": confidence, "engine": engine}
