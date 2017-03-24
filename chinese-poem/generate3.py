# coding:utf-8
import json
import random

pro_model = json.load(open("pro.json"))
link_model = json.load(open("link-model.json"))



key_list = list(pro_model.keys())

# 先随机出一个名词
index = random.randrange(0, len(key_list))
n_word = key_list[index]
begin_words = [n_word]  # 开头词

# 找剩余的三个名词
for i in range(3):
    key = begin_words[-1]
    words = pro_model[key]
    words = sorted(words, key=lambda x: x[1], reverse=True)
    for w in words:
        if w[0] not in begin_words:
            begin_words.append(w[0])
            break



poem = []
link_keys = list(link_model.keys())
random.shuffle(link_keys)
for bword in begin_words:
    for key in link_keys:
        lwords, rwords = link_model[key]
        if bword in lwords:
            random.shuffle(rwords)
            sentence = bword + key + rwords[0]
            poem.append(sentence)
            break

print()
for sentence in poem:
    print(sentence)