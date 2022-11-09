import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, Updater


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("supportbot")

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def main() -> None:
    load_dotenv()
    updater = Updater(token=os.getenv("TGBOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

