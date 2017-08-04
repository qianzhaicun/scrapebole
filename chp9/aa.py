import requests
url = 'https://c2b-services.bmw.com/c2b-localsearch/services/api/v3/clients/BMWDIGITAL_DLO/DE/pois?country=DE&category=BM&maxResults=%d&language=en&lat=52.507537768880056&lng=13.425269635701511'
jsonp = requests.get(url % 1000)
import json
pure_json = jsonp.text[jsonp.text.index('(') + 1 :
jsonp.text.rindex(')')]
dealers = json.loads(pure_json)
print(dealers.keys())
print(dealers['count'])
print(dealers['data']['pois'][0])

