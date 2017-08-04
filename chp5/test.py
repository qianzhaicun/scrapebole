import requests
import urllib.request
import os
i = 0
while i < 500:
    url = 'http://pic.sogou.com/pics?query=%D5%D4%C0%F6%D3%B1&mode=0&start={}&reqType=ajax&reqFrom=result&tn=-1'
    url = url.format(i)
    resp = requests.get(url)
    aitem = resp.json()['items']
    for item in aitem:
        aimg = item['pic_url_noredirect']
        path = 'data/'
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        try:
            urllib.request.urlretrieve(aimg,aimg)   
        except:
            pass
    i = i + 48

