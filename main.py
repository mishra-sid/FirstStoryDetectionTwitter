from StoryGeneration import StoryGenerator
from TFIDF_optim import TFIDF_optim 

#Main script
stories = StoryGenerator("./Dataset").getAllStories()
print(len(stories))
tfidf = TFIDF_optim(stories)
tfidf.tfidf()
print(tfidf.get_important_words())
