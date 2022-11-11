import os
import random
import logging

import telegram
from google.cloud import dialogflow
from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


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


def send_reply(event, vk_api):
    response_text = detect_intent_texts(event.text, "ru-RU")
    if response_text:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response_text,
            random_id=random.randint(1, 100)
        )


if __name__ == "__main__":
    load_dotenv()
    logger = logging.getLogger("supportbot")
    logger_bot = telegram.Bot(token=str(os.getenv("TG_LOGGER_TOKEN")))
    logger.setLevel(logging.WARNING)
    bot_logger = TgbotLogger(logger_bot, os.getenv("GG_DF_SESSION_ID"))
    logger.addHandler(bot_logger)
    vk_session = vk_api.VkApi(token=os.getenv("VK_API_KEY"))
    vk_api = vk_session.get_api()
    try:
        longpoll = VkLongPoll(vk_session)
        logger.warning("VK bot поддержки запущен!")
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
               send_reply(event, vk_api)
    except Exception as e:
        logger.error(f"VK bot упал с ошибкой:\n{e}")

