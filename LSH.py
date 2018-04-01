from constants import *
from hash_helper import *


class LSH:

    def __init__(self, signature_matrix, stories, important_words):
        self.signature_matrix = signature_matrix
        self.stories = stories
        self.important_words = important_words
        self.len_docs = len(stories)
        self.hash_func = xor_range_hasher(self.len_docs)
        
        self.buckets = [ { } for x in range(NUM_BUCKETS)]
    
    def hash_to_buckets(self):

