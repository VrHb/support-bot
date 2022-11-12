import argparse
import os
import logging
import json

from dotenv import load_dotenv
from google.cloud import dialogflow


logger = logging.getLogger("supportbot")

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
        str(os.getenv("GOOGLE_PROJECT_ID")),
        str(os.getenv("GOOGLE_SESSION_ID"))
    )
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        return None
    return response.query_result.fulfillment_text


def create_intent(
    project_id,
    display_name,
    training_phrases_parts,
    message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrase_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrase_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    print(f"Intent created: {response}")

    
if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Модуль обучает нейросеть DialogFlow"
    )
    parser.add_argument(
        "-p",
        "--json_path",
        help="Путь с json файлу с фразами",
        default="."
    )
    parser.add_argument(
        "-f",
        "--file_name",
        help="Имя json файла с фразами",
        default="questions.json"
    )
    args = parser.parse_args()
    json_phrases_path = os.path.join(args.json_path, args.file_name)
    with open(json_phrases_path, "rb") as file:
        learning_phrases = json.load(file)
    for intent_name in learning_phrases:
        create_intent(
            os.getenv("GOOGLE_PROJECT_ID"),
            intent_name,
            learning_phrases[intent_name]["questions"],
            [learning_phrases[intent_name]["answer"],],
        )

