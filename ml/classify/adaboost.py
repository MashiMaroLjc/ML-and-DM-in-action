from abc import ABCMeta, abstractmethod
import numpy
import time

#弱分类器接口
class WeakClassify(metaclass = ABCMeta):

	def __init__(self):
		pass

	@abstractmethod
	def train(self,dataSet,label,D):
		pass

	@abstractmethod
	def classify(self,inX):
		pass



#单层决策树
class SingleTree(WeakClassify):

	def __init__(self):
		super().__init__()
		#单纯决策树，只有一个key,这个key表述单层决策树的信息
		self._tree = {"index":-1,"opt":0,"stand":0}

	def _subClassify(self,inX,opt,stand):
		"""
		opt 为'l' 时，少于等于stand时为-1，为r时，则相反
		:param inX:
		:param opt:
		:return:
		"""
		# print(inX)
		if opt == 'l':
			return 	numpy.array([ -1 if x <= stand else 1 for x in inX])
		else:
			return numpy.array([ -1 if x > stand else 1 for x in inX])

	def fit(self,dataSet,label,D):
		if len(dataSet) != len(label):
			raise ValueError("dataSet and label must have same length……")
		minError = numpy.inf
		dataIn = numpy.array(dataSet)
		m,n = dataIn.shape
		for i in range(n):
			#第I列变成行的形式返回
			dataX = dataIn[:,i]
			MAX = dataX.max()
			MIN = dataX.min()
			#在MIN和MAX中，看看能不能找到i列的最佳分割
			for j in range(MIN,MAX*2):
				for opt in ("l","r"):
					#预测结果
					predictArray = self._subClassify(dataX,opt,j*0.5)
					#predictArray与label对比，错了就为1，正确为0
					errorList = numpy.mat(
						[ 1 if label[index] != predictArray[index] else 0 \
					              for index in range(len(label))])
					#错误得分
					matD = numpy.mat(D)
					# print("matD:",matD)
					errScore = errorList* matD.T
					# print("errScore:",errScore)
					if errScore < minError:
						minError = errScore
						self._tree["index"] = i
						self._tree["opt"] = opt
						self._tree["stand"] = j

		return self

	def classify(self,inX):
		if self._tree["index"] == -1:
			raise  ValueError("Maybe happen bug!")
		index = self._tree["index"]
		opt = self._tree["opt"]
		stand = self._tree["stand"]
		return self._subClassify([inX[index]],opt,stand)[0]


#AdaBoost决策分类器
class AdaBoost:

	def __init__(self,weakClassify):
		if not weakClassify.__base__ == WeakClassify:
			raise ValueError("Illegal  weakClassify!It must implement WeakClassify!")
		self._weak = weakClassify
		self._classifyList = []
		self._alpha = []


	def fit(self,dataSet,labels,maxIter,printTime =False):
		lengthOfDataSet = len(dataSet)
		D = numpy.ones(lengthOfDataSet)/lengthOfDataSet
		n = 0 #迭代次数
		sigma = -1 #错误率
		t1 = time.time()
		while (n <= maxIter) and (sigma!=0):
			n += 1
			#分类器
			cla = self._weak()
			cla = cla.fit(dataSet,labels,D)
			error = 0
			#被错误分类的数据的下标集合
			errorIndexList =[]
			for index in range(lengthOfDataSet):
				answer = cla.classify(dataSet[index])
				y = labels[index]
				if answer!= y:
					# print(dataSet[index],"||",answer,"||",y)
					error += 1
					errorIndexList.append(index)
			sigma = error / lengthOfDataSet
			alpha = 1

			if error != 0:
				alpha = 0.5 * numpy.log((1 - sigma)/sigma)
			# print("sigma:", sigma)
			# print("alpha:",alpha)
			# print("----------")
			#更新D
			for index in range(lengthOfDataSet):
				if index in errorIndexList:
					#该样本被分错了
					D[index] = D[index] *numpy.exp(alpha)/sum(D)
				else:
					#正确分类
					D[index] = D[index] * numpy.exp(-alpha)/sum(D)
			#记录该分类器
			self._alpha.append(alpha)
			self._classifyList.append(cla)
		t2 = time.time()
		if printTime:
			print("Cost time %s"%(t2-t1))
		return self

	def classify(self,inX):
		length = len(self._classifyList)
		if length == 0:
			raise ValueError("You must train the model")
		temp = [self._alpha[index]*self._classifyList[index].classify(inX)
		        for index in range(length)]
		temp = sum(temp)
		return numpy.sign(temp)

