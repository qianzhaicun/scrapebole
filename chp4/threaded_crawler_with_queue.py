import multiprocessing
import re
import socket
import threading
import time
from urllib import robotparser
from urllib.parse import urljoin, urlparse
from downloader import Downloader
from redis_queue import RedisQueue

from throttle import Throttle
import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
from lxml.html import fromstring
import os

SLEEP_TIME = 1
socket.setdefaulttimeout(60)


def get_robots_parser(robots_url):
    " Return the robots parser object using the robots_url "
    try:
        rp = robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp
    except Exception as e:
        print('Error finding robots_url:', robots_url, e)


def clean_link(url, domain, link):
    if link.startswith('//'):
        link = '{}:{}'.format(urlparse(url).scheme, link)
    elif link.startswith('://'):
        link = '{}{}'.format(urlparse(url).scheme, link)
    else:
        link = urljoin(domain, link)
    return link


def get_links(html, link_regex):
    " Return a list of links (using simple regex matching) from the html content "
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    # list of all links from the webpage
    links = webpage_regex.findall(html)
    links = (link for link in links if re.match(link_regex, link))
    return list(links)

def url_to_path(url):
    """ Return file system path string for given URL """
    components = urllib.parse.urlsplit(url)
    # append index.html to empty paths
    path = components.path
    filename = components.netloc + path
    # replace invalid characters
    filename = re.sub(r'[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
    # restrict maximum number of characters
    filename = '/'.join(seg[:255] for seg in filename.split('/'))
    return os.path.join('data/img', filename)

def img_callback(url,html):
    if re.search(r'^(http://date.jobbole.com/)(\d+)/$', url):
        #link_crawler(url, r'^(http://date.jobbole.com/page/)(\d+)/$',max_depth=-1, img_callback=img_callback)
        tree = fromstring(html)
        atitlelist = tree.cssselect('h1.p-tit-single')
        if len(atitlelist)==0:
            return None;

        td = atitlelist[0]
        title = td.text_content()

        ptd = tree.cssselect('div.p-entry')[0]
        p = ptd.text_content()
 
        newp = p.split('\n')
        ptext = []
        for ap in newp:
            if ap.strip() != '':
              ptext.append(ap.strip())
        thetext = title + '\n'
        for ap in ptext:
            if ap.strip() != '':
                thetext = thetext + ap.strip() + '\n'

        alist = tree.xpath('//img[@class="alignnone"]//@src')
        if len(alist)>0:
            img = alist[0]
            print(img)
            if img != None:
                path = url_to_path(url)

                folder = os.path.dirname(path)
                if not os.path.exists(folder):
                    os.makedirs(folder)
                try:
                    urllib.request.urlretrieve(img,'{}{}.jpg'.format(path,title))  
##                    file_object = open(path + title +'.txt', 'w')
##                    file_object.write(thetext)
##                    file_object.close()
                except:
                    pass
                    

def threaded_crawler_rq(start_url, link_regex, user_agent='wswp', proxies=None,
                        delay=3, max_depth=4, num_retries=2, cache={}, max_threads=10, scraper_callback=None,img_callback=None):
    """ Crawl from the given start URLs following links matched by link_regex. In this
        implementation, we do not actually scrape any information.

        args:
            start_url (str or list of strs): web site(s) to start crawl
            link_regex (str): regex to match for links
        kwargs:
            user_agent (str): user agent (default: wswp)
            proxies (list of dicts): a list of possible dicts
                for http / https proxies
                For formatting, see the requests library
            delay (int): seconds to throttle between requests to one domain
                        (default: 3)
            max_depth (int): maximum crawl depth (to avoid traps) (default: 4)
            num_retries (int): # of retries when 5xx error (default: 2)
            cache (dict): cache dict with urls as keys
                          and dicts for responses (default: {})
            scraper_callback: function to be called on url and html content
    """
    crawl_queue = RedisQueue()
    crawl_queue.push(start_url)
    # keep track which URL's have seen before
    robots = {}
    D = Downloader(delay=delay, user_agent=user_agent,
                   proxies=proxies, cache=cache)

    def process_queue():
        while len(crawl_queue):
            url = crawl_queue.pop()
            no_robots = False
            url = str(url, encoding = "utf-8")
            if not url or 'http' not in url :
                continue
            domain = '{}://{}'.format(urlparse(url).scheme,
                                      urlparse(url).netloc)
            rp = robots.get(domain)
            if not rp and domain not in robots:
                robots_url = '{}/robots.txt'.format(domain)
                rp = get_robots_parser(robots_url)
                if not rp:
                    # issue finding robots.txt, still crawl
                    no_robots = True
                robots[domain] = rp
            elif domain in robots:
                no_robots = True
            # check url passes robots.txt restrictions
            if no_robots or rp.can_fetch(user_agent, url):
                depth = crawl_queue.get_depth(url)
                if depth == max_depth:
                    print('Skipping %s due to depth' % url)
                    continue
                html = D(url, num_retries=num_retries)
                if not html:
                    continue
                if scraper_callback:
                    links = scraper_callback(url, html) or []
                else:
                    links = []
                print("here")
                if links == []:
                    if img_callback:
                        print("img")
                        links = img_callback(url, html) or []
                    else:
                        links = []                    
                # filter for links matching our regular expression
                for link in get_links(html, link_regex) + links:
                    if 'http' not in link:
                        link = clean_link(url, domain, link)
                    crawl_queue.push(link)
                    crawl_queue.set_depth(link, depth + 1)
            else:
                print('Blocked by robots.txt:', url)

    # wait for all download threads to finish
    threads = []
    while threads or len(crawl_queue):
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue:
            # can start some more threads
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)  # set daemon so main thread can exit w/ ctrl-c
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        time.sleep(SLEEP_TIME)


