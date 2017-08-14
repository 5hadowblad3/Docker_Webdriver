from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

path = '/Users/Shadow/Downloads/Imperial/Individual/selenium/chromedriver'
sublist = '19abcdefghijklmnopqrstuvwxyz'
url = 'https://www.ucsf.edu/azlist/'

class_name = 'view-content'

f = open('sitelist.txt', 'a')

browser = webdriver.Chrome(path)

# browser.get(url)
#
# lists = browser.find_elements_by_xpath("//table[@class='table table-striped tablePhone']/tbody/tr/td/img")
#
# for item in lists:
#     print item.get_attribute('src')
#     source = str(item.get_attribute('src'))
#     print
#     f.write(source[source.index('=') + 1:] + '\n')
#     # f.write(str(item.get_attribute('href')) + '\n')

for i in sublist:
    browser.get(url + i)
    lists = browser.find_elements_by_xpath("//div[@class='view-content']/ul/li/a")
    for item in lists:
        url = item.get_attribute('href')
