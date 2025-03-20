import random
from typing import Protocol

WORDS_LIST: list[str] = []


class WordServiceport(Protocol):
    def is_word_valid(self, word: str) -> bool: ...

    def get_random_word(self, word_length: int) -> str: ...


class WordService(WordServiceport):

    def __init__(self):
        global WORDS_LIST
        if not WORDS_LIST:
            with open("./core/word_list.txt", "r") as f:
                words_list = f.readlines()
                WORDS_LIST = [word.strip().replace("\n", "") for word in words_list]

    def is_word_valid(self, word: str) -> bool:
        return word in WORDS_LIST

    def get_random_word(self, word_length: int) -> str:
        return random.choice([word for word in WORDS_LIST if len(word) == word_length])
