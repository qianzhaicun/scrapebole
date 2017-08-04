##import redis
##r = redis.StrictRedis(host='localhost', port=6379, db=0)
##r.set('test', 'answer')
##

##diskcache
##from diskcache import DiskCache
##from advanced_link_crawler import link_crawler
##from advanced_link_crawler import img_callback
##from advanced_link_crawler import main_link_crawler
##url = "http://date.jobbole.com/page/0"
##main_pages = main_link_crawler(url, r'^(http://date.jobbole.com/page/)(\d+)/$',max_depth=-1,user_agent="sfdf")
##print(main_pages)
##if len(main_pages) > 0:
##    for key in main_pages:
##        print(key)
##        link_crawler(key, r'^(http://date.jobbole.com/)(\d+)/$',max_depth=-1, img_callback=img_callback,cache=DiskCache(),user_agent="dfdfsfgdf")

##redis-cache
from rediscache import RedisCache
from advanced_link_crawler import link_crawler
from advanced_link_crawler import img_callback
from advanced_link_crawler import main_link_crawler
url = "http://date.jobbole.com/page/0"
main_pages = main_link_crawler(url, r'^(http://date.jobbole.com/page/)(\d+)/$',max_depth=-1,user_agent="sfdf")
print(main_pages)
if len(main_pages) > 0:
    for key in main_pages:
        print(key)
        link_crawler(key, r'^(http://date.jobbole.com/)(\d+)/$',max_depth=-1, img_callback=img_callback,cache=RedisCache(),user_agent="dfdfsfgdf")

##from diskcache import RedisCache
##from advanced_link_crawler import link_crawler
##link_crawler('http://example.webscraping.com/places/default/','/(places/default/(index|view))',cache=RedisCache())
##
##

##from urllib.parse import urlsplit
##components = urlsplit('http://date.jobbole.com/4380')
##print(components)
##print(components.path)
