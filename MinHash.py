from constants import *

class MinHash:
    def __init__(self, stories, important_words):
        self.stories = stories
        self.important_words = important_words

    def init_hash_functions(self):

