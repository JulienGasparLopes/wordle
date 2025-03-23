import os
import random
from typing import Protocol

WORDS_LIST: list[str] = []
WORDS_COMMON: list[str] = []


class WordServiceport(Protocol):
    def is_word_valid(self, word: str) -> bool: ...

    def get_random_word(self, word_length: int) -> str: ...


class WordService(WordServiceport):

    def __init__(self):
        path = "./core" if os.path.exists("./core") else "./backend/core"
        global WORDS_LIST
        if not WORDS_LIST:
            with open(path + "/words_all.txt", "r") as f:
                words_list = f.readlines()
                WORDS_LIST = [word.strip().replace("\n", "") for word in words_list]

        global WORDS_COMMON
        if not WORDS_COMMON:
            with open(path + "/words_common.txt", "r") as f:
                words_common = f.readlines()
                WORDS_COMMON = [word.strip().replace("\n", "") for word in words_common]

    def is_word_valid(self, word: str) -> bool:
        return word in WORDS_LIST

    def get_random_word(self, word_length: int) -> str:
        while True:
            word = random.choice(
                [word for word in WORDS_COMMON if len(word) == word_length]
            )
            if word in WORDS_LIST:
                return word
