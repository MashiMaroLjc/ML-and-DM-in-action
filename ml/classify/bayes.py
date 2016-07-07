#coding:utf-8
import time
import numpy

class Bayes:

	def __init__(self):
		self._length = -1
		self._labelRecord = dict()
		self._vectorRecord = dict()

	def fit(self,dataSet:list,labels:list,printTime=False):
		"""

		:param dataSet: 2D list
		:param labels:  1D list
		:param printTime:
		:return: Bayes after training
		"""
		if len(dataSet) != len(labels):
			raise  ValueError("DataSet and labels must have same length")
		self._length = len(dataSet[0])
		numLabels = len(labels)
		tempSet = set(labels)
		t1= time.time()
		for temp in tempSet:
			self._labelRecord[temp] = labels.count(temp)/ numLabels

		for vector,label in zip(dataSet,labels):
			if label not in self._vectorRecord:
				self._vectorRecord[label] = []
			self._vectorRecord[label].append(vector)

		t2 = time.time()
		if printTime:
			print("Cost time: %s"%(t2-t1))
		return self




	def classify(self,inX,resultSet,func=None):
		"""
		根据贝叶斯定理算出各个类别的概率，选出最大概率的那个，因为只需比较厚的结果，所以算概率时，忽略掉分母
		:param inX: 测试向量
		:param func: 自定义计算概率方式
		:return:
		"""
		if self._length == -1:
			raise  ValueError("You must train the model")
		if self._length != len(inX):
			raise ValueError("inX must have %d Unit"%(self._length))
		maybeDict = dict()

		for maybe in resultSet:
			probability = 1
			pLabel = self._labelRecord[maybe]
			allVector = self._vectorRecord[maybe]
			numVector = len(allVector)
			allVector = numpy.array(allVector).T
			for index in range(len(inX)):
				if not func:
					vector = list(allVector[index])
					probability *= vector.count(inX[index]) / numVector
				else:
					probability *= func(inX[index])
			maybeDict[maybe] = probability * pLabel
		return sorted(maybeDict,key=lambda x:maybeDict[x],reverse=True)[0]


