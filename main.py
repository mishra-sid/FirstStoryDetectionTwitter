from StoryGeneration import StoryGenerator
from TFIDF_optim import TFIDF_optim 
from MinHash import MinHash
from LSH import LSH
from FalsePositiveRemoval import FalsePositiveRemoval
from DeclareStories import DeclareStories


stories, titles = StoryGenerator("./Dataset").getAllStories()
tfidf = TFIDF_optim(stories)
tfidf.tfidf()
important_words = tfidf.get_important_words()
print('tfidf completed')
minHasher = MinHash(tfidf.stories, important_words)
signature_matrix = minHasher.get_signature_matrix()

print('signature matrix generated')

# print('imp words\n', important_words)
# print('sig mat\n', signature_matrix)
lsh = LSH( signature_matrix, stories, important_words)
candidates = lsh.hash_get_candidates()
candidatesNum = len(candidates)
print('candidate pairs generated')
print('number of candidates:', candidatesNum)

FPRemover = FalsePositiveRemoval(candidates, tfidf.stories, titles)
true_pairs = FPRemover.RemoveFalsePositives()
print('false positives identified')
print ((1-(len(true_pairs)/candidatesNum)) * 100, 'percent of candidate pairs were false positives')

StorySplitter = DeclareStories(true_pairs, len(stories))
connectedComponents = StorySplitter.findConnectedComponents()
print('Connected Components have been seperated')
print('Found', len(connectedComponents), ' connected components of graph')

for value in sorted(connectedComponents.values(), key = lambda l: len(l), reverse = True):
	#print("Connected Stories:-")
	for i, story in enumerate(value):
		if (i >= 5):
			break
		#print('\t', titles[story]['title'])
