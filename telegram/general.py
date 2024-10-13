from telebot.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Message,
)
from storage.user import UserStorage
from translations.translations import translations
from telegram.menu import send_menu
from logger.logger import setup_logger

logger = setup_logger(__name__, log_file="bot.log")

user_storage = UserStorage()
temp_user_storage = {}


def start_command(bot, message: Message, lang: str = "uk") -> None:
    user_id = message.chat.id
    logger.info("Start command invoked by user %s", user_id)

    if user_storage.user_exists(user_id):
        _welcome_back(bot, user_id, lang)
    else:
        _ask_language_selection(bot, user_id)


def process_contact(bot, message: Message) -> None:
    user_id = message.chat.id
    logger.info("Processing contact for user %s", user_id)

    if user_id not in temp_user_storage:
        logger.warning("User %s is not in temporary storage.", user_id)
        return

    lang = temp_user_storage[user_id]["language"]

    if not _is_valid_contact(message):
        _request_contact_again(bot, user_id, lang)
        return

    phone_number = message.contact.phone_number
    _register_user(bot, user_id, phone_number, lang)


def _welcome_back(bot, user_id: int, lang: str) -> None:
    logger.info("User %s found in storage. Sending welcome back message.", user_id)
    bot.send_message(
        user_id,
        translations["welcome_back"][lang],
        reply_markup=ReplyKeyboardRemove(),
    )
    show_menu(bot, user_id, lang)


def _ask_language_selection(bot, chat_id: int) -> None:
    logger.debug("Asking user %s for language selection.", chat_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("🇺🇦 Українська"), KeyboardButton("🇬🇧 English"))

    bot.send_message(
        chat_id, translations["select_language"]["en"], reply_markup=keyboard
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id, lambda message: _handle_language_selection(bot, message)
    )


def _handle_language_selection(bot, message: Message) -> None:
    user_id = message.chat.id
    selected_lang = "uk" if message.text == "🇺🇦 Українська" else "en"
    temp_user_storage[user_id] = {"language": selected_lang}

    logger.info("User %s selected language: %s", user_id, selected_lang)
    _send_contact_request(bot, user_id, selected_lang)


def _register_user(bot, user_id: int, phone_number: str, lang: str) -> None:
    logger.debug("Received contact for user %s: %s", user_id, phone_number)
    try:
        if user_storage.save_user(user_id, phone_number, lang):
            bot.send_message(
                user_id,
                translations["registration_success"][lang],
                reply_markup=ReplyKeyboardRemove(),
            )
            show_menu(bot, user_id, lang)
            logger.info("User %s saved with phone number: %s", user_id, phone_number)
        else:
            _handle_save_error(bot, user_id, lang)
        del temp_user_storage[user_id]
    except Exception as e:
        _handle_save_error(bot, user_id, lang, e)


def show_menu(bot, chat_id: int, lang: str) -> None:
    logger.info("Showing menu for user %s", chat_id)
    send_menu(bot, chat_id, translations["menu_prompt"][lang], lang)


def _send_contact_request(bot, user_id: int, lang: str) -> None:
    bot.send_message(
        user_id,
        translations["request_contact"][lang],
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        ).add(
            KeyboardButton(translations["contact_button"][lang], request_contact=True)
        ),
    )


def _request_contact_again(bot, user_id: int, lang: str) -> None:
    logger.warning("Contact information not received for user %s.", user_id)
    _send_contact_request(bot, user_id, lang)


def _is_valid_contact(message: Message) -> bool:
    return message.content_type == "contact" and message.contact is not None


def _handle_save_error(bot, user_id: int, lang: str, error: Exception = None) -> None:
    if error:
        logger.error("Error saving user %s: %s", user_id, error)
    else:
        logger.warning("Failed to save user %s", user_id)
    bot.send_message(user_id, translations["registration_failed"][lang])
