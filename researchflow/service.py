"""Pipeline execution service with retry logic and progress tracking."""
from __future__ import annotations

import time
import logging
from typing import Any, Callable

from httpx import HTTPStatusError

from agents import build_scrape_agent, build_search_agent, critic_chain, revision_chain, writer_chain

ProgressCallback = Callable[[int, str, str], None]

logger = logging.getLogger(__name__)


def _invoke_with_retry(runnable, payload, retries: int = 3, delay: float = 2.0) -> Any:
    """Invoke a runnable with retry logic for rate limiting.
    
    Args:
        runnable: LangChain runnable to invoke
        payload: Input payload
        retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
        
    Returns:
        Response from the runnable
        
    Raises:
        HTTPStatusError: If all retries fail
    """
    last_error = None
    
    for attempt in range(retries):
        try:
            return runnable.invoke(payload)
        except HTTPStatusError as exc:
            last_error = exc
            status = getattr(getattr(exc, "response", None), "status_code", None)
            
            if status == 429 and attempt < retries - 1:
                wait_time = delay * (attempt + 1)  # Exponential backoff
                logger.warning(f"Rate limited. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            raise
        except Exception as e:
            logger.error(f"Unexpected error in invoke: {e}")
            raise
    
    if last_error:
        raise last_error


def _response_text(response: Any) -> str:
    """Extract text content from various response formats.
    
    Args:
        response: Response from agent or chain
        
    Returns:
        Extracted text content
    """
    if isinstance(response, dict):
        messages = response.get("messages", [])
        if messages:
            last_msg = messages[-1]
            return getattr(last_msg, "content", str(last_msg))
    
    content = getattr(response, "content", None)
    if content is not None:
        return str(content)
    
    return str(response)


def run_research_pipeline(
    topic: str,
    *,
    max_results: int = 3,
    scrape_limit: int = 3000,
    progress: ProgressCallback | None = None,
) -> dict[str, Any]:
    """Execute the full research pipeline.
    
    Args:
        topic: Research topic to investigate
        max_results: Maximum number of search results
        scrape_limit: Character limit for scraped content
        progress: Optional callback for progress updates
        
    Returns:
        Dictionary containing all pipeline outputs
        
    Raises:
        Exception: If any pipeline step fails
    """
    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty")
    
    state: dict[str, Any] = {}

    def emit(step: int, status: str, message: str) -> None:
        if progress is not None:
            try:
                progress(step, status, message)
            except Exception as e:
                logger.error(f"Progress callback error: {e}")

    try:
        # Step 1: Search
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

        # Step 2: Scrape
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

        # Step 3: Write
        emit(2, "running", "Drafting the report")
        state["report"] = _response_text(
            _invoke_with_retry(writer_chain, {"topic": topic, "research": research})
        )
        emit(2, "done", "Draft complete")

        # Step 4: Critique
        emit(3, "running", "Reviewing the draft")
        state["feedback"] = _response_text(
            _invoke_with_retry(
                critic_chain, 
                {"topic": topic, "research": research, "report": state["report"]}
            )
        )
        emit(3, "done", "Review complete")

        # Step 5: Revise
        emit(4, "running", "Applying final revisions")
        state["final_report"] = _response_text(
            _invoke_with_retry(
                revision_chain, 
                {
                    "topic": topic, 
                    "report": state["report"], 
                    "research": research, 
                    "feedback": state["feedback"]
                }
            )
        )
        emit(4, "done", "Revision complete")

        return state
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


def extract_scores(feedback: str) -> dict[str, int]:
    """Extract numeric scores from critic feedback.
    
    Args:
        feedback: Critic feedback text
        
    Returns:
        Dictionary mapping metric names to scores
    """
    import re

    scores: dict[str, int] = {}
    metrics = [
        "Accuracy", "Depth", "Clarity", 
        "Source Usage", "Insight Quality", "Overall Quality"
    ]
    
    for metric in metrics:
        match = re.search(rf"{metric}[:\s]+(\d+)/10", feedback, re.IGNORECASE)
        if match:
            try:
                scores[metric] = int(match.group(1))
            except ValueError:
                logger.warning(f"Could not parse score for {metric}")
    
    return scores


def extract_verdict(feedback: str) -> str:
    """Extract final verdict from critic feedback.
    
    Args:
        feedback: Critic feedback text
        
    Returns:
        Verdict string (Accept, Minor Revision, Major Revision, Reject, or Unknown)
    """
    verdicts = ["Accept", "Minor Revision", "Major Revision", "Reject"]
    
    for verdict in verdicts:
        if verdict.lower() in feedback.lower():
            return verdict
    
    return "Unknown"


def score_color(val: int) -> str:
    """Get CSS class for score color coding.
    
    Args:
        val: Score value (0-10)
        
    Returns:
        CSS class name
    """
    if val >= 8:
        return "score-high"
    if val >= 6:
        return "score-mid"
    return "score-low"
