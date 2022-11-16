import os
from functools import partial
import logging

from dotenv import load_dotenv

import telegram
from telegram.ext import MessageHandler, Filters, Updater

from bot_learning import detect_intent_texts, TgbotLogger 


logger = logging.getLogger("supportbot")

def send_reply(update, context, project_id, session_id):
    response = detect_intent_texts(
        update.message.text, 
        "ru-RU",
        project_id=project_id,
        session_id=session_id 
        )
    response_text = response.query_result.fulfillment_text
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text
    )
    

def main() -> None:
    load_dotenv()
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    tg_session_id = f"tg-{os.getenv('TG_USER_ID')}"
    tg_logger_chat_id = os.getenv("TG_USER_ID")
    logger_bot = telegram.Bot(token=str(os.getenv("TG_LOGGER_TOKEN")))
    logger.setLevel(logging.WARNING)
    bot_logger = TgbotLogger(logger_bot, tg_logger_chat_id)
    logger.addHandler(bot_logger)
    try:
        updater = Updater(token=os.getenv("TGBOT_TOKEN"), use_context=True)
        dispatcher = updater.dispatcher
        message_handler = MessageHandler(
            Filters.text & (~Filters.command),
            partial(send_reply, session_id=tg_session_id, project_id=project_id)
        )
        dispatcher.add_handler(message_handler)
        updater.start_polling()
        logger.warning("Telegram bot поддержки запущен!")
        updater.idle()
    except Exception as e:
        logger.error(f"Telegram bot поддержки упал с ошибкой:\n{e}")


if __name__ == "__main__":
    main()

