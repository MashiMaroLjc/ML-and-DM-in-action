#coding：utf-8
import operator
from math import *
from queue import Queue



class DecisionTree:

	def __init__(self):
		self._t = dict()

	@property
	def tree(self):
		return self._t

	@tree.setter
	def tree(self,value):
		raise ValueError("You can't change it!")


	def _calcShannonEnt(self,dataSet):
		numEntries = len(dataSet)
		labelCount = dict()
		for featVec in dataSet:
			currentLabel = featVec[-1]
			labelCount[currentLabel] = labelCount.get(currentLabel, 0) + 1
		shannonEnt = 0.0
		for key in labelCount.keys():
			prob = float(labelCount[key]) / numEntries
			shannonEnt -= prob * log(prob, 2)
		return shannonEnt

	def _splitDataSet(self,dataSet, axis, value):
		retDataSet = []
		for featVec in dataSet:
			if featVec[axis] == value:
				reducedFeatVec = featVec[:axis]
				reducedFeatVec.extend(featVec[axis + 1:])
				retDataSet.append(reducedFeatVec)
		return retDataSet

	def _chooseBestFeatureToSplit(self,dataSet: list):
		numFeatures = len(dataSet[0]) - 1
		baseEntropy = self._calcShannonEnt(dataSet)
		bestInfoGain = 0.0
		bestFeature = -1
		for i in range(numFeatures):
			featList = [example[i] for example in dataSet]
			uniqueVals = set(featList)
			newEntropy = 0.0
			for value in uniqueVals:
				subDataSet =self. _splitDataSet(dataSet, i, value)
				prob = len(subDataSet) / float(len(dataSet))
				newEntropy += prob * self._calcShannonEnt(subDataSet)
			infoGain = baseEntropy - newEntropy
			if infoGain > bestInfoGain:
				bestInfoGain = infoGain
				bestFeature = i
		return bestFeature

	def _majorityCnt(self,classList):
		classCount = dict()
		for vote in classList:
			if vote not in classCount.keys():
				classCount[vote] = 0
			classCount[vote] += 1
		sortedClassCount = sorted(classCount.items(), \
		                          key=operator.itemgetter(1), reverse=True)
		return sortedClassCount[0][0]

	def _createTree(self,dataSet, labels):
		"""

		:param dataSet: 2D List should be longer than labels 1 Unit.
		:param labels: 1D List
		:return:
		"""
		if len(dataSet[0]) - 1 != len(labels):
			raise ValueError("error!can't not create tree!the length of dataList is %d," \
			                 "the num of labels is %d" % (len(dataSet[0]) - 1, len(labels)))
		tempLabels = labels[:]
		classList = [example[-1] for example in dataSet]
		if classList.count(classList[0]) == len(classList):
			return classList[0]
		if len(dataSet[0]) == 1:
			return self._majorityCnt(classList)
		bestFeat = self._chooseBestFeatureToSplit(dataSet)
		bestFeatLabel = tempLabels[bestFeat]
		# bestFeatLabel = str(bestFeatLabel)
		myTree = {bestFeatLabel: {}}
		del (tempLabels[bestFeat])
		featValues = [example[bestFeat] for example in dataSet]
		uniqueVals = set(featValues)
		for value in uniqueVals:
			subLabels = tempLabels
			myTree[bestFeatLabel][value] = self._createTree(
				self._splitDataSet(dataSet, bestFeat, value),
				subLabels
			)
		return myTree

	def _getName(self,d: dict):
		assert isinstance(d, dict), "d must be a dict,now d is %s" % (type(d))
		if len(d) == 0:
			return None
		key = list(d.keys())
		return key[0]

	def _findData(self,data, List):
		assert type(data) == type(List[0]), "data must have same type as List[0],now the type of data" \
		                                    "is %s ,type of List[0] is %s" % (type(data), type(List[0]))
		length = len(List)
		for index in range(length):
			if data == List[index]:
				return index
		return -1



	def fit(self,dataSet, labels):
		self._t = self._createTree(dataSet,labels)
		return self

	def classify(self,data: list, labels: list):
		if len(self._t) == 0:
			raise  ValueError("You must train it")

		qu = Queue()
		qu.put((self._t, 0))
		while not qu.empty():
			node, deep = qu.get()
			name = self._getName(node)
			childTree = node.get(name)
			index = self._findData(name, labels)
			if index != -1:
				# k =  str(data[index] )
				k = data[index]
				value = childTree.get(k)
				if isinstance(value, dict):
					qu.put((value, deep + 1))
				elif value != None:
					return value
				else:
					return list(childTree.values())[0]
			else:
				for value in childTree.values():
					if isinstance(value, dict):
						qu.put((value, deep + 1))
					else:
						return value



