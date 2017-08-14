# -*- coding: utf-8 -*-
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'https://savvybookwriters.wordpress.com/2012/08/01/63-top-websites-to-announce-your-book-for-free/'

f = open('sitelist.txt', 'w')

ind = 0

res = requests.get(url)


while ind < len(res.text):
    start = res.text.find('<a title=\"', ind)
    title = res.text.find('')
    end = res.text.find('\" _target=\"', start)
    # print "sss " + res.text[start:end]
    if start == -1:
        break
    payload = res.text[start + 10:end - 1]
    print 'lala'
    print payload
    if payload.count('class') == 0 and len(payload) > 0 and payload.count('.') > 0:
        print payload
        f.write(payload + '\n')

    # print payload
    ind = end



