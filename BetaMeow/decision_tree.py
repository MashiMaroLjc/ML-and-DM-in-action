#coing:utf-8

from base_decision_tree import BaseDecisionTree
import json


class DecisionTree(BaseDecisionTree):
	def __init__(self,**dic):
		self._fromPath = False
		if "dataSet" in dic:
			dataSet = dic.get("dataSet")
			labels = dic.get("labels")
			assert labels,"Need labels!! "
			super().__init__(dataSet,labels)
		elif "path" in dic:
			path = dic.get("path")
			f = open(path,"r")
			self._tree = json.load(f)
			f.close()
			self._fromPath = True
		else:
			self._tree = dict()

	def save(self,fileName):
		f = open(fileName,"w")
		json.dump(self._tree,f)
		f.close()




