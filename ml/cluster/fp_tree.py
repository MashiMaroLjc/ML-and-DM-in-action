#coding:utf-8
from .apriori import Apriori
class treeNode:
	def __init__(self,nameValue,numOccur,parentNode):
		self.name = nameValue
		self.count = numOccur
		self.nodeLink  = None
		self.parent = parentNode
		self.children =dict()

	def inc(self,numOccur):
		self.count += numOccur


class fpTree(Apriori):

	def _createTree(self,dataSet,minSup):
		number = len(dataSet)
		headerTable = {}
		for trans in dataSet:
			for item in trans:
				headerTable[item] = headerTable.get(item,0) + dataSet[trans]
		keys = list(headerTable.keys())
		for k in keys:
			if headerTable[k]/number < minSup:
				del (headerTable[k])

		freqItemSet = set(headerTable.keys())
		if len(freqItemSet) == 0:
			return None,None
		for k in headerTable:
			headerTable[k] = [headerTable[k],None]

		retTree = treeNode("Null Set",1,None)
		for tranSet,count in dataSet.items():
			localD = dict()
			for item in tranSet:
				if item in freqItemSet:
					localD[item] = headerTable[item][0]
			if len(localD) > 0:
				orderedItems = [v[0] for v in sorted(localD.items(),key=lambda p:p[1],reverse=True)]
				self._updateTree(orderedItems,retTree,headerTable,count)
		return retTree,headerTable

	def _updateTree(self,item,inTree,headerTable,count):
		if item[0] in inTree.children:
			inTree.children[item[0]].inc(count)
		else:
			inTree.children[item[0]] = treeNode(item[0],count,inTree)
			if headerTable[item[0]][1] == None:
				headerTable[item[0]][1] = inTree.children[item[0]]
			else:
				self._updateHeader(headerTable[item[0]][1],inTree.children[item[0]])
		if len(item) >1:
			self._updateTree(item[1::],inTree.children[item[0]],headerTable,count)

	def _updateHeader(self,nodeToTest,targetNone):
		while (nodeToTest.nodeLink != None):
			nodeToTest = nodeToTest.nodeLink
		nodeToTest.nodeLink = targetNone

	def _createInitSet(self,dataSet):
		"""
		包装数据集
		:param dataSet:
		:return:
		"""
		retDict = dict()
		for trans in dataSet:
			retDict[frozenset(trans)] = 1
		return retDict

	def _ascendTree(self,leafNode,prefixPath):
		if leafNode.parent != None:
			prefixPath.append(leafNode.name)
			self._ascendTree(leafNode.parent,prefixPath)

	def _findPrefixPath(self,basePat,treeNode):
		condPats = dict()
		while treeNode != None:
			prefixPath = []
			self._ascendTree(treeNode,prefixPath)
			if len(prefixPath) > 1:
				condPats[frozenset(prefixPath[1:])] = treeNode.count
			treeNode = treeNode.nodeLink
		return condPats

	def _mineTree(self,inTree,headerTable,minSup,preFix,freqItemList):
		def t(p):

			return p[1][0]
		bigL = [v[0] for v in sorted(headerTable.items(),key=t)]
		for basePat in bigL:
			newFreqSet = preFix.copy()
			newFreqSet.add(basePat)
			freqItemList.append(frozenset(newFreqSet))
			condPattBases = self._findPrefixPath(basePat,headerTable[basePat][1])
			myCondTree,myHead = self._createTree(condPattBases,minSup)
			if myHead != None:
				self._mineTree(myCondTree,myHead,minSup,newFreqSet,freqItemList)


	def frequentSet(self, dataSet, minSup=0.5):
		minSup = minSup if 0 < minSup and minSup <= 1 else abs(minSup / len(dataSet))
		initSet = self._createInitSet(dataSet)
		tree,header = self._createTree(initSet,minSup)
		res = []
		#print(header)
		self._mineTree(tree,header,minSup,set([]),res)
		return  res