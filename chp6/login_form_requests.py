import requests
from login import parse_form

LOGIN_URL = 'http://example.webscraping.com/places/default/user/login'
LOGIN_EMAIL = 'example@webscraping.com'
LOGIN_PASSWORD = 'example'
data = {'email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD}

html = requests.get(LOGIN_URL)
data = parse_form(html.content)
data['email'] = LOGIN_EMAIL
data['password'] = LOGIN_PASSWORD
response = requests.post(LOGIN_URL, data)
response.url

print(response.url)

second_response = requests.post(LOGIN_URL, data, cookies=html.cookies)
print(second_response.url)
