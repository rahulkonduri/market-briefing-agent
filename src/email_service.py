import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from .config import config
from .utils.logger import setup_logger

logger = setup_logger(__name__)

class EmailSender:
    """Service to send emails via SMTP."""
    
    def __init__(self):
        self.host = config.SMTP_HOST
        self.port = config.SMTP_PORT
        self.user = config.SMTP_USER
        self.password = config.SMTP_PASS
        self.target = config.TARGET_EMAIL

    def send_daily_briefing(self, html_content: str) -> bool:
        """
        Wraps the HTML content in a template and sends the email.
        """
        if not self.user or not self.password or not self.target:
            logger.error("SMTP credentials or target email missing from configuration.")
            raise ValueError("Email delivery is not configured properly.")

        today_str = datetime.now().strftime("%B %d, %Y")
        subject = f"📈 Morning Market Briefing - {today_str}"

        # Build full HTML
        full_html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ border-bottom: 2px solid #2B547E; padding-bottom: 10px; margin-bottom: 20px; }}
                    .header h1 {{ color: #2B547E; margin: 0; }}
                    .footer {{ margin-top: 30px; font-size: 0.8em; color: #777; border-top: 1px solid #ddd; padding-top: 10px; }}
                    a {{ color: #0066cc; text-decoration: none; }}
                    a:hover {{ text-decoration: underline; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Daily Market Briefing</h1>
                        <i>{today_str}</i>
                    </div>
                    
                    <div class="content">
                        {html_content}
                    </div>
                    
                    <div class="footer">
                        <p>🤖 <strong>Disclaimer:</strong> This briefing was generated autonomously by a Morning Market <strong>Agentic AI</strong>. Analyses and recommendations are produced by AI models combining real-time news with live market data, and should not replace professional financial advice.</p>
                    </div>
                </div>
            </body>
        </html>
        """

        # Parse multiple emails if comma-separated
        target_list = [email.strip() for email in self.target.split(',') if email.strip()]

        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = ", ".join(target_list)
        msg['Subject'] = subject

        msg.attach(MIMEText(full_html, 'html'))

        try:
            logger.info(f"Connecting to SMTP server {self.host}:{self.port}...")
            # For STARTTLS port 587
            server = smtplib.SMTP(self.host, self.port)
            server.ehlo()
            server.starttls()
            server.login(self.user, self.password)
            
            logger.info(f"Sending email to {len(target_list)} recipients...")
            server.send_message(msg, to_addrs=target_list)
            server.quit()
            
            logger.info("Email sent successfully!")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise
