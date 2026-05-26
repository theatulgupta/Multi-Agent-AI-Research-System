# ResearchFlow

ResearchFlow is a dark, professional research workspace that searches sources, extracts evidence, drafts a report, reviews it, and publishes a final revision.

## Flow

```
Topic Brief → Search → Scrape → Draft → Review → Revise → Final Report
```

## Run

```bash
streamlit run app.py
```

## Project Structure

- `app.py` - thin Streamlit entrypoint
- `researchflow/app.py` - main UI assembly and workflow wiring
- `researchflow/ui.py` - reusable UI components and process tracker
- `researchflow/service.py` - pipeline execution and scoring helpers
- `researchflow/theme.py` - shared dark theme and styling
- `researchflow/config.py` - app metadata and UI constants

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file with your API keys:

```
TAVILY_API_KEY=<your_key>
MISTRAL_API_KEY=<your_key>
```

## Stack

- LangChain for agent and chain orchestration
- LangGraph for agent execution via `create_agent`
- Mistral AI for the language model
- Tavily for web search
- BeautifulSoup4 for web scraping
