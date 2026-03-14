# AI Expense Tracker Bot 💰

A user-friendly Telegram bot for individuals to manage and track their daily expenses through simple natural language chat interactions — no commands to memorize!

## Features
- 🧠 **AI-powered input** — just type naturally, e.g. "spent 12 on lunch"
- 📂 **Auto categorization** — AI assigns categories automatically
- 📅 **Flexible date tracking** — "in january", "yesterday", "last week"
- 📊 **Stats & charts** — pie charts for any time period
- 🗑 **Data management** — clear your history anytime

## Tech Stack

| Component | Tool |
|-----------|------|
| Language | Python |
| Telegram Framework | aiogram 3 |
| AI / NLP | Groq (LLaMA 3.3 70B) |
| Database | SQLite |
| Visualization | Matplotlib |

## Project Structure

```
expense_bot/
├── bot.py                 # Entry point
├── config.py              # Env variables
├── .env                   # API keys (not committed)
├── database/
│   ├── models.py          # Table creation
│   └── db.py              # DB queries
├── handlers/
│   └── ai_handler.py      # Message routing
├── services/
│   ├── ai_service.py      # Groq AI integration
│   └── budget.py          # Budget recommendations (coming soon)
├── utils/
│   └── charts.py          # Chart generation
├── tests/                 # Tests (coming soon)
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

1. Clone the repo
```bash
git clone https://github.com/your-username/expense_bot.git
cd expense_bot
```

2. Create and activate virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file
```
BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
```

5. Run the bot
```bash
python bot.py
```

## Usage Examples

| You say | Bot does |
|--------|----------|
| "spent 12 on lunch" | Saves $12 under Food |
| "paid 30 for transport yesterday" | Saves with yesterday's date |
| "in january spent 50 on clothes" | Saves under January 2026 |
| "show this week's expenses" | Lists all expenses this week |
| "stats for january" | Category breakdown for January |
| "chart for this month" | Pie chart image |
| /clear | Deletes all your data |

## API Keys

- **Telegram Bot Token** — get from [@BotFather](https://t.me/BotFather)
- **Groq API Key** — get for free at [console.groq.com](https://console.groq.com)
