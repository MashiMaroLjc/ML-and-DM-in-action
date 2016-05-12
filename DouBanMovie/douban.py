#coding:utf-8
#多一个线程时不时序列化
#{
#  visited
#  n
#}
#载入时自动使viited.pop()作为最新的url
#n = num
#提供一些爬取豆瓣的api

import requests
from bs4 import BeautifulSoup
from queue import Queue
import threading
import re
import time
import os.path
import json
import random

HEADER={
"Host": "movie.douban.com",
"scheme":"https",
"version":"HTTP/1.1",
"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q = 0.8",
"accept-encoding":"gzip,deflate,sdch",
"accept-language":"zh-CN,zh;q=0.8",
"cache-control":"max-age=0",
"cookie":'',#add your cookie
"referer":"https://book.douban.com/subject/26757148/?icn=index-editionrecommend",
"upgrade-insecure -requests":"1",
"user-agent":"Mozilla / 5.0(WindowsNT6.3;"\
	"WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 48.0.2564.116Safari / 537.36"
}

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='spider.log',
                    filemode='a')



class myQueue(Queue):

	def __init__(self,type1=None,type2=None):
		super().__init__()

	#return list
	def to_list(self):
		copy_list = []
		length = self.qsize()
		for x in range(length):
			value = self.get()
			copy_list.append(value)
			self.put(value)
		return copy_list










