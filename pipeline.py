from researchflow.service import run_research_pipeline


if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    result = run_research_pipeline(topic)
    print(result.get("final_report", ""))