def mp_threaded_crawler(*args, **kwargs):
    """ create a multiprocessing threaded crawler """
    processes = []
    num_procs = kwargs.pop('num_procs')
    if not num_procs:
        num_procs = multiprocessing.cpu_count()
    for _ in range(num_procs):
        proc = multiprocessing.Process(target=threaded_crawler_rq,
                                       args=args, kwargs=kwargs)
        proc.start()
        processes.append(proc)
    # wait for processes to complete
    for proc in processes:
        proc.join()


if __name__ == '__main__':
    from alexa_callback import AlexaCallback
    from rediscache import RedisCache
    import argparse

    parser = argparse.ArgumentParser(description='Multiprocessing threaded link crawler')
    parser.add_argument('max_threads', type=int, help='maximum number of threads',
                        nargs='?', default=5)
    parser.add_argument('num_procs', type=int, help='number of processes',
                        nargs='?', default=None)
    parser.add_argument('url_pattern', type=str, help='regex pattern for url matching',
                        nargs='?', default=r'^(http://date.jobbole.com/)(\d+)/$')
    par_args = parser.parse_args()

##    AC = AlexaCallback()
##    AC()
    main_pages = ['http://date.jobbole.com/page/0','http://date.jobbole.com/page/2','http://date.jobbole.com/page/3','http://date.jobbole.com/page/4','http://date.jobbole.com/page/5'
        ,'http://date.jobbole.com/page/6','http://date.jobbole.com/page/7'
        ,'http://date.jobbole.com/page/8','http://date.jobbole.com/page/9','http://date.jobbole.com/page/10','http://date.jobbole.com/page/11'
        ,'http://date.jobbole.com/page/12','http://date.jobbole.com/page/13','http://date.jobbole.com/page/14','http://date.jobbole.com/page/15','http://date.jobbole.com/page/16'
        ,'http://date.jobbole.com/page/17']
    start_time = time.time()

    mp_threaded_crawler(main_pages, par_args.url_pattern, cache=RedisCache(),
                        num_procs=par_args.num_procs, max_threads=par_args.max_threads,img_callback= img_callback)
    print('Total time: %ss' % (time.time() - start_time))
