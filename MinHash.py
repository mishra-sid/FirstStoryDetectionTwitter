from constants import *
from hash_helper import *



class MinHash:
    def __init__(self, stories, important_words):
        self.stories = stories
        self.len_docs = len(stories)
        for story in self.stories:
            story['story'] = set(story['story'])

        self.important_words = important_words 
        self.len_words = len(important_words)
        print("length of words", self.len_words)
        self.hash_functions = generate_permutation_hash_functions(self.len_words, NUM_MINHASH_FUNCTIONS)

    def get_signature_matrix(self):
        self.signature_matrix = [ [0 for x in range(self.len_docs)] for y in range(NUM_MINHASH_FUNCTIONS) ]
        
        iter_hash = 0 
        for func in self.hash_functions:
            a , b = func['a'] , func['b']
            iter_count = 0

            document_set = set(range(self.len_docs)) 
            x = 1
            print("iter hash", iter_hash)
            while iter_count < self.len_words:
                if len(document_set) == 0:
                    break
                #print("iter_hash", iter_hash, "iter_count", iter_count)
                curr = self.important_words[x][0]
                to_remove = []
                for element in document_set:
                    if curr in self.stories[element]['story']:
                        to_remove.append(element)
                        self.signature_matrix[iter_hash][element] = x
                
                for element in to_remove:
                    document_set.remove(element)

                x = (a * x + b) % self.len_words
                iter_count += 1

            iter_hash += 1

        return self.signature_matrix
