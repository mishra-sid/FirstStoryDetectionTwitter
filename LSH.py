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
                hash_func = weighted_sum_hasher(int(NUM_MINHASH_FUNCTIONS/NUM_BANDS), self.len_imp_words, NUM_BANDS)
                print ("Hash functions are ready")
                for doc in range(self.len_docs):
                    for band_no in range( NUM_BANDS):
                        starting =  int((NUM_MINHASH_FUNCTIONS * band_no) / NUM_BANDS)
                        ending = int((NUM_MINHASH_FUNCTIONS * (band_no + 1)) / NUM_BANDS)
                        rows = []
                        for index in range(starting, ending):
                            rows.append(self.signature_matrix[index][doc])
                        bucket = int(hash_func[band_no](rows))
                        self.buckets[bucket].append([doc, band_no])  

        def hash_get_candidates(self):  
                self.hash_to_buckets()
                print ("Docs have been Hashed")
                candidate_pairs = []
                count_pair_num_bands = {}
                count = 0
                for bucket in self.buckets:
                    count += 1
                    print("Content in bucket", count,  len(bucket))
                    for key1, key2 in combinations(bucket, 2):
                        if key1[1] == key2[1]: 
                            if (key1[0],key2[0]) in count_pair_num_bands:
                                count_pair_num_bands[(key1[0], key2[0])] += 1
                            else:
                                count_pair_num_bands[(key1[0], key2[0])] = 1
                print ("Docs have been counted")
                for pair in count_pair_num_bands.keys():
                    #print (pair)
                    if count_pair_num_bands[pair] >= THRESHOLD_PAIRS_HASHED_SAME_BUCKET:
                        #print(pair, count_pair_num_bands[pair])
                        candidate_pairs.append(pair)
                print ("Candidate pairs have been generated")
                return candidate_pairs




