# FirstStoryDetectionTwitter

#Dataset : http://www.daviddlewis.com/resources/testcollections/reuters21578/
#Steps:
1. Pre-processing Reuters dataset : Write regex to parse and extract stories in memory.# Return a iterator (yield) to extracted stories)  
2. Character shingle : Length - 7 :Function that takes a string and returns it's shingle id 
3. Count and calculate tf and idf scores:
   i) Python dictionary, add key as we see.
4. Get the tf-idf scores of those shingles.
5. Throw away stop words ( idf > 0.9 ) and do for each key in dictionary : key -> index. 
6. Generate 100 hash functions ( ( k * x + r) % c ) G.C.D (k, c) == 1.
7. Get signature matrix for each hash function.
   i) the value in each element of matrix is bool(tf-idf score > PARAM_threshold_tf_idf).
8. L.S.H : 
   i) PARAM_number_of_bands , PARAM_number_of_rows_in_each_band and split.
   ii) Generate K bucket hash functions : f(xor of the band per document) mod K.
   iii) Confirm it with cosine similarity for candidate pairs O(Summation(Candidate pairsC2))
   iv) Key : PARAM_number_bands_matched, PARAM_threshold_cosine_similarity : Remove the false positives.
   v) Pick the ones with the least time stamp -> First story & family detected.
   
LSH split :
Ankit : False positive removal , candidate pair checking and final decision 
Raaghav : Dynamic bucketing using (Method - ii) 
Siddhartha : Static bucketing + False postitive removal using similarity score in all pairs per bucket.

#Extension:
1. Extend dynamic method without ML
Abhinav:
1. Extend dynamic method using ML ( Transfer Learning) 
