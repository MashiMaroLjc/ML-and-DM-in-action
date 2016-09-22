#coding:utf-8

from itertools import combinations

class Apriori:

	def __init__(self):
		pass


	def _support(self,dataSet,minSup):
		"""
		求data所有元素的一维的支持度，并过滤满足条件的数据
		:param data:
		:return: set
		"""
		info = dict()
		number = len(dataSet)
		for data in dataSet:
			for e in data:
				info[e] = info.get(e,0) + 1


		s_list = [key for key in info if (info[key]/number) >=minSup]

		return s_list


	def _Gen(self,Lk,k):
		resList = []
		lenLK = len(Lk)
		for i in range(lenLK):
			for j in range(i+1,lenLK):
				L1 = list(Lk[i])[:k-2]
				L2 = list(Lk[j])[:k-2]
				L1.sort()
				L2.sort()
				if L1==L2:
					resList.append(Lk[i] | Lk[j])
		return resList


	def _scan(self,dataSet,data,minSup):
		"""
		求data的所有集合的支持度
		:param dataSet: set
		:param data: [[]]
		:return: set
		"""
		info = dict()
		number = len(dataSet)
		for t in dataSet:
			for c in data:
				c= frozenset(c)
				if c.issubset(t):
					info[c] = info.get(c,0)+1

		#
		s_list = [key for key in info if (info[key] / number) >= minSup]
		return s_list




	def frequentSet(self,dataSet,minSup=0.5):
		"""
		全部频繁集合，用这个返回的结果来关联分析
		:param dataSet:
		:param minSup:
		:return:
		"""
		D = map(set,dataSet)
		D = list(D)
		minSup = minSup if 0 < minSup and minSup <= 1 else abs(minSup / len(dataSet))
		baseSet = self._support(D,minSup)
		#print(baseSet)
		#新的交集
		# comb =[]
		# res = []
		# for x in combinations(baseSet,2):
		# 	comb.append(x)
		# 	res.append(frozenset(x))
		# # #找到最大的满足支持度的交集
		# while len(comb) > 2:
		# 	res = self._scan(dataSet,comb,minSup)
		# 	temp = combinations(res,2)
		# 	comb = []
		# 	for x in temp:
		# 		comb.append(x[0] | x[1])
		# return res
		L = [[ frozenset([base]) for base in baseSet]]
		k = 2
		while(len(L[k-2])>0):
			temp = L[k-2]
			comb = self._Gen(temp,k)
			res = self._scan(D,comb,minSup)
			L.append(res)
			k += 1
		return [j for i in L for j in i]


	def _allRule(self,Set):
		"""
		列出全出关联
		:param Set:
		:return:[()]
		"""
		relationship = []
		for num in range(2,len(Set)):
			temp = combinations(Set,num)
			temp = list(temp)
			for _map in temp:
				for keep in range(1,len(_map)):
					key = frozenset(_map[:keep])
					value = frozenset(_map[keep:])
					relationship.append((key,value))

		return relationship


	def _rule(self,allData,Set,minConf):
		"""
		在一个频繁集中获得关联规则
		:param dataSet:
		:param minConf:
		:return:
		"""
		def sup(value:set):
			numSup = 0
			for s in allData :
				if value.issubset(s):
					numSup += 1
			return numSup
		res = []
		allRule = self._allRule(Set)
		relationshipInfo = dict()
		for r in allRule:
			union = r[0] | r[1]
			condition = r[1]

			if union in relationshipInfo:
				pUnion = relationshipInfo[union]
			else:
				#计算在Set中的支持度
				pUnion = sup(union)
				relationshipInfo[union] = pUnion
			if condition in relationshipInfo:
				pCondition = relationshipInfo[condition]
			else:
				#计算
				pCondition = sup(condition)
				relationshipInfo[condition] = pCondition
			res.append(
				(r[0],r[1],pUnion/pCondition)
			)
		return frozenset(res)

	def rule(self,dataSet,minConf=0.7,minSup= 0.5):
		"""
		获取关联规则
		:param dataSet:
		:param minConf:
		:param minSup:
		:return:
		"""
		minSup = minSup if 0< minSup  and minSup<=1 else abs(minSup/len(dataSet))
		minConf = minConf if 0 < minConf and minConf <= 1 else abs(minConf/len(dataSet))

		supportSet = self.frequentSet(dataSet,minSup) #[set,set,set]
		rules = []
		for fSet in supportSet:
			res = self._rule(dataSet,fSet,minConf)
			rules += res
		return [r for r in rules if r[2] >= minConf]
