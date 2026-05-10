import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import sqlite3
from datetime import date
from database.models import get_connection, init_db
from database import db

# Use a separate test database
TEST_DB = "test_expenses.db"
os.environ["DB_NAME"] = TEST_DB  # override before importing config


@pytest.fixture(autouse=True)
def setup_db():
    """Create fresh test database before each test, delete after"""
    # Patch DB_NAME
    import config
    config.DB_NAME = TEST_DB

    import database.models as models
    models.DB_NAME = TEST_DB

    import database.db as db_module
    db_module.DB_NAME = TEST_DB  # not directly used but good practice

    # Reinit models connection
    conn = sqlite3.connect(TEST_DB)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id  INTEGER PRIMARY KEY,
            language TEXT NOT NULL DEFAULT 'en'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL DEFAULT 'Other',
            note        TEXT,
            date        TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()

    yield

    # Cleanup
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


class TestAddExpense:
    def test_add_basic_expense(self):
        db.add_expense(user_id=1, amount=50.0, category="Food", note="lunch", date="2026-04-01")
        rows = db.get_expenses(user_id=1)
        assert len(rows) == 1
        assert rows[0]["amount"] == 50.0
        assert rows[0]["category"] == "Food"
        assert rows[0]["note"] == "lunch"

    def test_add_expense_default_date(self):
        db.add_expense(user_id=1, amount=20.0, category="Transport")
        rows = db.get_expenses(user_id=1)
        assert len(rows) == 1
        assert rows[0]["date"] == str(date.today())

    def test_add_multiple_expenses(self):
        db.add_expense(user_id=1, amount=10.0, category="Food", date="2026-04-01")
        db.add_expense(user_id=1, amount=20.0, category="Transport", date="2026-04-02")
        db.add_expense(user_id=1, amount=30.0, category="Health", date="2026-04-03")
        rows = db.get_expenses(user_id=1)
        assert len(rows) == 3

    def test_expenses_isolated_by_user(self):
        db.add_expense(user_id=1, amount=50.0, category="Food", date="2026-04-01")
        db.add_expense(user_id=2, amount=99.0, category="Housing", date="2026-04-01")
        rows_user1 = db.get_expenses(user_id=1)
        rows_user2 = db.get_expenses(user_id=2)
        assert len(rows_user1) == 1
        assert len(rows_user2) == 1
        assert rows_user1[0]["amount"] == 50.0
        assert rows_user2[0]["amount"] == 99.0


class TestGetExpenses:
    def test_filter_by_date_from(self):
        db.add_expense(user_id=1, amount=10.0, category="Food", date="2026-01-01")
        db.add_expense(user_id=1, amount=20.0, category="Food", date="2026-03-01")
        db.add_expense(user_id=1, amount=30.0, category="Food", date="2026-04-01")
        rows = db.get_expenses(user_id=1, date_from="2026-03-01")
        assert len(rows) == 2

    def test_filter_by_date_to(self):
        db.add_expense(user_id=1, amount=10.0, category="Food", date="2026-01-01")
        db.add_expense(user_id=1, amount=20.0, category="Food", date="2026-03-01")
        db.add_expense(user_id=1, amount=30.0, category="Food", date="2026-04-01")
        rows = db.get_expenses(user_id=1, date_to="2026-02-28")
        assert len(rows) == 1

    def test_filter_by_date_range(self):
        db.add_expense(user_id=1, amount=10.0, category="Food", date="2026-01-01")
        db.add_expense(user_id=1, amount=20.0, category="Food", date="2026-02-01")
        db.add_expense(user_id=1, amount=30.0, category="Food", date="2026-04-01")
        rows = db.get_expenses(user_id=1, date_from="2026-01-01", date_to="2026-02-28")
        assert len(rows) == 2

    def test_no_expenses_returns_empty(self):
        rows = db.get_expenses(user_id=999)
        assert rows == []


