from flask import Flask
from decision_tree import DecisionTree
import json
from flask import request
from flask import render_template
import random
import sys

__author__  = "fatRabit"
__version__ = 1.6 

app = Flask(__name__)

#The p_tree,which stored in P_TREE.txt, is a decison 
#tree which decide how to prevent the player winning game.
#The w_tree,which stored in W_TREE.txt,is a decison
#tree which decide  how to win the game.
p_labels = ["your self","neighbor1","neighbor2","neighbor3"]
p_tree = DecisionTree(path="P_TREE.txt")

w_labels = ["your self","neighbor1","neighbor2","neighbor3","neighbor4"]
w_tree = DecisionTree(path="W_TREE.txt")


#Return the home page to client.
@app.route("/five",methods=["GET","POST"])
def home_page():
	return render_template("index.html")

#To create a vector based on the direction.
#Number 1 mean that there is a chess，which have same color with the chess of AI,here.
#Number 0 mean that it is empty here.
#Number -1 mean that this position can't put any chess.  
#This function is used in the function named answer.  
def build_vector(i:int,j:int,table:list,des:str,sta:bool):
	step = 4 if sta else 5
	vector = [1]
	chess = table[i][j]
	if des == "LEFT":
		for k in range(1,step):
			try:
				if j - k < 0:
					vector.append(-1)
				elif table[i][j-k] == chess:
					vector.append(1)  
				elif table[i][j-k] == 0 :
					vector.append(0)
				else:
					vector.append(-1)
			except IndexError:
				vector.append(-1)
	elif des == "RIGHT":
		for k in range(1, step):
			try:
				if table[i][j+k] == chess:
					vector.append(1)  
				elif table[i][j+k] == 0:
					vector.append(0)
				else:
					vector.append(-1)
			except IndexError:
				vector.append(-1)
	elif des == "UP":
		for k in range(1, step):
			try:
				if i-k < 0:
					vector.append(-1)
				elif table[i-k][j] == chess:
					vector.append(1)  
				elif table[i-k][j] == 0:
					vector.append(0)
				else:
					vector.append(-1)
			except IndexError:
				vector.append(-1)
	elif des == "DOWN":
		for k in range(1, step):
			try:
				if table[i + k][j] == chess:
					vector.append(1)  
				elif table[i + k][j] == 0:
					vector.append(0)
				else:
					vector.append(-1)
			except IndexError:
				vector.append(-1)
	elif des == "UP LEFT":
		for k in range(1, step):
			try:
				if i-k < 0 or j-k < 0:
					vector.append(-1)
				elif table[i - k][j-k] == chess:
					vector.append(1)  
				elif table[i - k][j-k] == 0:
					vector.append(0)
				else:
					vector.append(-1)
			except IndexError:
				vector.append(-1)
	elif des == "UP RIGHT":
		for k in range(1, step):
			try:
				if i - k <0:
					vector.append(-1)
				elif table[i - k][j+k] == chess:
					vector.append(1)  
				elif table[i - k][j+k] == 0:
					vector.append(0)
				else:
					vector.append(-1)
			except IndexError:
				vector.append(-1)
	elif des == "DOWN LEFT":
		for k in range(1, step):
			try:
				if j-k < 0:
					vector.append(-1)
				elif table[i+k][j-k] == chess:
					vector.append(1)  
				elif table[i+k][j-k] == 0:
					vector.append(0)
				else:
					vector.append(-1)
			except IndexError:
				vector.append(-1)
	elif des == "DOWN RIGHT":
		for k in range(1, step):
			try:
				if table[i+k][j+k] == chess:
					vector.append(1)  
				elif table[i+k][j+k] == 0:
					vector.append(0)
				else:
					vector.append(-1)
			except IndexError:
				vector.append(-1)
	return vector




