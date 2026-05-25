from langchain.tools import tool
import requests
import html
import os
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Searches the web for recent and reliable information. Returns titles, URLs and snippets."""

    results = tavily.search(query=query, max_results=3).get("results", [])

    return "\n---\n".join(
        f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}"
        for r in results
    )


@tool
def scrape_url(url: str) -> str:
    """Scrapes and returns clean text content from a given URL for deeper reading."""
    try:
        response = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # strip noise tags before extracting text
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        return html.escape(soup.get_text(strip=True, separator=" ")[:3000])

    except Exception as e:
        return f"Could not scrape {url}. Error: {e}"
