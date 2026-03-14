from datetime import datetime
from database.models import get_connection


def add_expense(user_id: int, amount: float, category: str, note: str = "", date: str = None):
    """Yangi xarajat qo'shadi"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (user_id, amount, category, note, date) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, category, note, date)
    )
    conn.commit()
    conn.close()


def get_expenses(user_id: int, period: str = "month"):
    """
    Xarajatlar ro'yxatini qaytaradi.
    period: 'today' | 'week' | 'month'
    """
    conn = get_connection()
    date_filter = _date_filter(period)
    rows = conn.execute(
        f"SELECT * FROM expenses WHERE user_id = ? AND {date_filter} ORDER BY date DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def get_stats(user_id: int, period: str = "month"):
    """Kategoriya bo'yicha umumiy xarajatlarni qaytaradi"""
    conn = get_connection()
    date_filter = _date_filter(period)
    rows = conn.execute(
        f"""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE user_id = ? AND {date_filter}
        GROUP BY category
        ORDER BY total DESC
        """,
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def get_all_expenses_csv(user_id: int):
    """Export uchun barcha xarajatlarni qaytaradi"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT date, amount, category, note FROM expenses WHERE user_id = ? ORDER BY date DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def _date_filter(period: str) -> str:
    if period == "today":
        return "date = date('now')"
    elif period == "week":
        return "date >= date('now', '-7 days')"
    elif period == "year":
        return "date >= date('now', '-365 days')"
    elif period == "all":
        return "1=1"
    else:  # month
        return "date >= date('now', '-30 days')"


def clear_expenses(user_id: int):
    """Delete all expenses for a user"""
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
