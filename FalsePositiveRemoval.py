from constants import *

class FalsePositiveRemoval:
	def __init__(self, stories, titles):
		self.stories = stories
		self.titles = titles

	def RemoveFalsePositives(self, candidates):
		intersect = 0
		union = 0
		averageJacSim = 0.0
		truePositiveCount = 0
		badCandidates = []
		badCandidateCount = [0 for _ in range(len(candidates))]
		for i in range(len(candidates)-1):
			for j in range(i+1,len(candidates)):
				first, second = map(lambda x : set(self.stories[x]['story']), (candidates[i],candidates[j]))
				jacSim = ( len(first & second) / len(first | second) )
				if jacSim > THRESHOLD_JACC_SIMILARITY:
					pass
				else:
					badCandidates.append((i,j))
					badCandidateCount[i] += 1
					badCandidateCount[j] += 1
					#print(self.titles[a]['title'], 'and', self.titles[b]['title'],'are false positives!')
		
		delList = []
		while(len(badCandidates) > 0):
			i, val = max(enumerate(badCandidateCount), key = lambda x: x[1])
			if (val == 0):
				print("badCandidates still exist when all counts are zero!")
				map(print, candidates, i, badCandidates, badCandidateCount)
				exit()

			for candidate in badCandidates:
				if i in candidate:
					badCandidateCount[candidate[0]] -= 1
					badCandidateCount[candidate[1]] -= 1

			if badCandidateCount[i] != 0:
				print("Could not eliminate all candidates!")
				map(print, candidates, i, badCandidates, badCandidateCount)
				exit()
			badCandidates = [x for x in badCandidates if i not in x]
			delList.append(i)


		return ([x for i,x in enumerate(candidates) if i not in delList], [x for i,x in enumerate(candidates) if i in delList])
