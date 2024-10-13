from typing import Optional, Tuple
from models.bmi import BMIModel
from telebot.types import Message
from translations.translations import translations
from telegram.menu import send_menu
from logger.logger import setup_logger

logger = setup_logger(__name__, log_file="bmi_app.log")


def process_bmi_command(message: Message, bot, storage, lang: str) -> None:
    weight, height = _extract_weight_height(message)

    if weight is None or height is None:
        _send_usage_message(message.chat.id, bot, lang)
        return

    user_id = message.from_user.id

    try:
        bmi_value, recommendations = _update_or_create_bmi(
            storage, user_id, weight, height, lang
        )

        bot.send_message(
            message.chat.id,
            translations["bmi_result"][lang].format(
                bmi=bmi_value, recommendation=recommendations
            ),
        )
        send_menu(bot, message.chat.id, translations["menu_prompt"][lang], lang)

    except ValueError as ve:
        logger.warning("ValueError processing BMI for user %s: %s", user_id, ve)
        bot.send_message(message.chat.id, translations["invalid_bmi_input"][lang])
    except RuntimeError as re:
        _handle_runtime_error(re, message, bot, lang)
    except Exception as e:
        logger.error(
            "Unexpected error processing BMI command for user %s: %s", user_id, e
        )
        bot.send_message(message.chat.id, translations["error_occurred"][lang])


def _update_or_create_bmi(
    storage, user_id: int, weight: float, height: float, lang: str
) -> Tuple[float, str]:
    bmi_model = BMIModel(user_id, weight, height, lang)

    if not bmi_model.validate():
        error_message = translations["invalid_bmi_input"][lang]
        raise ValueError(error_message)

    if storage.bmi_exists(user_id):
        storage.update_bmi_record(user_id, weight, height, bmi_model.calculate_bmi())
        return bmi_model.calculate_bmi(), bmi_model.get_recommendation()

    if not storage.save_bmi_record(user_id, bmi_model):
        raise RuntimeError("Failed to save BMI record")

    return bmi_model.calculate_bmi(), bmi_model.get_recommendation()


def _send_usage_message(chat_id: int, bot, lang: str = "uk") -> None:
    bot.send_message(chat_id, translations["invalid_input"][lang])


def _extract_weight_height(message: Message) -> Tuple[Optional[float], Optional[float]]:
    if not message.text:
        logger.warning("Message from user %s has no text", message.from_user.id)
        return None, None

    try:
        weight, height = map(float, message.text.split())
        return weight, height
    except (ValueError, TypeError):
        logger.warning(
            "Invalid input for weight/height from user %s: %s",
            message.from_user.id,
            message.text,
        )
        return None, None


def _handle_runtime_error(re: RuntimeError, message: Message, bot, lang: str) -> None:
    error_message = (
        translations["bmi_exists"][lang]
        if "already exists" in str(re)
        else translations["error_occurred"][lang]
    )
    bot.send_message(message.chat.id, error_message)
