import argparse
import sys
from src.utils.logger import setup_logger
from src.news_service import NewsFetcher
from src.ai_service import AISummarizer
from src.market_service import MarketService
from src.email_service import EmailSender

logger = setup_logger(__name__)

def run(dry_run: bool = False):
    """
    Main orchestration function.
    1. Fetches news
    2. Fetches live indices
    3. Summarizes it via LLM
    4. Sends it via Email
    """
    logger.info("Initializing Morning Market AI Agent...")
    
    try:
        # Step 1: Fetch News
        news_fetcher = NewsFetcher()
        logger.info("Starting Phase 1: Data Ingestion")
        articles = news_fetcher.fetch_latest_news(page_size=15)
        
        if not articles:
            logger.warning("No articles fetched. Exiting early.")
            sys.exit(0)

        # Step 1.5: Fetch Live Indices
        logger.info("Starting Phase 1.5: Live Market Indices Ingestion")
        market_service = MarketService()
        indices_html = market_service.fetch_live_indices_html()

        # Step 2: AI Summarization
        summarizer = AISummarizer()
        logger.info("Starting Phase 2: AI Summarization")
        summary_html = summarizer.summarize(articles)
        
        # Combine the content
        final_html_content = indices_html + "\n<hr>\n" + summary_html

        # Step 3: Delivery
        logger.info("Starting Phase 3: Delivery")
        if dry_run:
            logger.info("Dry run enabled. Skipping email delivery.")
            print("\n" + "="*50)
            print("GENERATED HTML SUMMARY:")
            print("="*50)
            print(final_html_content)
            print("="*50 + "\n")
        else:
            email_sender = EmailSender()
            email_sender.send_daily_briefing(final_html_content)
            
        logger.info("Morning Market AI Agent completed successfully.")
        
    except ValueError as val_err:
        logger.error(f"Configuration Error: {val_err}")
        logger.error("Please ensure your .env file is fully populated.")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"An unexpected error occurred during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Morning Market AI Agent")
    parser.add_argument("--dry-run", action="store_true", help="Run without sending an email and print the HTML locally.")
    args = parser.parse_args()
    
    run(dry_run=args.dry_run)