class TestGetStats:
    def test_stats_grouped_by_category(self):
        db.add_expense(user_id=1, amount=50.0, category="Food", date="2026-04-01")
        db.add_expense(user_id=1, amount=30.0, category="Food", date="2026-04-02")
        db.add_expense(user_id=1, amount=20.0, category="Transport", date="2026-04-01")
        stats = db.get_stats(user_id=1)
        assert len(stats) == 2
        food = next(r for r in stats if r["category"] == "Food")
        assert food["total"] == 80.0

    def test_stats_ordered_by_total_desc(self):
        db.add_expense(user_id=1, amount=10.0, category="Health", date="2026-04-01")
        db.add_expense(user_id=1, amount=100.0, category="Food", date="2026-04-01")
        db.add_expense(user_id=1, amount=50.0, category="Transport", date="2026-04-01")
        stats = db.get_stats(user_id=1)
        assert stats[0]["category"] == "Food"
        assert stats[1]["category"] == "Transport"


class TestDeleteExpense:
    def test_delete_expense(self):
        db.add_expense(user_id=1, amount=50.0, category="Food", date="2026-04-01")
        rows = db.get_expenses(user_id=1)
        expense_id = rows[0]["id"]
        db.delete_expense(expense_id=expense_id, user_id=1)
        rows_after = db.get_expenses(user_id=1)
        assert len(rows_after) == 0

    def test_delete_only_affects_own_expense(self):
        db.add_expense(user_id=1, amount=50.0, category="Food", date="2026-04-01")
        db.add_expense(user_id=2, amount=99.0, category="Food", date="2026-04-01")
        rows = db.get_expenses(user_id=1)
        db.delete_expense(expense_id=rows[0]["id"], user_id=2)  # wrong user
        rows_after = db.get_expenses(user_id=1)
        assert len(rows_after) == 1  # not deleted


class TestUpdateExpense:
    def test_update_amount(self):
        db.add_expense(user_id=1, amount=50.0, category="Food", date="2026-04-01")
        rows = db.get_expenses(user_id=1)
        expense_id = rows[0]["id"]
        db.update_expense(expense_id=expense_id, user_id=1, amount=75.0)
        updated = db.get_expense_by_id(expense_id, user_id=1)
        assert updated["amount"] == 75.0

    def test_update_category(self):
        db.add_expense(user_id=1, amount=50.0, category="Food", date="2026-04-01")
        rows = db.get_expenses(user_id=1)
        expense_id = rows[0]["id"]
        db.update_expense(expense_id=expense_id, user_id=1, category="Transport")
        updated = db.get_expense_by_id(expense_id, user_id=1)
        assert updated["category"] == "Transport"


class TestClearExpenses:
    def test_clear_all_expenses(self):
        db.add_expense(user_id=1, amount=10.0, category="Food", date="2026-04-01")
        db.add_expense(user_id=1, amount=20.0, category="Food", date="2026-04-02")
        db.clear_expenses(user_id=1)
        rows = db.get_expenses(user_id=1)
        assert len(rows) == 0

    def test_clear_only_affects_own_data(self):
        db.add_expense(user_id=1, amount=10.0, category="Food", date="2026-04-01")
        db.add_expense(user_id=2, amount=20.0, category="Food", date="2026-04-01")
        db.clear_expenses(user_id=1)
        rows_user2 = db.get_expenses(user_id=2)
        assert len(rows_user2) == 1


class TestLanguage:
    def test_default_language_is_english(self):
        lang = db.get_user_language(user_id=999)
        assert lang == "en"

    def test_set_and_get_language(self):
        db.set_user_language(user_id=1, language="uz")
        lang = db.get_user_language(user_id=1)
        assert lang == "uz"

    def test_update_language(self):
        db.set_user_language(user_id=1, language="uz")
        db.set_user_language(user_id=1, language="en")
        lang = db.get_user_language(user_id=1)
        assert lang == "en"
