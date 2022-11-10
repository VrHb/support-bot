import os
import logging

from google.cloud import storage, dialogflow
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, Updater


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("supportbot")


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
    return response


def send_hello(update: Update, context: CallbackContext):
    intent_text = detect_intent_texts(update.message.text, "ru-RU")
    response_text = intent_text.query_result.fulfillment_text
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)


def main() -> None:
    load_dotenv()
    updater = Updater(token=os.getenv("TGBOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), send_hello)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

