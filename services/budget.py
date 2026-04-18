import json
from groq import Groq
from config import GROQ_API_KEY
from database.db import get_stats, get_expenses
from datetime import date, timedelta

client = Groq(api_key=GROQ_API_KEY)


def _get_monthly_summary(user_id: int, months: int = 3) -> str:
    """Build a spending summary for the last N months"""
    today = date.today()
    lines = []

    for i in range(months):
        # Calculate month range
        month_end = today.replace(day=1) - timedelta(days=1) if i > 0 else today
        month_start = month_end.replace(day=1)

        if i == 0:
            month_start = today.replace(day=1)
            month_end = today

        stats = get_stats(user_id, str(month_start), str(month_end))
        if stats:
            total = sum(row["total"] for row in stats)
            breakdown = ", ".join([f"{row['category']}: ${row['total']:.2f}" for row in stats])
            lines.append(f"{month_start.strftime('%B %Y')}: Total ${total:.2f} ({breakdown})")

    return "\n".join(lines) if lines else "No spending data available."


async def get_budget_advice(user_id: int, lang: str = "en") -> str:
    """Generate personalized budget advice based on spending history"""
    summary = _get_monthly_summary(user_id, months=3)

    lang_instruction = "Respond in Uzbek language." if lang == "uz" else "Respond in English."

    prompt = f"""You are a friendly personal finance advisor for a Telegram expense tracking bot.

Here is the user's recent spending history:
{summary}

Give personalized, practical budget advice based on this data. Be specific — mention actual numbers and categories from their data.
Include:
1. How they are doing overall
2. Which category they spend the most on
3. One specific actionable tip to save money
4. An encouraging closing sentence

Keep it concise (4-6 sentences max). Use emojis. {lang_instruction}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[BUDGET ERROR] {e}")
        return "Sorry, couldn't generate advice right now. Try again later."
