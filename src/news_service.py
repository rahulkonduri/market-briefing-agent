import requests
from typing import List, Dict, Any
from .config import config
from .utils.logger import setup_logger

logger = setup_logger(__name__)

class NewsFetcher:
    """Service to fetch and filter market news using NewsAPI.org."""
    
    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        self.api_key = config.NEWS_API_KEY
        self.query = config.NEWS_QUERY

    def fetch_latest_news(self, page_size: int = 10) -> List[Dict[str, Any]]:
        """
        Fetches the latest news articles based on the configured query.
        Returns a list of articles.
        Njuhabgd oyiuou zdfyid yh
        """
        if not self.api_key:
            logger.error("NEWS_API_KEY is missing from configuration!")
            raise ValueError("NEWS_API_KEY is not configured.")

        params = {
            "q": self.query,
            "apiKey": self.api_key,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size
        }

        try:
            logger.info(f"Fetching news from NewsAPI.org for query: '{self.query}'")
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get("articles", [])
            
            if not articles:
                logger.warning("NewsAPI.org returned zero articles.")
                return []
                
            filtered_articles = self._filter_and_format(articles)
            logger.info(f"Successfully fetched and formatted {len(filtered_articles)} articles.")
            return filtered_articles
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch news from API: {e}")
            raise

    def _filter_and_format(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out articles with missing critical fields."""
        formatted = []
        for article in articles:
            # Skip [Removed] articles or articles missing title/url
            if article.get("title") == "[Removed]" or not article.get("title") or not article.get("url"):
                continue
                
            formatted.append({
                "title": article.get("title", "No Title"),
                "description": article.get("description", "No Description"),
                "url": article.get("url", "#"),
                "source": article.get("source", {}).get("name", "Unknown Source")
            })
            
        return formatted
