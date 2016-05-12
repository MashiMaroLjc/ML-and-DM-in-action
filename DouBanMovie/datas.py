#coding:utf-8
# 分析脚本

import json
import glob
import matplotlib.pyplot as plt
import matplotlib.font_manager
ZH = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
from queue import  PriorityQueue
#
PATH = "data/"

#载入json数据
def load_json(path:str):
	file_list = glob.glob(path + "*.txt")
	print("total file:",len(file_list),"---------",end="")
	json_list = []
	for file in file_list:
		fp = open(file)
		json_list.append(
			json.load(fp)
		)
		fp.close()
	return json_list

#分析时长跟star的关系
def runtime_and_star(json_list:list,Star=5):
	record = dict()
	record["less_than_60"] = {"good":0,"bad":0}
	record["60-100"] =  {"good":0,"bad":0}
	record["100-145"] = {"good":0,"bad":0}
	record["145-185"] = {"good":0,"bad":0}
	record["more_than_185"] = {"good":0,"bad":0}
	for j in json_list:
		try:
			star = float(j.get("star",0) )
		except Exception:
			star = 0
		runtime = j.get("runtime","")
		try:
			number_runtime = int(
				runtime.replace("分钟","")
			)
		except Exception:
			number_runtime = 0
		# >= 7 good（+1） / <7 Bad（-1）
		g_score = 0
		b_score = 0
		if star >= Star:
			g_score = 1
		elif star > 0:
			b_score = 1

		if number_runtime < 60 and number_runtime>0:
			record["less_than_60"]["good"] += g_score
			record["less_than_60"]["bad"] += b_score
		elif number_runtime >= 60 and number_runtime < 100:
			record["60-100"]["good"] += g_score
			record["60-100"]["bad"] += b_score
		elif number_runtime >= 100 and number_runtime < 145:
			record["100-145"]["good"] += g_score
			record["100-145"]["bad"] += b_score
		elif number_runtime >= 145 and number_runtime <= 185:
			record["145-185"]["good"] += g_score
			record["145-185"]["bad"] += b_score
		elif number_runtime >185:
			record["more_than_185"]["good"] += g_score
			record["more_than_185"]["bad"] += b_score

	return  record


#分析所有单值与star的关系，比如地区，导演，类型，演员等,因为数据太多，所以要对返回值做进一步处理
def any_and_star(json_list:list,key,Star=5)->dict:
	record = dict()
	for j in json_list:
		try:
			star = j.get("star",0)
			star = float(star)
		except Exception:
			star = 0

		g_score = 0
		b_score = 0
		if star>=Star:
			g_score = 1
		elif star > 0:
			b_score = 1
		key_str = j.get(key)
		if key_str:
			key_list = key_str.split("/")
			for value in key_list:
				value = value.replace(" ","")
				if value not in record:
					record[value] = {"good":0,"bad":0}
				record[value]["good"] += g_score
				record[value]["bad"] += b_score
	return record

#主演与类型
def actor_and_type(json_list:list)->dict:
	record = dict()
	for j  in json_list:
		actor_str = j.get("actor")
		if not actor_str:
			continue
		actor_list = actor_str.split("/")
		type_str = j.get("type")
		if not type_str:
			continue
		type_list = type_str.split("/")
		for actor in actor_list:
			if actor not in record:
				record[actor] = dict()
			for type in type_list:
				if type not  in record[actor]:
					record[actor][type] = 0
				record[actor][type] += 1
	return record

def runtime_and_any(json_list:list,key:str)->dict:
	record = dict()
	for j in json_list:
		key_str = j.get(key)
		if not key_str:
			continue
		key_list = key_str.split("/")
		runtime = j.get("runtime")
		try:
			number_runtime = int(
				runtime.replace("分钟","")
			)
		except ValueError:
			number_runtime = 0
		less_than_60 = 0
		_60_100 = 0
		_100_145 = 0
		_145_185 = 0
		more_than_180 = 0

		if number_runtime < 60 and number_runtime>0:
			less_than_60 = 1
		elif number_runtime >= 60 and number_runtime < 100:
			_60_100 = 1
		elif number_runtime >= 100 and number_runtime < 145:
			_100_145 = 1
		elif number_runtime >= 145 and number_runtime < 185:
			_145_185 = 1
		elif number_runtime >=185:
			more_than_180 = 1

		for _key in key_list:
			if _key not in record:
				record[_key] = {
					"less_than_60":0,
					"60-100":0,
					"100-145":0,
					"145-185":0,
					"more_than_185":0
				}
			record[_key]["less_than_60"] += less_than_60
			record[_key]["60-100"] += _60_100
			record[_key]["100-145"] += _100_145
			record[_key]["145-185"] += _145_185
			record[_key]["more_than_185"] += more_than_180

	return record



