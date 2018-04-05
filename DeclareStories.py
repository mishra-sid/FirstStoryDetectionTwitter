class DeclareStories:
	def __init__(self, truePairs, storyCount):
		self.truePairs = truePairs
		self.unionSet = [-1 for _ in range(storyCount)]
	def getParent(self, index):
		if self.unionSet[index] == -1:
			return index
		else:
			return self.unionSet[self.unionSet[index]]
	def findConnectedComponents(self):
		for x,y in self.truePairs:
			x,y = min(x,y), max(x,y)
			self.unionSet[self.getParent(y)] = self.unionSet[self.getParent(x)]
		print('Finished generating UnionSet')
		for i, _ in enumerate(self.unionSet):
			self.unionSet[i] = self.getParent(i)
		print('Finished Optimizaing UnionSet')
		components = {}
		for i, item in enumerate(self.unionSet):
			if item not in components:
				components[item] = []
			components[item].append(i)
		return components



