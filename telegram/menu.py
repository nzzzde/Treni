from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from translations.translations import translations
from storage.bmi import BmiStorage

bmi_storage = BmiStorage()


def create_keyboard(user_id: int, lang="uk"):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn_bmi_text = translations.get("bmi_update_button", {}).get(lang, "Update BMI 🔄")
    if bmi_storage.bmi_exists(user_id):
        btn_bmi = KeyboardButton(btn_bmi_text)
    else:
        btn_bmi_text = translations.get("bmi_calculate_button", {}).get(
            lang, "Calculate BMI 📈"
        )
        btn_bmi = KeyboardButton(btn_bmi_text)

    btn_donate = KeyboardButton(
        translations.get("donate_button", {}).get(lang, "Donate 💖")
    )
    btn_guide = KeyboardButton(
        translations.get("guide_button", {}).get(lang, "Guide 📚")
    )
    btn_info = KeyboardButton(translations.get("info_button", {}).get(lang, "Info ℹ️"))

    keyboard.add(btn_bmi, btn_donate, btn_guide, btn_info)

    return keyboard


def send_menu(bot, chat_id, message, lang="uk"):
    user_id = chat_id
    bot.send_message(chat_id, message, reply_markup=create_keyboard(user_id, lang))
