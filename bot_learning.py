import argparse
import os
import json

from dotenv import load_dotenv
from google.cloud import dialogflow


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
    create_intent(
        os.getenv("GG_DF_ID"),
        "Как устроиться на работу",
       learning_phrases["Устройство на работу"]["questions"],
       [learning_phrases["Устройство на работу"]["answer"],],
    )

