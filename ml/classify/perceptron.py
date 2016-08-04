#coding:utf-8
import time
import numpy
import random

_zero_or_one = lambda  x:1 if x >= 0 else 0



class Perceptron:

	def __init__(self,weight=None):
		self._w = weight

	def fit(self,dataSet:list,labels:list,trainN:int,printTime=False):
		length = len(dataSet)
		if length != len(labels):
			raise  ValueError("DataSet and labels must have same length")
		eachD = len(dataSet[0])
		w = numpy.random.rand(eachD)
		choiceList = [
			(
				numpy.array(dataSet[index]),
			    _zero_or_one(int(labels[index]))
			 ) for index in range(length)
		]
		t1 = time.time()
		#train begin
		for i in range(trainN):
			data,excepted = random.choice(choiceList)
			try:
				result = numpy.dot(data,w)
			except :
				raise  ValueError("Every dimension in dataSet must has same length: %d"%(eachD))
			error = excepted - _zero_or_one(result)
			#fix the weight
			w += error * data
		#train end
		t2 = time.time()

		if printTime:
			print("Cost time: %s"%(t2-t1))
		self._w = w
		return self


	def classify(self,inX):
		inx = numpy.array(inX)
		if not isinstance(self._w,numpy.ndarray):
			raise  ValueError("You must train the model!")
		if len(inx) != len(self._w):
			raise  ValueError("InX must be %d unit"%(len(self._w)))
		res = 1 if numpy.dot(inx,self._w) >= 0 else 0
		return res