#To get the new point where AI plan to put the chess
#The param named des and step was decide by the decison tree.
#This function is used in the function named answer. 
def get_new_p(i:int,j:int,des:str,step:int):
	if des == "LEFT":
		return i,j-step
	elif des == "RIGHT":
		return i,j+step
	elif des == "UP":
		return i-step,j
	elif des == "DOWN":
		return i+step,j
	elif des =="UP LEFT":
		return i-step,j-step
	elif des == "UP RIGHT":
		return i-step,j+step
	elif des == "DOWN LEFT":
		return i+step,j-step
	else:
		return i+step,j+step


#To get the the coordinates of place where AI want to put chess.
#AI will think whether it should stop you winning the game or not first.
#Then the AI will think about how to beat you.
#If AI can't get answer from these two methods,it will give two 
#random number from between 0 and 18 as answer.
#By the way,The file named log.txt will record that how does the AI think.
#This function is used in the function named ai_answer.
def answer(ai_color:int,color:str,table):
	ai_color = int(ai_color)
	des = ("LEFT","RIGHT","UP","DOWN","UP LEFT","UP RIGHT",\
	       "DOWN LEFT","DOWN RIGHT")
	win_answer = None
	win_w = 0
	pre_w = 0
	for i in range(len(table)):
		for j in range(len(table[i])):
			if table[i][j] != 0:
				if table[i][j] != ai_color:
					record = [-1,"",[]]
					for d in des:
						vector = build_vector(i, j, table, d,True)
						assert len(vector) == len(p_labels), \
							"p_tree %s error,vector is %s" % (d,vector)
						res = p_tree.decision((vector,p_labels))
						if res:
							res = json.loads(res)
							if res[0] != -1 and res[1] > pre_w:
								record[0] = res[0]
								record[1] = d
								record[2] =vector
								pre_w = res[1]
								if res[1] == 5:
									return get_new_p(i, j, record[1], record[0])
					if record[0] != -1:
						new_p = get_new_p(i,j,record[1],record[0])
						log = open("log.txt", "a")
						log.write(str(vector)+"---->I prevent it!  I put on %s,%s\n"%(new_p))
						log.flush()
						log.close()
						return new_p
				else:
					w_record = [-1, ""]
					for d in des:
						vector = build_vector(i, j, table, d,False)
						assert len(vector) == len(w_labels),\
							"w_tree %s error,vector is %s" % (d,vector)
						res = w_tree.decision((vector,w_labels))
						if res:
							res = json.loads(res)
							if res[0] != -1 and res[1] > win_w:
								w_record[0] = res[0]
								w_record[1] = d
								if res[1] == 5:
									return get_new_p(i, j, w_record[1], w_record[0])
								win_w = res[1]

					if w_record[0] != -1:
						win_answer = get_new_p(i, j, w_record[1], w_record[0])

	if win_answer:
		log = open("log.txt", "a")
		log.write("Maybe I will win!  I put on %s,%s\n"%(win_answer))
		log.flush()
		log.close()
		return win_answer
	i = random.randrange(0,18,1)
	j = random.randrange(0,18,1)
	while table[i][j] !=0:
		i = random.randrange(0, 18, 1)
		j = random.randrange(0, 18, 1)
	log = open("log.txt", "a")
	log.write("I don't know where I should put! But I still put on %s,%s\n"%(i,j))
	log.flush()
	log.close()
	return i,j


#Return the coordinates of place where AI want to put chess to client.
@app.route("/five/ai",methods=["POST"])
def ai_answer():
	ai_color = request.form.get("ai_color",None)
	if not ai_color:
		return  json.dumps({"sta":"failed","reason":"give me ai_color!"})
	elif "1" == str(ai_color):
		color = "BLACK"
	else:
		color ="WHITE"
	table = request.form.get("data",None)
	if not table:
		return json.dumps({"sta":"failed","reason":"give me table!"})
	table = json.loads(table)
	i,j = answer(ai_color,color,table)
	res = {
		"sta":"succ",
		"location":[i,j]
	}
	return json.dumps(res)


if __name__ == "__main__":
	try:
		port = int(sys.argv[1])
	except IndexError:
		port = 80
	app.run(port=port)