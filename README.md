# AI-powered Telegram bot for tracking 
# personal expenses 💰

An AI-powered Telegram bot for tracking personal expenses using natural language processing.  
The application allows users to record expenses in plain English or Uzbek, analyze spending habits, generate charts, export data, and receive AI-based budget recommendations.

---

## 📌 Project Overview

The purpose of this project is to simplify personal finance tracking through conversational interaction.  
Instead of manually filling forms or using complex interfaces, users can communicate with the bot naturally:

- “spent 20 on lunch”
- “paid 15 for taxi yesterday”
- “show this month stats”

The system automatically extracts:
- amount
- category
- note
- date
- user intent

using AI-based natural language processing.

---

## ✨ Features

### Expense Management
- Add expenses using natural language
- Automatic category detection
- Flexible date parsing
- View expense history
- Edit existing expenses
- Delete expenses
- Clear all user data

### Analytics
- Expense statistics by category
- Pie chart visualization
- Monthly and custom period analysis
- AI-generated budget advice

### Data Export
- Export all expenses to CSV
- Compatible with Excel and Google Sheets

### User Experience
- Inline keyboard navigation
- English and Uzbek language support
- Friendly conversational interface

---

## 🧠 AI Integration

The bot uses the Groq API with the LLaMA 3.3 70B model for:
- Intent recognition
- Entity extraction
- Date interpretation
- Budget analysis
- Conversational responses

Example:

| User Message | Extracted Data |
|---|---|
| “spent 25 on lunch yesterday” | amount=25, category=Food, date=yesterday |
| “stats for january” | intent=get_stats |
| “how am I doing?” | intent=budget_advice |

---

## 🏗 System Architecture

The project follows a modular architecture:

- **Handlers** — process Telegram updates and commands
- **Services** — AI processing and business logic
- **Database layer** — SQLite data management
- **Utilities** — charts and translations
- **Tests** — automated unit testing

### Architecture Diagram

See:
- `docs/architecture_diagram.png`

### User Flow Diagram

See:
- `docs/user_flow_diagram.png`

---

## 🛠 Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Telegram Framework | aiogram 3 |
| AI Model | LLaMA 3.3 70B |
| AI Provider | Groq |
| Database | SQLite |
| Visualization | Matplotlib |
| Testing | Pytest |
| Deployment | VPS (Linux) |

---

## 📂 Project Structure

```text
expense_bot/
│
├── database/
│   ├── db.py
│   └── models.py
│
├── handlers/
│   ├── ai_handler.py
│   ├── manage.py
│   └── export.py
│
├── services/
│   ├── ai_service.py
│   └── budget.py
│
├── tests/
│   ├── test_ai_service.py
│   ├── test_db.py
│   └── test_translations.py
│
├── utils/
│   ├── charts.py
│   └── translations.py
│
├── docs/
│   ├── architecture_diagram.png
│   └── user_flow_diagram.png
│
├── config.py
├── requirements.txt
├── README.md
└── .env.example
```

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/DilaKhva/expense-telegram-bot.git
cd expense-telegram-bot
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

Activate environment:

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` file:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the application

```bash
python bot.py
```

---

## 📊 Usage Examples

| User Request | Bot Action |
|---|---|
| “spent 12 on lunch” | Saves expense |
| “show this week expenses” | Displays expense history |
| “stats for this month” | Generates statistics |
| “chart for january” | Creates pie chart |
| “how am I doing?” | AI budget advice |
| “export csv” | Sends CSV file |
| “manage expenses” | Opens edit/delete menu |

---

## 🧪 Testing

The project includes automated unit tests for:
- database operations
- translation system
- AI helper functions
- expense management logic

Run tests:

```bash
pytest
```

### Current Status

- ✅ 40/40 tests passing

---

## 🚀 Deployment

The bot is deployed on a Linux VPS server and runs continuously.

Deployment includes:
- Python virtual environment
- Linux service management
- Git-based updates
- Environment variable configuration

---

## 🔒 Security Notes

Sensitive information such as API keys and tokens are stored in environment variables and excluded from version control using `.gitignore`.

---

## 📈 Future Improvements

Possible future enhancements:
- Web dashboard
- Authentication system
- Multi-currency support
- OCR receipt scanning
- Advanced analytics
- Monthly spending goals
- Docker containerization

---

## 👩‍💻 Author

Dilnoza Kholisova  
Bachelor of Software Engineering  
IT Park University

---

## 📄 License

This project was developed for educational and research purposes as a capstone project.
