from turtle import update
from typing import Optional, Tuple
from models.bmi import BMIModel
from telebot import types, ContinueHandling
from translations.translations import translations
from handlers.menu import send_menu
from logger.logger import setup_logger

logger = setup_logger(__name__, log_file="bmi_handler.log")

def process_bmi_command(message: types.Message, bot, storage, lang: str) -> None:
    logger.info(
        "Received BMI command from user %s with message: %s",
        message.from_user.id,
        message.text,
    )

    weight, height = _extract_weight_height(message)

    if weight is None or height is None:
        logger.info(
            "Invalid weight or height extracted from message %s: weight=%s, height=%s",
            message.text,
            weight,
            height,
        )
        _send_usage_message(message.chat.id, bot, lang)
        return

    user_id = message.from_user.id
    logger.info(
        "Processing BMI for user %s: weight=%s, height=%s", user_id, weight, height
    )

    try:
        bmi_value, recommendations, category = _update_or_create_bmi(
            storage, user_id, weight, height, lang
        )

        logger.info(
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

        _send_training_options(bot, message.chat.id, lang, category)
        return ContinueHandling()

    except ValueError as ve:
        logger.warning("ValueError processing BMI for user %s: %s", user_id, ve)
        bot.send_message(message.chat.id, translations["invalid_bmi_input"][lang])
        send_menu(bot, message.chat.id, translations["menu_prompt"][lang], user_lang)
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
) -> Tuple[float, str, str]:
    logger.info("Updating or creating BMI for user %s", user_id)
    bmi_model = BMIModel(user_id, weight, height, lang)

    if not bmi_model.validate():
        error_message = translations["invalid_bmi_input"][lang]
        logger.info(
            "BMI validation failed for user %s: weight=%s, height=%s",
            user_id,
            weight,
            height,
        )
        raise ValueError(error_message)

    if storage.bmi_exists(user_id):
        logger.info("Updating existing BMI record for user %s", user_id)
        storage.update_bmi_record(user_id, weight, height, bmi_model.calculate_bmi())
        return bmi_model.calculate_bmi(), bmi_model.get_recommendation(), bmi_model.get_category()

    logger.info("Creating new BMI record for user %s", user_id)
    if not storage.save_bmi_record(user_id, bmi_model, bmi_model.calculate_bmi()):
        logger.error("Failed to save BMI record for user %s", user_id)
        raise RuntimeError("Failed to save BMI record")

    return bmi_model.calculate_bmi(), bmi_model.get_recommendation(), bmi_model.get_category()


def _send_usage_message(chat_id: int, bot, lang: str = "uk") -> None:
    logger.info("Sending usage message to chat %s", chat_id)
    bot.send_message(chat_id, translations["invalid_input"][lang])
    send_menu(bot, chat_id, translations["menu_prompt"][lang], lang)


def _extract_weight_height(message: types.Message) -> Tuple[Optional[float], Optional[float]]:
    logger.info("Extracting weight and height from message %s", message.text)
    if not message.text:
        logger.warning("Message from user %s has no text", message.from_user.id)
        return None, None

    try:
        weight, height = map(float, message.text.split())
        logger.info("Extracted weight=%s, height=%s from message", weight, height)
        return weight, height
    except (ValueError, TypeError):
        logger.warning(
            "Invalid input for weight/height from user %s: %s",
            message.from_user.id,
            message.text,
        )
        return None, None

def _send_training_options(bot, chat_id: int, lang: str, category: str) -> None:
    logger.info("Sending training options to user %s based on category %s", chat_id, category)

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    if category == "underweight":
        keyboard.add(types.InlineKeyboardButton(text=translations["weight_gain"][lang], callback_data="weight_gain"))
    elif category == "normal":
        keyboard.add(
            types.InlineKeyboardButton(text=translations["weight_gain"][lang], callback_data="weight_gain"),
            types.InlineKeyboardButton(text=translations["maintenance"][lang], callback_data="maintenance"),
            types.InlineKeyboardButton(text=translations["weight_loss"][lang], callback_data="weight_loss"),
        )
    elif category == "overweight":
        keyboard.add(
            types.InlineKeyboardButton(text=translations["support"][lang], callback_data="support"),
            types.InlineKeyboardButton(text=translations["weight_loss"][lang], callback_data="weight_loss"),
        )
    elif category == "obesity":
        bot.send_message(chat_id, translations["consultation_nutritionist"][lang])
        return


    bot.send_message(
        chat_id,
        translations["choose_training_plan"][lang],
        reply_markup=keyboard,
    )


def _handle_runtime_error(re: RuntimeError, message: types.Message, bot, lang: str) -> None:
    logger.info("Handling RuntimeError for user %s: %s", message.from_user.id, re)
    error_message = (
        translations["bmi_exists"][lang]
        if "already exists" in str(re)
        else translations["error_occurred"][lang]
    )
    bot.send_message(message.chat.id, error_message)
    send_menu(bot, message.chat.id, translations["menu_prompt"][lang], lang)
