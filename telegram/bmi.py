from typing import Optional
from models.bmi import BMIModel
from telebot.types import Message
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def process_bmi_command(bot, storage, message: Message) -> None:
    try:
        args = message.text.split()
        if len(args) != 2:
            _send_usage_message(bot, message.chat.id)
            return

        weight, height = _parse_weight_height(args)
        if weight is None or height is None:
            _send_usage_message(bot, message.chat.id)
            return

        user_id = message.from_user.id

        bmi_value = _calculate_and_save_bmi(storage, user_id, weight, height)
        recommendations = BMIModel(weight, height).get_recommendation(bmi_value)
        bot.send_message(
            message.chat.id, f"Ваш ІМТ: {bmi_value}\nРекомендація: {recommendations}"
        )

    except RuntimeError as re:
        if str(re) == "BMI record already exists for this user":
            bot.send_message(
                message.chat.id, "Ви вже додали свій ІМТ. Оновлення неможливе."
            )
        else:
            bot.send_message(
                message.chat.id, "На жаль, сталася помилка при додаванні вашого ІМТ."
            )

    except Exception as e:
        logger.error(
            "Unexpected error processing BMI command for user %s: %s",
            message.from_user.id,
            e,
        )
        bot.send_message(
            message.chat.id, "На жаль, у TreniBot виникла проблема. Спробуйте ще раз."
        )


def _send_usage_message(bot, chat_id: int) -> None:
    bot.send_message(chat_id, "Введіть вагу (кг) та ріст (см). Наприклад: 70 175")


def _parse_weight_height(args: list[str]) -> tuple[Optional[float], Optional[float]]:
    try:
        weight = float(args[0])
        height = float(args[1])
        return weight, height
    except ValueError as ve:
        logger.error("Invalid weight or height input: %s. Error: %s", args, ve)
        return None, None


def _calculate_and_save_bmi(
    storage, user_id: int, weight: float, height: float
) -> float:
    try:
        if storage.bmi_exists(user_id):
            logger.error("BMI record already exists for user %s", user_id)
            raise RuntimeError("BMI record already exists for this user")

        # Calculate BMI and save the record
        bmi_model = BMIModel(weight, height)
        bmi_value = bmi_model.calculate_bmi()

        success = storage.save_bmi_record(user_id, bmi_model)
        if not success:
            logger.error("Failed to save BMI record for user %s", user_id)
            raise RuntimeError("Failed to save BMI record")

        return bmi_value

    except Exception as e:
        logger.error("Error calculating and saving BMI for user %s: %s", user_id, e)
        raise
