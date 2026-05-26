from __future__ import annotations

import time
from typing import Any, Callable

from httpx import HTTPStatusError

from agents import build_scrape_agent, build_search_agent, critic_chain, revision_chain, writer_chain

ProgressCallback = Callable[[int, str, str], None]


def _invoke_with_retry(runnable, payload, retries: int = 2, delay: float = 3.0) -> Any:
    for attempt in range(retries):
        try:
            return runnable.invoke(payload)
        except HTTPStatusError as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            if status == 429 and attempt < retries - 1:
                time.sleep(delay)
                continue
            raise


def _response_text(response: Any) -> str:
    if isinstance(response, dict):
        messages = response.get("messages", [])
        if messages:
            return getattr(messages[-1], "content", str(messages[-1]))
    content = getattr(response, "content", None)
    if content is not None:
        return content
    return str(response)


def run_research_pipeline(
    topic: str,
    *,
    max_results: int = 3,
    scrape_limit: int = 3000,
    progress: ProgressCallback | None = None,
) -> dict[str, Any]:
    state: dict[str, Any] = {}

    def emit(step: int, status: str, message: str) -> None:
        if progress is not None:
            progress(step, status, message)

    emit(0, "running", "Searching the web for credible sources")
    search_agent = build_search_agent()
    search_response = _invoke_with_retry(
        search_agent,
        {
            "messages": [
                (
                    "user",
                    f"Find the top {max_results} recent, reliable, and detailed sources about:\n\nTOPIC: {topic}\n\nFocus on trusted sources, factual information, useful URLs, and recent developments.",
                )
            ]
        },
    )
    state["search_result"] = _response_text(search_response)
    emit(0, "done", "Search complete")

    emit(1, "running", "Extracting the strongest source")
    scrape_agent = build_scrape_agent()
    scrape_response = _invoke_with_retry(
        scrape_agent,
        {
            "messages": [
                (
                    "user",
                    f"From the search results below, pick the best URL and use scrape_url to extract its content.\n\nSEARCH RESULTS:\n{state['search_result'][:scrape_limit]}",
                )
            ]
        },
    )
    state["scrape_result"] = _response_text(scrape_response)
    emit(1, "done", "Scrape complete")

    research = f"SEARCH RESULTS:\n{state['search_result']}\n\nSCRAPED CONTENT:\n{state['scrape_result']}"

    emit(2, "running", "Drafting the report")
    state["report"] = _response_text(_invoke_with_retry(writer_chain, {"topic": topic, "research": research}))
    emit(2, "done", "Draft complete")

    emit(3, "running", "Reviewing the draft")
    state["feedback"] = _response_text(_invoke_with_retry(critic_chain, {"topic": topic, "research": research, "report": state["report"]}))
    emit(3, "done", "Review complete")

    emit(4, "running", "Applying final revisions")
    state["final_report"] = _response_text(
        _invoke_with_retry(revision_chain, {"topic": topic, "report": state["report"], "research": research, "feedback": state["feedback"]})
    )
    emit(4, "done", "Revision complete")

    return state


def extract_scores(feedback: str) -> dict[str, int]:
    import re

    scores: dict[str, int] = {}
    for metric in ["Accuracy", "Depth", "Clarity", "Source Usage", "Insight Quality", "Overall Quality"]:
        match = re.search(rf"{metric}[:\s]+(\d+)/10", feedback, re.IGNORECASE)
        if match:
            scores[metric] = int(match.group(1))
    return scores


def extract_verdict(feedback: str) -> str:
    for verdict in ["Accept", "Minor Revision", "Major Revision", "Reject"]:
        if verdict.lower() in feedback.lower():
            return verdict
    return "Unknown"


def score_color(val: int) -> str:
    if val >= 8:
        return "score-high"
    if val >= 6:
        return "score-mid"
    return "score-low"
