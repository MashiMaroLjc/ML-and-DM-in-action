#coding：utf-8
import operator
from math import *
from queue import Queue

def calcShannonEnt(dataSet):
	numEntries = len(dataSet)
	labelCount = dict()
	for featVec in dataSet:
		currentLabel = featVec[-1]
		labelCount[currentLabel] = labelCount.get(currentLabel,0)+1
	shannonEnt = 0.0
	for key in labelCount.keys():
		prob = float(labelCount[key])/numEntries
		shannonEnt -= prob * log(prob,2)
	return shannonEnt

def splitDataSet(dataSet,axis,value):
	retDataSet=[]
	for featVec in dataSet:
		if featVec[axis] == value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis+1:])
			retDataSet.append(reducedFeatVec)
	return retDataSet

def chooseBestFeatureToSplit(dataSet:list):
	numFeatures = len(dataSet[0])-1
	baseEntropy = calcShannonEnt(dataSet)
	bestInfoGain = 0.0
	bestFeature = -1
	for i in range(numFeatures):
		featList=[example[i] for example in dataSet]
		uniqueVals = set(featList) 
		newEntropy = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob * calcShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy
		if infoGain > bestInfoGain:
			bestInfoGain = infoGain
			bestFeature = i
	return bestFeature
	 	 

def majorityCnt(classList):
	classCount = dict()
	for vote in classList:
		if vote not in classCount.keys():
			classCount[vote] = 0
		classCount[vote] += 1
	sortedClassCount = sorted(classCount.items(),\
		key = operator.itemgetter(1),reverse=True)
	return sortedClassCount[0][0]

def createTree(dataSet,labels):
	assert len(dataSet[0])-1  == len(labels),\
		"error!can't not create tree!the length of datalist is %d,"\
		"the num of labels is %d"%(len(dataSet[0])-1,len(labels))
	tempLabels = labels[:]
	classList = [ example[-1] for example in dataSet]
	if classList.count( classList[0] ) == len(classList):
		return classList[0]
	if len(dataSet[0]) == 1:
		return majorityCnt(classList)
	bestFeat = chooseBestFeatureToSplit(dataSet)
	bestFeatLabel = tempLabels[bestFeat]
	bestFeatLabel = str(bestFeatLabel)
	myTree = {bestFeatLabel:{}}
	del(tempLabels[bestFeat] )
	featValues = [ example[bestFeat] for example in dataSet ]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = tempLabels
		myTree[bestFeatLabel][value] = createTree(
			splitDataSet(dataSet,bestFeat,value),
			subLabels
		)
	return myTree

def getName(d:dict):
	assert isinstance(d,dict),"d must be a dict,now d is %s"%(type(d))
	if len(d) == 0:
		return None
	key = list(d.keys())
	return key[0]


def findData(data,List):
	assert  type(data) == type(List[0]),"data must have same type as List[0],now the type of data" \
		"is %s ,type of List[0] is %s"%(type(data),type(List[0]))
	length = len(List)
	for index in range(length):
		if data == List[index]:
			return index
	return -1


def result(tree:dict,data:list,labels:list):
	qu = Queue()
	qu.put((tree,0))
	while not qu.empty():
		node,deep = qu.get()
		name = getName(node)
		childTree = node.get(name)
		index = findData(name,labels)
		if index != -1:
			k =  str(data[index] )
			value = childTree.get(k)
			if isinstance(value,dict):
				qu.put((value,deep+1))
			else:
				return value
		else:
			for value in childTree.values():
				if isinstance(value,dict):
					qu.put((value,deep+1))
				else:
					return value

def createDataSet():
	dataSet = [
		[1,1,0,'yes'],
		[1, 1, 3, 'yes'],
		[3,0,1,'yes'],
		[2,1,0,'no'],
		[3, 1, 1, 'no'],
		[2,4,1,'no'],
		[0,0,3,'no']
	]
	labels = ['no surfacing',"fuck",'flippers']
	return dataSet,labels



