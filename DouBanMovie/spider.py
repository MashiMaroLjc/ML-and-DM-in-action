import douban 
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='spider.log',
                    filemode='a')


#
SAVE_PATH = "F://doubandata2"
NUM = 15000
CONFIGURE_PATH = "info.txt"
try:
	doubanSp = douban.DouBanMovieSpider()
	doubanSp.configure("info.txt")
	print("OK")
	print("url: ",doubanSp._url)
	doubanSp.spider(SAVE_PATH,num=NUM)
except Exception as err:
	logging.error("Fuck!  %s"%(str(err)))
	#raise  err
else:
	logging.info("Finish!")
