"""LangGraph agentic workflow: autonomous triage with CI/CD decision gate.

Flow:
    classify -> retrieve -> generate_analysis -> decide
        confident      -> auto_action  -> report
        low confidence -> human_review -> report
"""

from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph

from classifier import classify
from knowledge_base import format_context, retrieve
from llm_client import generate_triage, llm_available

CONFIDENCE_THRESHOLD = 0.6

# CI decision policy: failure category -> advisory pipeline action.
CI_ACTIONS = {
    "infra": "rerun_after_health_check",
    "flaky-ui": "quarantine_and_ticket",
    "locator-issue": "open_page_object_fix_pr",
    "async-timing": "add_polling_and_rerun",
    "product-defect": "block_merge_and_file_defect",
    "unknown": "human_review",
}


class TriageState(TypedDict, total=False):
    failure_text: str
    use_hf: bool
    category: str
    confidence: float
    engine: str
    similar_incidents: list[str]
    context: str
    analysis: str
    llm_mode: str
    route: str
    ci_action: str
    report: dict


def classify_node(state: TriageState) -> TriageState:
    return {**state, **classify(state["failure_text"], use_hf=state.get("use_hf", True))}


def retrieve_node(state: TriageState) -> TriageState:
    chunks = retrieve(state["failure_text"], top_k=3)
    return {
        **state,
        "similar_incidents": [c["id"] for c in chunks],
        "context": format_context(chunks),
    }


def generate_node(state: TriageState) -> TriageState:
    analysis = generate_triage(
        failure=state["failure_text"],
        category=state["category"],
        confidence=state["confidence"],
        context=state["context"],
    )
    return {**state, "analysis": analysis, "llm_mode": "llm" if llm_available() else "offline"}


def decide_node(state: TriageState) -> TriageState:
    low_confidence = state["confidence"] < CONFIDENCE_THRESHOLD or state["category"] == "unknown"
    return {**state, "route": "human_review" if low_confidence else "auto_action"}


def auto_action_node(state: TriageState) -> TriageState:
    return {**state, "ci_action": CI_ACTIONS.get(state["category"], "human_review")}


def human_review_node(state: TriageState) -> TriageState:
    return {**state, "ci_action": "human_review"}


def report_node(state: TriageState) -> TriageState:
    return {
        **state,
        "report": {
            "failure": state["failure_text"][:120],
            "category": state["category"],
            "confidence": state["confidence"],
            "classifier_engine": state["engine"],
            "similar_incidents": state["similar_incidents"],
            "analysis": state["analysis"],
            "llm_mode": state["llm_mode"],
            "route": state["route"],
            "ci_action": state["ci_action"],
            "advisory": "AI recommendation only - hard CI gates still apply",
        },
    }


def build_graph():
    graph = StateGraph(TriageState)
    graph.add_node("classify", classify_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate_analysis", generate_node)
    graph.add_node("decide", decide_node)
    graph.add_node("auto_action", auto_action_node)
    graph.add_node("human_review", human_review_node)
    graph.add_node("report", report_node)

    graph.set_entry_point("classify")
    graph.add_edge("classify", "retrieve")
    graph.add_edge("retrieve", "generate_analysis")
    graph.add_edge("generate_analysis", "decide")
    graph.add_conditional_edges(
        "decide",
        lambda s: s["route"],
        {"auto_action": "auto_action", "human_review": "human_review"},
    )
    graph.add_edge("auto_action", "report")
    graph.add_edge("human_review", "report")
    graph.add_edge("report", END)
    return graph.compile()


def run_triage(failure_text: str, use_hf: bool = True) -> dict:
    app = build_graph()
    final_state = app.invoke({"failure_text": failure_text, "use_hf": use_hf})
    return final_state["report"]
