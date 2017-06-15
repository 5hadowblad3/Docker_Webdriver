from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

path = '/Users/Shadow/Downloads/Imperial/Individual/selenium/chromedriver'

extension_p = '/Users/Shadow/Downloads/Imperial/Individual/selenium/ecap.crx'

url = 'http://www.ranker.com/list/the-best-shoe-websites/sirsinister'

class_name = 'listItem__properties black default'

browser = webdriver.Chrome(path)

browser.get(url)

print browser.page_source
browser.f
lists = browser.find_element_by_class_name(class_name)


for item in lists:
    print 1
    print item






# browser.get(url)