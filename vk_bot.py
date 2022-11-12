import os
import random
import logging

import telegram
from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from bot_learning import detect_intent_texts, TgbotLogger 


logger = logging.getLogger("supportbot")

def send_reply(event, vk_api):
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    session_id = os.getenv("GOOGLE_SESSION_ID")
    response = detect_intent_texts(
        event.text,
        "ru-RU",
        project_id,
        session_id
    )
    response_text = response.query_result.fulfillment_text
    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response_text,
            random_id=random.randint(1, 100)
        )


if __name__ == "__main__":
    load_dotenv()
    session_id = os.getenv("GOOGLE_SESSION_ID")
    logger_bot = telegram.Bot(token=str(os.getenv("TG_LOGGER_TOKEN")))
    logger.setLevel(logging.WARNING)
    bot_logger = TgbotLogger(logger_bot, session_id)
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

