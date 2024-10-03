import os
import logging
from dotenv import load_dotenv
import telebot
from telegram.handler import register_handlers


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_config() -> str:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables.")
        raise ValueError("TELEGRAM_BOT_TOKEN not found.")

    return token


def initialize_bot(token: str) -> telebot.TeleBot:
    bot_instance = telebot.TeleBot(token)
    register_handlers(bot_instance)
    return bot_instance


def start_bot(bot: telebot.TeleBot) -> None:
    logger.info("Bot is starting...")
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error("An error occurred while polling: %s", e)


if __name__ == "__main__":
    try:
        token = load_config()
        bot = initialize_bot(token)
        start_bot(bot)
    except Exception as e:
        logger.error("Failed to initialize the bot: %s", e)
