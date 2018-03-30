from StoryGeneration import StoryGenerator
from TFIDF import TFIDF 

#Main script
stories = StoryGenerator("./Dataset").getAllStories()
tfidf = TFIDF(stories, 'english')
sparse_matrix = tfidf.get_sparse_matrix()

print(sparse_matrix)
