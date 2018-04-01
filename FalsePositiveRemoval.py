from constants import *

class FalsePositiveRemoval:
	def __init__(self, candidates, stories):
		self.candidates = candidates
		self.stories = stories
		self.final = []
	def RemoveFalsePositives(self):
		intersect = 0
		union = 0
		while self.candidates:
			a,b = self.candidates.pop()
			first, second = map(lambda x : set(self.stories[x]['story']), (a,b))
			if ( len(first & second) / len(first | second) ) > THRESHOLD_JACC_SIMILARITY:
				self.final.append((a,b))
		return self.final