class DouBanMovieSpider:

	def __init__(self):
		self._visited =[]
		self._n = 1
		self._url = "https://movie.douban.com/"
		self._mutex = threading.Lock()
		self._threading_flag = True
		self._mission = myQueue()

	#读入文件的配置
	def configure(self,filename):
		fp = open(filename,'r')
		js = json.load(fp)
		fp.close()
		self._visited = js.get("visited",[])
		self._n = int(js.get("n",1))
		mission_list = js.get("mission",myQueue())
		if isinstance(mission_list,myQueue):
			self._mission = mission_list
		else:
			for url in mission_list:
				self._mission.put(url)
		if len(self._visited) >= 1:
			self._url = self._visited.pop()
		print("now have %d mission totally"%(self._mission.qsize()))

	#周期检查，如果查找满了50 条，则序列化
	def _check(self):
		temp = -1
		while self._threading_flag:
			# print(self._n)
			flag = False
			length = len(self._visited)
			if (length % 15 ==0) and temp != length:
				flag = True
				temp = length
			if flag :
				if self._mutex.acquire():
					try:
						#print("写入！")
						fp = open("info.txt","w")
						json.dump({
							"visited":self._visited,
							"n":length,
							"mission":self._mission.to_list()
						},fp)
						fp.close()
						logging.info("Write information succeed!")
					except Exception as err:
						logging.info("Check Error %s"%(str(err)))
					self._mutex.release()
			time.sleep(1)
		fp = open("info.txt","w")
		json.dump({
				"visited":self._visited,
				"n":len(self._visited),
				"mission":self._mission.to_list()
		},fp)
		fp.close()

	#提取出最新的电影
	def _new_movie(self,html):
		#print(html)
		soup = BeautifulSoup(html,"html.parser")
		li_list = soup.find_all('li')
		new_movie_list = []
		for li in li_list:
			if li.get("data-title"):
				title = li.get("data-title","unknown")
				release = li.get("data-release","unknown")
				duration = li.get("data-duration","unknown")
				region = li.get("data-region","unknown")
				director = li.get("data-director","unknown")
				actors = li.get("data-actors","unknown")
				new_movie_list.append(
					(title,release,duration,region,director,actors)
				)
		return new_movie_list

	#获取最新电影
	def get_new_movie(self,timeout=5):
		response = requests.get("https://movie.douban.com/", headers=HEADER,timeout=timeout)
		if str(response.status_code) == '200':
			response.encoding="utf-8"
			html = response.text
			movie_info_list = self._new_movie(html)
			return movie_info_list
		else:
			return []

	#从html页面内获取电影信息，以列表的方式返回
	def _get_info(self,html):
		soup = BeautifulSoup(html, "html.parser")
		span = soup.find("span",attrs={"property":"v:itemreviewed"})
		#title
		try:
			title = span.string
		except Exception:
			title = ""
		# span2 = soup.find("span",attrs={"class":"year"})
		# #year
		# year = span2.string
		#导演名字
		d_a = soup.find("a",attrs={"rel":"v:directedBy"})
		try:
			d_name = d_a.string
		except Exception:
			d_name = ""
		#编剧名字列表
		w_list = soup.find_all(href = re.compile("/celebrity/\d{7}/"),attrs={"rel":""})
		try:
			w_name_list = [name.string for name in w_list]
		except Exception:
			w_name_list = [""] 
		#主演名字列表
		actor_list = soup.find_all(attrs={"rel":"v:starring"})
		try:
			actor_name_list = [name.string for name in actor_list]
		except Exception:
			actor_name_list = [""]
		#电影类型
		movie_type_span = soup.find("span",attrs={"property":"v:genre"})
		try:
			movie_type_name = movie_type_span.string
		except Exception:
			movie_type_name = ""
		#片长
		runtime_span = soup.find("span",attrs={"property":"v:runtime"})
		
		try:
			runtime = runtime_span.string
		except Exception:
			runtime = ""

		#地区
		area_index = html.find("制片国家/地区:</span>")
		end_index = html.find("br",area_index)
		if area_index != -1 and end_index != -1:
			area = html[area_index+16:end_index-1]
		else:
			area = ""
		#具体上映日期
		date_span = soup.find("span",attrs={"property":"v:initialReleaseDate"})
		try:
			date = date_span.string
		except Exception:
			date = ""
		#评分
		star_strong = soup.find("strong",attrs={"property":"v:average"})
		try:
			star = star_strong.string
		except Exception:
			star = "-1"
		#影评区
		comment_div_list = soup.find_all("div",attrs={"class":"comment"})
		#筛选出纯影评
		def _get_comment(tag):
			try:
				return tag.p.string.replace(" ","").replace("\n","")
			except Exception:
				return ""

		comment_list = [_get_comment(comment) for comment in comment_div_list]
		#print(comment_div_list)
		#电影信息归结
		info = {
			"title":title,
			"director":d_name,
			"writer":"/".join(w_name_list),
			"actor":"/".join(actor_name_list),
			"type":movie_type_name,
			"runtime":runtime,
			"area":area,
			"date":date,
			"star":star,
			"comment_list":comment_list
		}
		return info


	#从电影url中获取信息
	def get_info_from_movie(self,url,timeout=5):
		response = requests.get(url, headers=HEADER, timeout=timeout)
		if str(response.status_code) == '200':
			response.encoding = "utf-8"
			html = response.text
			return self._get_info(html)
		else:
			return dict()


	#从主页中提取出需要爬取得url，返回其列表
	def _get_movie_url(self,html):
		#主页入口
		exp = "https://movie.douban.com/subject/\d{8}/\?from"
		soup = BeautifulSoup(html,"html.parser")
		movie_list = soup.find_all("a",href=re.compile(exp))
		url_list = [movie.get("href") for movie in movie_list]
		return url_list


	#将info序列化,写进n.txt
	def _write_file(self,dirname,info,n):
		filename = os.path.join(dirname,"{}.txt".format(n))
		f = open(filename,'w')
		json.dump(info,f)
		f.close()

	#spider内部实现函数
	def _spider(self,dirname,mission,timeout,num):
		record = dict()#(value:time out number,key:url)
		#爬取
		while (not mission.empty() )and ((self._n <= num) or (num == -1)):
			url = mission.get(timeout=5)

			try:
				if url not in self._visited:
					response = requests.get(url,headers=HEADER,timeout=timeout)
				else:
					logging.info("%s is in %s"%(url,self._visited.index(url)))
					continue

			except Exception as err:
				#曾经的错误次数
				was = record.get(url,0)
				# if was == 5:
				# 	logging.error(url + "    Give Up!\n")
				# 	time.sleep(5)
				# 	continue
				#print("\n%s error !\nError is %s!\n Wait a moment!"%(url,str(err)))
				logging.error("%s error !\nError is %s!\n Wait a moment!\n"%(url,str(err)))
				time.sleep(10)
				
				mission.put(url)
				record[url] = was + 1
			else:
				if str(response.status_code) != '200':
					logging.error("url：%s   The code is %s"%(url,response.status_code))
					was = record.get(url, 0)
					if was == 2:
						logging.error(url + "    Give Up!\n")
						time.sleep(5)
						continue
					mission.put(url)
					time.sleep(10)
					record[url] = was + 1
					# logging.error(url + "    Give Up!\n")
					continue
				else:
					#成功访问
					response.encoding = "utf-8"
					html = response.text
					next_url_list = self._get_movie_url(html)
					for next_url in next_url_list:
						mission.put(next_url)
					try:

						info = self._get_info(html)
						# for key,value in info.items():
						# 	print(key," : ",value)
						self._write_file(dirname,info,self._n)
					except Exception as err:
						logging.error("URL: %s  Get information error!  Reason: "%(url)+str(err))
						#was = record.get(url, 0)
						# if was == 2:
						# 	logging.error(url + "    Give Up!\n")
						# 	time.sleep(5)
						# 	continue
						#mission.put(url)
						time.sleep(10)
						#record[url] = was + 1
					else:
						#print("%s succeed! Already finish %d/%d"%(url,self._n,num))
						logging.info("%s succeed! Already finish %d/%d\n"%(url,self._n,num))
						if self._mutex.acquire():
							#print("append")
							self._visited.append(url)
							self._mutex.release()
						self._n += 1
						time.sleep(random.randrange(10,22,1))
						





	#在dirname下建立收集下来的库
	def spider(self,dirname,timeout=5,num=-1):
		#开启检测进程
		check_t = threading.Thread(target=self._check,name="check")
		check_t.start()
		#打开主页
		response = requests.get(self._url,headers=HEADER,timeout=timeout)
		if str(response.status_code) != '200':
			print("Begin Failed!")
		response.encoding="utf-8"
		html = response.text
		movie_url = self._get_movie_url(html)
		#print(movie_url)
		for url in movie_url:
			self._mission.put(url,timeout=5)
		self._spider(dirname=dirname,mission=self._mission,timeout=timeout,num=num)
		self._threading_flag = False


# if __name__ == '__main__':
# 	# f = open("123.html",'r',encoding='utf-8')
# 	# html = f.read()
# 	# f.close()
# 	d = DouBanMovieSpider()
# 	# res = d._get_movie_url(html)
# 	# print(res)
# 	# info = d._get_info(html)
# 	# for key,value in info.items():
# 	# 	print(key+": "+str(value))
# 	# res = d.get_new_movie()
# 	# for movie in res:
# 	# 	print(movie)
# 	d.spider("F://doubandata",num=10)