#  ）


# 演员和类型的清洗
# return{
# info:[(name1,权重),(name2,权重……)……]，
# info2:[……]
# }
def clear0(record:dict,number=5):
	def set_key(key):
		def func(x):
			try:
				return record[x][key]
			except KeyError:
				return -1
		return func

	type_list = ["喜剧","剧情","爱情","悬疑","科幻","惊悚","动作","恐怖","犯罪"]
	result = dict()
	for _type in type_list:
		info_list = sorted(record,key=set_key(_type),reverse=True)
		info = [(key,record[key].get(_type,0)) for key in info_list[:number]]
		result[_type] = info
	return result

#类型和主演
def picture0(clear_res:dict,filename:str):
	plt.figure(1, figsize=(12, 9))
	# 总题目
	plt.suptitle("Type and Actor", fontsize=17, fontweight='bold')
	label_all = [t for t in clear_res]
	for index in range(len(label_all)):
		color_list = ["red", "blue", "lightskyblue", "orange", "green"]#"pink","purple","yellow",'yellowgreen']
		p1 = plt.subplot(331 + index)
		key = label_all[index]
		p1.set_title(key,fontproperties=ZH)
		explode = [0 for x in range(5)]
		label = [info[0] for info in clear_res[key]]
		size = [info[1] for info in clear_res[key]]
		# print(label_all)
		Angle = 0
		if len(size) == 0 or size == [0 for x in range(5)]:
			size = [0]
			label = [""]
			explode = [0]
			color_list = ["white"]
			Angle = 90
		else:

			# 手动计算百分比，去掉一些比例过小的元素的标签，统称other
			_sum = sum(size)
			size = [round((x / _sum), 2) for x in size]
			label = [  label[x]   if size[x] > 0.02 else "Other"
			         for x in range(len(label))]
			# 寻找size中的最大元素，然后返回其下标
			def find_index(l: list):
				temp = 0
				index = 0  # 全部相对返回0，将第一块圆饼分出来
				for i in range(len(l)):
					if l[i] > temp:
						temp = l[i]
						index = i
				return index

			explode[find_index(size)] = 0.08
		patches, l_text, p_text = p1.pie(size, colors=color_list, startangle=Angle, shadow=False, explode=explode
		                                 , labels=label, autopct='%3.1f%%', pctdistance=0.6)
		for text in l_text:
			text.set_fontproperties(ZH)
			text.set_size(9)
		p1.axis('equal')
	plt.savefig(filename)
	# plt.show()
	plt.close(1)

#对于一个带有key(good，bad)的信息的字典，
#选出good前n位，bad前n位，可以更改number修改
#返回
# （
#    {   //good字典
#       "name":n
#       ……
#    },
#    {  //bad字典
#       "name":n
#    }
def clear(record:dict,number=5):
	#sorted()中指定key时会把键值传进来
	def func(key):
		return record[key]["good"]
	def func2(key):
		return record[key]["bad"]
	good_list = sorted(record,key=func,reverse=True)
	bad_list = sorted(record,key=func2,reverse=True)
	sub_good_list = good_list[:number]
	sub_bad_list =bad_list[:number]
	good_info = dict()
	for good_key in sub_good_list:
		good_info[good_key] = record[good_key]["good"]
	bad_info = dict()
	for bad_key in sub_bad_list:
		bad_info[bad_key] = record[bad_key]["bad"]
	return (good_info,bad_info)

