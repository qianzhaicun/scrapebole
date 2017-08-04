import requests
template_url = 'http://example.webscraping.com/places/ajax/search.json?&search_term={}&page_size={}&page={}'
letter = "a"
PAGE_SIZE = 10
page = 0
resp = requests.get(template_url.format(letter, PAGE_SIZE,page))
print(resp.json())