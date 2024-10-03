from telegram.general import start_command, process_contact
from telegram.bmi import process_bmi_command
from storage.bmi import BmiStorage
from telebot.types import Message


def register_handlers(bot):
    storage = BmiStorage()

    @bot.message_handler(commands=["start"])
    def handle_start(message):
        start_command(bot, message)

    @bot.message_handler(content_types=["contact"])
    def handle_contact(message):
        process_contact(bot, message)

    @bot.message_handler(commands=["bmi"])
    def handle_bmi_command(message):
        process_bmi_command(bot, storage, message)

    @bot.message_handler(func=lambda message: True)
    def handle_message(message: Message):
        # Check if the message contains only numbers
        if message.text.replace(" ", "").replace(".", "").isdigit():
            process_bmi_command(bot, storage, message)  # Pass instance, not class
        else:
            bot.send_message(
                message.chat.id, "Будь ласка, введіть коректну команду або дані."
            )
