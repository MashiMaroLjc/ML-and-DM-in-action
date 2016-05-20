from flask import Flask
from flask import request
from recommend2 import Recommend2
import json
import glob
import os.path

configuration={
	"DATA_PATH":"data",
	"PORT":8080
}

#LOAD THE DATA
JSON_LIST = []
paths = glob.glob(
	os.path.join(configuration["DATA_PATH"],"*.txt")
)
for path in paths:
	fp = open(path,"r")
	JSON_LIST.append(
		json.load(fp)
	)
	fp.close()



def filter_json(json_list:list):
	"""
	过滤每一条数据，用于测试集合
	保留title
	:param json_list:电影数据
	:return: 过滤后的结果
	"""
	res = []
	def func(inf:dict,json,key:str):
		"""
		对于 A/B/C这样在同一个标签下有多个属性的进行过滤
		:param inf: 字典
		:param json: 需要过滤的单个json对象
		:return:
		"""
		if key == "title":
			info["title"]=json["title"]
			return
		ks = j.get(key, "")
		k_l = ks.split("/")
		for k_i in range(len(k_l)):
			# print(ty_l[t_i])
			info["%s%s" % (key,k_i + 1)] = k_l[k_i]

	for j in json_list:
		info = dict()
		info["title"] = j.get("title")
		for k in j :
			if k not in  ["comment_list","date","runtime"]:
				func(info,j,k)
		res.append(info)
	return  res

# print(filter_json(JSON_LIST))


app = Flask(__name__)
system = Recommend2(7*24*3600)

@app.route("/recommend/get",methods=['GET'])
def get():
	"""
	获取推荐结果
	:return: 推荐结果
	"""
	test_set=filter_json(JSON_LIST)
	res = system.result(test_set,5)
	def _filter(j):
		"""
		将comment_list弄成字符串
		"""
		nj = j.copy()
		nj["comment_list"] = "|".join(nj["comment_list"])
		return nj
	return json.dumps(
		[ _filter(JSON_LIST[i]) for i in res]
	)


@app.route("/recommend/put",methods=["GET"])
def put():
	"""
	提取数据再学习
	:return:
	"""
	movie_name = request.args.get("moviename",None)
	comment = request.args.get("comment",None)
	if (not movie_name) or (not comment):
		return json.dumps({"sta":"failed"})
	print(movie_name)
	if comment == "good":
		temp = [ filter_json([x])[0]  for x in JSON_LIST if x.get("title","") == movie_name ]
		system.learn(temp[0])
	return json.dumps({"sta":"succeed"})

@app.route("/recommend/info")
def get_info():
	return json.dumps(system.getLike())

if __name__ == "__main__":
	app.run(port=configuration["PORT"],debug=True)
