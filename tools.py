from langchain.tools import tool
import requests
import html
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv
from rich import print
import os

load_dotenv()

# Initialize Tavily client
tavily = TavilyClient(os.getenv("TAVILY_API_KEY"))


# Web search tool to get results for a query
@tool
def web_search(query: str) -> str:
  """Searches the web for recent and reliable information for the query. Returns Titles, URLs and snippets."""

  search_results = tavily.search(query=query, max_results=3)

  out = [
    f"Title: {result['title']}\nURL: {result['url']}\nSnippet: {result['content'][:300]}\n"
    for result in search_results.get("results", [])
  ]

  return "\n------------------------\n".join(out)


# Extract information from a website using bs4
@tool
def scrape_url(url: str) -> str:
  """Scrapes and returns clean text content from a given URL for deeper reading."""
  try:
    response = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav","footer"]):
      tag.decompose()

    return html.escape(soup.get_text(strip=True, separator=" ")[:3000])

  except Exception as e:
    return f"Could not scrape {url}. Error: {e}"
