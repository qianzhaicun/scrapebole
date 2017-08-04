from rediscache import RedisCache
from threaded_crawler import threaded_crawler
from threaded_crawler import img_callback
from threaded_crawler import main_link_crawler
url = "http://date.jobbole.com/page/0"
##main_pages = main_link_crawler(url, r'^(http://date.jobbole.com/page/)(\d+)/$',max_depth=-1,user_agent="sfdf",robots_url="http://date.jobbole.com/robots.txt")
##print(main_pages)
main_pages = ['http://date.jobbole.com/page/0','http://date.jobbole.com/page/2','http://date.jobbole.com/page/3','http://date.jobbole.com/page/4','http://date.jobbole.com/page/5'
    ,'http://date.jobbole.com/page/6','http://date.jobbole.com/page/7'
    ,'http://date.jobbole.com/page/8','http://date.jobbole.com/page/9','http://date.jobbole.com/page/10','http://date.jobbole.com/page/11'
    ,'http://date.jobbole.com/page/12','http://date.jobbole.com/page/13','http://date.jobbole.com/page/14','http://date.jobbole.com/page/15','http://date.jobbole.com/page/16'
    ,'http://date.jobbole.com/page/17']
if len(main_pages) > 0:
    threaded_crawler(main_pages, r'^(http://date.jobbole.com/)(\d+)/$',max_depth=-1,max_threads=10, img_callback=img_callback,cache=RedisCache(),user_agent="dfdfsfgdf")
        
import shutil
import os
path = '/home/caicai/scrapebole/chp4/data/img/date.jobbole.com'
dirpath = '/home/caicai/scrapebole/chp4/data/img'
files = os.listdir(path)
for file in files:
    afile = path + '/' + file
    f = os.listdir(afile)
    if len(f)==1:
        ajpg = f[0]
        os.chdir(afile)
        shutil.copy(afile + '/'+ ajpg, dirpath)