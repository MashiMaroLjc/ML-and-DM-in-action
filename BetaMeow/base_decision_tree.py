#coing:utf-8

from tree import createTree,result

class BaseDecisionTree():

	def __init__(self,dataSet,labels):
		newDataSet = []
		for dataList in dataSet:
			newDataList = []
			for data in dataList:
				newDataList.append(str(data))
			newDataSet.append(newDataList)
		newLabels = [ str(label) for label in labels]

		self._tree = createTree(newDataSet,newLabels )

	#example = (data:list,labels:list)
	def decision(self,example:tuple):
		if not self._tree: return False
		if len(self._tree) == 0: return False
		data = example[0]
		labels =[ str(label) for label in example[1]]
		return result(self._tree,data,labels)

	def __str__(self):
		return 	"DecisionTree : {}".format(self._tree)

	def __repr__(self):
		return str(self._tree)


