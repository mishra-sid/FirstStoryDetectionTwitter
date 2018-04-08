from constants import *
from hash_helper import *
from threading import Thread
import multiprocessing

class MinHash:
    def __init__(self, stories, important_words):
        self.stories = stories
        self.len_docs = len(stories)
        for story in self.stories:
            story['story'] = set(story['story'])

        self.important_words = important_words 
        self.len_words = len(important_words)
        self.num_threads = multiprocessing.cpu_count()
        print("length of words", self.len_words)
        self.hash_functions = generate_permutation_hash_functions(self.len_words, NUM_MINHASH_FUNCTIONS)
    
    def worker_thread(self, index):
        starting = int((index * NUM_MINHASH_FUNCTIONS) / self.num_threads)
        ending = int(((index + 1) * NUM_MINHASH_FUNCTIONS) / self.num_threads)
        iter_hash = starting 
        for func in self.hash_functions[ starting : ending]: 
            a , b = func['a'] , func['b']
            iter_count = 0
            document_set = set(range(self.len_docs)) 
            x = 1
            while iter_count < self.len_words:
                if len(document_set) == 0:
                    break
                curr = self.important_words[x][0]
                to_remove = []
                for element in document_set:
                    if curr in self.stories[element]['story']:
                        to_remove.append(element)
                        self.signature_matrix[iter_hash][element] = iter_count

                for element in to_remove:
                    document_set.remove(element)

                x = (a * x + b) % self.len_words
                iter_count += 1


            print("iter hash", iter_hash)
            iter_hash += 1


        
    def get_signature_matrix(self):
        self.signature_matrix = [ [0 for x in range(self.len_docs)] for y in range(NUM_MINHASH_FUNCTIONS) ]
        
        threads = []
        for index in range(self.num_threads):
            threads.append(Thread(target=self.worker_thread, args=(index, )))

        for index in range(self.num_threads):
            threads[index].start()
        for index in range(self.num_threads):
            threads[index].join()

        return self.signature_matrix
