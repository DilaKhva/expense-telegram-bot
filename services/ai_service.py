import json
import re
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are an AI assistant for an expense tracking Telegram bot.
Today's date is 2026-03-14.

When the user sends a message, respond ONLY in this JSON format:

{
  "intent": "add_expense" | "list_expenses" | "get_stats" | "get_chart" | "chat",
  "data": {
    "amount": number or null,
    "category": string or null,
    "note": string or null,
    "date": "YYYY-MM-DD" or null,
    "date_from": "YYYY-MM-DD" or null,
    "date_to": "YYYY-MM-DD" or null
  },
  "reply": "A friendly short reply to the user"
}

Rules:
- Only help with expense topics. For anything else, set intent = "chat" and politely decline.
- Categories: Food, Transport, Clothing, Entertainment, Health, Education, Housing, Other
- "amount" must be a plain number, no currency symbols. "$50" -> 50, "20 euros" -> 20
- For add_expense: extract "date" from message using real dates:
    "today" -> "2026-03-14"
    "yesterday" -> "2026-03-13"
    "in january" -> date = "2026-01-01"
    "january 15" -> date = "2026-01-15"
    "last year march" -> date = "2025-03-01"
    If no date mentioned, set date = null (will default to today)
- For list/stats/chart: extract "date_from" and "date_to" as real dates:
    "today" -> date_from = "2026-03-14", date_to = "2026-03-14"
    "this week" -> date_from = "2026-03-08", date_to = "2026-03-14"
    "this month" -> date_from = "2026-03-01", date_to = "2026-03-14"
    "this year" -> date_from = "2026-01-01", date_to = "2026-03-14"
    "january" -> date_from = "2026-01-01", date_to = "2026-01-31"
    "last month" -> date_from = "2026-02-01", date_to = "2026-02-28"
    "all" or no period -> date_from = null, date_to = null

Examples:
- "spent 12 on lunch" -> intent: add_expense, amount: 12, category: Food, date: null
- "paid 50 for shoes last monday" -> intent: add_expense, amount: 50, category: Clothing, date: "2026-03-09"
- "in january i spent 20 on gift" -> intent: add_expense, amount: 20, category: Other, note: gift, date: "2026-01-01"
- "show this week expenses" -> intent: list_expenses, date_from: "2026-03-08", date_to: "2026-03-14"
- "stats for january" -> intent: get_stats, date_from: "2026-01-01", date_to: "2026-01-31"
- "chart for this month" -> intent: get_chart, date_from: "2026-03-01", date_to: "2026-03-14"
- "all time stats" -> intent: get_stats, date_from: null, date_to: null

Return JSON only, nothing else."""


def _parse_amount(value) -> float | None:
    if value is None:
        return None
    cleaned = re.sub(r'[^\d.]', '', str(value))
    try:
        return float(cleaned)
    except ValueError:
        return None


async def analyze_message(user_message: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        text = response.choices[0].message.content.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            text = match.group()
        result = json.loads(text)
        if "data" in result and "amount" in result["data"]:
            result["data"]["amount"] = _parse_amount(result["data"]["amount"])
        return result

    except Exception as e:
        print(f"[AI ERROR] {type(e).__name__}: {e}")
        return {
            "intent": "chat",
            "data": {},
            "reply": f"Error: {type(e).__name__}: {e}"
        }
