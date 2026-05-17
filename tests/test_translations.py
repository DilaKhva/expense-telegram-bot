import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from utils.translations import t, TEXTS


class TestTranslations:
    def test_english_start_message(self):
        result = t("en", "start")
        assert "expense" in result.lower()

    def test_uzbek_start_message(self):
        result = t("uz", "start")
        assert "xarajat" in result.lower()

    def test_fallback_to_english_for_unknown_lang(self):
        result = t("fr", "start")
        assert result == t("en", "start")

    def test_saved_message_with_placeholders(self):
        result = t("en", "saved", date="Today", amount="12.00", category="Food", note="lunch")
        assert "12.00" in result
        assert "Food" in result
        assert "Today" in result

    def test_uz_saved_message(self):
        result = t("uz", "saved", date="Bugun", amount="12.00", category="Food", note="tushlik")
        assert "12.00" in result
        assert "saqlandi" in result

    def test_all_english_keys_exist(self):
        required_keys = ["start", "cleared", "saved", "no_amount", "no_expenses",
                        "no_stats", "no_chart", "expenses_header", "stats_header",
                        "choose_language", "language_set", "export_caption"]
        for key in required_keys:
            assert key in TEXTS["en"], f"Missing key in English: {key}"

    def test_all_uzbek_keys_exist(self):
        required_keys = ["start", "cleared", "saved", "no_amount", "no_expenses",
                        "no_stats", "no_chart", "expenses_header", "stats_header",
                        "choose_language", "language_set", "export_caption"]
        for key in required_keys:
            assert key in TEXTS["uz"], f"Missing key in Uzbek: {key}"

    def test_no_expenses_with_label(self):
        result = t("en", "no_expenses", label="January 2026")
        assert "January 2026" in result

    def test_expenses_total_with_amount(self):
        result = t("en", "expenses_total", total="221.00")
        assert "221.00" in result
