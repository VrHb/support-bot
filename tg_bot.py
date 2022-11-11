import os
import logging

from google.cloud import dialogflow
from dotenv import load_dotenv

import telegram
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, Updater


class TgbotLogger(logging.Handler):
    
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def detect_intent_texts(text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(
        str(os.getenv("GG_DF_ID")),
        str(os.getenv("GG_DF_SESSION_ID"))
    )
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        return None
    return response.query_result.fulfillment_text


def send_reply(update: Update, context: CallbackContext):
    response_text = detect_intent_texts(update.message.text, "ru-RU")
    if response_text:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_text
        )
    

def main() -> None:
    load_dotenv()
    logger = logging.getLogger("supportbot")
    logger_bot = telegram.Bot(token=str(os.getenv("TG_LOGGER_TOKEN")))
    logger.setLevel(logging.WARNING)
    bot_logger = TgbotLogger(logger_bot, os.getenv("GG_DF_SESSION_ID"))
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

