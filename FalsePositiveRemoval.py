from constants import *

class FalsePositiveRemoval:
	def __init__(self, candidates, stories, titles):
		self.candidates = candidates
		self.stories = stories
		self.titles = titles

		self.final = []

	def RemoveFalsePositives(self):
		intersect = 0
		union = 0
		averageJacSim = 0.0
		truePositiveCount = 0
		while self.candidates:
			a,b = self.candidates.pop()
			first, second = map(lambda x : set(self.stories[x]['story']), (a,b))
			jacSim = ( len(first & second) / len(first | second) )
			if jacSim > THRESHOLD_JACC_SIMILARITY:
				truePositiveCount += 1
				averageJacSim += jacSim
				self.final.append((a,b))
			else:
				pass
				#print(self.titles[a]['title'], 'and', self.titles[b]['title'],'are false positives!')
		print("Average Jaccard Similarity for true positives is:", (averageJacSim/truePositiveCount))
		return self.final
