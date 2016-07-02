#coding:utf-8
import numpy
import time

class SVM:

	RBF = "rbf"
	L = "line"
	def __init__(self):
		self._alpha = []
		#record alpha * y
		self._alphaXy = []
		#dataSet
		self._X = []
		self._b = 0
		self._optType = None
		self._sigma = None


	def _kernel(self,inX,Xi,optType,sigma):
		if optType == self.L:
			return numpy.dot(inX,Xi)
		elif optType == self.RBF:
			temp = inX - Xi
			norm = numpy.linalg.norm(temp)**2
			m = -norm / 2 * (sigma**2)
			return numpy.exp(m)
		else:
			raise  ValueError("Illegal optType！")

	def _g(self,alpha,y,Xi,allX,b,kernelType,sigma):
		temp = [alpha[j]*y[j]*self._kernel(allX[j],Xi,kernelType,sigma) for j in range(len(alpha))]
		return sum(temp) + b


	def fit(self,dataSet:list,labels:list,MaxIter,optType,sigma=1,C=0.6,printTime=False):
		self._X = numpy.array(dataSet)
		dataSet = numpy.array(dataSet)
		length = len(dataSet)
		length2 = len(dataSet[0])
		if length != len(labels):
			raise ValueError("dataSet and labels must have same length")

		self._optType = optType
		self._sigma = sigma
		self._alpha = numpy.zeros(length)
		#记录全部数据集除了alpha的结果,提高计算速度
		self._record = [labels[i]*self._kernel(dataSet[i],self._X[i],self._optType,self._sigma)
		            for i in range(length)]
		isKTT = False
		n = 0
		t1 = time.time()
		while (not isKTT) and (n <= MaxIter):
			#选取ai
			n+=1
			#假设全部满足KTT
			isAllKTT = True
			for i in range(length):
				needToAdjust = False
				vX = dataSet[i]
				if len(vX) != length2:
					raise ValueError("Every D in dataSet must have same length")
				if self._alpha[i] == 0:
					temp = labels[i]*self._g(self._alpha,labels,vX,dataSet,self._b,optType,sigma)
					if temp < 1:
						needToAdjust =True
				elif self._alpha[i] == C:
					temp = labels[i] * self._g(self._alpha, labels, vX, dataSet, self._b, optType, sigma)
					if temp > 1:
						needToAdjust = True
				elif self._alpha[i] < 0 or self._alpha[i] >C:
					temp = labels[i] * self._g(self._alpha, labels, vX, dataSet, self._b, optType, sigma)
					if temp != 1:
						needToAdjust = True


				#需要调整alpha
				if needToAdjust:
					isAllKTT = False

					#选取aj
					temp = [self._alpha[i]*record for record in self._record]
					fi = sum(temp) + self._b
					Ei = fi - labels[i]
					MAX = 0
					Jindex = 0
					Ej = 0
					for j in range(len(self._alpha)):
						temp = [self._alpha[j] * record for record in self._record]
						fj = sum(temp) + self._b
						Ek = fj - labels[j]
						e = abs(Ek - Ei)
						if  e > MAX:

							MAX = e
							Jindex = j
							Ej = Ek
					#开始调整
					L = 0
					H = 0
					if labels[i] != labels[Jindex]:
						L = max(0,self._alpha[Jindex]-self._alpha[i])
						H = min(C,C+self._alpha[Jindex]-self._alpha[i])

					else:
						L = max(0, self._alpha[i]+ self._alpha[Jindex]-C)
						H = min(C, self._alpha[Jindex] + self._alpha[i])

					#调整alpha j
					oldAlphaJ = self._alpha[Jindex]
					eta = 2*numpy.dot(dataSet[i],dataSet[Jindex]) - numpy.dot(dataSet[i],dataSet[i])\
						- numpy.dot(dataSet[Jindex],dataSet[Jindex])
					self._alpha[Jindex] -= labels[Jindex] * (Ei -Ej)/eta
					if self._alpha[Jindex]>H:
						self._alpha[Jindex] = H

					elif self._alpha[Jindex] < L:
						self._alpha[Jindex] = L

					# 调整alpha i
					oldAlphaI = self._alpha[i]
					self._alpha[i] += labels[i]*labels[Jindex]*(oldAlphaJ-self._alpha[Jindex])

					#调整b
					b1 = self._b -Ei -labels[i]*(self._alpha[i]-oldAlphaI)*numpy.dot(dataSet[i],dataSet[i])\
						- labels[Jindex]*(self._alpha[Jindex] - oldAlphaJ)*numpy.dot(dataSet[i],dataSet[Jindex])
					b2 = self._b - Ej - labels[i] * (self._alpha[i] - oldAlphaI) * numpy.dot(dataSet[i],dataSet[Jindex]) \
		                - labels[Jindex] * (self._alpha[Jindex] - oldAlphaJ) * numpy.dot(dataSet[Jindex],dataSet[Jindex])
					if self._alpha[i] > 0 and self._alpha[i] < C:
						self._b = b1
					elif self._alpha[Jindex] >0 and self._alpha[Jindex] < C:
						self._b = b2
					else:
						self._b = (b1 + b2) / 2

			#一次都不需要调整，则不再需要下一轮测试
			if isAllKTT:
				isKTT =True
		self._alphaXy = [self._alpha[i]*labels[i] for i in range(len(self._alpha))]
		t2 = time.time()
		if printTime:
			print("Cost time : %s"%(t2 -t1))

		return self



	def classify(self,inX):
		if len(self._alphaXy) == 0:
			raise  ValueError("You must train the model")
		length = len(self._X[0])
		if len(inX) != length:
			raise  ValueError("inX must have %d unit"%(length))
		temp = [self._alphaXy[i]*self._kernel(inX,self._X[i],self._optType,self._sigma)
		        for i in range(len(self._X))]
		temp = sum(temp) + self._b
		res = numpy.sign(temp)
		return res
