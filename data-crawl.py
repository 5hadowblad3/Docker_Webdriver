# -*- coding: utf-8 -*-
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://www.independent.co.uk/extras/indybest/food-drink/the-50-best-food-websites-8665600.html'

f = open('food_case2.txt', 'w')

ind = 0

res = requests.get(url)


while ind < len(res.text):
    start = res.text.find('\" target=\"_blank\" title=', ind)
    end = res.text.find('>', start)
    # print "sss " + res.text[start:end]
    if start == -1:
        break
    payload = res.text[start + 25:end - 1]
    if payload.count('class') == 0 and len(payload) > 0 and payload.count('.') > 0:
        print payload
        f.write(payload + '\n')

    # print payload
    ind = end



