import json
import re
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are an AI assistant for an expense tracking Telegram bot.
The user tracks their daily expenses through simple chat messages.

When the user sends a message, you MUST respond in the following JSON format:

{
  "intent": "add_expense" | "list_expenses" | "get_stats" | "get_chart" | "chat",
  "data": {
    "amount": number or null,
    "category": string or null,
    "note": string or null,
    "period": "today" | "week" | "month" | "year" | "all" or null,
    "date": "YYYY-MM-DD" or null
  },
  "reply": "A friendly short reply to the user"
}

Rules:
- Only help with expense-related topics. For anything else, politely decline and set intent = "chat"
- Categories must be in English: Food, Transport, Clothing, Entertainment, Health, Education, Housing, Other
- "amount" MUST always be a plain number (e.g. 50, 12.99). NEVER include $, £, €, USD, EUR or any currency symbol/text in the amount field.
- If the user writes "$50" or "50 dollars" or "€20", extract just the number: 50, 50, 20
- Detect period from the message: today=today, week=week, month=month, year=year, all time/everything=all (default: month)
- If the user mentions a specific date like "yesterday", "last monday", "3 days ago", set "date" to the correct YYYY-MM-DD. Today is 2026-03-14.
- If the user mentions only a month like "in january", "last february", set "date" to YYYY-MM-01 (first day of that month). Example: "in january" -> "2026-01-01", "last december" -> "2025-12-01".
- If the user mentions a specific day like "january 15" or "3rd of march", use the exact date.
- Keep the "reply" short, friendly, and use emojis

Examples:
- "spent $50 on lunch" -> intent: add_expense, amount: 50, category: Food
- "paid 15 for the bus today" -> intent: add_expense, amount: 15, category: Transport, period: today
- "20 on coffee" -> intent: add_expense, amount: 20, category: Food
- "what did I spend this month?" -> intent: list_expenses, period: month
- "show my stats" -> intent: get_stats, period: month
- "visualize my stats" -> intent: get_chart, period: month
- "show chart" -> intent: get_chart, period: month
- "pie chart of this week" -> intent: get_chart, period: week
- "hi" -> intent: chat, reply: friendly greeting + remind them what the bot does
- "what is the weather?" -> intent: chat, reply: politely say you only help with expenses

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
    """Analyzes the user message and returns what action to take"""
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
