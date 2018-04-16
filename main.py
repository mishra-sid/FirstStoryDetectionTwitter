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
import os
import pickle
PICKLE_FILE = './signature_matrix_cache.dat'

stories, titles = StoryGenerator("./Dataset").getAllStories()
tfidf = TFIDF_optim(stories)
tfidf.tfidf()
important_words = tfidf.get_important_words()
print('tfidf completed')

signature_matrix = None 
if not os.path.exists(PICKLE_FILE):
    minHasher = MinHash(tfidf.stories, important_words)
    signature_matrix = minHasher.get_signature_matrix()
    print('signature matrix generated and cached')
    with open(PICKLE_FILE, 'wb') as wfile:
        pickle.dump(signature_matrix, wfile, pickle.HIGHEST_PROTOCOL) 
else:
    with open(PICKLE_FILE, 'rb') as rfile:
        signature_matrix = pickle.load(rfile)
        print('Signature matrix loaded from cache')

sigmat = numpy.array(signature_matrix).T
pca = PCA(n_components = 2, copy = False)
reducedVector = pca.fit_transform(sigmat)

plot.scatter(reducedVector[:,0], reducedVector[:,1])
plot.show()

print("Starting Clustering with kmeans")
numClusters = 100
kmeans = KMeans(n_clusters=numClusters, random_state = 0).fit(reducedVector)

story_threads = [[] for _ in range(numClusters)]
storycount = 0
for i, item in enumerate(kmeans.labels_.tolist()):
	storycount += 1
	story_threads[item].append(i)

nonzeroclusters = 0
for value in story_threads:
	print("Connected Stories (First 5 titles):-")
	if len(value) != 0:
		nonzeroclusters += 1
	print(len(value))
	for i, story in enumerate(value):
		if (i >= 5):
			break
		#print('\t', titles[story]['title'])

print('Average non-zero cluster size is ', (storycount/nonzeroclusters), 'and', 100-nonzeroclusters, 'out of 100 clusters are empty')

