from agents import build_search_agent, build_scrape_agent, writer_chain, critic_chain, revision_chain


def run_research_pipeline(topic: str) -> dict:
  state = {}

  # Search Agent Working
  print("\n" + "="*50)
  print("Step 1 : Search Agent is working...")
  print("\n" + "="*50)


  search_agent = build_search_agent()
  # call the agent with a plain string input to satisfy the invoke signature
  result = search_agent.invoke(f"Find recent, reliable and detailed information about: {topic}.")

  # store the agent's response (string or simple object) as search results
  state["search_results"] = result

  print()