#对好坏都画图
def picture(clear_res:tuple,x_name:str,filename:str):
	good_dict = clear_res[0]
	bad_dict=clear_res[1]
	fig = plt.figure(1, figsize=(12, 8))
	plt.xlabel(x_name)
	plt.ylabel("Number")
	plt.xticks()
	ax1 = fig.add_subplot(111)
	ax1.set_title("%s And Good"%(x_name))
	#good
	label = [key for key in good_dict]
	plt.xticks([x + 1.1 for x in range(len(label))], label,fontproperties=ZH)
	ax1.bar([1, 2, 3, 4, 5],
	        [good_dict[k] for k in good_dict],
	        width=.2, color='orange', alpha=.8, label="good",yerr=0.000001)
	plt.legend()
	plt.savefig(filename+"—good.jpg")
	#plt.close(1)
	#
	#plt.show()
	plt.close(1)
	#bad
	fig2 = plt.figure(2, figsize=(12, 8))
	ax2 = fig2.add_subplot(111)
	ax2.set_title("%s And Bad" % (x_name))
	plt.ylabel("Number")
	plt.xlabel(x_name)
	label2 = [key for key in bad_dict]
	plt.xticks([x + 1.1 for x in range(len(label2))], label2,fontproperties=ZH)
	ax2.bar([1, 2, 3, 4, 5], [bad_dict[k] for k in bad_dict],
	        width=.2, color='r', alpha=.7, label="bad",yerr=0.000001)
	plt.legend()
	#plt.show()
	plt.savefig(filename + "—bad.jpg")
	plt.close(2)


#清理时间关系
#返回{
# time1:[(info1,比重),(info2,比重),……]
# time2:[(info1,比重),(info2,比重),……]
# }
def clear2(record:dict,number=5):
	result = {
		"less_than_60": [],
		"60-100":[],
		"100-145":[],
		"145-185":[],
		"more_than_185":[]
	}
	def set_key(key):
		def func(x):
			return record[x][key]
		return func
	less_than_60 = sorted(record,key=set_key("less_than_60"),reverse=True)
	result["less_than_60"] = [(key,record[key]["less_than_60"]) for key in less_than_60[:number]]

	_60_100 = sorted(record,key=set_key("60-100"),reverse=True)
	result["60-100"] = [(key, record[key]["60-100"]) for key in _60_100[:number]]

	_100_145 = sorted(record,key=set_key("100-145"),reverse=True)
	result["100-145"] = [(key, record[key]["100-145"]) for key in _100_145[:number]]

	_145_185 = sorted(record, key=set_key("145-185"), reverse=True)
	result["100-145"] = [(key, record[key]["145-185"]) for key in _145_185[:number]]

	more_than_185 = sorted(record, key=set_key("more_than_185"), reverse=True)
	result["more_than_185"] = [(key, record[key]["more_than_185"]) for key in more_than_185[:number]]
	return result


#弄饼状图，共5个，
def picture2(clear_res:dict,name:str,filename:str):
	plt.figure(1,figsize=(12,9))
	#总题目
	plt.suptitle("%s And Runtime" % (name),fontsize=17, fontweight='bold')
	label_all = [time for time in clear_res]

	for index in range(len(label_all)):
		color_list = ["red", "blue", "lightskyblue", "orange", "green"]
		p1 = plt.subplot(231 + index)
		key = label_all[index]
		p1.set_title(key)
		explode = [0.0,0,0,0,0]
		label = [info[0] for info in clear_res[key]]
		size = [info[1] for info in clear_res[key]]
		#print(label_all)
		Angle = 20
		if len(size) == 0 or size == [0,0,0,0,0]:
			size =[0]
			label = [""]
			explode = [0]
			color_list = ["white"]
			Angle = 90
		else:

			#手动计算百分比，去掉一些比例过小的元素的标签，统称other
			_sum = sum(size)
			size = [round((x/_sum),2) for x in size]
			label = [label[x] if size[x] >0.02 else "Other"
			         for x in range(len(label)) ]
			if "Other" in label:
				Angle = 270
			#寻找size中的最大元素，然后返回其下标
			def find_index(l:list):
				temp = 0
				index = 0 #全部相对返回0，将第一块圆饼分出来
				for i in range(len(l)):
					if l[i] > temp:
						temp = l[i]
						index = i
				return index

			explode[find_index(size)] = 0.08

		patches, l_text, p_text=p1.pie(size,colors=color_list,startangle = Angle,shadow = False,explode=explode
		       ,labels=label,autopct = '%3.1f%%',pctdistance = 0.6)
		for text in l_text:
			text.set_fontproperties(ZH)
			text.set_size(12)

		p1.axis('equal')
	plt.savefig(filename)
	plt.close(1)


