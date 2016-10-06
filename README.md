ML and DM in action
====================

[中文](README-chinese.md)

##Directory

 - [Learn-to-identify-similar-images](#user-content-Learn-to-identify-similar-images)
 - [BetaMeow](#user-content-betameow)
 - [DouBanMovie](#user-content-doubanmovie)
 - [my-ml-package](#user-content-ml)
 - [dudulu](#user-content-dudulu)

##Detail


###<span id="Learn-to-identify-similar-images">Learn-to-identify-similar-images</span>

After reading some papers from internet,I implement three algorithms including Average Hash,
Discrete cosine transform and so on,which about how to identify the similar images,by Python
,Pillow and OpenCV.

I also complete a program to find the face from picture and identify the simliar face base on
the modal called Heer provided by OpenCV. 

This is another repository and you can find it  following this link. 

> [Learn-to-identify-similar-images](https://github.com/MashiMaroLjc/Learn-to-identify-similar-images)

I wrote a article about it to Segmentfault,but I wrote it in chinese.


> [识别相似图片(一)](https://segmentfault.com/a/1190000004467183)</br>
> [识别相似图片(二)](https://segmentfault.com/a/1190000004500523?_ea=630748)


-----


###<span id="BetaMeow">BetaMeow</span>

I create BetaMeow,which can play **gobang game** with you 
after learning about the interesting match between AlphaGo and Lee se-dol. Comparing with the previous version,the current version has a great difference from the traditional gobang game AI. It makes a decision by Decision tree instead of search algorithms that the traditional
gobang game AI did.

BetaMeow can keep studying only if you provide data. Of course, thought it's not so perfect, I will do my best to update it.

####How To Begin

Download the code and enter following code when you are in the correct directory.

```
python ai.py
```
Open your browser and enter ```http://localhost/five``` then you can play with BetaMeow 

Please make sure that your**Port 80 is free**, otherwise you need to modify the code.


####Request

- python >= 3.4 
- flask 0.10.1


----

###<span id="DouBanMovie">DouBanMovie</span>

 - The web spider made up of ```spider.py``` and ```douban.py``` baesd on the model named ```requests```.
    It can collect the information of movie and other video from douban.com，including follow items.
    
    - title
    - runtime
    - type
    - director
    - actor
    - area
    - star
    - one or more comments

 The information will save as JSON format.
 
  You can set the number of information you want to collect.The spider will collect util the queue of mission to be empty
 when the number is default.Also the spider **support breakpoint collecting**.The file named info.txt will record the information 
 about the program.**When you continue the process after interruption,this information will be load as configuration.**So,
 **don't modify it unless you need.**


- ```datas.py```is an analysis of the data of the script.At present it can do that.
  
  - The relationship between actor and runtime.  
  - The five actors who has most roles in the good movie or bad movie.You can change the standard to 
    distinguish between good movie and bad movie by change the code. 
  - The relationship between area and runtime.
  - The relationship director actor and runtime.  
  - The five areas Where is the production of much of the good movie or bad movie.
  - The five directors who has most roles in the good movie or bad movie.
  - The five types which has most good movie or bad movie
  - The relationship between star and runtime. 
  - Choose five actors in each type，who has most movie in this type,without good or bad.



- DouBanMovie/data
  
 You can find about 500 randomly selected data about the movie.

- DouBanMovie/result

  You can find the result of running the ```datas.py``` based on 500 randomly selected data.


- recommend.py

  Implements an simple algorithm，,which recommend goods based on some labels
that customer love recently.It is suitable for a small number of users and 
individual users.Also,the code is very easy reading and understanding.

- api.py

  This is a web api based on ```flask``` and ```recommend.py```.Using it,you can do following things
   
   - /recommend/get  
      
   Get the information about recommend movie with JSON format.

   - /recommend/put?moviename=anyname&comment=good
   
   Let the system know Which movie you choose and your comment,like good or bad.
   Then system will update the model.


####Request
 - python >= 3.4
 - requests  2.8.1

------

<h3 id="ml">My-ML-algorithm-package</h3>

click the link for deatil.
 
[My-ML-algorithm-package](ml) 
 

------

<h3 id="dudulu">dudulu</h3>
API server of text mining
[dudulu](https://github.com/MashiMaroLjc/dudulu)

##To Do List

- [x] Learn-to-identify-similar-images
- [x] gobang game AI
- [ ] ~~Recommend music according to your mood on sina weibo~~ 
- [x] APIs of text mining
- [x] Get the data from web site of movie and analyze it
- [x] Build a personal  system to recommend movie,based on last point.
- [ ] My web spider**s**
- [x] A basic ML algorithm package

To Be Continue……


##Other

The reposiory record the code I write during I learning the machine learnning and data mining.
I won't provide a complete data file because they are generally too large to be stored.
But I will provide some important examples of data if necessary. 

**If you are interested in it.you can recommend your project about ML or DM and give me your URL.I will 
write the URL on my README file .At the same time I also hope you can write  URL of this reposiory
on  README file of your project.**

You can open a issue or Pull Request to me if you have a suggestion or better idea.

I will continue update the Repository for a long time,**welcome to watch it or 
give me a star for support**，thank you.



##License
Apache License 2.0

##Contact Me

Twitter [@fatfatrabbit](https://twitter.com/fat_fat_Rabbit)