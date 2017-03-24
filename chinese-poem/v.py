# coding:utf-8
# 
import json

poemfile = open("five_poem.txt").readlines()
n = 1
length = len(poemfile)

modelfile = open("link-model.json", "w")

fuck = dict()  # v - [[n],[n]]

for poemline in poemfile:
    print("finish:%.5f" % (n / length))
    poemline = poemline.strip().replace("\n", "")
    sentences = poemline.split(".")
    for sen in sentences:
        if len(sen) != 5:
            continue
        v = sen[2]
        ln = sen[:2]
        rn = sen[3:]
        if v not in fuck:
            fuck[v] = [[], []]
        fuck[v][0].append(ln)
        fuck[v][1].append(rn)

    n += 1

json.dump(fuck, modelfile)
