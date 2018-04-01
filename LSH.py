from constants import *
from hash_helper import *
from itertools import combinations

class LSH:

	def __init__(self, signature_matrix, stories, important_words):
		self.signature_matrix = signature_matrix
		self.stories = stories
		self.important_words = important_words
		self.len_docs = len(stories)
		self.len_imp_words = len(important_words)
		self.hash_func = xor_range_hasher(self.len_imp_words)
		self.buckets = [ { } for x in range(NUM_BUCKETS)]
    
	def hash_to_buckets(self):
		for doc in range(self.len_docs):
			xor_vals = []
			for band_no in range( NUM_BANDS):
				starting =  int(NUM_MINHASH_FUNCTIONS/ NUM_BANDS) * band_no
				ending = starting + int(NUM_MINHASH_FUNCTIONS/ NUM_BANDS)
				xor_vals.append(self.signature_matrix[starting][doc])
				for i in range(starting+1, ending): 
					xor_vals[band_no] = xor_vals[band_no] ^ self.signature_matrix[i][doc]

				if doc in self.buckets[int(self.hash_func(xor_vals[band_no]))]:
					self.buckets[int(self.hash_func(xor_vals[band_no]))][doc] += 1
				else:
					self.buckets[int(self.hash_func(xor_vals[band_no]))][doc] = 1	

	def hash_get_candidates(self):
		self.hash_to_buckets()
		candidate_pairs = []
		count = 0
		count_of_pairs = {}
		# for bucket in self.buckets:
			#print (len(bucket.keys()))
		for bucket in self.buckets:
			count = count +1
			#print (count)
			for key1, key2 in combinations ( bucket.keys(), 2):
			#	presence_count = 0
			#	for other_bucket in self.buckets:
			#		if key1 in other_bucket and key2 in other_bucket:
			#			presence_count += 1 
			
				if (key1,key2) in count_of_pairs:
					count_of_pairs[(key1,key2)] += 1
				else :
					count_of_pairs[(key1,key2)] = 1
		for pair in count_of_pairs.keys():
			#print (pair)
			if count_of_pairs[pair] >= THRESHOLD_NUM_BUCKETS_PAIR_PRESENT:
				#print(pair, count_of_pairs[pair])
				candidate_pairs.append(pair)
		return candidate_pairs



