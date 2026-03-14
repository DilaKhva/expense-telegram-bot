from datetime import datetime
from database.models import get_connection


def add_expense(user_id: int, amount: float, category: str, note: str = "", date: str = None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (user_id, amount, category, note, date) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, category, note, date)
    )
    conn.commit()
    conn.close()


def get_expenses(user_id: int, date_from: str = None, date_to: str = None):
    conn = get_connection()
    query, params = _build_query("SELECT *", user_id, date_from, date_to)
    query += " ORDER BY date DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


def get_stats(user_id: int, date_from: str = None, date_to: str = None):
    conn = get_connection()
    query, params = _build_query(
        "SELECT category, SUM(amount) as total", user_id, date_from, date_to
    )
    query += " GROUP BY category ORDER BY total DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


def get_all_expenses_csv(user_id: int):
    conn = get_connection()
    rows = conn.execute(
        "SELECT date, amount, category, note FROM expenses WHERE user_id = ? ORDER BY date DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def clear_expenses(user_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def _build_query(select: str, user_id: int, date_from: str, date_to: str):
    query = f"{select} FROM expenses WHERE user_id = ?"
    params = [user_id]
    if date_from:
        query += " AND date >= ?"
        params.append(date_from)
    if date_to:
        query += " AND date <= ?"
        params.append(date_to)
    return query, params
