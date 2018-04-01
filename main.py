from StoryGeneration import StoryGenerator
from TFIDF_optim import TFIDF_optim 
from MinHash import MinHash
from LSH import LSH
from FalsePositiveRemoval import FalsePositiveRemoval
#Main script
stories, titles = StoryGenerator("./Dataset").getAllStories()
print('Stories found:', len(stories))
print('Titles found:', len(titles))
tfidf = TFIDF_optim(stories)
tfidf.tfidf()
print('tfidf completed')
# print('stories')
# for item in list(map(lambda x: set(x['story']), tfidf.stories)):
# 	print(item)

important_words = tfidf.get_important_words()
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