TEXTS = {
    "en": {
        "start": (
            "👋 *Welcome to ExpenseAI!*\n\n"
            "I help you track your daily expenses using natural language.\n\n"
            "💬 *Examples:*\n"
            "• \"spent 25 on lunch\"\n"
            "• \"paid 15 for transport yesterday\"\n"
            "• \"in january I spent 50 on clothes\"\n\n"
            "✨ *Features:*\n"
            "➕ Add expenses naturally\n"
            "📋 View expense history\n"
            "📊 Statistics & charts\n"
            "💡 AI budget advice\n"
            "📁 CSV export\n"
            "🌐 English & Uzbek support\n\n"
            "Choose an option below or just start chatting! 👇"
        ),
        "cleared": "🗑 All your expenses have been deleted. Fresh start! ✨",
        "multi_line": (
            "⚠️ Please send *one expense per message!*\n\n"
            "Try:\n"
            "• \"spent 12 on lunch\"\n"
            "• \"paid 3.50 for coffee\""
        ),
        "saved": "✅ *Expense saved!*\n\n📅 Date: {date}\n💰 Amount: ${amount}\n📂 Category: {category}\n📝 Note: {note}",
        "no_amount": (
            "❌ I couldn't understand that expense.\n\n"
            "Try:\n"
            "• \"spent 20 on food\"\n"
            "• \"paid 15 for taxi yesterday\"\n"
            "• \"50 on groceries in january\""
        ),
        "no_expenses": "📭 No expenses found for *{label}*.",
        "no_stats": "📭 No stats available for *{label}*.",
        "no_chart": "📭 No data to chart for *{label}*.",
        "expenses_header": "📋 *{label} expenses:*\n",
        "expenses_total": "\n💰 *Total: ${total}*",
        "stats_header": "📊 *{label} stats:*\n",
        "chart_caption": "📊 {label} spending breakdown",
        "choose_language": "🌐 Choose your language:",
        "language_set": "✅ Language set to English!",
        "export_caption": "📁 Here are your *{count}* expenses as a CSV file.\nYou can open it in Excel or Google Sheets! 📊",
        "export_cmd": "📁 Export CSV",
        "analyzing": "🤖 Analyzing your message...",
        "generating_stats": "📊 Generating statistics...",
        "generating_chart": "📈 Building your chart...",
        "generating_advice": "💡 Preparing budget advice...",
        "manage_title": "📋 *Your recent expenses — tap to manage:*",
        "delete_btn": "🗑 Delete",
        "edit_btn": "✏️ Edit",
        "deleted": "✅ Expense deleted successfully!",
        "edit_prompt": (
            "✏️ *What do you want to change?*\n\n"
            "Send me the new details, for example:\n"
            "• \"change amount to 20\"\n"
            "• \"change category to Transport\"\n"
            "• \"change date to March 5\""
        ),
        "edit_saved": "✅ *Updated successfully!*\n\n📅 Date: {date}\n💰 Amount: ${amount}\n📂 Category: {category}\n📝 Note: {note}",
        "expense_not_found": "❌ Expense not found.",
        "btn_stats": "📊 Statistics",
        "btn_advice": "💡 Budget Advice",
        "btn_export": "📁 Export CSV",
        "btn_language": "🌐 Language",
        "btn_manage": "✏️ Manage Expenses",
    },
    "uz": {
        "start": (
            "👋 *ExpenseAI ga xush kelibsiz!*\n\n"
            "Men sizning kunlik xarajatlaringizni oddiy suhbat orqali kuzataman.\n\n"
            "💬 *Misollar:*\n"
            "• \"tushlikka 25 dollar sarfladim\"\n"
            "• \"kecha transportga 15 to'ladim\"\n"
            "• \"yanvarda kiyimga 50 sarfladim\"\n\n"
            "✨ *Imkoniyatlar:*\n"
            "➕ Xarajat qo'shish\n"
            "📋 Xarajatlar tarixi\n"
            "📊 Statistika va grafiklar\n"
            "💡 AI byudjet maslahati\n"
            "📁 CSV yuklab olish\n"
            "🌐 Ingliz va O'zbek tili\n\n"
            "Quyidagi tugmalardan birini tanlang yoki yozishni boshlang! 👇"
        ),
        "cleared": "🗑 Barcha xarajatlaringiz o'chirildi. Yangi boshlanish! ✨",
        "multi_line": (
            "⚠️ Iltimos *bitta xarajat* yuboring!\n\n"
            "Masalan:\n"
            "• \"tushlikka 12 dollar\"\n"
            "• \"qahvaga 3.50 dollar\""
        ),
        "saved": "✅ *Xarajat saqlandi!*\n\n📅 Sana: {date}\n💰 Summa: ${amount}\n📂 Kategoriya: {category}\n📝 Izoh: {note}",
        "no_amount": (
            "❌ Xarajatni tushunmadim.\n\n"
            "Masalan:\n"
            "• \"ovqatga 20 dollar sarfladim\"\n"
            "• \"kecha taksiga 15 to'ladim\"\n"
            "• \"yanvarda oziq-ovqatga 50\""
        ),
        "no_expenses": "📭 *{label}* uchun xarajat topilmadi.",
        "no_stats": "📭 *{label}* uchun statistika yo'q.",
        "no_chart": "📭 *{label}* uchun ma'lumot yo'q.",
        "expenses_header": "📋 *{label} xarajatlari:*\n",
        "expenses_total": "\n💰 *Jami: ${total}*",
        "stats_header": "📊 *{label} statistikasi:*\n",
        "chart_caption": "📊 {label} xarajatlar taqsimoti",
        "choose_language": "🌐 Tilni tanlang:",
        "language_set": "✅ Til o'zbekchaga o'zgartirildi!",
        "export_caption": "📁 *{count}* ta xarajatingiz CSV formatda.\nExcel yoki Google Sheets da ochishingiz mumkin! 📊",
        "export_cmd": "📁 CSV yuklab olish",
        "analyzing": "🤖 Xabaringiz tahlil qilinmoqda...",
        "generating_stats": "📊 Statistika tayyorlanmoqda...",
        "generating_chart": "📈 Grafik yaratilmoqda...",
        "generating_advice": "💡 Byudjet maslahati tayyorlanmoqda...",
        "manage_title": "📋 *So'nggi xarajatlar — boshqarish uchun bosing:*",
        "delete_btn": "🗑 O'chirish",
        "edit_btn": "✏️ Tahrirlash",
        "deleted": "✅ Xarajat muvaffaqiyatli o'chirildi!",
        "edit_prompt": (
            "✏️ *Nimani o'zgartirmoqchisiz?*\n\n"
            "Yangi ma'lumotlarni yuboring:\n"
            "• \"summani 20 ga o'zgartir\"\n"
            "• \"kategoriyani Transportga o'zgartir\"\n"
            "• \"sanani mart 5 ga o'zgartir\""
        ),
        "edit_saved": "✅ *Muvaffaqiyatli yangilandi!*\n\n📅 Sana: {date}\n💰 Summa: ${amount}\n📂 Kategoriya: {category}\n📝 Izoh: {note}",
        "expense_not_found": "❌ Xarajat topilmadi.",
        "btn_stats": "📊 Statistika",
        "btn_advice": "💡 Byudjet maslahati",
        "btn_export": "📁 CSV yuklab olish",
        "btn_language": "🌐 Til",
        "btn_manage": "✏️ Xarajatlarni boshqarish",
    }
}


def t(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS["en"]).get(key, TEXTS["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text
