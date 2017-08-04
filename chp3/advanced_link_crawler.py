import re
from urllib import robotparser
from urllib.parse import urljoin
from downloader import Downloader
from throttle import Throttle
import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
from lxml.html import fromstring
import os

def get_robots_parser(robots_url):
    " Return the robots parser object using the robots_url "
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp
def download(url, user_agent='wswp', num_retries=2, charset='utf-8', proxy=None):
    """ Download a given URL and return the page content
        args:
            url (str): URL
        kwargs:
            user_agent (str): user agent (default: wswp)
            charset (str): charset if website does not include one in headers
            proxy (str): proxy url, ex 'http://IP' (default: None)
            num_retries (int): number of retries if a 5xx error is seen (default: 2)
    """
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        if proxy:
            proxy_support = urllib.request.ProxyHandler({'http': proxy})
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)
        resp = urllib.request.urlopen(request)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
        html = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html

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
                if not path.find("3929"):
                    urllib.request.urlretrieve(img,'{}{}.jpg'.format(path,title))  
                    file_object = open(path + title +'.txt', 'w')
                    file_object.write(thetext)
                    file_object.close()

def main_link_crawler(start_url, link_regex, robots_url=None, user_agent='bbbbbbb',proxies=None, delay=3, max_depth=4,num_retries=2,cache={}):
    """ Crawl from the given start URL following links matched by link_regex. In the current
        implementation, we do not actually scrapy any information.

        args:
            start_url (str): web site to start crawl
            link_regex (str): regex to match for links
        kwargs:
            robots_url (str): url of the site's robots.txt (default: start_url + /robots.txt)
            user_agent (str): user agent (default: wswp)
            proxy (str): proxy url, ex 'http://IP' (default: None)
            delay (int): seconds to throttle between requests to one domain (default: 3)
            max_depth (int): maximum crawl depth (to avoid traps) (default: 4)
            scrape_callback (function): function to call after each download (default: None)
    """
    crawl_queue = [start_url]
    # keep track which URL's have seen before
    seen = {}
    data = []
    if not robots_url:
        robots_url = '{}/robots.txt'.format(start_url)
    rp = get_robots_parser(robots_url)
    throttle = Throttle(delay)
    while crawl_queue:
        url = crawl_queue.pop()
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            depth = seen.get(url, 0)
            if depth == max_depth:
                print('Skipping %s due to depth' % url)
                continue
            throttle.wait(url)
        
            html = download(url, user_agent=user_agent, proxy=proxies)
            if not html:
                continue
            # filter for links matching our regular expression
            for link in get_links(html):
                if re.match(link_regex, link):
                    abs_link = urljoin(start_url, link)
                    if abs_link not in seen:
                        seen[abs_link] = depth + 1
                        crawl_queue.append(abs_link)
        else:
            print('Blocked by robots.txt:', url)
    return seen

def get_links(html):
    " Return a list of links (using simple regex matching) from the html content "
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)


def link_crawler(start_url, link_regex, robots_url=None, user_agent='wswp',
                 proxies=None, delay=3, max_depth=-1, num_retries=2, cache={}, scraper_callback=None,img_callback=None):
    """ Crawl from the given start URL following links matched by link_regex. In the current
        implementation, we do not actually scrape any information.

        args:
            start_url (str): web site to start crawl
            link_regex (str): regex to match for links
        kwargs:
            robots_url (str): url of the site's robots.txt (default: start_url + /robots.txt)
            user_agent (str): user agent (default: wswp)
            proxies (list of dicts): a list of possible dicts for http / https proxies
                For formatting, see the requests library
            delay (int): seconds to throttle between requests to one domain (default: 3)
            max_depth (int): maximum crawl depth (to avoid traps) (default: 4)
            num_retries (int): # of retries when 5xx error (default: 2)
            cache (dict): cache dict with urls as keys and dicts for responses (default: {})
            scraper_callback: function to be called on url and html content
    """
    crawl_queue = [start_url]
    # keep track which URL's have seen before
    seen = {}
    if not robots_url:
        robots_url = '{}/robots.txt'.format(start_url)
    rp = get_robots_parser(robots_url)
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, cache=cache)
    while crawl_queue:
        url = crawl_queue.pop()
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            depth = seen.get(url, 0)
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
            if links == []:
                if img_callback:
                    links = img_callback(url, html) or []
                else:
                    links = []
            # filter for links matching our regular expression
            for link in get_links(html) + links:
                if re.match(link_regex, link):
                    abs_link = urljoin(start_url, link)
                    if abs_link not in seen:
                        seen[abs_link] = depth + 1
                        crawl_queue.append(abs_link)
        else:
            print('Blocked by robots.txt:', url)
            
if __name__ == '__main__' :
    from diskcache import DiskCache
    link_crawler('http://example.webscraping.com/places/default/','/(places/default/(index|view))', cache=DiskCache())           
