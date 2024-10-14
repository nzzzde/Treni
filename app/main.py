import os
import signal
import sys
from dotenv import load_dotenv
import telebot
from telegram.handler import register_handlers
from logger.logger import setup_logger

logger = setup_logger(__name__)

bot_instance = None


def load_config() -> str:
    logger.info("Loading configuration from environment variables.")
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables.")
        raise ValueError("TELEGRAM_BOT_TOKEN not found.")

    logger.info("Successfully loaded TELEGRAM_BOT_TOKEN.")
    return token


def initialize_bot(token: str) -> telebot.TeleBot:
    logger.info("Initializing the bot.")
    bot = telebot.TeleBot(token)
    register_handlers(bot)
    logger.info("Bot handlers registered successfully.")
    return bot


def start_bot(bot: telebot.TeleBot) -> None:
    logger.info("Bot is starting...")
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error("An error occurred while polling: %s", e)
        raise


def graceful_shutdown(signal_num, frame):
    logger.info("Received shutdown signal (%s). Stopping bot...", signal_num)
    if bot_instance:
        logger.info("Shutting down the bot.")
    sys.exit(0)


if __name__ == "__main__":
    try:
        token = load_config()
        bot_instance = initialize_bot(token)

        signal.signal(signal.SIGINT, graceful_shutdown)
        signal.signal(signal.SIGTERM, graceful_shutdown)

        start_bot(bot_instance)
    except Exception as e:
        logger.error("Failed to initialize the bot: %s", e)
        sys.exit(1)
