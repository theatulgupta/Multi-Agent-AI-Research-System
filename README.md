# Multi-Agent AI Research System

A multi-agent pipeline that researches any topic and produces a reviewed, revised research report — fully automated.

## How it works

```
User Input → Search Agent → Scrape Agent → Writer → Critic → Revision → Final Report
```

1. **Search Agent** — uses Tavily to find recent, reliable sources
2. **Scrape Agent** — picks the best URL and extracts full page content
3. **Writer Chain** — drafts a structured research report from the gathered material
4. **Critic Chain** — reviews the report for accuracy, depth, and clarity
5. **Revision Chain** — rewrites the report based on critic feedback

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file with your API keys:

```
TAVILY_API_KEY=<your_key>
MISTRAL_API_KEY=<your_key>
```

## Run

```bash
python pipeline.py
```

You'll be prompted to enter a research topic. The final revised report is printed at the end.

## Stack

- [LangChain](https://github.com/langchain-ai/langchain) — agent and chain orchestration
- [LangGraph](https://github.com/langchain-ai/langgraph) — agent execution via `create_agent`
- [Mistral AI](https://mistral.ai/) — LLM (`mistral-small`)
- [Tavily](https://tavily.com/) — web search API
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — web scraping
