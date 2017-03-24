# coding:utf-8
# 

def two(words):
    """

    :param words:
    :return:
    """
    new = []
    s = len(words)
    for index in range(s):
        w = words[index]
        for next_index in range(index + 1, s):
            next_w = words[next_index]
            new.append(frozenset([w, next_w]))
    return new


poemfile = open("five_poem.txt").readlines()

feature = []
n = 1
length = len(poemfile)

for poemline in poemfile:
    print("finish:%.5f" % (n / length))
    poemline = poemline.strip().replace("\n", "")
    sentences = poemline.split(".")
    temp = []
    for sen in sentences:
        if len(sen) != 5:
            continue
        temp.append(sen[:2])
    feature.append(temp)
    n += 1
size = len(feature)


word_fre = dict()

for fea in feature:
    for word in set(fea):
        word_fre[word] = word_fre.get(word, 0) + 1 / size

two_fre = dict()
two_feature = []
#
for fea in feature:
    fea = list(set(fea))
    two_feature.append(two(fea))

for fea in two_feature:
    for word in fea:
        two_fre[word] = two_fre.get(word, 0) + 1 / size

#
pro = dict()
for k, v in two_fre.items():
    event = list(k)
    # 
    key = event[0]
    if key not in pro:
        pro[key] = []

    pro[key].append(
        [event[1], two_fre[k] / word_fre[key]]
    )

    key = event[1]
    if key not in pro:
        pro[key] = []
    pro[key].append(
        [event[0], two_fre[k] / word_fre[key]]
    )

#
import json

out = open("pro.json", "w")
json.dump(pro, out)
