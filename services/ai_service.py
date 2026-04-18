import json
import re
from datetime import date, timedelta
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are an AI assistant for an expense tracking Telegram bot.
Today's date is {today}.

When the user sends a message, respond ONLY in this JSON format:

{{
  "intent": "add_expense" | "list_expenses" | "get_stats" | "get_chart" | "export" | "manage" | "budget_advice" | "chat",
  "data": {{
    "amount": number or null,
    "category": string or null,
    "note": string or null,
    "date": "YYYY-MM-DD" or null,
    "date_from": "YYYY-MM-DD" or null,
    "date_to": "YYYY-MM-DD" or null
  }},
  "reply": "A friendly short reply to the user"
}}

Rules:
- Only help with expense topics. For anything else, set intent = "chat" and politely decline.
- Categories: Food, Transport, Clothing, Entertainment, Health, Education, Housing, Other
- "amount" must be a plain number, no currency symbols. "$50" -> 50, "20 euros" -> 20
- For add_expense: extract "date" from message using real dates:
    "today" -> "{today}"
    "yesterday" -> "{yesterday}"
    "in january" -> date = "2026-01-01"
    "january 15" -> date = "2026-01-15"
    "last year march" -> date = "2025-03-01"
    If no date mentioned, set date = null (will default to today)
- For list/stats/chart: extract "date_from" and "date_to" as real dates:
    "today" -> date_from = "{today}", date_to = "{today}"
    "this week" -> date_from = "{week_start}", date_to = "{today}"
    "this month" -> date_from = "{month_start}", date_to = "{today}"
    "this year" -> date_from = "{year_start}", date_to = "{today}"
    "january" -> date_from = "2026-01-01", date_to = "2026-01-31"
    "last month" -> date_from = "{last_month_start}", date_to = "{last_month_end}"
    "all" or no period -> date_from = null, date_to = null

Examples:
- "spent 12 on lunch" -> intent: add_expense, amount: 12, category: Food, date: null
- "paid 50 for shoes yesterday" -> intent: add_expense, amount: 50, category: Clothing, date: "{yesterday}"
- "in january i spent 20 on gift" -> intent: add_expense, amount: 20, category: Other, note: gift, date: "2026-01-01"
- "show this week expenses" -> intent: list_expenses, date_from: "{week_start}", date_to: "{today}"
- "stats for january" -> intent: get_stats, date_from: "2026-01-01", date_to: "2026-01-31"
- "chart for this month" -> intent: get_chart, date_from: "{month_start}", date_to: "{today}"
- "all time stats" -> intent: get_stats, date_from: null, date_to: null
- "send csv", "export my data", "excel file" -> intent: export
- "delete expense", "edit expense", "manage expenses" -> intent: manage
- "budget advice", "am I overspending?", "how am I doing?", "give me tips", "save money", "spending advice", "how i was doing", "analyze my spending", "any tips?", "what do you think about my spending" -> intent: budget_advice
NOTE: "how am I doing" and "how i was doing" ALWAYS = budget_advice, never get_stats

Return JSON only, nothing else."""


def _build_prompt() -> str:
    today = date.today()
    yesterday = today - timedelta(days=1)
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)
    # last month
    last_month_end = month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    return SYSTEM_PROMPT.format(
        today=today,
        yesterday=yesterday,
        week_start=week_start,
        month_start=month_start,
        year_start=year_start,
        last_month_start=last_month_start,
        last_month_end=last_month_end,
    )


def _parse_amount(value) -> float | None:
    if value is None:
        return None
    cleaned = re.sub(r'[^\d.]', '', str(value))
    try:
        return float(cleaned)
    except ValueError:
        return None


async def analyze_message(user_message: str, lang: str = "en") -> dict:
    try:
        prompt = _build_prompt()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt + "\n\nReply field language: " + ("Uzbek" if lang == "uz" else "English")},
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
