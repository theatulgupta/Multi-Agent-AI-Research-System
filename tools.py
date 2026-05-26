"""Web search and scraping tools for research pipeline."""
from langchain.tools import tool
import requests
import html
from bs4 import BeautifulSoup
from tavily import TavilyClient
from researchflow.env import get_api_key

tavily = TavilyClient(get_api_key("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Searches the web for recent and reliable information.
    
    Args:
        query: Search query string
        
    Returns:
        Formatted search results with titles, URLs and snippets
    """
    try:
        results = tavily.search(query=query, max_results=3).get("results", [])
        
        if not results:
            return "No search results found."
        
        return "\n---\n".join(
            f"Title: {r.get('title', 'N/A')}\nURL: {r.get('url', 'N/A')}\nSnippet: {r.get('content', '')[:300]}"
            for r in results
        )
    except Exception as e:
        return f"Search failed: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """Scrapes and returns clean text content from a given URL.
    
    Args:
        url: URL to scrape
        
    Returns:
        Cleaned text content from the webpage (max 3000 chars)
    """
    if not url or not url.startswith(('http://', 'https://')):
        return f"Invalid URL: {url}"
    
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove noise tags before extracting text
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        text = soup.get_text(strip=True, separator=" ")
        
        if not text:
            return f"No content extracted from {url}"
        
        # Escape HTML and limit length
        return html.escape(text[:3000])

    except requests.Timeout:
        return f"Timeout while scraping {url}"
    except requests.RequestException as e:
        return f"Could not scrape {url}. Error: {str(e)}"
    except Exception as e:
        return f"Unexpected error scraping {url}: {str(e)}"
