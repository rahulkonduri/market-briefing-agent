# 📈 Morning Market AI Agent

An intelligent, scheduled AI agent that fetches global market and business news every morning, summarizes the findings using an LLM (OpenAI), and delivers a personalized, concise email briefing directly to your inbox before you wake up.

## Features
- **Automated Data Ingestion**: Pulls top stories via NewsAPI.org.
- **AI-Powered Summarization**: Synthesizes market trends and key stories into a readable bullet-format briefing using LLMs.
- **Email Delivery**: Formats the briefing professionally using HTML and sends it via SMTP (Gmail).
- **Production-Ready Skeleton**: Implements robust logging, error handling, and environment-based configuration.

---

## 🚀 Setup & Installation

### 1. Requirements
- Python 3.10+
- A Google/Gmail Account (with an [App Password](https://support.google.com/accounts/answer/185833?hl=en) generated)
- A [NewsAPI](https://newsapi.org/) Key
- An [OpenAI API](https://platform.openai.com/) Key

### 2. Local Installation
```bash
# Clone or navigate to the repository
cd "NEWS API"

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
1. Copy the sample environment file:
   ```bash
   cp .env.sample .env
   ```
2. Open `.env` and fill in your keys:
   - `NEWS_API_KEY`: Your key from NewsAPI.org.
   - `OPENAI_API_KEY`: Your key from OpenAI.
   - `SMTP_USER`: Your Gmail address.
   - `SMTP_PASS`: Your 16-character Gmail App Password (do not use your real password!).
   - `TARGET_EMAIL`: The destination email address.

### 4. Running the Agent
Test the agent safely using the dry-run flag, which bypasses the email delivery and outputs the generated HTML directly to your console:
```bash
python main.py --dry-run
```
Once verified, run it for real:
```bash
python main.py
```

---

## ⏰ Scheduling 

### Option A: Local Cron (Linux/macOS)
To run this automatically every morning (e.g., 6:00 AM), add a CRON job:
```bash
crontab -e
```
Add the following line (update paths accordingly):
```cron
0 6 * * * cd /path/to/NEWS_API && /path/to/NEWS_API/venv/bin/python main.py
```
*(On Windows, you can use Task Scheduler to trigger a `.bat` file that runs `main.py`).*

### Option B: Cloud Deployment (GCP Cloud Scheduler + Cloud Run Functions)
For a serverless setup:
1. Wrap the `main.py` logic into a Flask or FastAPI endpoint.
2. Deploy this code to **GCP Cloud Run** or **AWS Lambda**.
3. Use **Google Cloud Scheduler** (or AWS EventBridge) to trigger an HTTP GET/POST request to your endpoint every morning at 06:00 AM.
4. Set your Environment Variables in the cloud provider's Secret Manager.

---

## 🏗 System Architecture & Scalability

- **Data Flow**: `Cron Trigger -> main.py -> fetch_news() -> LLM summary() -> format_html() -> send_email()`.
- **Scaling to millions of users**: 
  - Switch from sequential synchronous scripts to a **Kafka** or **RabbitMQ** message queue.
  - Workers pick up generation tasks, querying user preferences from a **PostgreSQL** DB.
  - Implement **Redis** caching for the news feed APIs (to avoid hitting rate limits since thousands of users might need the same base news data).

---

## 💡 Extensions & Future Growth

1. **WhatsApp/Telegram Bot**: Replace `email_service.py` with the Twilio API or python-telegram-bot. Let users message "Summary" to get on-demand briefings.
2. **Multi-Source Aggregation**: Expand `news_service.py` to ingest Twitter APIs, Reddit sentiment (/r/wallstreetbets), and Yahoo Finance tickers.
3. **Personalization Engine**: Allow users to specify `"TSLA, Tech, S&P 500"` in their config, dynamically injecting this into the NewsAPI query and the LLM prompt.
4. **Autonomous Trading Agent**: Grant the AI agent write-level tools to interface with a paper-trading API (like Alpaca) based on sentiment analysis (Requires extreme caution).

---

## 📄 Resume Bullet Points

- **Architected and developed** a scheduled AI-powered market analysis agent using Python, integrating NewsAPI for real-time data ingestion and Gemini 2.0 Flash for autonomous financial summarization.
- **Engineered** a robust modular backend with structured logging, isolated environment configuration, and decoupled service layers (Ingestion, Processing, Delivery) ensuring a production-ready codebase.
- **Automated** daily briefing pipelines by orchestrating internal services via Cron/Cloud Scheduler, sending formatted HTML reports via SMTP, and drastically reducing manual market research time.
