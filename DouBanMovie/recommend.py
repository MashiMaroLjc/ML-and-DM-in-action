#coding:utf-8
#推荐系统2.0

import time
import random
import json

class Recommend2:
	"""
	like 是反应该用户最近的趋势，趋势用value[0]表示，value[1]表示其开始时间
	learn用再学习，info参数接受一个用户选择的结果(例如一部电影)，
	result是获取test集合的推荐结果，返回下标值
	      遍历like，其中的表情若过期了，则自动删除，不过期则与该样本比对，符合一个该样本的推荐系数+1
	"""
	def __init__(self,limit_time):
		"""
		:param limit_time: 表示一个标签的有效时间 按秒算
		"""
		self._like = dict()
		self._time = limit_time



	def learn(self,info):
		"""
		根据info的内容学习，学习内容会连同当前时间被记录下来
		:param info: info是一个代表选择的属性，例如电影会具有{“title”:"ABC","type":"喜剧"} 的形式
					这些值就是它需要学习的地方。
		:return:
		"""
		for key in info.values():
			if key in self._like:
				self._like[key] = (self._like[key][0]+1,time.time())
			else:
				self._like[key] = (1,time.time())


	def result(self,test_set:list,number:int):
		"""
		给出测试集合，会与记录中的用户偏好进行进行比较，选出标签符合数最多的集合在测试集合中的下标
		:param test_set: 一个列表，其单个元素的内容是{p1:v1,p2:v2}，v会用于和self._like的key比较
		:param number:  需要返回的选择数目，
		:return: 返回一个列表，内容是test_set的下标
		"""
		#第一次
		if len(self._like) == 0:
			return [random.randrange(0,len(test_set),1) for x in range(number)]
		#已经有资料了
		t = time.time()
		res = dict()
		for index in range(len(test_set)):
			res[index]=0
			#选出self._like中前5个标签(用户近端时间的喜好)
			key_list = sorted(self._like,key=lambda x:int(self._like[x][0]),reverse=True)
			if len(key_list) >= 5:
				key_list = key_list[:5]
			for like in key_list:
				w,begin_time=self._like[like]
				if begin_time >= t - self._time:
					if like in test_set[index].values():
						#推荐系数
						res[index]+=1
				else:
					del self._like[like]
		return sorted(res,key=lambda x:res[x],reverse=True)[:number]

	def save(self,filename):
		fp = open(filename,"w")
		json.dump(self._like,fp)
		fp.close()

	def load(self,filename):
		fp = open(filename, "r")
		self._like = json.load(fp)
		fp.close()
