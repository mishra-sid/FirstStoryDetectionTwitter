from StoryGeneration import StoryGenerator
from TFIDF_optim import TFIDF_optim 
from MinHash import MinHash

#Main script
stories = StoryGenerator("./Dataset").getAllStories()
print(len(stories))
tfidf = TFIDF_optim(stories)
tfidf.tfidf()
important_words = tfidf.get_important_words()
minHasher = MinHash(tfidf.stories, important_words)
signature_matrix = minHasher.get_signature_matrix()

lsh = LSH( signature_matrix, stories, important_words)
print (lsh.hash_to_buckets())