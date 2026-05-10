import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from services.ai_service import _parse_amount, _build_prompt
from datetime import date


class TestParseAmount:
    def test_plain_number(self):
        assert _parse_amount(50) == 50.0

    def test_float_number(self):
        assert _parse_amount(12.99) == 12.99

    def test_string_with_dollar(self):
        assert _parse_amount("$50") == 50.0

    def test_string_with_euro(self):
        assert _parse_amount("€20") == 20.0

    def test_string_with_pound(self):
        assert _parse_amount("£15") == 15.0

    def test_plain_string_number(self):
        assert _parse_amount("100") == 100.0

    def test_none_returns_none(self):
        assert _parse_amount(None) is None

    def test_invalid_returns_none(self):
        assert _parse_amount("abc") is None

    def test_decimal_string(self):
        assert _parse_amount("3.50") == 3.50


class TestBuildPrompt:
    def test_prompt_contains_today(self):
        prompt = _build_prompt()
        today = str(date.today())
        assert today in prompt

    def test_prompt_contains_required_intents(self):
        prompt = _build_prompt()
        assert "add_expense" in prompt
        assert "list_expenses" in prompt
        assert "get_stats" in prompt
        assert "get_chart" in prompt
        assert "export" in prompt
        assert "manage" in prompt
        assert "budget_advice" in prompt

    def test_prompt_contains_categories(self):
        prompt = _build_prompt()
        assert "Food" in prompt
        assert "Transport" in prompt
        assert "Housing" in prompt
