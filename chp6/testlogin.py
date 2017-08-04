from lxml.html import fromstring
import requests
def parse_form(html):
    tree = fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data

##LOGIN_URL = 'http://example.webscraping.com/places/default/user/login'
##LOGIN_EMAIL = 'example@webscraping.com'
##LOGIN_PASSWORD = 'example'
##data = {'email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD}
##
##html = requests.get(LOGIN_URL)
##data = parse_form(html.content)
##data['email'] = LOGIN_EMAIL
##data['password'] = LOGIN_PASSWORD
##print(data)
##response = requests.post(LOGIN_URL, data)
##response.url
##
##print(response.url)
##
##second_response = requests.post(LOGIN_URL, data, cookies=html.cookies)
##print(second_response.url)

LOGIN_URL = 'http://www.jobbole.com/wp-admin/admin-ajax.php'
LOGIN_EMAIL = 'caicai'
LOGIN_PASSWORD = 'asdjkl!@#'
data = {'user_login': LOGIN_EMAIL, 'user_pass': LOGIN_PASSWORD,'action':'user_login'
    ,'remember_me':'1','redirect_url':'http://www.jobbole.com/'}

#wordpress_0efdf49af511fd88681529ef8c2e5fbf	"caicai|1504401792|X9KmSup5dOW…2d7520bfb9a6dcb92396dad2375a"
#UM_distinctid	"15d9b334c7f9-0e36b480d01cfb8-…6f004c-1fa400-15d9b334c8823e"
#PHPSESSID	"bcgfc110gdk7f0daip0chljbq3"
#wordpress_logged_in_0efdf49af511fd88681529ef8c2e5fbf	"caicai|1504401792|X9KmSup5dOW…d73fd251ceae0db0f5db8b95b288"

cookies = {'wordpress_0efdf49af511fd88681529ef8c2e5fbf':'1caicai|1504401792|X9KmSup5dOWiOvOt8CC2fHD6uxMoTARQ89CLxDHgtH7|6500a0898edef3e1ad6208996b34a8aa632a2d7520bfb9a6dcb92396dad2375a',
    'UM_distinctid':'15d9b334c7f9-0e36b480d01cfb8-3e6f004c-1fa400-15d9b334c8823e'
    ,'PHPSESSID':'bcgfc110gdk7f0daip0chljbq3'
    ,'wordpress_logged_in_0efdf49af511fd88681529ef8c2e5fbf':'caicai|1504401792|X9KmSup5dOWiOvOt8CC2fHD6uxMoTARQ89CLxDHgtH7|3f550f756ce1f65b55fc8c740e31c063fabcd73fd251ceae0db0f5db8b95b288'}

data = {'user_login': LOGIN_EMAIL, 'user_pass': LOGIN_PASSWORD,'action':'user_login'
    ,'remember_me':'1','redirect_url':'http://www.jobbole.com/'}

response = requests.post('http://www.jobbole.com/wp-admin/admin-ajax.php', data)
response.url

print(response.url)

second_response = requests.post('http://www.jobbole.com/wp-admin/admin-ajax.php', data, cookies=cookies)
print(second_response.url)
