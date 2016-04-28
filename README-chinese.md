#机器学习&数据挖掘实战


##目录

 - [相似图像判别](#相似图像判别)
 - [BetaMeow](#BetaMeow)


##具体内容 


###相似图像判别

参考论文后，利用```python3.4```，```Pillow```,```OpenCV```利用平均哈希算法，
感知哈希算法(离散余弦变换)等算法，实现**相似图片识别**。

结合```OpenCV```提供的```Heer````模型实现**人脸的定位和识别。**

该项目是本人的另外一个Repository,感兴趣的话可以在以下给出地址找到

> [Learn-to-identify-similar-images](https://github.com/MashiMaroLjc/Learn-to-identify-similar-images)

更多的文字描述可以在我在Segmentfault的专栏上看到。

> [识别相似图片(一)](https://segmentfault.com/a/1190000004467183)</br>
> [识别相似图片(二)](https://segmentfault.com/a/1190000004500523?_ea=630748)


###BetaMeow

BetaMeow(五子棋AI)是我在AlphaGo大战李世石后一时兴起弄出来的，经过几次版本的迭代，当前版本有别于传统的五子棋ai。
传统的五子棋采用了搜索算法实现，而**BetaMeow是采用决策树算法实现**，通过人工提供数据，可以进行学习。
虽然现在还有很多不足的地方，但我会慢慢维护和更新。

####如何和BetaMeow一起玩耍

下载BetaMeow相应代码，切换到对应目录，输入以下命令。

```
python ai.py
```

打开浏览器，输入```http://localhost/five```来和BetaMeow一起欢快的玩耍吧。

**注意**，请确保你的**80端口没有被占用**，否则需要你手动修改代码。

###Request

- python >= 3.4 
- flask 0.10.1


##To Do List

- [x] 相似图片判别
- [x] 五子棋
- [ ] 根据你在新浪微博上的动态情绪推荐音乐
- [ ] 某网站电影信息分析
- [ ] 基于上一点，做一个私人电影推荐系统

未完待续……


##其他的碎碎语

该Repository是记录我学习**机器学习**`或**数据挖掘**方面的实践记录，由于考虑到文件体积的关系，**如若
涉及大数据文件，我并不会开源全部内容，但会提供部分样例数据。**同时，**如果你对这方面有兴趣，并且有项目
开源在github或者其他地方，欢迎向我推荐你项目的URL，我会在我的README文件上给出友情链接**。当然，你也得**在
你的主页上给出本项目的友情链接**。

如果你对这个Repository有任何的疑问或者建议，可以在issue上告诉我，如果有更好的算法实现，也可PR
给我。

没神马特别情况的话，我会持续更新这个Repository很长一段时间，**欢迎保持Watch或给star支持**，谢谢哒。

##开源协议
Apache License 2.0

##联系我

Twitter [@fatfatrabbit](https://twitter.com/fat_fat_Rabbit)