from openai import OpenAI
from typing import List, Dict, Any
from .config import config
from .utils.logger import setup_logger

logger = setup_logger(__name__)

class AISummarizer:
    """Service to summarize news articles using an LLM (OpenAI)."""

    def __init__(self):
        self.api_key = config.OPENAI_API_KEY
        if not self.api_key:
            logger.error("OPENAI_API_KEY is missing from configuration!")
            
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def summarize(self, articles: List[Dict[str, Any]]) -> str:
        """
        Takes a list of articles, builds a prompt, and calls OpenAI to summarize.
        Returns HTML-formatted summary ready for email body.
        """
        if not articles:
            logger.warning("No articles provided for summarization.")
            return "<p>No significant market news to report today.</p>"
            
        if not self.client:
            raise ValueError("Cannot summarize because OPENAI_API_KEY is not configured.")

        # Prepare context
        context_parts = []
        for i, article in enumerate(articles, 1):
            context_parts.append(
                f"Article {i}:\n"
                f"Source: {article.get('source', 'Unknown')}\n"
                f"Title: {article.get('title', 'No Title')}\n"
                f"Description: {article.get('description', 'No Description')}\n"
                f"URL: {article.get('url', '#')}\n"
            )
        
        context_text = "\n".join(context_parts)
        
        prompt = f"""
You are an expert Wall Street financial analyst and executive assistant.
I am providing you with today's top market and business news articles. 
Your task is to analyze them and write a comprehensive, compelling Daily Briefing.

Articles:
{context_text}

Instructions:
1. **Market Overview & Analysis**: Provide a cohesive paragraph synthesizing the general mood/trends and what they mean for the market today.
2. **Top Impactful Stories**: Identify the 3-5 most important stories. For each, provide a bullet point with a bold title, a concise 2-sentence summary, and an HTML hyperlink to the original URL.
3. **Stock Movements (Rose / Fell)**: Based on the news context, explicitly list a few specific stocks that rose and stocks that fell (or are expected to fall), explaining briefly why. 
4. **Sector Predictions**: Based on these events, predict which specific market sectors (e.g., Tech, Energy, Pharma) will experience the highest fluctuation or volume during the current day's open.
5. **Stock Recommendations**: Provide 2-3 specific stock recommendations or "watch-list" targets based on the current news cycle's momentum.
6. Output your response entirely in clean, professional HTML (using <h2>, <h3>, <p>, <ul>, <li>, <strong>, <a> tags) so it renders beautifully in an email.
7. Do NOT include ```html markdown formatting blocks in your output. Just return the raw HTML string.
"""
        
        try:
            logger.info("Sending summarization request to OpenAI API.")
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful financial assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
            )
            
            logger.info("Successfully generated summary.")
            
            summary = response.choices[0].message.content
            # Clean up potential markdown formatting
            if summary.startswith("```html"):
                summary = summary.replace("```html", "", 1)
            if summary.endswith("```"):
                summary = summary[::-1].replace("```", "", 1)[::-1]
                
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Error communicating with OpenAI API: {e}")
            raise
