import os
import logging

from dotenv import load_dotenv

import telegram
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, Updater

from bot_learning import detect_intent_texts, TgbotLogger 


def send_reply(update: Update, context: CallbackContext):
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    session_id = os.getenv("GOOGLE_SESSION_ID")
    response_text = detect_intent_texts(
        update.message.text, 
        "ru-RU",
        project_id,
        session_id
        )
    if response_text:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_text
        )
    

def main() -> None:
    load_dotenv()
    session_id = os.getenv("GOOGLE_SESSION_ID")
    logger = logging.getLogger("supportbot")
    logger_bot = telegram.Bot(token=str(os.getenv("TG_LOGGER_TOKEN")))
    logger.setLevel(logging.WARNING)
    bot_logger = TgbotLogger(logger_bot, session_id)
    logger.addHandler(bot_logger)
    try:
        updater = Updater(token=os.getenv("TGBOT_TOKEN"), use_context=True)
        dispatcher = updater.dispatcher
        echo_handler = MessageHandler(
            Filters.text & (~Filters.command),
            send_reply
        )
        dispatcher.add_handler(echo_handler)
        updater.start_polling()
        logger.warning("Telegram bot поддержки запущен!")
        updater.idle()
    except Exception as e:
        logger.error(f"Telegram bot поддержки упал с ошибкой:\n{e}")


if __name__ == "__main__":
    main()

