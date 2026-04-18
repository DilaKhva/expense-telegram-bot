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


def get_user_language(user_id: int) -> str:
    conn = get_connection()
    row = conn.execute("SELECT language FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return row["language"] if row else "en"


def set_user_language(user_id: int, language: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO users (user_id, language) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET language = ?",
        (user_id, language, language)
    )
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


def get_recent_expenses(user_id: int, limit: int = 10):
    """Get most recent expenses for showing in list"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return rows


def delete_expense(expense_id: int, user_id: int):
    """Delete a single expense by id (user_id check for safety)"""
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id))
    conn.commit()
    conn.close()


def update_expense(expense_id: int, user_id: int, amount: float = None, category: str = None, note: str = None, date: str = None):
    """Update fields of an expense"""
    conn = get_connection()
    if amount is not None:
        conn.execute("UPDATE expenses SET amount = ? WHERE id = ? AND user_id = ?", (amount, expense_id, user_id))
    if category is not None:
        conn.execute("UPDATE expenses SET category = ? WHERE id = ? AND user_id = ?", (category, expense_id, user_id))
    if note is not None:
        conn.execute("UPDATE expenses SET note = ? WHERE id = ? AND user_id = ?", (note, expense_id, user_id))
    if date is not None:
        conn.execute("UPDATE expenses SET date = ? WHERE id = ? AND user_id = ?", (date, expense_id, user_id))
    conn.commit()
    conn.close()


def get_expense_by_id(expense_id: int, user_id: int):
    """Get a single expense by id"""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id)
    ).fetchone()
    conn.close()
    return row
