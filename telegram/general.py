from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from storage.user import UserStorage
import logging


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

user_storage = UserStorage()


def start_command(bot, message) -> None:
    welcome_message = "Раді вас вітати у TreniBot!"
    bot.send_message(message.chat.id, welcome_message)

    contact_button = KeyboardButton("Поділитися номером", request_contact=True)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(contact_button)

    bot.send_message(
        message.chat.id,
        "Для початку роботи надішліть ваш номер телефону!",
        reply_markup=keyboard,
    )


def process_contact(bot, message) -> None:
    if message.contact and hasattr(message.contact, "phone_number"):
        phone_number = message.contact.phone_number
        user_id = message.chat.id

        try:
            user_saved = user_storage.save_user(user_id, phone_number)
            if user_saved:
                bot.send_message(
                    message.chat.id,
                    "Дякуємо за реєстрацію! Тепер ви можете користуватися TreniBot.",
                    reply_markup=ReplyKeyboardRemove(),
                )
                show_bmi_button(bot, message.chat.id)
                logger.info(
                    "User %s saved with phone number: %s", user_id, phone_number
                )
            else:
                error_message = (
                    "Не вдалося зберегти ваш номер телефону. Спробуйте ще раз."
                )
                bot.send_message(message.chat.id, error_message)
                logger.error(
                    "Failed to save user %s: Database operation failed", user_id
                )

        except Exception as e:
            error_message = "Не вдалося зберегти ваш номер телефону. Спробуйте ще раз."
            bot.send_message(message.chat.id, error_message)
            logger.error("Error saving user %s: %s", user_id, e)

    else:
        logger.warning("Contact information not received for user %s.", message.chat.id)
        prompt_contact_request(bot, message)


def show_bmi_button(bot, chat_id: int) -> None:
    bmi_button = KeyboardButton("/bmi")
    bmi_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bmi_keyboard.add(bmi_button)

    bot.send_message(
        chat_id,
        "Тепер ви можете ввести ваші дані для обчислення BMI.",
        reply_markup=bmi_keyboard,
    )


def prompt_contact_request(bot, message) -> None:
    contact_button = KeyboardButton("Поділитися номером", request_contact=True)
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(contact_button)

    bot.send_message(
        message.chat.id,
        "Будь ласка, надішліть ваш номер телефону.",
        reply_markup=keyboard,
    )
