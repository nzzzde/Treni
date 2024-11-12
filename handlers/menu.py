from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from translations.translations import translations
from storage.bmi import BmiStorage

bmi_storage = BmiStorage()


def get_translation(key, lang="uk", fallback=""):
    return translations.get(key, {}).get(lang, fallback)


def create_keyboard(user_id: int, lang="uk"):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    if bmi_storage.bmi_exists(user_id):
        btn_bmi_text = get_translation("bmi_update_button", lang, "Update BMI 🔄")
    else:
        btn_bmi_text = get_translation("bmi_calculate_button", lang, "Calculate BMI 📈")

    btn_bmi = KeyboardButton(btn_bmi_text)
    reference_btn = KeyboardButton(
        get_translation("reference_button", lang, "Reference 📚")
    )
    btn_about = KeyboardButton(get_translation("about_button", lang, "About 📖"))
    btn_change_language = KeyboardButton(
        get_translation("change_language_button", lang, "Change Language 🌐")
    )

    keyboard.add(btn_bmi, btn_about, reference_btn, btn_change_language)
    return keyboard


def send_menu(bot, chat_id, message, lang="uk"):
    user_id = chat_id
    try:
        bot.send_message(chat_id, message, reply_markup=create_keyboard(user_id, lang))
    except Exception as e:
        print(f"Error sending menu: {e}")
        bot.send_message(
            chat_id, get_translation("error_occurred", lang, "Error occurred.")
        )
