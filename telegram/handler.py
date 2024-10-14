from telegram.general import start_command, process_contact
from telegram.bmi import process_bmi_command
from storage.bmi import BmiStorage
from storage.user import UserStorage
from telebot.types import Message
from translations.translations import translations
from telegram.general import temp_user_storage
from logger.logger import setup_logger

user_storage = UserStorage()
bmi_storage = BmiStorage()
logger = setup_logger(__name__, log_file="bmi_app.log")


def register_handlers(bot):
    @bot.message_handler(commands=["start"])
    def handle_start(message: Message):
        lang = user_storage.get_language(message.chat.id)
        if lang:
            start_command(bot, message, lang)
        else:
            start_command(bot, message)

    @bot.message_handler(
        func=lambda message: message.text in ["🇺🇦 Українська", "🇬🇧 English"]
    )
    def set_language(message: Message):
        lang = "uk" if message.text == "🇺🇦 Українська" else "en"
        temp_user_storage[message.chat.id] = {"language": lang}
        bot.send_message(message.chat.id, translations["start_welcome"][lang])

    @bot.message_handler(content_types=["contact"])
    def handle_contact(message: Message):
        process_contact(bot, message)

    @bot.message_handler(
        func=lambda message: message.text
        and message.text.lower()
        in [
            translations["bmi_calculate_button"]
            .get(user_storage.get_language(message.chat.id), "")
            .lower(),
        ]
    )
    def handle_bmi_command(message: Message):
        lang = user_storage.get_language(message.chat.id)
        logger.debug("Received BMI calculate command from user %s", message.chat.id)
        bot.send_message(message.chat.id, translations["bmi_input_prompt"][lang])
        bot.register_next_step_handler(
            message, process_bmi_command, bot, bmi_storage, lang
        )

    @bot.message_handler(
        func=lambda message: message.text
        and message.text.lower()
        in [
            translations["bmi_update_button"]
            .get(user_storage.get_language(message.chat.id), "")
            .lower(),
        ]
    )
    def handle_update_bmi_command(message: Message):
        lang = user_storage.get_language(message.chat.id)
        logger.debug("Received BMI update command from user %s", message.chat.id)
        bot.send_message(message.chat.id, translations["bmi_input_prompt"][lang])
        bot.register_next_step_handler(
            message, process_bmi_command, bot, bmi_storage, lang
        )

    @bot.message_handler(func=lambda message: True)
    def handle_unknown_message(message: Message):
        lang = user_storage.get_language(message.chat.id)
        logger.debug(
            "Unknown message received from user %s: %s", message.chat.id, message.text
        )
        bot.send_message(message.chat.id, translations["unknown_command"][lang])
