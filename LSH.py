from constants import *
from hash_helper import *
from itertools import combinations

class LSH:

    def __init__(self, signature_matrix, stories, important_words):
        self.signature_matrix = signature_matrix
        self.stories = stories
        self.important_words = important_words
        self.len_docs = len(stories)
        self.hash_func = xor_range_hasher(self.len_docs)
        self.len_imp_words = len(important_words)
        self.buckets = [ { } for x in range(NUM_BUCKETS)]
    
    def hash_to_buckets(self):
		for doc in range(self.len_docs):
			xor_vals = []
			for band_no in range( NUM_BANDS):
				starting =  (self.len_imp_words/ NUM_BANDS) * band_no
				ending = starting + (self.len_imp_words/ NUM_BANDS)
				xor_vals.append(self.signature_matrix[starting][doc])
				for i in range(starting+1, ending): 
					xor_vals[band_no] = xor_vals[band_no] ^ self.signature_matrix[i][doc]

				if doc in self.buckets[self.hash_func(xor_vals[band_no])]:
					self.buckets[self.hash_func(xor_vals[band_no])][doc] += 1
				else :
					self.buckets[self.hash_func(xor_vals[band_no])][doc] = 1	

	def hash_get_candidates(self):
		self.hash_to_buckets()
		candidate_pairs = []
		for bucket in self.buckets:
			for key1, key2 in combinations ( bucket.keys()):
				presence_count = 0
				for other_bucket in self.buckets:
					if key1 in bucket and key2 in other_bucket:
						presence_count += 1 
				if presence_count >= THRESHOLD_NUM_BUCKETS_PAIR_PRESENT:
					candidate_pairs.append( (key1, key2))
		return candidate_pairs



