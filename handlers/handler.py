import os
import random
from handlers.general import start_command, process_contact
from handlers.bmi import process_bmi_command
from storage.bmi import BmiStorage
from storage.user import UserStorage
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telebot import ContinueHandling
from translations.translations import translations
from handlers.general import temp_user_storage
from handlers.menu import send_menu
from logger.logger import setup_logger

user_storage = UserStorage()
bmi_storage = BmiStorage()
logger = setup_logger(__name__, log_file="handler.log")
user_workout_selection = {}
user_reminders = {}

video_sets = {
    "normal_lg": [
        ["n_lg_set1_p1.MP4", "n_lg_set1_p2.MP4"],
        ["n_lg_set2_p1.MP4", "n_lg_set2_p2.MP4"],
        ["n_lg_set3_p1.MP4", "n_lg_set3_p2.MP4"],
    ],
    "normal_keep": [
        ["n_keep_set1_p1.MP4", "n_keep_set1_p2.MP4"],
        ["n_keep_set2_p1.MP4", "n_keep_set2_p2.MP4"],
        ["n_keep_set3_p1.MP4", "n_keep_set3_p2.MP4"],
    ],
    "underweight": [
        ["uw_set1.MP4"],
        ["uw_set2.MP4"],
        ["uw_set3.MP4"],
    ],
    "overweight": [
        ["ow_set1_p1.MP4", "ow_set1_p2.MP4"],
        ["ow_set2_p1.MP4", "ow_set2_p2.MP4"],
        ["ow_set3_p1.MP4", "ow_set3_p2.MP4"],
    ],
}

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
        return ContinueHandling()

    @bot.message_handler(content_types=["contact"])
    def handle_contact(message: Message):
        process_contact(bot, message)
        return ContinueHandling()

    @bot.message_handler(func=lambda message: message.text == translations["reference_button"].get(user_storage.get_language(message.chat.id), "📖 Reference"))
    def handle_guide_button(message: Message):
        lang = user_storage.get_language(message.chat.id)
        guide_text = translations["guide_text"].get(lang, "")

        if guide_text:
            logger.info("Guide button clicked by user %s", message.chat.id)
            bot.send_message(message.chat.id, guide_text)
        else:
            logger.error("Guide text not found for user %s", message.chat.id)
            bot.send_message(message.chat.id, translations["unknown_command"][lang])

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
        logger.info("Received BMI calculate command from user %s", message.chat.id)
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
        logger.info("Received BMI update command from user %s", message.chat.id)
        bot.send_message(message.chat.id, translations["bmi_input_prompt"][lang])
        bot.register_next_step_handler(
            message, process_bmi_command, bot, bmi_storage, lang
        )

    @bot.callback_query_handler(func=lambda call: call.data in ["weight_gain", "maintenance", "weight_loss", "support"])
    def handle_workout_selection(call):
        workout_selected = call.data

        user_workout_selection[call.message.chat.id] = workout_selected
        logger.info("User %s selected workout: %s", call.message.chat.id, workout_selected)

        _send_training_days_options(bot, call.message.chat.id)


    @bot.callback_query_handler(func=lambda call: call.data in ["1_day", "2_days", "3_days"])
    def handle_day_selection(call):
        days_selected = call.data
        lang = user_storage.get_language(call.message.chat.id)
        workout_choice = user_workout_selection.get(call.message.chat.id)
        bmi_value = user_storage.get_user_bmi_value(call.message.chat.id)

        logger.info("User %s selected days: %s", call.message.chat.id, days_selected)

        if bmi_value == "underweight":
            workout_type = "underweight"
        elif bmi_value == "overweight":
            workout_type = "overweight" if workout_choice == "normal_lg" else "normal_keep"
        else:
            workout_type = "normal_keep" if workout_choice == "normal_keep" else "normal_lg"

        def extract_set_number(video_name):
            if "set" in video_name:
                return video_name.split('set')[1][0]
            return None

        def extract_set_number(video_name):
            return video_name.split('set')[1][0] if "set" in video_name else None

        num_sets_to_send = 1 if days_selected == "1_day" else 2 if days_selected == "2_days" else len(video_sets[workout_type])

        selected_sets = random.sample(video_sets[workout_type], num_sets_to_send)

        for video_set in selected_sets:
            set_number = extract_set_number(video_set[0])
            for video in video_set:
                video_path = os.path.abspath(f"resources/{video}")
                logger.info("Sending video: %s", video_path)
                with open(video_path, 'rb') as video_file:
                    bot.send_video(call.message.chat.id, video_file)

            instructions = translations["workouts"][workout_type][lang][f"set_{set_number}"]
            bot.send_message(call.message.chat.id, "\n".join(instructions))

        _prompt_reminder_days(bot, call.message.chat.id, days_selected, lang)


    @bot.message_handler(func=lambda message: message.chat.id in user_reminders)
    def handle_day_selection_for_reminder(message):
        chat_id = message.chat.id
        selected_day = message.text.replace(" ✅", "")
        user_lang = user_reminders[chat_id]["lang"]

        if selected_day not in user_reminders[chat_id]["selected_days"]:
            user_reminders[chat_id]["selected_days"].append(selected_day)

            remaining_days = user_reminders[chat_id]["total_days_needed"] - len(user_reminders[chat_id]["selected_days"])

            if remaining_days > 0:
                bot.send_message(
                    chat_id,
                    translations["select_more_days"][user_lang].format(remaining=remaining_days)
                )
            else:
                selected_days_text = ", ".join(user_reminders[chat_id]["selected_days"])
                bot.send_message(
                    chat_id,
                    translations["reminder_days_set"][user_lang].format(selected_days=selected_days_text),
                    reply_markup=ReplyKeyboardRemove()
                )
                logger.info("User %s reminder days saved: %s", chat_id, user_reminders[chat_id]["selected_days"])

                user_reminders.pop(chat_id, None)
                send_menu(bot, chat_id, translations["menu_prompt"][user_lang], user_lang)

                update_day_selection_keyboard(bot, chat_id, user_lang)

def _prompt_reminder_days(bot, chat_id: int, days_selected: str, lang: str):
    days_options = {
        "1_day": ["1"],
        "2_days": ["1", "2"],
        "3_days": ["1", "2", "3"]
    }

    user_reminders[chat_id] = {
        "selected_days": [],
        "total_days_needed": len(days_options[days_selected]),
        "lang": lang
    }

    update_day_selection_keyboard(bot, chat_id, lang)

def update_day_selection_keyboard(bot, chat_id: int, lang: str):
    keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    selected_days = user_reminders[chat_id]["selected_days"]
    lang_days = translations["days_of_week"][lang]

    for day in lang_days:
        day_text = f"{day} ✅" if day in selected_days else day
        keyboard.add(KeyboardButton(text=day_text))

    bot.send_message(
        chat_id,
        translations["select_reminder_days"][lang],
        reply_markup=keyboard
    )

def _send_training_days_options(bot, chat_id: int) -> None:
    lang = user_storage.get_language(chat_id)

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text=translations["1_day"][lang], callback_data="1_day"))
    keyboard.add(InlineKeyboardButton(text=translations["2_days"][lang], callback_data="2_days"))
    keyboard.add(InlineKeyboardButton(text=translations["3_days"][lang], callback_data="3_days"))

    bot.send_message(chat_id, translations["choose_training_days"][lang], reply_markup=keyboard)

def get_instruction_text(bmi_category, days_selected, lang):
    return translations["workouts"][f"{bmi_category}_training_keep"][lang][days_selected]