def save_r_a_s(x,y1,y2,filename):
	fig = plt.figure(1, figsize=(12, 8))
	ax1 = fig.add_subplot(111)
	plt.xticks([a + 1.25 for a in range(len(y1))], x, rotation=0)
	plt.xlabel("Runtime(min)")
	plt.ylabel("Number")
	ax1.bar([1, 2, 3, 4, 5], y1, width=.25, color='orange', alpha=.5, label="good")
	ax1.bar([1.25, 2.25, 3.25, 4.25, 5.25], y2, width=.25, color='r', alpha=.5, label="bad")
	ax1.set_title('Runtime And Star')
	plt.legend()
	plt.savefig(filename)
	plt.close(1)


#转饼图
def save_r_a_t(record,filename):
	res = clear2(record)
	picture2(res,"Type",filename)


#转饼图
def save_t_a_s(record:dict,filename:str):
	res = clear(record)
	picture(res,"Type",filename)

if __name__ == "__main__":
	print("loading-----",end="")
	json_list = load_json(PATH)
	print("OK!")
	#获取播映时间和评分数的数据
	r_a_s = runtime_and_star(json_list)
	x = []
	y1 =[]
	y2 =[]
	for k,v in r_a_s.items():
		x.append(k.replace("_"," "))
		y1.append(v.get("good")+1)
		y2.append(v.get("bad")+1)
	save_r_a_s(x,y1,y2,"result/runtime_and_star.jpg")
	print("Finish-----Runtime and star")


	# 主演和类型(过滤选出前5位，每人一个饼状图)
	a_a_t = actor_and_type(json_list)
	res = clear0(a_a_t)
	picture0(res,"result/Type_and_Actor.jpg")
	print("Finish-----Type and Actor")
	#播放时间系列=========================================
	#播放时间与类型
	r_a_t = runtime_and_any(json_list,key="type")
	save_r_a_t(r_a_t,"result/runtime_and_type.jpg")
	print("Finish-----Runtime and type")

	#播放时间和主演(每个阶段过滤出5位，饼状图，占5位总数的百分比)
	r_a_a = runtime_and_any(json_list,key="actor")
	res = clear2(r_a_a)
	picture2(res,"Actor","result/Actor_and_runtime.jpg")
	print("Finish-----Actor and runtime")


	#播放时间与导演(每个阶段过滤出5位)
	r_a_d = runtime_and_any(json_list,key="director")
	res = clear2(r_a_d)
	picture2(res,"Director","result/Director_and_runtime.jpg")
	print("Finish-----Director and runtime")
	#播放时间和地区(每个阶段过滤出5位)
	r_a_area =  runtime_and_any(json_list,key="area")
	res = clear2(r_a_area)
	picture2(res, "Area", "result/Area_and_runtime.jpg")
	print("Finish-----Area and runtime")
	#评分系列=============================================

	#演员和评分（最高和最低各出五位，条形图，具体的数据）
	a_a_s = any_and_star(json_list,key="actor")
	clear_res = clear(a_a_s)
	picture(clear_res,"Actor","result/actor")
	print("Finish-----actor and star！")

	# #地区和评分（最高和最低各出五位）
	area_a_s = any_and_star(json_list,key="area")
	clear_res = clear(area_a_s)
	picture(clear_res,"Area","result/area")
	print("Finish-----area and star！")


	# #导演和评分（最高和最低各出五位）
	d_a_s = any_and_star(json_list,key="director")
	clear_res = clear(d_a_s)
	picture(clear_res,"Director","result/director")
	print("Finish-----director and star!")


	#类型和评分
	t_a_s = any_and_star(json_list,key="type")
	save_t_a_s(t_a_s,"result/Type")
	print("Finish ALL!")