from StoryGeneration import StoryGenerator
from TFIDF_optim import TFIDF_optim 
from MinHash import MinHash
from LSH import LSH
from FalsePositiveRemoval import FalsePositiveRemoval
from DeclareStories import DeclareStories
import numpy
from sklearn.decomposition import PCA
import matplotlib.pyplot as plot
from sklearn.cluster import KMeans

stories, titles = StoryGenerator("./Dataset").getAllStories()
tfidf = TFIDF_optim(stories)
tfidf.tfidf()
important_words = tfidf.get_important_words()
print('tfidf completed')
minHasher = MinHash(tfidf.stories, important_words)
signature_matrix = minHasher.get_signature_matrix()
print('signature matrix generated')
sigmat = numpy.array(signature_matrix).T
pca = PCA(n_components = 2, copy = False)
reducedVector = pca.fit_transform(sigmat)

plot.scatter(reducedVector[:,0], reducedVector[:,1])
plot.show()
kmeans = KMeans(n_clusters=2000, random_state = 0).fit(reducedVector)

story_threads = [[] for _ in range(2001)]
for i, item in enumerate(kmeans.labels_.tolist()):
	story_threads[item].append(i)

for value in story_threads:
	print("Connected Stories:-")
	for i, story in enumerate(value):
		if (i >= 5):
			break
		print('\t', titles[story]['title'])

# print('imp words\n', important_words)
# print('sig mat\n', signature_matrix)
# lsh = LSH( signature_matrix, stories, important_words)
# candidates = lsh.hash_get_candidates()
# candidatesNum = len(candidates)
# print('candidate pairs generated')
# print('number of candidates:', candidatesNum)

# FPRemover = FalsePositiveRemoval(candidates, tfidf.stories, titles)
# true_pairs = FPRemover.RemoveFalsePositives()
# print('false positives identified')
# print ((1-(len(true_pairs)/candidatesNum)) * 100, 'percent of candidate pairs were false positives')

# StorySplitter = DeclareStories(true_pairs, len(stories))
# connectedComponents = StorySplitter.findConnectedComponents()
# print('Connected Components have been seperated')
# print('Found', len(connectedComponents), ' connected components of graph')

# for value in sorted(connectedComponents.values(), key = lambda l: len(l), reverse = True):
# 	#print("Connected Stories:-")
# 	for i, story in enumerate(value):
# 		if (i >= 5):
# 			break
# 		#print('\t', titles[story]['title'])
