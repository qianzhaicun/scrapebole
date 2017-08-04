import re
#print(link_crawler("http://date.jobbole.com/",'/(/d+)/'))
#    print(link_crawler("http://date.jobbole.com/",r'^(http://date.jobbole.com/)(\d+)$'))
link_regex = r'^(http://date.jobbole.com/)(\d+)/$'
link = "http://date.jobbole.com/123/"
if re.match(link_regex, link):
    print(1)