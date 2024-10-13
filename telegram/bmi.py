from typing import Optional, Tuple
from models.bmi import BMIModel
from telebot.types import Message
from translations.translations import translations
from telegram.menu import send_menu
from logger.logger import setup_logger

logger = setup_logger(__name__, log_file="bmi_app.log")


def process_bmi_command(message: Message, bot, storage, lang: str) -> None:
    logger.debug(
        "Received BMI command from user %s with message: %s",
        message.from_user.id,
        message.text,
    )

    weight, height = _extract_weight_height(message)

    if weight is None or height is None:
        logger.debug(
            "Invalid weight or height extracted from message %s: weight=%s, height=%s",
            message.text,
            weight,
            height,
        )
        _send_usage_message(message.chat.id, bot, lang)
        return

    user_id = message.from_user.id
    logger.debug(
        "Processing BMI for user %s: weight=%s, height=%s", user_id, weight, height
    )

    try:
        bmi_value, recommendations = _update_or_create_bmi(
            storage, user_id, weight, height, lang
        )

        logger.debug(
            "BMI calculation complete for user %s: bmi_value=%s, recommendations=%s",
            user_id,
            bmi_value,
            recommendations,
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
        send_menu(bot, message.chat.id, translations["menu_prompt"][lang])
    except RuntimeError as re:
        logger.error("RuntimeError processing BMI for user %s: %s", user_id, re)
        _handle_runtime_error(re, message, bot, lang)
    except Exception as e:
        logger.error(
            "Unexpected error processing BMI command for user %s: %s", user_id, e
        )
        bot.send_message(message.chat.id, translations["error_occurred"][lang])
        send_menu(bot, message.chat.id, translations["menu_prompt"][lang], lang)


def _update_or_create_bmi(
    storage, user_id: int, weight: float, height: float, lang: str
) -> Tuple[float, str]:
    logger.debug("Updating or creating BMI for user %s", user_id)
    bmi_model = BMIModel(user_id, weight, height, lang)

    if not bmi_model.validate():
        error_message = translations["invalid_bmi_input"][lang]
        logger.debug(
            "BMI validation failed for user %s: weight=%s, height=%s",
            user_id,
            weight,
            height,
        )
        raise ValueError(error_message)

    if storage.bmi_exists(user_id):
        logger.debug("Updating existing BMI record for user %s", user_id)
        storage.update_bmi_record(user_id, weight, height, bmi_model.calculate_bmi())
        return bmi_model.calculate_bmi(), bmi_model.get_recommendation()

    logger.debug("Creating new BMI record for user %s", user_id)
    if not storage.save_bmi_record(user_id, bmi_model):
        logger.error("Failed to save BMI record for user %s", user_id)
        raise RuntimeError("Failed to save BMI record")

    return bmi_model.calculate_bmi(), bmi_model.get_recommendation()


def _send_usage_message(chat_id: int, bot, lang: str = "uk") -> None:
    logger.debug("Sending usage message to chat %s", chat_id)
    bot.send_message(chat_id, translations["invalid_input"][lang])
    send_menu(bot, chat_id, translations["menu_prompt"][lang], lang)


def _extract_weight_height(message: Message) -> Tuple[Optional[float], Optional[float]]:
    logger.debug("Extracting weight and height from message %s", message.text)
    if not message.text:
        logger.warning("Message from user %s has no text", message.from_user.id)
        return None, None

    try:
        weight, height = map(float, message.text.split())
        logger.debug("Extracted weight=%s, height=%s from message", weight, height)
        return weight, height
    except (ValueError, TypeError):
        logger.warning(
            "Invalid input for weight/height from user %s: %s",
            message.from_user.id,
            message.text,
        )
        return None, None


def _handle_runtime_error(re: RuntimeError, message: Message, bot, lang: str) -> None:
    logger.error("Handling RuntimeError for user %s: %s", message.from_user.id, re)
    error_message = (
        translations["bmi_exists"][lang]
        if "already exists" in str(re)
        else translations["error_occurred"][lang]
    )
    bot.send_message(message.chat.id, error_message)
    send_menu(bot, message.chat.id, translations["menu_prompt"][lang], lang)
