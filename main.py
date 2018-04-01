from StoryGeneration import StoryGenerator
from TFIDF_optim import TFIDF_optim 
from MinHash import MinHash

#Main script
stories = StoryGenerator("./Dataset").getAllStories()
print(len(stories))
tfidf = TFIDF_optim(stories)
tfidf.tfidf()

minHasher = MinHash(tfidf.stories, tfidf.get_important_words())
print(minHasher.get_signature_matrix())
