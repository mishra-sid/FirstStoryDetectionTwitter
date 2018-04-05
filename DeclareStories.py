class DeclareStories:
	def __init__(self, truePairs, storyCount):
		self.truePairs = truePairs
		self.unionSet = [-1 for _ in range(storyCount)]
	def getParent(index):
		if self.unionSet[self.index] == -1:
			return self.index
		else:
			return self.unionSet[self.unionSet[self.index]]
	def findConnectedComponents(self):
		for x,y in self.truePairs:
			x,y = min(x,y), max(x,y)
			self.unionSet[self.getParent(y)] = self.unionSet[self.getParent(x)]
		print('Finished generating UnionSet')
		for i, _ in enumerate(unionSet):
			self.unionSet[i] = self.getParent(i)
		print('Finished Optimizaing UnionSet')
		components = {}
		for i, item in enumerate(self.unionSet):
			if item not in components:
				components[item] = []
			components[item].append(i)
		return components



