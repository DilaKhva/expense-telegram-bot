TEXTS = {
    "en": {
        "start": (
            "👋 Hey! I'm your AI expense tracker.\n\n"
            "Here's what I can do for you:\n\n"
            "➕ *Add expense* — describe what you spent\n"
            "   👉 \"12 on lunch\", \"3.50 for coffee today\"\n\n"
            "📋 *View expenses* — ask for a list\n"
            "   👉 \"show this week's expenses\"\n\n"
            "📊 *Statistics* — breakdown by category\n"
            "   👉 \"stats for january\", \"this month's stats\"\n\n"
            "📈 *Charts* — visual pie chart\n"
            "   👉 \"chart for this month\", \"chart for all time\"\n\n"
            "💵 Use USD ($) for all amounts.\n"
            "⚠️ One expense per message please!\n\n"
            "🌐 /language — change language\n"
            "🗑 /clear — delete all your data"
        ),
        "cleared": "🗑 All your expenses have been deleted. Fresh start! ✨",
        "multi_line": "⚠️ Please send *one expense per message!*\n\n👉 \"12 on lunch\"\n👉 \"3.50 for coffee\"",
        "saved": "✅ Saved!\n\n📅 Date: {date}\n💰 Amount: ${amount}\n📂 Category: {category}\n📝 Note: {note}",
        "no_amount": "❌ Couldn't detect the amount.\nTry: \"spent 50 on lunch\"",
        "no_expenses": "📭 No expenses found for *{label}*.",
        "no_stats": "📭 No stats for *{label}*.",
        "no_chart": "📭 No data to chart for *{label}*.",
        "expenses_header": "📋 *{label} expenses:*\n",
        "expenses_total": "\n💰 *Total: ${total}*",
        "stats_header": "📊 *{label} stats:*\n",
        "chart_caption": "📊 {label} spending breakdown",
        "choose_language": "🌐 Choose your language:",
        "language_set": "✅ Language set to English!",
        "manage_title": "📋 Your recent expenses — tap to manage:",
        "delete_btn": "🗑 Delete",
        "edit_btn": "✏️ Edit",
        "deleted": "✅ Expense deleted!",
        "edit_prompt": "✏️ What do you want to change?\n\nSend me the new details, for example:\n\"change amount to 20\"\n\"change category to Transport\"\n\"change date to March 5\"",
        "edit_saved": "✅ Updated!\n\n📅 Date: {date}\n💰 Amount: ${amount}\n📂 Category: {category}\n📝 Note: {note}",
        "expense_not_found": "❌ Expense not found.",
        "manage_hint": "To manage expenses say: \"delete my expenses\" or \"edit expenses\"",
        "export_caption": "📁 Here are your {count} expenses as a CSV file. You can open it in Excel or Google Sheets!",
        "export_cmd": "📤 /export — download all expenses as CSV",
    },
    "uz": {
        "start": (
            "👋 Salom! Men AI xarajat kuzatuvchi botman.\n\n"
            "Men quyidagilarni qila olaman:\n\n"
            "➕ *Xarajat qo'shish* — nima sarflaganingizni yozing\n"
            "   👉 \"tushlikka 12 dollar\", \"bugun qahvaga 3.50\"\n\n"
            "📋 *Xarajatlarni ko'rish* — ro'yxat so'rang\n"
            "   👉 \"bu haftagi xarajatlar\"\n\n"
            "📊 *Statistika* — kategoriya bo'yicha tahlil\n"
            "   👉 \"yanvar statistikasi\", \"bu oygi statistika\"\n\n"
            "📈 *Grafik* — doiraviy diagramma\n"
            "   👉 \"bu oygi grafik\", \"barcha vaqt grafigi\"\n\n"
            "💵 Barcha summalar USD ($) da bo'lsin.\n"
            "⚠️ Har safar faqat bitta xarajat yuboring!\n\n"
            "🌐 /language — tilni o'zgartirish\n"
            "🗑 /clear — barcha ma'lumotlarni o'chirish"
        ),
        "cleared": "🗑 Barcha xarajatlaringiz o'chirildi. Yangi boshlanish! ✨",
        "multi_line": "⚠️ Iltimos *bitta xarajat* yuboring!\n\n👉 \"tushlikka 12 dollar\"\n👉 \"qahvaga 3.50 dollar\"",
        "saved": "✅ Saqlandi!\n\n📅 Sana: {date}\n💰 Summa: ${amount}\n📂 Kategoriya: {category}\n📝 Izoh: {note}",
        "no_amount": "❌ Summani aniqlay olmadim.\nMasalan: \"tushlikka 50 dollar\"",
        "no_expenses": "📭 *{label}* uchun xarajat topilmadi.",
        "no_stats": "📭 *{label}* uchun statistika yo'q.",
        "no_chart": "📭 *{label}* uchun ma'lumot yo'q.",
        "expenses_header": "📋 *{label} xarajatlari:*\n",
        "expenses_total": "\n💰 *Jami: ${total}*",
        "stats_header": "📊 *{label} statistikasi:*\n",
        "chart_caption": "📊 {label} xarajatlar taqsimoti",
        "choose_language": "🌐 Tilni tanlang:",
        "language_set": "✅ Til o'zbekchaga o'zgartirildi!",
        "manage_title": "📋 So'nggi xarajatlar — boshqarish uchun bosing:",
        "delete_btn": "🗑 O'chirish",
        "edit_btn": "✏️ Tahrirlash",
        "deleted": "✅ Xarajat o'chirildi!",
        "edit_prompt": "✏️ Nimani o'zgartirmoqchisiz?\n\nYangi ma'lumotlarni yuboring, masalan:\n\"summani 20 ga o'zgartir\"\n\"kategoriyani Transportga o'zgartir\"",
        "edit_saved": "✅ Yangilandi!\n\n📅 Sana: {date}\n💰 Summa: ${amount}\n📂 Kategoriya: {category}\n📝 Izoh: {note}",
        "expense_not_found": "❌ Xarajat topilmadi.",
        "manage_hint": "Xarajatlarni boshqarish uchun: \"xarajatlarni o'chir\" yoki \"xarajatni tahrirlash\"",
        "export_caption": "📁 {count} ta xarajatingiz CSV formatda. Excel yoki Google Sheets da ochishingiz mumkin!",
        "export_cmd": "📤 /export — barcha xarajatlarni CSV yuklab olish",
    }
}


def t(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS["en"]).get(key, TEXTS["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text
