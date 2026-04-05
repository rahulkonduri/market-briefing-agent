import yfinance as yf
from .utils.logger import setup_logger

logger = setup_logger(__name__)

class MarketService:
    """Service to fetch live data for Indian Market Indices using yfinance."""

    def __init__(self):
        # Ticker symbols for NIFTY 50, BSE SENSEX, and Nifty Bank
        self.indices = {
            "NIFTY 50": "^NSEI",
            "BSE SENSEX": "^BSESN",
            "NIFTY BANK": "^NSEBANK"
        }

    def fetch_live_indices_html(self) -> str:
        """
        Fetches the latest closing price and percentage change for key Indian indices.
        Returns a beautifully formatted HTML block to append to the email.
        """
        logger.info("Fetching live Indian market indices via yfinance...")
        html_blocks = []

        html_blocks.append('<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">')
        html_blocks.append('<h3 style="margin-top: 0; color: #2B547E;">📊 Live Market Indices</h3>')
        html_blocks.append('<ul style="list-style-type: none; padding-left: 0;">')

        for name, symbol in self.indices.items():
            try:
                ticker = yf.Ticker(symbol)
                # Get the last 2 days to calculate change if current price is unavailable, but usually fast_info or history works best
                hist = ticker.history(period="2d")
                
                if len(hist) >= 2:
                    current_price = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]
                    
                    change = current_price - prev_close
                    pct_change = (change / prev_close) * 100
                    
                    color = "green" if change >= 0 else "red"
                    arrow = "▲" if change >= 0 else "▼"
                    
                    html_blocks.append(
                        f'<li style="margin-bottom: 8px;">'
                        f'<strong>{name}:</strong> {current_price:,.2f} '
                        f'<span style="color: {color}; font-weight: bold;">{arrow} {abs(change):,.2f} ({pct_change:+.2f}%)</span>'
                        f'</li>'
                    )
                else:
                    logger.warning(f"Could not retrieve sufficient history for {symbol}")
                    html_blocks.append(f'<li><strong>{name}:</strong> Data unavailable</li>')
                    
            except Exception as e:
                logger.error(f"Error fetching data for {name} ({symbol}): {e}")
                html_blocks.append(f'<li><strong>{name}:</strong> Data unavailable</li>')

        html_blocks.append('</ul>')
        html_blocks.append('</div>')

        logger.info("Successfully fetched and formatted market indices.")
        return "\n".join(html_blocks)
