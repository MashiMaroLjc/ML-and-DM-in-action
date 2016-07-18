#coding:utf-8

import numpy
import random
import time



class Logistic:

	def __init__(self):
		self._w = None
		self._dataIn = []
		self._labels = []

	def _sigmoid(self,inX):
		return 1.0/(1+numpy.exp(-inX))

	def fit(self,dataSet,labels,trainN,alpha=0.01,printTime=False):
		length = len(dataSet)
		if length != len(labels):
			raise  ValueError("DataSet and labels must have same length")

		dataIn = numpy.array(dataSet)
		m,n = dataIn.shape
		weight = numpy.ones(n)
		t1 = time.time()
		for i in range(trainN):
			randIndex = random.choice(range(length))
			excepted = 1 if int(labels[randIndex]) >= 0 else 0
			result = self._sigmoid(sum(dataIn[randIndex]*weight))
			result = 1 if result > 0.5 else 0
			error  = excepted - result
			weight += error * alpha *dataIn[randIndex]
			alpha = 4/(1+i)+0.01
		t2 = time.time()
		if printTime:
			print("cost time : %s"%(t2-t1))
		self._w = weight
		self._dataIn = dataIn
		self._labels = labels
		return self



	def classify(self, inX):
		inx = numpy.array(inX)
		if not isinstance(self._w, numpy.ndarray):
			raise ValueError("You must train the model!")
		if len(inx) != len(self._w):
			raise ValueError("InX must be %d unit" % (len(self._w)))
		res = 1 if self._sigmoid(sum(inx*self._w)) > 0.5 else 0
		return res

