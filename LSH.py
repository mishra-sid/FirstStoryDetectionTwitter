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
		self.buckets = [ [ ] for x in range(NUM_BUCKETS)]
    
	def hash_to_buckets(self):
		print (" Started to Hash Docs")
		
		hash_func = [xor_range_hasher(self.len_imp_words) for x in range(NUM_BANDS)]
		
		print ("Hash functions are ready")
		for doc in range(self.len_docs):
			xor_vals = []
			for band_no in range( NUM_BANDS):
				starting =  int(NUM_MINHASH_FUNCTIONS/ NUM_BANDS) * band_no
				ending = starting + int(NUM_MINHASH_FUNCTIONS/ NUM_BANDS)
				xor_vals.append(self.signature_matrix[starting][doc])
				for i in range(starting+1, ending): 
					xor_vals[band_no] = xor_vals[band_no] ^ self.signature_matrix[i][doc]
				self.buckets[int(hash_func[band_no](xor_vals[band_no]))].append( [doc,band_no])

	def hash_get_candidates(self):	
		self.hash_to_buckets()
		print ("Docs have been Hashed")
		candidate_pairs = []
		count = 0
		count_of_pairs = {}
		# for bucket in self.buckets:
			#print (len(bucket.keys()))
		for bucket in self.buckets:
			count = count +1
			#print (count)
			for key1, key2 in combinations ( bucket, 2):
			#	presence_count = 0
			#	for other_bucket in self.buckets:
			#		if key1 in other_bucket and key2 in other_bucket:
			#			presence_count += 1 
				if key1[1] == key2[1] : 
					if (key1[0],key2[0]) in count_of_pairs:
						count_of_pairs[(key1[0],key2[0])] += 1
					else :
						count_of_pairs[(key1[0],key2[0])] = 1
		print ("Docs have been counted")
		for pair in count_of_pairs.keys():
			#print (pair)
			if count_of_pairs[pair] >= THRESHOLD_NUM_BUCKETS_PAIR_PRESENT:
				#print(pair, count_of_pairs[pair])
				candidate_pairs.append(pair)
		print ("Candidate pairs have been generated")
		return candidate_pairs




