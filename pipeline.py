from agents import (
    build_search_agent,
    build_scrape_agent,
    writer_chain,
    critic_chain,
    revision_chain
)

import time
from typing import Any
from httpx import HTTPStatusError


def _invoke_with_retry(runnable, payload, retries: int = 2, delay: float = 3.0) -> Any:
    """Retries on rate limit errors (HTTP 429) with a short delay."""
    for attempt in range(retries):
        try:
            return runnable.invoke(payload)
        except HTTPStatusError as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            if status == 429 and attempt < retries - 1:
                time.sleep(delay)
                continue
            raise


def run_research_pipeline(topic: str) -> dict:

    state = {}

    # ----------------------------------------------------------
    # Step 1: Search Agent — find relevant sources on the topic
    # ----------------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 1 : SEARCH AGENT")
    print("=" * 60)

    search_agent = build_search_agent()

    search_response = _invoke_with_retry(search_agent, {
        "messages": [(
            "user",
            f"Find recent, reliable, and detailed information about:\n\nTOPIC: {topic}\n\nFocus on trusted sources, factual information, useful URLs, and recent developments."
        )]
    })

    state["search_result"] = search_response["messages"][-1].content
    print("\nSEARCH RESULT:\n")
    print(state["search_result"])

    # ----------------------------------------------------------
    # Step 2: Scrape Agent — extract full content from best URL
    # ----------------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 2 : SCRAPE AGENT")
    print("=" * 60)

    scrape_agent = build_scrape_agent()

    scrape_response = _invoke_with_retry(scrape_agent, {
        "messages": [(
            "user",
            f"From the search results below, pick the best URL and use scrape_url to extract its content.\n\nSEARCH RESULTS:\n{state['search_result'][:1500]}"
        )]
    })

    state["scrape_result"] = scrape_response["messages"][-1].content
    print("\nSCRAPE RESULT:\n")
    print(state["scrape_result"])

    # combine both sources for downstream chains
    research = f"SEARCH RESULTS:\n{state['search_result']}\n\nSCRAPED CONTENT:\n{state['scrape_result']}"

    # ----------------------------------------------------------
    # Step 3: Writer Chain — draft the research report
    # ----------------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 3 : WRITER CHAIN")
    print("=" * 60)

    state["report"] = _invoke_with_retry(writer_chain, {
        "topic": topic,
        "research": research
    })

    print("\nWRITER OUTPUT:\n")
    print(state["report"])

    # ----------------------------------------------------------
    # Step 4: Critic Chain — review and score the report
    # ----------------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 4 : CRITIC CHAIN")
    print("=" * 60)

    state["feedback"] = _invoke_with_retry(critic_chain, {
        "topic": topic,
        "research": research,
        "report": state["report"]
    })

    print("\nCRITIC OUTPUT:\n")
    print(state["feedback"])

    # ----------------------------------------------------------
    # Step 5: Revision Chain — improve report based on feedback
    # ----------------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 5 : REVISION CHAIN")
    print("=" * 60)

    state["final_report"] = _invoke_with_retry(revision_chain, {
        "topic": topic,
        "report": state["report"],
        "research": research,
        "feedback": state["feedback"]
    })

    print("\nFINAL REPORT:\n")
    print(state["final_report"])

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ").strip()
    if not topic:
        print("No topic provided. Exiting.")
    else:
        run_research_pipeline(topic)
