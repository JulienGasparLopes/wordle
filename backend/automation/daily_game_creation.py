from datetime import datetime
from os import environ
import random

from backend.core.game_repository import GameRepository
from backend.core.word_service import WordService
from backend.database.database import Database
import requests
from dotenv import load_dotenv


def main() -> None:
    database = Database()
    game_repository = GameRepository(database)
    word_service = WordService()

    word_length = random.choice([*[5] * 10, *[6] * 12, *[7] * 5, *[8] * 2, *[9] * 1])

    while True:
        new_word = word_service.get_random_word(word_length)
        if len(new_word) == len({letter for letter in new_word}):
            break

    game_repository.add_game(new_word, start_date=datetime.now())

    print("Game created with word:", new_word)

    if slack_url := environ.get("SLACK_GAME_CREATION_WEBHOOK_URL"):
        response: requests.Response = requests.post(
            slack_url,
        )
        if response.ok:
            print("Notification sent to Slack:", response.text)
        else:
            print("Failed to send notification to Slack:", response.text)


if __name__ == "__main__":
    load_dotenv()
    main()
