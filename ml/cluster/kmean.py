#coding:utf-8
import numpy
import random
from math import sqrt
class KMean:

	def __init__(self):
		self._train = False
		#记录训练好的标签
		self._label = []
		#质心的信息
		self._heart = []
		#样本与质心信息(质心下标，距离)
		self._centerInfo = []


	#获取聚好类的标签
	@property
	def label(self):
		return self._label

	@property
	def heart(self):
		return  self._heart

	@property
	def centerInfo (self):
		return self._centerInfo

	#初始化质心
	def _initHeart(self,dataIn,k,n):
		hearts = [
			numpy.array(
				[
					dataIn[:,j].min()+
					(dataIn[:,j].max()-dataIn[:,j].min())*numpy.random.rand()
				 for j in range(n)]
			) for i in range(k)
		]
		return hearts


	def fit(self,dataSet,k,maxIter=300):
		self._train = True
		dataIn = numpy.array(dataSet)
		self._heart = [0 for i in range(k)]
		try:
			m,n = dataIn.shape
		except ValueError:
			raise ValueError("dataSet every D must have same unit")
		if m < k:
			raise ValueError("The D of dataSet must > or = k! D=%s k=%s"%(m,k))

		centerInfo = numpy.zeros((m, 2))
		hearts = self._initHeart(dataIn,k,n)
		#计算欧式距离
		num = 0
		current = True

		while current:
			num += 1
			current = False
			for i in range(m):
				minDis = numpy.inf
				bestIndex = -1
				data = dataIn[i]
				for j in range(len(hearts)):
					dis = sqrt(
						sum(
						(data-hearts[j])**2
					))
					if dis < minDis:
						bestIndex = j
						minDis = dis
				#数据点的最佳质心改动，bestIndex改动，仍未是最佳
				if centerInfo[i][0] !=  bestIndex:
					current = True
				#记录第i个数据最近的质心与距离
				centerInfo[i][0] = bestIndex
				centerInfo[i][1] = minDis**2
			#以下为重设质心部分
			clu = centerInfo[:,0]
			#本次聚类质心被抛弃了，一般发生在第一次，重来
			cluSet = set(clu)
			if len(cluSet) != k:
				current = True
				hearts = self._initHeart(dataIn,k,n)
				continue
			elif num > maxIter:
				break
			#新质心
			info = [numpy.array(
			[0.0 for i in range(n)]
		) for j in range(k)]
			numOfClu = dict()
			for i in  range(len(clu)):
				data = dataIn[i]
				#标签编号
				noc = int(clu[i])

				info[noc] += data

				numOfClu[noc] = numOfClu.get(noc,0) + 1
			#取平均
			for key in numOfClu:
				noc = key
				info[noc] = info[noc]/numOfClu[noc]
			hearts = info

		self._centerInfo = centerInfo
		self._label = numpy.array(centerInfo[:,0],dtype="int")
		self._heart = hearts
		return self


	def predict(self,X):
		if not self._train:
			raise ValueError("Please train the model")
		res = 0
		minDis= numpy.inf
		data = numpy.array(X)
		#算样本点距离
		for index in range(len(self._heart)):
			dis = sqrt(
				sum(
					(data - self._heart[index]) ** 2
				))
			if dis <minDis:
				res = index
				minDis = dis
		return res












class BinKMean(KMean):

	def __init__(self):
		super().__init__()

	def _SSE(self,dataIn):
		dataIn = numpy.array(dataIn)
		return sum(dataIn[:,1])

	def _distance(self,data1,data2):
		return sqrt(
			sum((data1-data2)**2)
		)

	def fit(self,dataSet,k,minCNum=1):
		self._train = True
		dataIn = numpy.array(dataSet)
		self._heart = [0 for i in range(k)]
		try:
			m,n = dataIn.shape
		except ValueError:
			raise ValueError("dataSet every D must have same unit")
		if m < k:
			raise ValueError("The D of dataSet must > or = k! D=%s k=%s"%(m,k))
		#质心信心表
		centerInfo = numpy.zeros((m, 2))

		#质心
		hearts = [
			numpy.sum(dataIn,0)/m
		]
		centerInfo[:,1] = [self._distance(dataIn[i],hearts[0])**2 for i in range(m)]

		while len(hearts)<k:
			minSSE = numpy.inf
			bestSplitIndex  = -1
			bestHeart = None
			bestCenterInfo = None
			for i in range(len(hearts)):
				#计算当前质心所分的簇巅峰SSE
				#currentMistake = self._SSE([center for center in centerInfo if center[0] == i])
				km = KMean()
				cluster = [dataIn[j] for j in range(len(centerInfo)) if centerInfo[j][0] == i]
				#如果该簇少于一定数目就不用分了
				if len(cluster) <= minCNum:
					continue
				km = km.fit(cluster, 2)
				#计算分类后的误差
				centers = km.centerInfo
				mistake = self._SSE(centers)
				if mistake < minSSE:
					minSSE = mistake
					bestHeart = km.heart
					bestSplitIndex = i
					bestCenterInfo = centers

			#将bestSplitIndex的质心一分为二
			new_hearts = []
			for i in range(len(hearts)):
				if i == bestSplitIndex:
					new_hearts.append(bestHeart[0])
					new_hearts.append(bestHeart[1])
				else:
					new_hearts.append(hearts[i])
			hearts = new_hearts

			#更新信息表
			#print("center INFO", centerInfo)

			for i in range(len(centerInfo)):
				info = centerInfo[i]
				if int(info[0]) == int(bestSplitIndex):
					data = dataIn[i]
					distA = self._distance(data,bestHeart[0])
					distB = self._distance(data,bestHeart[1])
					if distA < distB:
						centerInfo[i][0] = bestSplitIndex
						centerInfo[i][1] = distA
					else:
						centerInfo[i][0] = bestSplitIndex+1
						centerInfo[i][1] = distB

		self._centerInfo = centerInfo
		self._label = numpy.array(centerInfo[:, 0], dtype="int")
		self._heart = hearts
		return self