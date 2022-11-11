import os
import random

from google.cloud import dialogflow
from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


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
    vk_session = vk_api.VkApi(token=os.getenv("VK_API_KEY"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
           send_reply(event, vk_api)

