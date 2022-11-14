import argparse
import os
import logging
import json

from dotenv import load_dotenv
from google.cloud import dialogflow


class TgbotLogger(logging.Handler):
    
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def detect_intent_texts(text, language_code, project_id, session_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(
        project_id,
        session_id
    )
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response


def create_intent(project_id, display_name, questions, answer):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrase_part in questions:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrase_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[answer])
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
    project_id = os.getenv("GOOGLE_PROJECT_ID")
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
            project_id, 
            intent_name,
            **learning_phrases[intent_name]
        )

