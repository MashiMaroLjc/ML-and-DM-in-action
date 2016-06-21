#coding:utf-8
import numpy

def classify(inX,dataSet,labels,k):
	"""

	:param inX: example
	:param dataSet:  dataSet 2D List
	:param labels:  1D List
	:param k the number of neighbor
	:return: The label of the example as classify result.
	"""
	if len(dataSet) != len(labels):
		raise ValueError("DataSet or labels was too less!"
		                 "The length of DataSet is %s"
		                 "But the length of labels is %s"%(len(dataSet),len(labels)))

	dArrays = numpy.array(dataSet)
	inArray = numpy.array(inX)
	result = (((dArrays-inArray)**2).sum(axis=1))**0.5
	index_list = result.argsort()
	classCount = dict()
	for i in range(k):
		label = labels[index_list[i]]
		classCount[label] = classCount.get(label,0) + 1
	return sorted(classCount,key=lambda x:classCount[x],reverse=True)[0]

